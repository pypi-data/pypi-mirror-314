from typing import List, Tuple, Dict
import numpy as np
from shapely.geometry import LineString
from scipy.spatial import KDTree

from ..BaseNetworkAnalyser import BaseNetworkAnalyser
from ...public.line.LineBase import LineBase
from ...public.line.LinePointsShifter import LinePointsShifter
from ...public.line.LinePointsSplitter import LinePointsSplitter
from pytessng.Config import NetworkImportConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


# 节点类
class Node:
    def __init__(self, node_id: str, loc: Tuple[float, float], adjacent_link_id_list: List[str]):
        # 节点编号
        self.id = node_id
        # 节点坐标
        self.loc = loc
        # 相邻路段ID列表
        self.adjacent_link_id_list = adjacent_link_id_list


# 路段类
class Link:
    def __init__(self, link_id: str, name: str, link_type: str, line: LineString, start_node_id: str, end_node_id: str, is_oneway: bool, lane_count: int):
        # 路段ID
        self.id: str = link_id
        # 路段名称
        self.name: str = name
        # 路段类型
        self.type: str = link_type

        # 路段点位
        self.line: LineString = line
        # 路段长度
        self.length: float = self.line.length

        # 起始节点ID
        self.start_node_id: str = start_node_id
        # 结束节点ID
        self.end_node_id: str = end_node_id
        # 是否是单向路段
        self.is_oneway: bool = is_oneway
        # 车道数
        self.lane_count: int = lane_count

        # 起始段的角度
        self._start_angle = None
        # 结束段的角度
        self._end_angle = None

    # 起始段的角度
    @property
    def start_angle(self):
        if self._start_angle is None:
            self._start_angle = LineBase.calculate_angle_with_y_axis(self.line.coords[0], self.line.coords[1])
        return self._start_angle

    # 结束段的角度
    @property
    def end_angle(self):
        if self._end_angle is None:
            self._end_angle = LineBase.calculate_angle_with_y_axis(self.line.coords[-2], self.line.coords[-1])
        return self._end_angle

    # mode=0表示把开始一段截取 mode=1表示把结束一段截取
    def cut(self, distance: int, mode: int) -> None:
        new_coords, _ = LinePointsSplitter.split_line_by_distance_and_mode(self.line.coords, distance, mode)
        self.line = LineString(new_coords)
        # 更新路段长度
        self.length = self.line.length

    # 向左右两侧偏移 得到两个Link对象
    def shift(self, width: float = None):
        if not width:
            # 计算横向偏移距离
            offset_x = NetworkImportConfig.OSM.DEFAULT_LANE_WIDTH * self.lane_count / 2
            width = offset_x

        line = list(self.line.coords)
        # 确保折线至少有两个点
        if len(line) < 2:
            raise ValueError("A polyline requires at least two points !")

        # 两侧偏移
        left_line = LineString(LinePointsShifter.shift_line_to_left(line, width)[::-1])
        right_line = LineString(LinePointsShifter.shift_line_to_left(line, -width))

        # 创建两个对象
        left_link = Link(
            f"L[{self.id}]", self.name, self.type,
            left_line, self.end_node_id, self.start_node_id, True, self.lane_count)
        right_link = Link(
            f"R[{self.id}]", self.name, self.type,
            right_line, self.start_node_id, self.end_node_id, True, self.lane_count)

        return left_link, right_link


# 连接段类
class Connector:
    def __init__(self, from_link_id: str, to_link_id: str, from_lane_numbers: List[int], to_lane_numbers: List[int]):
        # 上游路段ID
        self.from_link_id: str = from_link_id
        # 下游路段ID
        self.to_link_id: str = to_link_id
        # 上游车道序号列表
        self.from_lane_numbers: List[int] = from_lane_numbers  # start from one
        # 下游车道序号列表
        self.to_lane_numbers: List[int] = to_lane_numbers  # start from one


