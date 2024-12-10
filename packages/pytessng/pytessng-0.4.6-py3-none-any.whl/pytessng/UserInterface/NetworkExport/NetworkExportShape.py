from .BaseNetworkExport import BaseNetworkExport


class NetworkExportShape(BaseNetworkExport):
    name: str = "导出为Shape"
    mode: str = "shape"
    format: tuple = ("Shape", "shp")

    style: int = 2
    box_message: str = ""
