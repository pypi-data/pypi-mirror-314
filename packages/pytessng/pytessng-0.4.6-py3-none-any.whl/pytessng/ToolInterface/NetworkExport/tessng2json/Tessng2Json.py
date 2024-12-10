import json
from typing import Callable, Dict, List, Set
from pyproj import Proj

from ..BaseTessng2Other import BaseTessng2Other
from ...public.line.LineBase import LineBase
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class Tessng2Json(BaseTessng2Other):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 连接段ID到面域ID的映射
        self._connector_id_2_area_id_mapping: Dict[int, int] = {}
        # 车道转向类型
        self._lane_turn_type_mapping: Dict[int, Set[str]] = {}
        # 连接段ID到上下游路段ID的映射
        self._connector_id_2_link_id_mapping: Dict[int, Dict[str, int]] = {}
        # 车道连接ID到上下游车道信息的映射
        self._lane_connector_id_2_lane_info_mapping: Dict[int, Dict[str, int]] = {}

    def save_data(self, data: dict, file_path: str) -> None:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def analyze_data(self, proj_string: str = None) -> dict:
        # 路网属性
        attrs = self.netiface.netAttrs()

        # 移动距离
        move_distance = attrs.otherAttrs().get("move_distance")
        move_distance = {"x_move": 0, "y_move": 0} if move_distance is None else move_distance

        # 投影函数
        proj_func = Proj(proj_string) if proj_string else None

        # 头
        header = proj_string
        # 路网名称
        network_name: str = attrs.netName()
        # 面域数据
        area_data_list: List[dict] = self._read_area_data(move_distance, proj_func)
        # 连接段数据
        connector_data_list: List[dict] = self._read_connector_data(move_distance, proj_func)
        # 路段数据
        link_data_list: List[dict] = self._read_link_data(move_distance, proj_func)
        # # 交叉点数据
        # cross_point_list: List[dict] = self._read_cross_point_data()

        # 路网数据
        network_data = {
            "header": header,
            "name": network_name,
            "road": link_data_list,
            "connector": connector_data_list,
            "area": area_data_list,
            # "crossPoint": cross_point_list,
            "attr": attrs.otherAttrs(),
        }
        return network_data

    # 读取面域数据
    def _read_area_data(self, move_distance: dict, proj_func: Callable = None) -> list:
        area_data_list = []

        for area in pgd.progress(self.netiface.allConnectorArea(), '面域数据读取中（1/4）'):
            # 面域ID
            area_id = area.id()
            # 连接段ID列表
            connector_id_set = {connector.id() for connector in area.allConnector()}
            # 上游路段ID列表
            incoming_link_id_set = {connector.fromLink().id() for connector in area.allConnector()}
            # 下游路段ID列表
            outgoing_link_id_set = {connector.toLink().id() for connector in area.allConnector()}

            # 计算面域边界点
            boundary_points_tess = None
            boundary_points_real = None
            area_boundary_points = []
            # 保存连接段信息
            for connector in area.allConnector():
                # 获取连接段ID到面域ID的映射关系
                connector_id = connector.id()
                self._connector_id_2_area_id_mapping[connector_id] = area_id
                # 获取连接段边界点
                polygon = self._qtpoint2list(connector.polygon())
                area_boundary_points.append(polygon)

            # 计算面域边界点
            boundary_points = LineBase.calculate_boundary_points(area_boundary_points)
            if boundary_points:
                boundary_points_tess = boundary_points
                if proj_func:
                    boundary_points_real = [proj_func(x, y, inverse=True) for x, y in boundary_points]
            else:
                logger.logger_pytessng.error(f"Failed to calculate boundary points of area {area.id()}!")

            # 面域数据
            area_data = {
                "id": area_id,
                "connector": list(connector_id_set),
                "incomingRoads": list(incoming_link_id_set),
                "outgoingRoads": list(outgoing_link_id_set),
                # tess坐标
                "pointsTess": boundary_points_tess,
                # 经纬度坐标
                "pointsReal": boundary_points_real,
            }
            area_data_list.append(area_data)

        return area_data_list

    # 读取连接段数据
    def _read_connector_data(self, move_distance: dict, proj_func: Callable = None) -> list:
        connector_data_list = []

        connectors = self.netiface.connectors()
        for connector in pgd.progress(connectors, '连接段数据读取中（2/4）'):
            # 连接段ID
            connector_id = connector.id()
            # 连接段名称
            connector_name = connector.name()
            # 连接段上游路段ID
            from_link_id = connector.fromLink().id()
            # 连接段下游路段ID
            to_link_id = connector.toLink().id()
            # 面域ID
            area_id = self._connector_id_2_area_id_mapping[connector_id]
            # 连接段长度
            connector_length = self._p2m(connector.length())

            # 车道连接列表
            lane_connector_data_list = []
            for lane_connector in connector.laneConnectors():
                # 车道连接ID
                lane_connector_id = lane_connector.id()
                # 车道连接长度
                lane_connector_length = self._p2m(lane_connector.length())
                # 上游车道ID
                from_lane_id = lane_connector.fromLane().id()
                # 上游车道序号
                from_lane_number = lane_connector.fromLane().number()
                # 下游车道ID
                to_lane_id = lane_connector.toLane().id()
                # 下游车道序号
                to_lane_number = lane_connector.toLane().number()

                # 中心线
                center_points_tess = self._qtpoint2list(lane_connector.centerBreakPoint3Ds(), move_distance)
                # 左边线
                left_points_tess = self._qtpoint2list(lane_connector.leftBreakPoint3Ds(), move_distance)
                # 右边线
                right_points_tess = self._qtpoint2list(lane_connector.rightBreakPoint3Ds(), move_distance)
                # 中心线开始点
                start_center_point_tess = center_points_tess[0]
                # 中心线结束点
                end_center_point_tess = center_points_tess[-1]

                # 中心线
                center_points_real = self._xy2lonlat(center_points_tess, proj_func) if proj_func else None
                # 左边线
                left_points_real = self._xy2lonlat(left_points_tess, proj_func) if proj_func else None
                # 右边线
                right_points_real = self._xy2lonlat(right_points_tess, proj_func) if proj_func else None
                # 中心线开始点
                start_center_point_real = center_points_real[0] if proj_func else None
                # 中心线结束点
                end_center_point_real = center_points_real[-1] if proj_func else None

                # 车道连接数据
                lane_connector_data = {
                    'id': lane_connector_id,
                    'length': lane_connector_length,
                    'predecessor': from_lane_id,
                    'predecessorNumber': from_lane_number,
                    'successor': to_lane_id,
                    'successorNumber': to_lane_number,
                    # tess坐标
                    'centerPointsTess': center_points_tess,
                    'leftPointsTess': left_points_tess,
                    'rightPointsTess': right_points_tess,
                    'startPointsTess': start_center_point_tess,
                    'endPointsTess': end_center_point_tess,
                    # 经纬度坐标
                    'centerPointsReal': center_points_real,
                    'leftPointsReal': left_points_real,
                    'rightPointsReal': right_points_real,
                    'startPointsReal': start_center_point_real,
                    'endPointsReal': end_center_point_real,
                }
                lane_connector_data_list.append(lane_connector_data)

                # 记录车道连接ID到车道信息映射
                self._lane_connector_id_2_lane_info_mapping[lane_connector_id] = {
                    "from_link_id": from_link_id,
                    "to_link_id": to_link_id,
                    "from_lane_number": from_lane_number,
                    "to_lane_number": to_lane_number,
                    "connector_id": connector_id,
                }

                # 计算转向类型
                if from_lane_id not in self._lane_turn_type_mapping.keys():
                    self._lane_turn_type_mapping[from_lane_id] = set()
                turn_type = LineBase.calculate_turn_type(center_points_tess)
                self._lane_turn_type_mapping[from_lane_id].add(turn_type)

            # 连接段数据
            connector_data = {
                'id': connector_id,
                'name': connector_name,
                'predecessor': from_link_id,
                'successor': to_link_id,
                'areaId': area_id,
                'length': connector_length,
                'links': lane_connector_data_list,
            }
            connector_data_list.append(connector_data)

            # 记录连接段ID到上下游路段ID的映射
            self._connector_id_2_link_id_mapping[connector_id] = {
                "from_link_id": from_link_id,
                "to_link_id": to_link_id,
            }

        return connector_data_list

    # 读取路段数据
    def _read_link_data(self, move_distance: dict, proj_func: Callable = None) -> list:
        link_data_list = []

        links = self.netiface.links()
        for link in pgd.progress(links, '路段数据读取中（3/4）'):
            # 路段ID
            link_id = link.id()
            # 路段名称
            link_name = link.name()
            # 路段长度
            link_length = self._p2m(link.length())
            # 路段车道数
            link_lane_count = link.laneCount()
            # 车道限速
            link_limit_speed = link.limitSpeed()  # km/h

            # 路段上游连接段ID
            from_connectors = link.fromConnectors()
            from_connector_id_list = [connector.id() for connector in from_connectors]
            # 路段下游连接段ID
            to_connectors = link.toConnectors()
            to_connector_id_list = [connector.id() for connector in to_connectors]
            # 路段上游路段ID
            from_link_id_list = [self._connector_id_2_link_id_mapping[connector.id()]["from_link_id"] for connector in from_connectors]
            # 路段下游路段ID
            to_link_id_list = [self._connector_id_2_link_id_mapping[connector.id()]["to_link_id"] for connector in to_connectors]

            # 路段中心线
            link_center_points_tess = self._qtpoint2list(link.centerBreakPoint3Ds(), move_distance)
            link_center_points_real = self._xy2lonlat(link_center_points_tess, proj_func) if proj_func else None

            # 转向角度
            bearing_angle = LineBase.calculate_angle_with_y_axis(link_center_points_tess[-2], link_center_points_tess[-1])

            # 车道列表
            lanes = []
            for lane in link.lanes():
                # 车道ID
                lane_id = lane.id()
                # 车道序号
                lane_number = lane.number()
                # 车道长度
                lane_length = self._p2m(lane.length())
                # 车道宽度
                lane_width = self._p2m(lane.width())
                # 车道类型
                lane_type = lane.actionType()
                # 车道转向类型
                lane_turn_types = list(self._lane_turn_type_mapping.get(lane.id(), set()))

                # 中心线
                center_points_tess = self._qtpoint2list(lane.centerBreakPoint3Ds(), move_distance)
                # 左边线
                left_points_tess = self._qtpoint2list(lane.leftBreakPoint3Ds(), move_distance)
                # 右边线
                right_points_tess = self._qtpoint2list(lane.rightBreakPoint3Ds(), move_distance)
                # 中心线开始点
                start_center_point_tess = center_points_tess[0]
                # 中心线结束点
                end_center_point_tess = center_points_tess[-1]

                # 中心线
                center_points_real = self._xy2lonlat(center_points_tess, proj_func) if proj_func else None
                # 左边线
                left_points_real = self._xy2lonlat(left_points_tess, proj_func) if proj_func else None
                # 右边线
                right_points_real = self._xy2lonlat(right_points_tess, proj_func) if proj_func else None
                # 中心线开始点
                start_center_point_real = center_points_real[0] if proj_func else None
                # 中心线结束点
                end_center_point_real = center_points_real[-1] if proj_func else None

                # 车道数据
                lane_data = {
                    'id': lane_id,
                    'number': lane_number,
                    'length': lane_length,
                    'width': lane_width,
                    'type': lane_type,
                    'turnTypes': lane_turn_types,  # 新旧兼容
                    'turnType': lane_turn_types,  # 新旧兼容
                    'limitSpeed': link_limit_speed,
                    # tess坐标
                    'centerPointsTess': center_points_tess,
                    'leftPointsTess': left_points_tess,
                    'rightPointsTess': right_points_tess,
                    'startPointsTess': start_center_point_tess,
                    'endPointsTess': end_center_point_tess,
                    # 经纬度坐标
                    'centerPointsReal': center_points_real,
                    'leftPointsReal': left_points_real,
                    'rightPointsReal': right_points_real,
                    'startPointsReal': start_center_point_real,
                    'endPointsReal': end_center_point_real,
                }
                lanes.append(lane_data)

            # 路段数据
            link_data = {
                'id': link_id,
                'name': link_name,
                'length': link_length,
                'laneCount': link_lane_count,
                'limitSpeed': link_limit_speed,
                'bearing': bearing_angle,
                'predecessorConnectors': from_connector_id_list,
                'successorConnectors': to_connector_id_list,
                'predecessorRoads': from_link_id_list,
                'successorRoads': to_link_id_list,
                'pointsTess': link_center_points_tess,
                'pointsReal': link_center_points_real,
                'lanes': lanes,
            }
            link_data_list.append(link_data)

        return link_data_list

    # 读取交叉点数据
    def _read_cross_point_data(self) -> list:
        cross_point_data_list = []

        # 已经读取过的交叉点集合
        cp_set: set = set()

        # 遍历连接段
        for connector in pgd.progress(self.netiface.connectors(), "交叉点数据读取中（4/4）"):
            # 遍历连接段的各车道
            for lane_connector in connector.laneConnectors():
                # 获取交叉点
                cps = self.netiface.crossPoints(lane_connector)

                # 如果没有交叉点则跳过
                if len(cps) == 0:
                    continue

                # 遍历交叉点，提取信息
                for cp in cps:
                    # 如果已经读取过了则跳过
                    if cp in cp_set:
                        continue
                    cp_set.add(cp)

                    # 当前交叉点信息
                    cross_point_data: dict = {}

                    name_list = ["main", "minor"]
                    lane_connector_list = [cp.mpMainLaneConnector, cp.mpLaneConnector]
                    for name, _lane_connector in zip(name_list, lane_connector_list):
                        # 车道连接ID
                        lane_connector_id = _lane_connector.id()
                        # 上下游车道信息
                        lane_connector_info: Dict[str, int] = self._lane_connector_id_2_lane_info_mapping[lane_connector_id]
                        # 上游路段ID
                        from_link_id = lane_connector_info["from_link_id"]
                        # 下游路段ID
                        to_link_id = lane_connector_info["to_link_id"]
                        # 上游车道序号
                        from_lane_number = lane_connector_info["from_lane_number"]
                        # 下游车道序号
                        to_lane_number = lane_connector_info["to_lane_number"]
                        # 所在连接段ID
                        connector_id = lane_connector_info["connector_id"]

                        # 距离
                        if name == "main":
                            dist = _lane_connector.length() - cp.mrDistance
                        else:
                            dist = 0
                            # 遍历所有被交车道的交叉点
                            for point in self.netiface.crossPoints(_lane_connector):
                                if point.mpLaneConnector == lane_connector_list[0]:
                                    dist = _lane_connector.length() - point.mrDistance
                                    break

                        # 添加到字典
                        cross_point_data[name + "FromLink"] = from_link_id
                        cross_point_data[name + "ToLink"] = to_link_id
                        cross_point_data[name + "FromLane"] = from_lane_number
                        cross_point_data[name + "ToLane"] = to_lane_number
                        cross_point_data[name + "Connector"] = connector_id
                        cross_point_data[name + 'Dist'] = dist

                    # 添加到列表
                    cross_point_data_list.append(cross_point_data)

        return cross_point_data_list
