from ..BaseUI import BaseClass
from pytessng.ToolInterface.MyOperation import MyOperation


class NetworkExportUnity(BaseClass):
    name: str = "导出为Unity"
    mode: str = "unity"
    format: tuple = ("Unity", "json")

    def load(self):
        MyOperation.apply_network_export_operation(self)
