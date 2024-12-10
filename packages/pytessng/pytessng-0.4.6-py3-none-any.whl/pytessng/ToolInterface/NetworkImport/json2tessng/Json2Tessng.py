import json

from ..BaseOther2Tessng import BaseOther2Tessng
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class Json2Tessng(BaseOther2Tessng):
    """
    params:
        - file_path: str
    """

    data_source: str = "Json"
    pgd_indexes_create_network: tuple = (3, 4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 车道ID与车道序号的映射
        self._lane_id2index_mapping: dict = dict()

    def read_data(self, params: dict) -> dict:
        file_path = params["file_path"]
        # 获取文件后缀
        try:
            network_data = json.load(open(file_path, encoding="utf-8"))
        except:
            network_data = json.load(open(file_path, encoding="gbk"))
        return network_data

    def analyze_data(self, network_data: dict, params: dict) -> dict:
        # 读取路段数据
        links_data = self._read_link_data(network_data["road"])
        # 读取连接段数据
        connectors_data = self._read_connector_data(network_data["connector"]) if "connector" in network_data else []
        # 读取投影
        self.proj_string = network_data.get("header") or ""
        return {
            "links": links_data,
            "connectors": connectors_data,
        }

    def _read_link_data(self, links_data) -> list:
        standard_links_data = []

        for link_data in pgd.progress(links_data, '路段数据解析中（1/4）'):
            # 路段ID
            link_id = link_data["id"]
            # 路段名称
            link_name = link_data.get("name", str(link_id))
            # 路段中心线点位
            points = link_data["pointsTess"]
            # 根据车道ID对列表进行排序
            # link_data["lanes"] = sorted(link_data["lanes"], key=lambda x: x["id"])
            # 得到车道ID与车道序号的映射关系
            for index, lane in enumerate(link_data["lanes"], start=1):
                self._lane_id2index_mapping[lane["id"]] = index
            # 各车道数据
            lanes = link_data["lanes"]
            # 各车道类型
            lanes_type = [lane.get("type", "机动车道") for lane in lanes]
            # 如果有车道宽度
            if not lanes[0].get("centerPointsTess"):
                lanes_width = [
                    lane["width"]
                    for lane in lanes
                ]
                standard_link_data = dict(
                    id=link_id,
                    name=link_name,
                    points=points,
                    lanes_width=lanes_width,
                    lanes_type=lanes_type,
                )
            else:
                # 各车道点位
                lanes_points = [
                    {
                        "left": lane["leftPointsTess"],
                        "center": lane["centerPointsTess"],
                        "right": lane["rightPointsTess"],
                    }
                    for lane in link_data["lanes"]
                ]
                standard_link_data = dict(
                    id=link_id,
                    name=link_name,
                    points=points,
                    lanes_points=lanes_points,
                    lanes_type=lanes_type,
                )
            standard_links_data.append(standard_link_data)

        return standard_links_data

    def _read_connector_data(self, connectors_data) -> list:
        standard_connectors_data = []

        for connector_data in pgd.progress(connectors_data, '连接段数据解析中（2/4）'):
            # 上游路段ID
            from_link_id = connector_data["predecessor"]
            # 下游路段ID
            to_link_id = connector_data["successor"]
            # 连接段名称
            connector_name = connector_data.get("name", f"{from_link_id}-{to_link_id}")
            # 上游车道序号
            from_lane_numbers = [
                lane["predecessorNumber"] + 1
                if "predecessorNumber" in lane
                else self._lane_id2index_mapping[lane["predecessor"]]
                for lane in connector_data["links"]
            ]  # from one
            # 下游车道序号
            to_lane_numbers = [
                lane["successorNumber"] + 1
                if "successorNumber" in lane
                else self._lane_id2index_mapping[lane["successor"]]
                for lane in connector_data["links"]
            ]  # from one
            # TODO SXH 暂不考虑连接段点位

            standard_connector_data = dict(
                from_link_id=from_link_id,
                to_link_id=to_link_id,
                from_lane_numbers=from_lane_numbers,
                to_lane_numbers=to_lane_numbers,
                name=connector_name,
            )
            standard_connectors_data.append(standard_connector_data)

        return standard_connectors_data
