from abc import ABC, abstractmethod


class BaseNetworkAnalyser(ABC):
    def __init__(self):
        # 投影
        self.proj_string: str = ""
        # 移动距离
        self.move_distance: dict = {"x_move": 0, "y_move": 0}

    @abstractmethod
    def analyse_all_data(self, network_data, params: dict = None) -> dict:
        pass
