from .BaseNetworkImport import BaseNetworkImport


class NetworkImportAidaroe(BaseNetworkImport):
    name: str = "导入Aidaroe"
    mode: str = "aidaroe"
    format: list = [("Jat", "jat")]
