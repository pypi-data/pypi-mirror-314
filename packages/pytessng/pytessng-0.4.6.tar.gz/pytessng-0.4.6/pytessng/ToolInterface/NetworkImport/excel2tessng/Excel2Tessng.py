import os
import pandas as pd

from ..BaseOther2Tessng import BaseOther2Tessng
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class Excel2Tessng(BaseOther2Tessng):
    """
    params:
        - file_path: str
    """

    data_source: str = "Excel Table"
    pgd_indexes_create_network: tuple = (2, 2)

    def read_data(self, params: dict) -> pd.DataFrame:
        file_path = params["file_path"]
        # 获取文件后缀
        _, extension = os.path.splitext(file_path)
        # 读取文件
        if extension == ".csv":
            try:
                network_data = pd.read_csv(file_path, encoding="utf-8")
            except:
                network_data = pd.read_csv(file_path, encoding="gbk")
        elif extension in [".xlsx", ".xls"]:
            network_data = pd.read_excel(file_path)
        else:
            raise Exception("Invaild file format!")
        return network_data

    def analyze_data(self, network_data: pd.DataFrame, params: dict) -> dict:
        standard_links_data = []

        # ==================== 路段 ====================
        for index, col in pgd.progress(enumerate(network_data.to_numpy(), start=1), '路段数据解析中（1/2）'):
            points = [
                list(map(float, j.split(",")))
                for j in col[2:]
                if str(j) != "nan"
            ]
            lane_count = int(col[1])
            name = col[0] if col[0] else index
            link_data = dict(
                id=index,
                points=points,
                lane_count=lane_count,
                name=name
            )
            standard_links_data.append(link_data)

        return {
            "links": standard_links_data
        }
