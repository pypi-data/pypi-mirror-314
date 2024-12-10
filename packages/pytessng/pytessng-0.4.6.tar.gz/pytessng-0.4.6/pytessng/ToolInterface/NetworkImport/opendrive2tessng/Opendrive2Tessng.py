from lxml import etree

from ..BaseOther2Tessng import BaseOther2Tessng
from .OpendriveNetworkAnalyser import OpendriveNetwokAnalyser
from pytessng.Logger import logger


class Opendrive2Tessng(BaseOther2Tessng):
    """
    params:
        - file_path
        - step_length
        - lane_types
    """

    data_source = "OpenDrive"

    def read_data(self, params: dict) -> etree._Element:
        file_path = params["file_path"]
        tree = etree.parse(open(file_path, "r", encoding='utf-8'))
        root_node = tree.getroot()
        return root_node

    def analyze_data(self, root_node: etree._Element, params: dict):
        road_id_mapping = self.handle_root_node(root_node)

        # 路网数据分析者
        network_analyser = OpendriveNetwokAnalyser()
        temp_data = network_analyser.analyse_all_data(root_node, params)
        
        return temp_data[0], temp_data[1], road_id_mapping

    def create_network(self, temp_data) -> (bool, str):
        network, lane_types, road_id_mapping = temp_data
        error_junction = network.create_network(lane_types, self.netiface, road_id_mapping)

        if error_junction:
            logger.logger_pytessng.warning("error_junction:", error_junction)

        response = {
            "status": True,
            "message": "创建成功",
        }

        return response

    def handle_root_node(self, root_node: etree._Element) -> dict:
        road_id_mapping_1 = {}
        road_id_mapping_2 = {}
        global_road_id = 1

        for road in root_node.findall('.//road'):
            if 'id' in road.attrib:
                current_id: str = road.get('id')
                new_id: int = global_road_id
                global_road_id += 1
                road_id_mapping_1[current_id] = str(new_id)
                road_id_mapping_2[str(new_id)] = current_id
                road.set('id', str(new_id))

        for connection in root_node.findall('.//connection'):
            incomingRoad: str = connection.get('incomingRoad')
            if incomingRoad:
                new_id: str = road_id_mapping_1.get(incomingRoad)
                # print(f"{incomingRoad}->{new_id}")
                if new_id:
                    connection.set('incomingRoad', new_id)
                else:
                    print("warning1")
            connectingRoad: str = connection.get('connectingRoad')
            if connectingRoad:
                new_id: str = road_id_mapping_1.get(connectingRoad)
                # print(f"{connectingRoad}->{new_id}")
                if new_id:
                    connection.set('connectingRoad', new_id)
                else:
                    print("warning2")

        for predecessor in root_node.findall('.//predecessor'):
            elementType = predecessor.get('elementType')
            if elementType == 'junction':
                continue
            elementId: str = predecessor.get('elementId')
            if elementId:
                new_id: str = road_id_mapping_1.get(elementId)
                # print(f"{elementId}->{new_id}")
                if new_id:
                    predecessor.set('elementId', new_id)
                else:
                    print("warning3")
        for successor in root_node.findall('.//successor'):
            elementType = successor.get('elementType')
            if elementType == 'junction':
                continue
            elementId: str = successor.get('elementId')
            if elementId:
                new_id: str = road_id_mapping_1.get(elementId)
                # print(f"{elementId}->{new_id}")
                if new_id:
                    successor.set('elementId', new_id)
                else:
                    print("warning4")

        for comingRoad in root_node.findall('.//comingRoad'):
            linkID: str = comingRoad.get('linkID')
            if linkID:
                new_id: str = road_id_mapping_1.get(linkID)
                # print(f"{linkID}->{new_id}")
                if new_id:
                    comingRoad.set('linkID', new_id)
                else:
                    print(f"warning5: {linkID}")

        return road_id_mapping_2
