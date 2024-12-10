from .BaseNetworkExport import BaseNetworkExport


class NetworkExportJson(BaseNetworkExport):
    name: str = "导出为Json"
    mode: str = "json"
    format: tuple = ("Json", "json")

    style: int = 1
    box_message: str = "写入经纬度坐标"
