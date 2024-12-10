import os
from pyproj import Proj
from geopandas import GeoDataFrame
from shapely.geometry import LineString

from ..BaseTessng2Other import BaseTessng2Other
from pytessng.Config import NetworkExportConfig
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class Tessng2Shape(BaseTessng2Other):
    def save_data(self, data: tuple, file_path: str) -> None:
        lane_gdf, lane_connector_gdf = data

        # 创建文件夹
        os.makedirs(file_path, exist_ok=True)

        # 写入数据
        lane_gdf.to_file(os.path.join(file_path, "lane.shp"))
        if lane_connector_gdf is not None:
            lane_connector_gdf.to_file(os.path.join(file_path, "laneConnector.shp"))

    def analyze_data(self, proj_string: str = None) -> tuple:
        LANE_ACTION_TYPE = NetworkExportConfig.LANE_TYPE_MAPPING

        # ==================== 1.读取proj ====================
        projection = Proj(proj_string) if proj_string else None

        # ==================== 2.读取move ====================
        move_distance = self.netiface.netAttrs().otherAttrs().get("move_distance")
        move = {"x_move": 0, "y_move": 0} if move_distance is None or "tmerc" in proj_string else move_distance

        # ==================== 3.读取路段 ====================
        links = self.netiface.links()
        lane_features = []
        for link in pgd.progress(links, '路段数据保存中（1/2）'):
            link_id = link.id()
            for lane in link.lanes():
                lane_id = lane.id()
                lane_number = lane.number() + 1
                lane_type = LANE_ACTION_TYPE.get(lane.actionType(), "driving")
                lane_width = self._p2m(lane.width())
                lane_points = self._qtpoint2list(lane.centerBreakPoint3Ds(), move)
                if proj_string:
                    lane_points = self._xy2lonlat(lane_points, projection)
                feature = {
                    'id': lane_id,
                    'roadId': link_id,
                    'laneNumber': lane_number,
                    'type': lane_type,
                    'width': lane_width,
                    'geometry': LineString(lane_points)
                }
                lane_features.append(feature)
        lane_gdf = GeoDataFrame(lane_features, crs=proj_string)

        # ==================== 4.读取连接段 ====================
        connectors = self.netiface.connectors()
        if connectors:
            lane_connector_features = []
            for connector in pgd.progress(connectors, '连接段数据保存中（2/2）'):
                for lane_connector in connector.laneConnectors():
                    from_lane_id = lane_connector.fromLane().id()
                    to_lane_id = lane_connector.toLane().id()
                    lane_points = self._qtpoint2list(lane_connector.centerBreakPoint3Ds(), move)
                    if proj_string:
                        lane_points = self._xy2lonlat(lane_points, projection)
                    feature = {
                        'preLaneId': from_lane_id,
                        'sucLaneId': to_lane_id,
                        'geometry': LineString(lane_points)
                    }
                    lane_connector_features.append(feature)
            lane_connector_gdf = GeoDataFrame(lane_connector_features, crs=proj_string)
        else:
            lane_connector_gdf = None

        return lane_gdf, lane_connector_gdf
