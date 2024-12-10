from ..BaseOther2Tessng import BaseOther2Tessng
from .OsmNetworkReader import OSMNetworkReader
from .OsmNetworkAnalyser import OsmNetwokAnalyser


class Osm2Tessng(BaseOther2Tessng):
    """
    params:
        - osm_file_path
        - bounding_box_data
        - center_point_data
        - road_class
        - proj_mode
    """

    data_source: str = "OpenStreetMap"
    is_auto_move: bool = True
    pgd_indexes_create_network: tuple = (6, 7)

    def read_data(self, params: dict) -> dict:
        return OSMNetworkReader(params).read_data()

    def analyze_data(self, network_data: dict, params: dict) -> dict:
        # 数据解析者
        network_analyser = OsmNetwokAnalyser()
        # 解析后的路网数据
        analysed_network_data = network_analyser.analyse_all_data(network_data)
        # 更新投影
        self.proj_string = network_analyser.proj_string
        # 更新移动距离
        self.move_distance = network_analyser.move_distance

        return analysed_network_data
