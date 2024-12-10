import json

from ..tessng2shape.Tessng2Shape import Tessng2Shape


class Tessng2Geojson(Tessng2Shape):
    def save_data(self, data: tuple, file_path: str) -> None:
        lane_gdf, lane_connector_gdf = data

        # 将车道的 type 改为 lane
        lane_geojson = json.loads(lane_gdf.to_json())
        for features in lane_geojson["features"]:
            features["type"] = "lane"

        # 将车道连接的 type 改为 laneConnector
        if lane_connector_gdf is not None:
            connector_geojson = json.loads(lane_connector_gdf.to_json())
            for features in connector_geojson["features"]:
                features["type"] = "laneConnector"
            lane_geojson["features"].extend(connector_geojson["features"])

        # 写入数据
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(lane_geojson, json_file, indent=4, ensure_ascii=False)
