from functools import partial
from xml.dom import minidom

from ..BaseTessng2Other import BaseTessng2Other
from .models import Junction, Connector, Road
from .node import Doc
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class Tessng2Opendrive(BaseTessng2Other):
    def save_data(self, data: str, file_path: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)

    def analyze_data(self, proj_string: str = None) -> str:
        # ==================== 读取move ====================
        move = self.netiface.netAttrs().otherAttrs().get("move_distance")
        move = move if move else None

        # ==================== 读取连接段 ====================
        connectors = []
        junctions = []
        areas = self.netiface.allConnectorArea()
        for ConnectorArea in pgd.progress(areas, '连接段数据保存中（1/2）'):
            junction = Junction(ConnectorArea)
            junctions.append(junction)
            for connector in ConnectorArea.allConnector():
                # 为所有的车道连接创建独立的 road，关联至 junction
                for laneConnector in connector.laneConnectors():
                    connectors.append(Connector(laneConnector, junction, partial(self._qtpoint2list, move=move)))

        # ==================== 读取路段 ====================
        roads = []
        links = self.netiface.links()
        for link in pgd.progress(links, '路段数据保存中（2/2）'):
            roads.append(Road(link, partial(self._qtpoint2list, move=move)))

        # ==================== 写入xodr文件 ====================
        doc = Doc()
        doc.init_doc(proj_string=proj_string)
        doc.add_junction(junctions)
        doc.add_road(roads + connectors)

        uglyxml = doc.doc.toxml()
        xml = minidom.parseString(uglyxml)
        xml_pretty_str = xml.toprettyxml()

        return xml_pretty_str