# 进口道路段类
class ApproachLink:
    def __init__(self, from_link: Link, all_exit_link_mapping: dict):
        # 进口道路段对象
        self.current_link: Link = from_link

        # 左转出口道路段映射
        self._left_turn_link_mapping: Dict[str, Link] = all_exit_link_mapping["left"]
        # 直行出口道路段映射
        self._straight_link_mapping: Dict[str, Link] = all_exit_link_mapping["straight"]
        # 右转出口道路段映射
        self._right_turn_link_mapping: Dict[str, Link] = all_exit_link_mapping["right"]

        # 左转出口道路段的数量
        self._left_count = len(self._left_turn_link_mapping)
        # 直行出口道路段的数量
        self._straight_count = len(self._straight_link_mapping)
        # 右转出口道路段的数量
        self._right_count = len(self._right_turn_link_mapping)

        # 构建好的连接段的列表
        self.connectors_data: list = []
        # 有没有连接问题
        self.warning: bool = False

    # 添加所有方向的连接段
    def add_all_direction_connectors(self) -> None:
        if self._left_count > 1 or self._straight_count > 1 or self._right_count > 1:
            logger.logger_pytessng.debug(f"OpenStreetMap: Too much turn as [left]-[{self._left_count}] $ [straight]-[{self._straight_count}] $ [right]-[{self._right_count}].")
            self.warning = True

        # 添加右转方向的连接段
        self._add_right_turn_connectors()
        # 添加左转方向的连接段
        self._add_left_turn_connectors()
        # 添加直行方向的连接段
        self._add_straight_connectors()

    # 添加右转方向的连接段
    def _add_right_turn_connectors(self) -> None:
        from_link_id = self.current_link.id
        # 进口路段车道数
        from_lane_count = self.current_link.lane_count

        # 只有右转
        if self._left_count == 0 and self._straight_count == 0 and self._right_count > 0:
            for to_link_id, to_link in self._right_turn_link_mapping.items():
                # 出口路段车道数
                to_lane_count = to_link.lane_count
                # 最大车道数
                max_lane_count = max(from_lane_count, to_lane_count)
                # 构建连接段数据
                from_lane_numbers = [min(i + 1, from_lane_count) for i in range(max_lane_count)]
                to_lane_numbers = [min(i + 1, to_lane_count) for i in range(max_lane_count)]
                conn = Connector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers)
                self.connectors_data.append(conn)
        # 不是只有右转
        else:
            # 最右侧连最右侧
            for to_link_id, to_link in self._right_turn_link_mapping.items():
                # 构建连接段数据
                from_lane_numbers = [1]
                to_lane_numbers = [1]
                conn = Connector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers)
                self.connectors_data.append(conn)

    # 添加左转方向的连接段
    def _add_left_turn_connectors(self) -> None:
        from_link_id = self.current_link.id
        # 进口路段车道数
        from_lane_count = self.current_link.lane_count

        # 只有左转
        if self._left_count > 0 and self._straight_count == 0 and self._right_count == 0:
            for to_link_id, to_link in self._left_turn_link_mapping.items():
                # 出口路段车道数
                to_lane_count = to_link.lane_count
                # 最大车道数
                max_lane_count = max(from_lane_count, to_lane_count)
                # 构建连接段数据
                from_lane_numbers = [min(i + 1, from_lane_count) for i in range(max_lane_count)]
                to_lane_numbers = [min(i + 1, to_lane_count) for i in range(max_lane_count)]
                conn = Connector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers)
                self.connectors_data.append(conn)
        # 不是只有左转
        else:
            # 最左侧连最左侧
            for to_link_id, to_link in self._left_turn_link_mapping.items():
                # 出口路段车道数
                to_lane_count = to_link.lane_count
                # 构建连接段数据
                from_lane_numbers = [from_lane_count]
                to_lane_numbers = [to_lane_count]
                conn = Connector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers)
                self.connectors_data.append(conn)

    # 添加直行方向的连接段
    def _add_straight_connectors(self) -> None:
        from_link_id = self.current_link.id
        # 进口路段车道数
        from_lane_count = self.current_link.lane_count

        # 没有左转有直行
        if self._left_count == 0 and self._straight_count > 0:
            for to_link_id, to_link in self._straight_link_mapping.items():
                # 出口路段车道数
                to_lane_count = to_link.lane_count
                # 最大车道数
                max_lane_count = max(from_lane_count, to_lane_count)
                # 构建连接段数据
                from_lane_numbers = [min(i + 1, from_lane_count) for i in range(max_lane_count)]
                to_lane_numbers = [min(i + 1, to_lane_count) for i in range(max_lane_count)]
                conn = Connector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers)
                self.connectors_data.append(conn)
        # 只有一条车道
        elif from_lane_count == 1:
            for to_link_id, to_link in self._straight_link_mapping.items():
                # 出口路段车道数
                to_lane_count = to_link.lane_count
                # 构建连接段数据
                from_lane_numbers = [1 for _ in range(to_lane_count)]
                to_lane_numbers = [i + 1 for i in range(to_lane_count)]
                conn = Connector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers)
                self.connectors_data.append(conn)
        # 有左转有直行
        else:
            for to_link_id, to_link in self._straight_link_mapping.items():
                # 出口路段车道数
                to_lane_count = to_link.lane_count
                max_lane_count = min(from_lane_count, to_lane_count)
                # 构建连接段数据
                # 给左转留一条车道
                from_lane_numbers = [min(i + 1, from_lane_count - 1) for i in range(max_lane_count)]
                to_lane_numbers = [min(i + 1, to_lane_count) for i in range(max_lane_count)]
                conn = Connector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers)
                self.connectors_data.append(conn)


