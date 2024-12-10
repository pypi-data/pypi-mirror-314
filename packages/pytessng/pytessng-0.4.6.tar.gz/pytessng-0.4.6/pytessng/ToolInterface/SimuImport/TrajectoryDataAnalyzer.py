from typing import Optional, Callable
import pandas as pd
from pyproj import Proj
from PySide2.QtCore import QPointF


# 车辆数据解析者类
class TrajectoryDataAnalyzer:
    def __init__(self, netiface):
        self._netiface = netiface

        self._m2p: Optional[Callable] = None
        self._proj_func: Optional[Callable] = None
        self._move_distance: Optional[dict] = None

    def analyze_trajectory_data(self, traj_file_path: str, proj_string: str) -> pd.DataFrame:
        # 更新比例尺、投影、移动函数
        self._update_functions(proj_string)

        # 读取数据
        vehicles_data: pd.DataFrame = pd.read_csv(traj_file_path)

        # 使时间戳从0开始
        vehicles_data["timestamp"] -= vehicles_data["timestamp"].min()

        # 获取车辆创建信息
        analyzed_vehicles_data = vehicles_data.groupby("objId").apply(self._operation)

        # 释放内存
        del vehicles_data

        return analyzed_vehicles_data

    def _update_functions(self, proj_string: str) -> None:
        # (1) 比例尺转换
        scene_scale = self._netiface.sceneScale()
        self._m2p = lambda x: x / scene_scale

        # (2) 投影转换
        self._proj_func = Proj(proj_string) if proj_string else lambda x, y: (x, y)

        # (3) 移动距离
        move = self._netiface.netAttrs().otherAttrs().get("move_distance")
        self._move_distance = {"x_move": 0, "y_move": 0} if move is None or "tmerc" in proj_string else move

    # 对每个车辆的DataFrame做的操作
    def _operation(self, vehicle_data: pd.DataFrame) -> pd.Series:
        # 获取第一个数据点
        first_point = vehicle_data.iloc[0]
        # 获取经纬度
        lon0, lat0 = first_point["longitude"], first_point["latitude"]
        # 获取平面坐标
        x0, y0 = self._proj_func(lon0, lat0)
        # 加上偏移量
        x0, y0 = x0 + self._move_distance["x_move"], y0 + self._move_distance["y_move"]
        # 定位位置
        locations = self._netiface.locateOnCrid(QPointF(self._m2p(x0), -self._m2p(y0)), 9)
        if not locations:
            return pd.Series()

        # 所在路段、车道、距离
        location = locations[0]
        dist = location.distToStart
        lane_object = location.pLaneObject
        # 路段
        if lane_object.isLane():
            lane = location.pLaneObject.castToLane()
            link = lane.link()
            road_id = link.id()
            lane_number = lane.number()
            to_lane_number = None
        # 连接段
        else:
            lane_connector = location.pLaneObject.castToLaneConnector()
            connector = lane_connector.connector()
            road_id = connector.id()
            lane_number = lane_connector.fromLane().number()
            to_lane_number = lane_connector.toLane().number()

        # 创建时间
        create_time = int(first_point["timestamp"])  # ms
        # 车辆类型
        type_code = int(first_point["typeCode"])

        # 途径路段ID
        if "roadId" in vehicle_data.columns:
            route_link_id_list = vehicle_data["roadId"].drop_duplicates().tolist()
        else:
            coords = list(zip(vehicle_data["longitude"], vehicle_data["latitude"]))
            route_link_id_list = self._get_route_link_id_list_by_coords(coords)

        series = pd.Series(
            [create_time, type_code, road_id, dist, lane_number, to_lane_number, route_link_id_list],
            index=["create_time", "type_code", "road_id", "dist", "lane_number", "to_lane_number", "route_link_id_list"],
        )

        return series

    # 通过坐标获取途径路段ID
    def _get_route_link_id_list_by_coords(self, coords: list) -> list:
        route_link_id_list = []
        for lon, lat in coords:
            x, y = self._proj_func(lon, lat)
            locations = self._netiface.locateOnCrid(QPointF(self._m2p(x), -self._m2p(y)), 9)
            if locations:
                location = locations[0]
                lane_object = location.pLaneObject
                if lane_object.isLane():
                    lane = location.pLaneObject.castToLane()
                    link_id = lane.link().id()
                    # 避免重复添加
                    if not route_link_id_list or (route_link_id_list and route_link_id_list[-1] != link_id):
                        route_link_id_list.append(link_id)

        # 避免路段ID断裂
        completed_link_id_list = route_link_id_list[:1]
        route_link_list = [self._netiface.findLink(link_id) for link_id in route_link_id_list]
        for link_1, link_2 in zip(route_link_list[:-1], route_link_list[1:]):
            # 获取最短路径
            routing = self._netiface.shortestRouting(link_1, link_2)
            if routing is None:
                return completed_link_id_list
            temp_link_id_list = [link.id() for link in routing.getLinks()]
            completed_link_id_list += temp_link_id_list[1:]

        return completed_link_id_list
