from collections import defaultdict

from ..BaseTool import BaseTool


class NetworkIterator(BaseTool):
    # 获取现有的路网数据
    def get_existing_network_data(self) -> dict:
        return {
            "links": self.get_existing_links_data(),
            "connectors": self.get_existing_connector_data(),
            "connector_areas": self.get_connector_areas_data(),
        }

    # 获取已有路段数据
    def get_existing_links_data(self) -> dict:
        links_data = {}

        # 遍历路段
        for link in self.netiface.links():
            link_id = link.id()
            length = link.length()
            lane_count = link.laneCount()
            lane_type_list = [lane.actionType() for lane in link.lanes()]
            links_data[link_id] = {
                "link_id": link_id,
                "length": length,
                "lane_count": lane_count,
                "lane_type_list": lane_type_list,
                "last_link_ids": [],
                "next_link_ids": [],
            }

        # 遍历连接段
        for connector in self.netiface.connectors():
            last_link = connector.fromLink()
            next_link = connector.toLink()

            links_data[last_link.id()]["next_link_ids"].append(next_link.id())
            links_data[next_link.id()]["last_link_ids"].append(last_link.id())

        return links_data

    # 获取已有连接段数据
    def get_existing_connector_data(self) -> dict:
        connectors_data = {}

        # 遍历连接段
        for connector in self.netiface.connectors():
            from_link_id = connector.fromLink().id()
            to_link_id = connector.toLink().id()
            connector_id = connector.id()
            connector_name = connector.name()
            length = connector.length()
            lane_count = len(connector.laneConnectors())
            connectors_data[(from_link_id, to_link_id)] = {
                "from_link_id": from_link_id,
                "to_link_id": to_link_id,
                "connector_id": connector_id,
                "name": connector_name,
                "length": length,
                "lane_count": lane_count,
            }

        return connectors_data

    # 获取已有连接段面域数据
    def get_connector_areas_data(self) -> dict:
        connector_areas_data = defaultdict(list)

        # 遍历连接段面域
        for ConnectorArea in self.netiface.allConnectorArea():
            for connector in ConnectorArea.allConnector():
                connector_areas_data[ConnectorArea.id()].append(connector.id())

        return connector_areas_data
