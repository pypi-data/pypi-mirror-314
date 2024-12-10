from abc import abstractmethod
from typing import Union
from datetime import datetime
import pandas as pd

from ..BaseTool import BaseTool
from ..public.NetworkCreator import NetworkCreator


class BaseOther2Tessng(BaseTool):
    # 数据源
    data_source: str = ""
    # 是否是道路网络
    is_road_network: bool = True
    # 是否自动移动到画布中心
    is_auto_move: bool = False
    # 进度条序号
    pgd_indexes_create_network: tuple = (1, 2)

    def __init__(self, netiface):
        super().__init__(netiface)
        # 投影字符串
        self.proj_string: str = ""
        # 移动距离
        self.move_distance: dict = dict()

    def load_data(self, params: dict) -> dict:
        # ==================== 读取数据 ====================
        original_network_data = self.read_data(params)
        if original_network_data is None:
            return {
                "status": False,
                "message": "读取数据失败",
            }

        # ==================== 解析数据 ====================
        analyzed_network_data = self.analyze_data(original_network_data, params)
        if analyzed_network_data is None:
            return {
                "status": False,
                "message": "解析数据失败",
            }

        # 如果是导入道路网络且没有路段数据
        if self.is_road_network and type(analyzed_network_data) == dict and not analyzed_network_data.get("links"):  # 为None或为空
            return {
                "status": False,
                "message": "所选文件中无数据或无合法数据",
            }

        # ==================== 创建路网 ====================
        self.create_network(analyzed_network_data)
        return {
            "status": True,
            "message": "创建成功",
        }

    @abstractmethod
    def read_data(self, params: dict) -> Union[dict, tuple, pd.DataFrame, None]:
        # 从文件中读取数据
        pass

    @abstractmethod
    def analyze_data(self, original_network_data: Union[dict, tuple, pd.DataFrame, None], params: dict) -> dict:
        # 1.解析路网数据
        # 2.更新投影字符串
        # 3.更新移动距离
        pass

    def create_network(self, analyzed_network_data: dict) -> dict:
        # 计算路网要移动的距离
        if self.is_road_network:
            # osm会自己计算移动距离，如果没有提供就计算一个
            if not self.move_distance:
                links = analyzed_network_data["links"]
                # 计算路网中心坐标
                xs, ys = [], []
                for link in links:
                    points = link["points"]
                    xs.extend([point[0] for point in points])
                    ys.extend([point[1] for point in points])
                x_center, y_center = [(min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2] if xs and ys else [0, 0]
                # 计算移动距离
                self.move_distance = {
                    "x_move": -float(round(x_center, 3)),
                    "y_move": -float(round(y_center, 3)),
                }
            # 如果需要自动移动就传入移动距离 否则为None
            move_distance = self.move_distance if self.is_auto_move else None
        else:
            move_distance = None

        # 实例化路网创建者
        network_creator = NetworkCreator(
            self.netiface,
            is_road_network=self.is_road_network,
            move_distance=move_distance,
            pgd_indexes=self.pgd_indexes_create_network
        )

        # 如果是道路网络 就设置路网属性
        if self.is_road_network:
            # 构建路网属性
            attrs = dict(
                data_source=self.data_source,
                created_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                proj_string=self.proj_string,
                move_distance=self.move_distance,
            )
            # 设置路网属性
            network_creator.set_attrs(attrs)

        # 创建路网
        result_create_network = network_creator.create_network(analyzed_network_data)

        # 返回创建成败结果
        return result_create_network
