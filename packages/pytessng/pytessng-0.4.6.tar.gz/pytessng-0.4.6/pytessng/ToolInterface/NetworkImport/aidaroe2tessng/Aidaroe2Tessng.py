import json

from ..BaseOther2Tessng import BaseOther2Tessng
from .AidaroeNetworkAnalyser import AidaroeNetworkAnalyser


class Aidaroe2Tessng(BaseOther2Tessng):
    """
    params:
        - file_path: str
    """

    data_source: str = "Aidaroe"
    pgd_indexes_create_network: tuple = (11, 12)

    def read_data(self, params: dict) -> dict:
        file_path = params["file_path"]
        network_data = json.load(open(file_path, encoding="utf-8"))
        for k, v in network_data.items():
            try:
                # 部分字段需要转换
                network_data[k] = json.loads(v)
            except json.JSONDecodeError:
                pass
        return network_data

    def analyze_data(self, network_data: dict, params: dict) -> dict:
        return AidaroeNetworkAnalyser().analyse_all_data(network_data)
