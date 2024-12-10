from .BaseNetworkImport import BaseNetworkImport


class NetworkImportJson(BaseNetworkImport):
    name: str = "导入Json"
    mode: str = "json"
    format: list = [("Json", "json")]
