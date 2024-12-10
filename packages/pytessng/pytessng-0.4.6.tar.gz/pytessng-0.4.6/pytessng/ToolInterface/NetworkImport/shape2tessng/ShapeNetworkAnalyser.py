import random
import string
import traceback
import collections
import numpy as np
from pyproj import Proj
import scipy.spatial as spt

from ..BaseNetworkAnalyser import BaseNetworkAnalyser
from .LanesPointsCalculator import LanesPointsCalculator
from ...public.coordinate.CoordinateCalculator import CoordinateCalculator
from ...public.line.LinePointsDeviator import LinePointsDeviator
from ...public.line.LaneNumbersSorter import LaneNumbersSorter
from pytessng.Config import NetworkImportConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class ShapeNetworkAnalyser(BaseNetworkAnalyser):
    # 车道类型映射表 车道类型英文：车道类型中文
    LANE_TYPE_MAPPING = NetworkImportConfig.LANE_TYPE_MAPPING
    # 默认车道宽度映射表 车道类型：车道宽度
    DEFAULT_LANE_WIDTH_MAPPING = NetworkImportConfig.Shape.DEFAULT_LANE_WIDTH_MAPPING
    # 最小车道宽度
    MIN_LANE_WIDTH = NetworkImportConfig.Shape.MIN_LANE_WIDTH
    # 其他参数
    MAX_LENGTH_DIFF = NetworkImportConfig.Shape.MAX_LENGTH_DIFF
    MAX_DISTANCE_LANE_POINTS = NetworkImportConfig.Shape.MAX_DISTANCE_LANE_POINTS
    MIN_DISTANCE_LANE_POINTS = NetworkImportConfig.Shape.MIN_DISTANCE_LANE_POINTS
    MAX_DISTANCE_SEARCH_POINTS = NetworkImportConfig.Shape.MAX_DISTANCE_SEARCH_POINTS

    def __init__(self):
        super().__init__()
        # 投影
        self.proj = lambda x, y: (x, y)

    def analyse_all_data(self, network_data, params: dict = None) -> dict:
        lanes_data, lane_connectors_data, file_proj_string = network_data

        # 是否是使用经纬度
        is_use_lon_and_lat = params["is_use_lon_and_lat"]
        # 是否导入的是车道中心线
        is_use_center_line = params["is_use_center_line"]
        # 投影方式
        proj_mode = params["proj_mode"]

        # 解析路段数据
        links_data, lanes_data = self.analyse_links(lanes_data, file_proj_string, is_use_lon_and_lat, is_use_center_line, proj_mode)
        # 解析连接段数据
        connectors_data = self.analyse_connectors(lane_connectors_data, lanes_data) if lane_connectors_data is not None else collections.defaultdict(list)
        # 对距离过近的路段进行自动连接
        connectors_data = self.analyse_automatic_connect(links_data, connectors_data)
        # 处理渐变段（导入边界线才用到）
        links_data = self.analyse_gradient_section(links_data, is_use_center_line)
        # 重新计算路段中心线
        links_data = self.analyse_center_line(links_data)

        # 标准路段数据
        standard_links_data = [
            dict(
                id=link_id,
                points=link_data["points"],
                lanes_points=link_data["lanes_points"],
                lanes_type=link_data["lanes_type"],
            )
            for link_id, link_data in links_data.items()
        ]
        # 标准连接段数据
        standard_connectors_data = [
            dict(
                from_link_id=connector_id[0],
                to_link_id=connector_id[1],
                from_lane_numbers=[lane["from_lane_number"] for lane in connector_data],
                to_lane_numbers=[lane["to_lane_number"] for lane in connector_data],
                lanes_points=[lane["points"] for lane in connector_data] if all([lane.get("points") for lane in connector_data]) else None
            )
            for connector_id, connector_data in connectors_data.items()
        ]

        return {
            "links": standard_links_data,
            "connectors": standard_connectors_data,
        }

    # 解析路段数据
    def analyse_links(self, lanes_data: tuple, file_proj_string: str, is_use_lon_and_lat: bool, is_use_center_line: bool, proj_mode: str) -> (dict, dict):
        all_data_dbf_lane, all_data_shp_lane = lanes_data

        # 中心位置
        x_list, y_list = [], []
        for lane_data_shp in all_data_shp_lane:
            x_list.extend([point[0] for point in lane_data_shp.points])
            y_list.extend([point[1] for point in lane_data_shp.points])
        if is_use_lon_and_lat:
            x_0, y_0 = CoordinateCalculator.calculate_center_coordinate(min(x_list), max(x_list), min(y_list), max(y_list))
        else:
            x_0, y_0 = (min(x_list) + max(x_list)) / 2, (min(y_list) + max(y_list)) / 2

        # 投影方式
        if is_use_lon_and_lat:
            if "prj" in proj_mode:
                proj_string = file_proj_string
            elif "tmerc" in proj_mode:
                proj_string = f'+proj=tmerc +lon_0={x_0} +lat_0={y_0} +ellps=WGS84'
            elif "utm" in proj_mode:
                proj_string = f'+proj=utm +zone={x_0 // 6 + 31} +ellps=WGS84'
            elif "web" in proj_mode:
                proj_string = 'EPSG:3857'
            else:
                proj_string = f'+proj=tmerc +lon_0={x_0} +lat_0={y_0} +ellps=WGS84'
                logger.logger_pytessng.warning("No this projection mode!")
            self.proj = Proj(proj_string)
            self.proj_string = proj_string
        else:
            self.proj = lambda x, y: [x, y]

        # 保存路段信息
        links_info = collections.defaultdict(lambda: {'lanes_data': {}, 'obj': None})
        # 保存车道信息
        lanes_info = {}

        # 读取数据，并组合dbf数据和shp数据
        for index, lane_data_shp in pgd.progress(enumerate(all_data_shp_lane), "数据读取中（1/9）"):
            # 获取该路段的dbf数据
            lane_data_dbf = all_data_dbf_lane[index]

            # 经纬度转为平面坐标
            xy_list = [self.proj(point[0], point[1]) for point in lane_data_shp.points]

            # 判断属性z是否存在
            if hasattr(lane_data_shp, "z"):
                z_list = lane_data_shp.z
            else:
                z_list = [0 for _ in range(len(xy_list))]

            # 获取三维坐标
            points_3D = [[x, y, z] for (x, y), z in zip(xy_list, z_list)]

            # 记录link车道级信息, 两种关系，路段-车道 和 车道-路段
            road_id = lane_data_dbf.get('roadId')

            # 如果没有路段ID就跳过
            if not road_id:
                logger.logger_pytessng.error("The roadId is missing!")
                continue

            # 如果没有车道ID就用生成的随机字符串
            lane_id = lane_data_dbf.get('id') or ''.join(random.choice(string.ascii_letters) for _ in range(9))

            lane_type = lane_data_dbf.get('type') or "driving"
            lane_width = lane_data_dbf.get('width') or self.DEFAULT_LANE_WIDTH_MAPPING[lane_type]
            lane_type_chinese = self.LANE_TYPE_MAPPING.get(lane_type, "机动车道")

            links_info[road_id]["lanes_data"][lane_id] = {
                'roadId': road_id,
                'type': lane_type_chinese,
                'width': float(lane_width),
                'points': points_3D,
            }

        global_lane_id = 0  # 使用边界线才用到这个
        for road_id in pgd.progress(list(links_info.keys()), "数据解析中（2/9）"):
            # (1) 重新计算点，保证同一路段各条车道的断点的数量相同
            lanes_points = [lane["points"] for lane in links_info[road_id]["lanes_data"].values()]
            if not lanes_points or not all([len(lane) for lane in lanes_points]):
                del links_info[road_id]
                continue
            new_lanes_points = LanesPointsCalculator().calculate_lanes_with_same_points(
                lanes_points,
                self.MAX_LENGTH_DIFF,
                self.MAX_DISTANCE_LANE_POINTS,
                self.MIN_DISTANCE_LANE_POINTS,
                force=True
            )
            if not new_lanes_points:
                logger.logger_pytessng.error(f"Link {road_id} does not meet the constraint conditions.")
                del links_info[road_id]
                continue

            for index, lane_id in enumerate(links_info[road_id]["lanes_data"].keys()):
                links_info[road_id]["lanes_data"][lane_id]["points"] = new_lanes_points[index]

            # (2) 分中心线和边界线，获取车道的左/中/右线
            # (2.1) 如果使用中心线
            if is_use_center_line:
                # 遍历该路段上的车道
                for lane_id, lane in links_info[road_id]["lanes_data"].items():
                    lane_width = lane["width"]
                    lane_points_centerLine = lane["points"]
                    lane_points_threeLine = LinePointsDeviator.deviate_points(lane_points_centerLine, {
                        "right": ['right', lane_width * 0.5],
                        "center": ['right', lane_width * 0],
                        "left": ['right', lane_width * -0.5],
                    })
                    links_info[road_id]["lanes_data"][lane_id]["points"] = lane_points_threeLine
            # (2.2) 如果使用边界线
            else:
                temp_data_roadId = []
                temp_data_type = []
                temp_data_points = []

                # 遍历该路段上的车道
                for lane_id, lane in links_info[road_id]["lanes_data"].items():
                    road_id = lane["roadId"]
                    temp_data_roadId.append(road_id)

                    lane_type = lane["type"]
                    temp_data_type.append(lane_type)

                    lane_points_boundaryLine = lane["points"]
                    temp_data_points.append(lane_points_boundaryLine)

                # 清空字典，不用原来的车道ID
                links_info[road_id]["lanes_data"].clear()

                # 获取边界线顺序，从右向左
                order = LaneNumbersSorter.sort_lane_number(temp_data_points)

                for i in range(1, len(temp_data_points)):
                    road_id = temp_data_roadId[order.index(i)]
                    lane_type = temp_data_type[order.index(i)]

                    # 取中值计算中心线点位
                    rightLine = temp_data_points[order.index(i)]
                    leftLine = temp_data_points[order.index(i + 1)]
                    centerLine = [tuple(v) for v in (np.array(rightLine) + np.array(leftLine)) / 2]

                    lane_points_threeLine = {
                        "left": leftLine,
                        "right": rightLine,
                        "center": centerLine,
                    }

                    links_info[road_id]["lanes_data"][global_lane_id] = {
                        'roadId': road_id,
                        'type': lane_type,
                        'points': lane_points_threeLine
                    }

                    global_lane_id += 1

            # (3) 添加laneNumber
            lanes_points = [lane["points"]["center"] for lane in links_info[road_id]["lanes_data"].values()]
            if not lanes_points:
                logger.logger_pytessng.error(f"Link {road_id} does not meet the constraint conditions.")
                del links_info[road_id]
                continue
            # 获取车道序号列表
            laneNumber_list = LaneNumbersSorter.sort_lane_number(lanes_points)
            # 添加laneNumber信息
            for index, lane_id in enumerate(links_info[road_id]["lanes_data"].keys()):
                links_info[road_id]["lanes_data"][lane_id]["laneNumber"] = laneNumber_list[index]

                # 保存单独车道信息
                lanes_info[lane_id] = links_info[road_id]["lanes_data"][lane_id]

            # 按车道序号排序，主要是为了中心线的情况
            links_info[road_id]["lanes_data"] = dict(
                sorted(links_info[road_id]["lanes_data"].items(), key=lambda item: item[1]["laneNumber"]))

        return links_info, lanes_info

    # 解析连接段数据
    def analyse_connectors(self, lane_connectors_data: tuple, lanes_info) -> dict:
        all_data_dbf_laneConnector, all_data_shp_laneConnector = lane_connectors_data

        # 保存连接段信息
        connectors_info = collections.defaultdict(list)

        # 读取数据，并组合dbf数据和shp数据
        for index, laneConnector_data_shp in pgd.progress(enumerate(all_data_shp_laneConnector), "数据读取中（3/9）"):
            # 获取该路段的dbf数据
            laneConnector_data_dbf = all_data_dbf_laneConnector[index]

            # 经纬度转为平面坐标
            xy_list = [self.proj(point[0], point[1]) for point in laneConnector_data_shp.points]

            # 判断属性z是否存在
            if hasattr(laneConnector_data_shp, "z"):
                z_list = laneConnector_data_shp.z
            else:
                z_list = [0 for i in range(len(xy_list))]

            # 获取上下游路段ID
            try:
                from_lane_id = laneConnector_data_dbf['preLaneId']
                to_lane_id = laneConnector_data_dbf['sucLaneId']
                from_lane_info = lanes_info[from_lane_id]
                to_lane_info = lanes_info[to_lane_id]
            except:
                logger.logger_pytessng.error(f"Connector with the error: {traceback.format_exc()}")
                continue

            # 车道连接的属性
            from_lane_type = from_lane_info["type"]
            to_lane_type = to_lane_info["type"]
            if from_lane_type != to_lane_type:
                continue

            lane_width = laneConnector_data_dbf.get('width') or self.DEFAULT_LANE_WIDTH_MAPPING.get(from_lane_type, 3.5)

            # 获取三维坐标
            points_3D = [[x, y, z] for (x, y), z in zip(xy_list, z_list)]

            lane_points_threeLine = LinePointsDeviator.deviate_points(points_3D, {
                "right": ['right', lane_width * 0.5],
                "center": ['right', lane_width * 0],
                "left": ['right', lane_width * -0.5],
            })

            # 将同上下游路段的连接器放在一起
            connector_road_tuple = (from_lane_info['roadId'], to_lane_info['roadId'])
            connectors_info[connector_road_tuple].append(
                {
                    "from_lane_number": from_lane_info['laneNumber'],
                    "to_lane_number": to_lane_info['laneNumber'],
                    'points': lane_points_threeLine,
                }
            )

        return connectors_info

    # 根据距离新增连接属性
    def analyse_automatic_connect(self, links_info: dict, connectors_info: dict) -> dict:
        nodes = []
        for road_id in pgd.progress(links_info, "数据解析中（4/9）"):
            for lane_info in links_info[road_id]["lanes_data"].values():
                lane_points = lane_info['points']["center"]
                nodes += [
                    {
                        'point': lane_points[0],
                        'contactPoint': 'end',  # 车道起点、为连接的终点
                        'laneNumber': lane_info['laneNumber'],
                        'roadId': road_id,
                        'type': lane_info["type"]
                    },
                    {
                        'point': lane_points[-1],
                        'contactPoint': 'start',  # 车道终点、为连接的起点
                        'laneNumber': lane_info['laneNumber'],
                        'roadId': road_id,
                        'type': lane_info["type"]
                    },
                ]

        # 寻找最近点
        node_points = [node['point'] for node in nodes]

        if node_points:
            # 用于快速查找的KDTree类
            kt = spt.KDTree(data=node_points, leafsize=10)

            # 获取距离较近的所有的点对
            node_groups = kt.query_pairs(self.MAX_DISTANCE_SEARCH_POINTS)

            # 保持之前已经存在的连接段键值
            exist_connector_tuples = list(connectors_info.keys())

            for node_group in pgd.progress(node_groups, "数据解析中（5/9）"):
                node_0, node_1 = nodes[node_group[0]], nodes[node_group[1]]
                # 如果link中的两个点既不在一条路段上，又不是同一起终类型，可以认为具有连接关系
                if node_0['roadId'] != node_1['roadId'] and node_0['contactPoint'] != node_1['contactPoint'] and node_0['type'] == node_1['type']:

                    if node_0['contactPoint'] == 'start':
                        from_lane_info, to_lane_info = node_0, node_1
                    else:
                        from_lane_info, to_lane_info = node_1, node_0
                    connector_road_tuple = (from_lane_info['roadId'], to_lane_info['roadId'])
                    from_lane_number, to_lane_number = from_lane_info['laneNumber'], to_lane_info['laneNumber']

                    # 如果之前没有
                    if connector_road_tuple not in exist_connector_tuples:
                        connectors_info[connector_road_tuple].append(
                            {
                                "from_lane_number": from_lane_number,
                                "to_lane_number": to_lane_number,
                            }
                        )

        return connectors_info

    # 对拓宽段进行处理，窄的地方直接裁掉（导入边界线才用到）
    def analyse_gradient_section(self, links_info: dict, is_use_center_line: bool = False):
        # 如果是使用中心线，则直接返回
        if is_use_center_line:
            # 虚拟进度条
            for _ in pgd.progress(range(100), "数据解析中（6/9）"):
                pass
            return links_info

        # 如果使用边界线
        for road_id in pgd.progress(list(links_info.keys()), "数据解析中（6/9）"):
            # 只有该路段有至少两条车道才进行处理
            if len(links_info[road_id]["lanes_data"]) == 1:
                continue

            # 分别处理左侧拓宽和右侧拓宽的情况
            for num in [0, -1]:
                lane_id = list(links_info[road_id]["lanes_data"].keys())[num]
                lane_data = links_info[road_id]["lanes_data"][lane_id]
                leftLine = lane_data["points"]["left"]
                rightLine = lane_data["points"]["right"]
                # 只把大于最小宽度的点序号接入临时列表
                temp_list = []
                for j in range(len(leftLine)):
                    left_x, left_y = leftLine[j][0], leftLine[j][1]
                    right_x, right_y = rightLine[j][0], rightLine[j][1]
                    distance = ((left_x - right_x) ** 2 + (left_y - right_y) ** 2) ** 0.5
                    # 小于一定宽度路段要删除
                    if distance >= self.MIN_LANE_WIDTH:
                        temp_list.append(j)
                # 如果有比较窄的地方
                if len(temp_list) != len(links_info[road_id]["lanes_data"][lane_id]["points"]["left"]):
                    # N车道的路段
                    for lane_id in links_info[road_id]["lanes_data"]:
                        for j in ["left", "center", "right"]:
                            links_info[road_id]["lanes_data"][lane_id]["points"][j] = [
                                links_info[road_id]["lanes_data"][lane_id]["points"][j][k] for k in temp_list]

        return links_info

    # 重新计算路段的中心线
    def analyse_center_line(self, links_info: dict):
        new_links_info = {}
        for link_id, link_info in pgd.progress(links_info.items(), "数据解析中（7/9）"):
            lanes_type = [lane["type"] for lane in link_info["lanes_data"].values()]
            lanes_points = [dict(lane["points"]) for lane in link_info["lanes_data"].values()]

            # 获取路段点位
            # 如果是奇数，取中间车道的中心线
            laneCount = len(lanes_points)
            if laneCount % 2 == 1:
                link_points = lanes_points[int((laneCount - 1) / 2)]["center"]
            # 如果是偶数，取中间两车道的边线
            else:
                link_points = lanes_points[int(laneCount / 2)]["right"]

            new_links_info[link_id] = {
                "points": link_points,
                "lanes_type": lanes_type,
                "lanes_points": lanes_points
            }

        return new_links_info