# 交叉口类
class Intersection:
    """
    包含两个步骤：(1) 处理路段 (2) 处理连接段
    """

    def __init__(self, nodes_data: dict, links_data: dict):
        # 点的数据
        self.nodes_data: dict = nodes_data
        # 边的数据
        self.links_data: dict = links_data

        # 维持与路网数据的一致性
        self.update_node: dict = {}
        self.update_link: dict = {
            "insert": {},  # 增加
            "update": {},  # 更新
            "delete": {},  # 删除
        }

        # 交叉口内的连接段数据
        self.connectors_data: list = []
        # 问题转向
        self.warning_turn_list: list = []

    # 创建交叉口
    def init_intersection(self) -> None:
        if not self.nodes_data or not self.links_data:
            logger.logger_pytessng.warning("Empty intersection data !")
            return

        # 处理路段
        self._init_links()
        # 处理连接段
        self._init_connectors()

    ###########################################################################

    # 裁剪长度
    def _get_offset_y(self, node_num) -> (int, int):
        if node_num == 1:
            offset_oneway = 15
            offset_twoway = 15
        elif node_num == 2:
            offset_oneway = 15
            offset_twoway = 10
        elif node_num in [3, 4]:
            offset_oneway = 15
            offset_twoway = 15
        else:
            raise Exception("Too much node !")
        return offset_oneway, offset_twoway

    # 裁剪边
    def _cut_link(self, link) -> Link:
        offset_oneway, offset_twoway = self._get_offset_y(len(self.nodes_data))
        if link.is_oneway:
            # 出边
            if link.start_node_id in self.nodes_data:
                link.cut(offset_oneway, mode=0)
            # 入边
            elif link.end_node_id in self.nodes_data:
                link.cut(offset_oneway, mode=1)
        else:
            # 出边
            if link.start_node_id in self.nodes_data:
                link.cut(offset_twoway, mode=0)
            # 入边
            elif link.end_node_id in self.nodes_data:
                link.cut(offset_twoway, mode=1)
        return link

    # 裁剪和复制边
    def _init_links(self) -> None:
        links = self.links_data.copy()

        for link_id, link in links.items():
            # 如果是交叉口内部的边就删掉
            if link.start_node_id in self.nodes_data and link.end_node_id in self.nodes_data:
                # 自己要更新
                self.links_data.pop(link_id)
                # 路网要更新
                self.update_link["delete"][link_id] = True
                self.update_node[link_id] = []
            else:
                # 裁剪边
                link = self._cut_link(link)
                # 单向边
                if link.is_oneway:
                    # 自己要更新
                    self.links_data[link_id] = link
                    # 路网要更新
                    self.update_link["update"][link_id] = link
                # 双向边
                else:
                    link1, link2 = link.shift()
                    # 自己要更新
                    self.links_data.pop(link_id)
                    self.links_data[link1.id] = link1
                    self.links_data[link2.id] = link2
                    # 路网要更新
                    self.update_link["delete"][link_id] = True
                    self.update_link["insert"][link1.id] = link1
                    self.update_link["insert"][link2.id] = link2
                    self.update_node[link_id] = [link1.id, link2.id]

    ###########################################################################

    # 得到路段一圈的顺序
    def _get_link_order(self) -> list:
        cut_length = 5
        points = {}
        for link_id, link in self.links_data.items():
            if link.start_node_id in self.nodes_data:
                length = cut_length
            else:
                length = max(link.length - cut_length, 0)
            p = link.line.interpolate(length)
            points[link_id] = (p.x, p.y)

        # 计算交叉口中心位置
        center_x = np.mean([p[0] for p in points.values()])
        center_y = np.mean([p[1] for p in points.values()])
        center_point = (center_x, center_y)

        # 时针顺序
        link_order = []
        for link_id, point in points.items():
            angle = LineBase.calculate_angle_with_y_axis(center_point, point)
            link_order.append([link_id, angle])
        link_order = sorted(link_order, key=lambda x: x[1])
        link_order = [link_id for link_id, _ in link_order]
        return link_order

    # 判断谁进谁出
    def _get_link_inout(self, link_order: list) -> dict:
        link_inout = {"in": [], "out": []}
        for link_id in link_order:
            link = self.links_data[link_id]
            if link.start_node_id in self.nodes_data:
                link_inout["out"].append([link_id, link.start_angle])
            else:
                link_inout["in"].append([link_id, link.end_angle])
        return link_inout

    # 判断左直右
    def _get_to_links(self, link_inout: dict) -> dict:
        to_links = {}
        for link_id, angle_1 in link_inout["in"]:
            turn = {"left": {}, "straight": {}, "right": {}}
            for link_id_2, angle_2 in link_inout["out"]:
                link = self.links_data[link_id_2]
                # 将结果限制在-180~180
                diff_angle = (angle_2 - angle_1 + 180) % 360 - 180
                # 直行
                if -45 <= diff_angle <= 45:
                    turn["straight"][link_id_2] = link
                # 左转
                elif 45 < diff_angle < 135:
                    turn["right"][link_id_2] = link
                # 右转
                elif -135 < diff_angle < -45:
                    turn["left"][link_id_2] = link
            to_links[link_id] = turn
        return to_links

    # 进行交叉口连接
    def _init_connectors(self) -> None:
        # 时针顺序
        link_order = self._get_link_order()
        # 判断进出关系
        link_inout = self._get_link_inout(link_order)
        # 判断左直右
        to_links = self._get_to_links(link_inout)

        # 连接
        for link_id in to_links:
            from_link = self.links_data[link_id]  # Link
            single_to_links = to_links[link_id]  # dict(turn_type: Link)

            # 进口道路段对象
            approach_link = ApproachLink(from_link, single_to_links)
            approach_link.add_all_direction_connectors()
            self.connectors_data.extend(approach_link.connectors_data)
            # 如果有问题
            if approach_link.warning:
                self.warning_turn_list.append(approach_link)


