from .BaseNetworkImport import BaseNetworkImport


class NetworkImportExcel(BaseNetworkImport):
    name: str = "导入Excel"
    mode: str = "excel"
    format: list = [("Excel", "xlsx"), ("Excel", "xls"), ("CSV", "csv")]
