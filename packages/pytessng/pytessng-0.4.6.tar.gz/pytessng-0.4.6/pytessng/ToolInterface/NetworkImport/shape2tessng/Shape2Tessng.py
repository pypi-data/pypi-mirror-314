import os
import shapefile
import dbfread

from ..BaseOther2Tessng import BaseOther2Tessng
from .ShapeNetworkAnalyser import ShapeNetworkAnalyser


class Shape2Tessng(BaseOther2Tessng):
    """
    params:
        - folder_path: str
        - is_use_lon_and_lat: bool
        - is_use_center_line: bool
        - lane_file_name: str
        - lane_connector_file_name: str
        - proj_mode: str
    """

    data_source: str = "Shapefile"
    pgd_indexes_create_network: tuple = (8, 9)

    def read_data(self, params: dict) -> tuple:
        folder_path = params["folder_path"]
        is_use_lon_and_lat = params["is_use_lon_and_lat"]
        is_use_center_line = params["is_use_center_line"]
        lane_file_name = params["lane_file_name"]
        lane_connector_file_name = params["lane_connector_file_name"]
        proj_mode = params["proj_mode"]

        # =============== 读取车道文件 ===============
        # 文件路径
        file_path_dbf_lane = os.path.join(folder_path, f"{lane_file_name}.dbf")
        file_path_shp_lane = os.path.join(folder_path, f"{lane_file_name}.shp")

        if not os.path.exists(file_path_dbf_lane) or not os.path.exists(file_path_shp_lane):
            raise Exception("Some files are missing !")

        # 读取数据
        try:
            all_data_dbf_lane = list(dbfread.DBF(file_path_dbf_lane, encoding='utf-8'))
            all_data_shp_lane = shapefile.Reader(file_path_shp_lane, encoding='utf-8').shapes()
        except:
            all_data_dbf_lane = list(dbfread.DBF(file_path_dbf_lane, encoding='gbk'))
            all_data_shp_lane = shapefile.Reader(file_path_shp_lane, encoding='gbk').shapes()

        lanes_data = (all_data_dbf_lane, all_data_shp_lane)

        # =============== 读取车道连接文件 ===============
        lane_connectors_data = None

        if is_use_center_line:
            # 文件路径
            file_path_dbf_lane_connector = os.path.join(folder_path, f"{lane_connector_file_name}.dbf")
            file_path_shp_lane_connector = os.path.join(folder_path, f"{lane_connector_file_name}.shp")

            # 有连接段文件
            if os.path.exists(file_path_dbf_lane_connector) and os.path.exists(file_path_shp_lane_connector):
                # 读取数据
                try:
                    all_data_dbf_laneConnector = list(dbfread.DBF(file_path_dbf_lane_connector, encoding='utf-8'))
                    all_data_shp_laneConnector = shapefile.Reader(file_path_shp_lane_connector, encoding='utf-8').shapes()
                except:
                    all_data_dbf_laneConnector = list(dbfread.DBF(file_path_dbf_lane_connector, encoding='gbk'))
                    all_data_shp_laneConnector = shapefile.Reader(file_path_shp_lane_connector, encoding='gbk').shapes()

                lane_connectors_data = (all_data_dbf_laneConnector, all_data_shp_laneConnector)

        # =============== 读取投影文件 ===============
        file_proj_string = None
        if is_use_lon_and_lat and "prj" in proj_mode:
            file_path_prj = os.path.join(folder_path, f"{lane_file_name}.prj")
            file_proj_string = open(file_path_prj, "r").read()

        return lanes_data, lane_connectors_data, file_proj_string

    def analyze_data(self, network_data: tuple, params: dict) -> dict:
        # 路网数据分析者
        network_analyser = ShapeNetworkAnalyser()
        # 解析后的路网数据
        analysed_network_data = network_analyser.analyse_all_data(network_data, params)
        # 更新投影
        self.proj_string = network_analyser.proj_string

        return analysed_network_data