# 路网类
class Network:
    def __init__(self):
        # 路段数据
        self.network_link_obj_mapping: dict = dict()
        # 节点数据
        self.network_node_obj_mapping: dict = dict()
        # 其他数据
        self.network_other_data: dict = dict()

        # 连接段数据
        self.network_connectors_data: list = list()

        # 交叉口对象
        self._intersection_id: int = 0
        self._intersections: dict = dict()

        # 问题路段编号
        self.warning_link_list = {"type1": [], "type2": []}

    # 初始化数据
    def init_data(self, edges_data: dict, nodes_data: dict, other_data: dict) -> None:
        if not edges_data or not nodes_data:
            logger.logger_pytessng.warning("Empty network data!")
            return

        # 转换点数据
        for node_id, node in pgd.progress(nodes_data.items(), '数据解析中（3/7）'):
            node_id = str(node_id)
            loc = node["loc"]
            adjacent_edge_id_list = [str(link_id) for link_id in node["adjacent_edge_id_list"]]
            self.network_node_obj_mapping[node_id] = Node(node_id, loc, adjacent_edge_id_list)

        # 转换边数据
        for link_id, link in pgd.progress(edges_data.items(), '数据解析中（4/7）'):
            link_id = str(link_id)
            name = link.get("name", "")
            link_type = link["highway"]
            line = LineString(link["geometry"])
            start_node_id = str(link["start_node_id"])
            end_node_id = str(link["end_node_id"])
            is_oneway = link["is_oneway"]
            lane_count = link["lane_count"]
            self.network_link_obj_mapping[link_id] = Link(link_id, name, link_type, line, start_node_id, end_node_id, is_oneway, lane_count)

        # 其他数据
        self.network_other_data = other_data

    # 初始化路网
    def init_network(self) -> None:
        if not self.network_node_obj_mapping or not self.network_link_obj_mapping:
            return

        # 一、连接路段
        self._connect_links()

        # 二、定位交叉口
        group = self._find_closer_points(30)

        # 三、创建交叉口对象
        for nodes_id in pgd.progress(group.values(), '数据解析中（5/7）'):
            if len(nodes_id) <= 4:
                try:
                    error_turn_list = self._init_intersection(nodes_id)
                    # 转向有问题
                    self._record_error("type1", error_turn_list)
                except:
                    self._record_error("type2", nodes_id)
            else:
                # 路口的点太多
                self._record_error("type2", nodes_id)

        # 四、双向边复制为单向复制边
        self._copy_links()

    ###########################################################################

    # 一条路的中间连起来
    def _connect_links(self) -> None:
        network_nodes = self.network_node_obj_mapping.copy()

        for node_id, node in network_nodes.items():
            neighbor_id = node.adjacent_link_id_list
            neighbor_count = len(neighbor_id)

            # 只处理度为2的道路
            if neighbor_count != 2:
                continue

            link_id_1 = neighbor_id[0]
            link_id_2 = neighbor_id[1]
            link1 = self.network_link_obj_mapping[link_id_1]
            link2 = self.network_link_obj_mapping[link_id_2]

            # 单双属性要一样
            if link1.is_oneway != link2.is_oneway:
                logger.logger_pytessng.debug(
                    f"OpenStreetMap: The is_oneway of link{link_id_1} is different from that of link{link_id_2}.")
                continue

            # 获取道路角度
            if link1.start_node_id == node_id:
                angle1 = link1.start_angle
            else:
                angle1 = link1.end_angle
            if link2.start_node_id == node_id:
                angle2 = link2.start_angle
            else:
                angle2 = link2.end_angle

            # 计算角度差(-180~180)
            diff_angle = (angle2 - angle1 + 180) % 360 - 180

            # 不在一条线上不处理
            if not (-10 < diff_angle < 10 or diff_angle < -170 or diff_angle > 170):
                continue

            # 如果两段的车道数不一样
            if link1.lane_count != link2.lane_count:
                logger.logger_pytessng.debug(
                    f"OpenStreetMap: The lane count of link[{link_id_1}] ({link1.lane_count}) is different from that of link[{link_id_2}] ({link2.lane_count}).")
                lane_count = max(link1.lane_count, link2.lane_count)
            else:
                lane_count = link1.lane_count

            # →o→
            if link1.end_node_id == node_id and link2.start_node_id == node_id:
                start_node_id = link1.start_node_id
                end_node_id = link2.end_node_id
                new_line = LineString(list(link1.line.coords) + list(link2.line.coords)[1:])
                start_link_id = link_id_1
                end_link_id = link_id_2
            # →o←
            elif link1.end_node_id == node_id and link2.end_node_id == node_id:
                start_node_id = link1.start_node_id
                end_node_id = link2.start_node_id
                new_line = LineString(list(link1.line.coords)[:-1] + list(link2.line.coords)[::-1])
                start_link_id = link_id_1
                end_link_id = link_id_2
            # ←o←
            elif link1.start_node_id == node_id and link2.end_node_id == node_id:
                start_node_id = link2.start_node_id
                end_node_id = link1.end_node_id
                new_line = LineString(list(link2.line.coords) + list(link1.line.coords)[1:])
                start_link_id = link_id_2
                end_link_id = link_id_1
            # ←o→
            elif link1.start_node_id == node_id and link2.start_node_id == node_id:
                start_node_id = link1.end_node_id
                end_node_id = link2.end_node_id
                new_line = LineString(list(link1.line.coords)[::-1] + list(link2.line.coords)[1:])
                start_link_id = link_id_1
                end_link_id = link_id_2
            else:
                raise "123"

            # 处理边
            # ——删旧边
            for id_ in neighbor_id:
                self.network_link_obj_mapping.pop(id_)
            # ——加新边
            new_link_id = f"{link_id_1},{link_id_2}"
            new_link_name = ",".join(set(link1.name.split(",") + link2.name.split(",")))
            self.network_link_obj_mapping[new_link_id] = Link(new_link_id, new_link_name, link1.type, new_line, start_node_id,
                                                              end_node_id, link1.is_oneway, lane_count)

            # 处理点
            # ——删旧点
            self.network_node_obj_mapping.pop(node_id)
            # ——加新点
            self.network_node_obj_mapping[start_node_id].adjacent_link_id_list.remove(start_link_id)
            self.network_node_obj_mapping[end_node_id].adjacent_link_id_list.remove(end_link_id)
            self.network_node_obj_mapping[start_node_id].adjacent_link_id_list.append(new_link_id)
            self.network_node_obj_mapping[end_node_id].adjacent_link_id_list.append(new_link_id)

    ###########################################################################

    # 给定距离，搜索在该距离内的点集
    def _find_closer_points(self, max_distance: float) -> dict:
        # 只找度大于2的点
        nodes_id = []
        nodes = []
        for node_id, node in self.network_node_obj_mapping.items():
            if len(node.adjacent_link_id_list) >= 2:
                nodes_id.append(node_id)
                nodes.append(node.loc)

        # 树算法
        if len(nodes) >= 2:
            kdtree = KDTree(nodes, leafsize=10)
            pairs = kdtree.query_pairs(max_distance)
        else:
            pairs = []

        # 点分组
        group = {}
        group_id = 0
        for pair in pairs:
            node1_id = nodes_id[pair[0]]
            node2_id = nodes_id[pair[1]]
            if node1_id not in group and node2_id not in group:
                group[node1_id] = group_id
                group[node2_id] = group_id
                group_id += 1
            elif node1_id in group and node2_id not in group:
                group[node2_id] = group[node1_id]
            elif node1_id not in group and node2_id in group:
                group[node1_id] = group[node2_id]
            elif node1_id in group and node2_id in group:
                if group[node2_id] != group[node1_id]:
                    for k, v in group.items():
                        if v == group[node2_id]:
                            group[k] = group[node1_id]

        # 查缺补漏，只有一个点的交叉口
        for node_id in nodes_id:
            if node_id not in group:
                group[node_id] = group_id
                group_id += 1

        new_group = {}
        for node_id, group_id in group.items():
            if group_id not in new_group:
                new_group[group_id] = []
            new_group[group_id].append(node_id)

        return new_group

    ###########################################################################

    # 给node_id，搜索相邻link_id
    def _find_involved_elements(self, nodes_id: list) -> (dict, dict):
        links_id = set()
        for node_id in nodes_id:
            links_id.update(self.network_node_obj_mapping[node_id].adjacent_link_id_list)
        # 获取一个交叉口相关的点和边
        nodes = {node_id: self.network_node_obj_mapping[node_id] for node_id in nodes_id}
        links = {link_id: self.network_link_obj_mapping[link_id] for link_id in links_id}
        return nodes, links

    def _init_intersection(self, nodes_id: list) -> list:
        nodes, links = self._find_involved_elements(nodes_id)

        # 初始化交叉口对象
        intersection = Intersection(nodes, links)
        intersection.init_intersection()

        # 获取路网更新信息
        update_link = intersection.update_link
        update_node = intersection.update_node

        # 更新节点
        for old_link_id, new_links_id in update_node.items():
            nodes_id = [
                self.network_link_obj_mapping[old_link_id].start_node_id,
                self.network_link_obj_mapping[old_link_id].end_node_id
            ]
            for node_id in nodes_id:
                # 删
                self.network_node_obj_mapping[node_id].adjacent_link_id_list.remove(old_link_id)
                # 增
                self.network_node_obj_mapping[node_id].adjacent_link_id_list.extend(new_links_id)

        # 更新路段
        # 删
        for link_id in update_link["delete"]:
            self.network_link_obj_mapping.pop(link_id)
        # 改
        for link_id, link in update_link["update"].items():
            self.network_link_obj_mapping[link_id] = link
        # 增
        for link_id, link in update_link["insert"].items():
            self.network_link_obj_mapping[link_id] = link

        # 获取交叉口连接
        conns = intersection.connectors_data
        self.network_connectors_data.extend(conns)

        self._intersections[self._intersection_id] = intersection
        self._intersection_id += 1

        return intersection.warning_turn_list

    ###########################################################################

    # 单向边复制为双向边
    def _copy_links(self) -> None:
        network_links = self.network_link_obj_mapping.copy()
        for link_id, link in network_links.items():
            if not link.is_oneway:
                link1, link2 = link.shift()
                # 删
                self.network_link_obj_mapping.pop(link_id)
                # 增
                self.network_link_obj_mapping[link1.id] = link1
                self.network_link_obj_mapping[link1.id] = link2

    ###########################################################################

    # 记录问题
    def _record_error(self, error_type: str, error_list: list) -> None:
        # 转向太多
        if error_type == "type1":
            error_turn_list = error_list
            for turn in error_turn_list:
                self.warning_link_list["type1"].append(turn.current_link.id)
        # 交叉口的点太多
        elif error_type == "type2":
            nodes_id = error_list
            for node_id in nodes_id:
                links_id = self.network_node_obj_mapping[node_id].adjacent_link_id_list
                self.warning_link_list["type2"].extend(links_id)


class OsmNetwokAnalyser(BaseNetworkAnalyser):
    def analyse_all_data(self, network_data: dict, params: dict = None) -> dict:
        # 解析路网数据
        network = Network()
        network.init_data(**network_data)
        network.init_network()

        # 转为标准格式
        standard_links_data = [
            dict(
                id=link.id,
                points=list(link.line.coords),
                lane_count=link.lane_count,
                name=f"{link.type}: {link.name}"
            )
            for link_id, link in network.network_link_obj_mapping.items()
        ]
        standard_connectors_data = [
            dict(
                from_link_id=connector.from_link_id,
                to_link_id=connector.to_link_id,
                from_lane_numbers=connector.from_lane_numbers,
                to_lane_numbers=connector.to_lane_numbers,
            )
            for connector in network.network_connectors_data
        ]

        # 其他信息
        other_data = network.network_other_data
        # 更新投影
        self.proj_string = other_data["proj_string"]
        # 更新移动距离
        self.move_distance = other_data["move_distance"]

        return {
            "links": standard_links_data,
            "connectors": standard_connectors_data,
        }
