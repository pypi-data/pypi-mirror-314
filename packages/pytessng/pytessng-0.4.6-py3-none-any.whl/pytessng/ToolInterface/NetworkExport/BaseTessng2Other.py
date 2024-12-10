from abc import abstractmethod
from typing import Union

from ..BaseTool import BaseTool


class BaseTessng2Other(BaseTool):
    def load_data(self, params: dict) -> None:
        # 获取参数
        file_path = params["file_path"]
        proj_string = params["proj_string"]

        # 解析数据
        network_data = self.analyze_data(proj_string)
        # 保存数据
        self.save_data(network_data, file_path)

    @abstractmethod
    def analyze_data(self, proj_string: str = None) -> Union[dict, tuple, str]:
        pass

    @abstractmethod
    def save_data(self, network_data: Union[dict, tuple, str], file_path: str) -> None:
        pass
