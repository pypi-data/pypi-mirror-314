import json

from ..BaseOther2Tessng import BaseOther2Tessng
from .AnnexNetworkAnalyser import AnnexNetworkAnalyser
from ...public.NetworkCreator import NetworkCreator


class Annex2Tessng(BaseOther2Tessng):
    """
    params:
        - file_path: str
        - element_types: list[str]
        - auto_element_types: list[str]
    """

    data_source: str = "Annex"
    is_road_network: bool = False
    pgd_indexes_create_network: tuple = (3, 4)

    def read_data(self, params: dict) -> dict:
        file_path = params["file_path"]
        annex_data = json.load(open(file_path, encoding="utf-8")) if file_path else dict()
        return annex_data

    def analyze_data(self, annex_data: dict, params: dict) -> dict:
        return AnnexNetworkAnalyser(self.netiface).analyse_all_data(annex_data, params)
