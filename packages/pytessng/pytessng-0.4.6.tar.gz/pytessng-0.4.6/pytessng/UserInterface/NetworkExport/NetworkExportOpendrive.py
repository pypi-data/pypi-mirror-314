from .BaseNetworkExport import BaseNetworkExport


class NetworkExportOpendrive(BaseNetworkExport):
    name: str = "导出为OpenDrive"
    mode: str = "opendrive"
    format: tuple = ("OpenDrive", "xodr")

    style: int = 1
    box_message: str = "将投影关系写入header"
