from typing import Optional
import pandas as pd

from .TrajectoryDataAnalyzer import TrajectoryDataAnalyzer
from .VehiclesCreator import VehiclesCreator


class SimuImportTrajectoryActor:
    def __init__(self, netiface, simuiface, Online):
        # TESSNG接口
        self._netiface = netiface
        self._simuiface = simuiface

        # 车辆轨迹数据解析者
        self._trajectory_data_analyzer = TrajectoryDataAnalyzer(netiface)
        # 车辆创建者
        self._vehicles_creator = VehiclesCreator(netiface, simuiface, Online)

        # 全部车辆轨迹数据
        self._all_vehicles_data: Optional[pd.DataFrame] = None
        # 当前仿真将数据复制一份
        self._current_vehicles_data: Optional[pd.DataFrame] = None

    def init_data(self, params: dict) -> None:
        file_path: str = params["file_path"]
        proj_string: str = params["proj_string"]

        # 网格化
        self._netiface.buildNetGrid(5)
        # 车辆数据
        self._all_vehicles_data: pd.DataFrame = self._trajectory_data_analyzer.analyze_trajectory_data(file_path, proj_string)

    def ready(self):
        self._current_vehicles_data = self._all_vehicles_data.copy()

    def operate(self):
        # 当前仿真时间
        simu_time = self._simuiface.simuTimeIntervalWithAcceMutiples()  # ms
        # 当前需要创建的车辆
        current_vehicles_data: pd.DataFrame = self._current_vehicles_data[self._current_vehicles_data["create_time"] <= simu_time]
        # 创建车辆
        self._vehicles_creator.create_vehicles(current_vehicles_data)
        # 删去当前创建的车辆数据
        self._current_vehicles_data: pd.DataFrame = self._current_vehicles_data[self._current_vehicles_data["create_time"] > simu_time]

    def finish(self):
        self._current_vehicles_data = None
