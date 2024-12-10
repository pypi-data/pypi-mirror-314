from .BaseNetworkExport import BaseNetworkExport


class NetworkExportGeojson(BaseNetworkExport):
    name: str = "导出为GeoJson"
    mode: str = "geojson"
    format: tuple = ("GeoJson", "geojson")

    style: int = 2
