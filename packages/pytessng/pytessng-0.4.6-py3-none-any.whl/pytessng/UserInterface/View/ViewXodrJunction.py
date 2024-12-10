from typing import Dict, List
import numpy as np
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide2.QtGui import Qt, QTransform

from ..BaseUI import BaseUserInterface, MyQVBoxLayout
from ..public.HighLightPathItem import HighLightPathItem


class ViewXodrJunction(BaseUserInterface):
    name: str = "查看junction"
    width: int = 100
    height: int = 600
    show_in_center: bool = False

    def set_widget_layout(self):
        netiface = self.iface.netInterface()
        self.table = MyTable(netiface)
        layout = MyQVBoxLayout([
            self.table,
        ])
        self.setLayout(layout)

    def apply_monitor_state(self):
        pass

    def apply_button_action(self):
        pass

    def set_default_state(self):
        pass

    def set_monitor_connect(self):
        pass

    def set_button_connect(self):
        pass

    def closeEvent(self, event):
        self.table.remove_items()


class MyTable(QTableWidget):
    junction_data: dict = {}
    row_mapping: Dict[int, int] = {}

    def __init__(self, netiface):
        super().__init__()
        self.netiface = netiface
        self.scene = self.netiface.graphicsScene()
        self.view = self.netiface.graphicsView()

        # 当前界面上的items
        self.current_items: list = []

        # 读取连接段数据
        self._read_junction_data()
        # 初始化表格
        self._init_table()

    def _init_table(self):
        # 设置列数
        self.setColumnCount(1)
        # 设置行数
        self.setRowCount(len(self.junction_data))

        # 设置表头
        self.setHorizontalHeaderLabels(["JUNCTION_ID"])
        # 两边无间隙
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设置表格内容
        for index, junction_id in enumerate(list(self.junction_data.keys())):
            self.row_mapping[index] = junction_id
            text_item = self._create_text(str(junction_id))
            self.setItem(index, 0, text_item)

        # 表格单元关联槽函数
        self.cellClicked.connect(self._move_to_center)

    def _create_text(self, text: str):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    # 将视图移动到中心
    def _move_to_center(self, row: int, col: int):
        junction_id: int = self.row_mapping[row]
        # 获取中心点
        x, y = self.junction_data[junction_id]["center_point"]

        # 将视图移动到中心点
        self.view.centerOn(x, y)
        # 设置视图的缩放比例
        transform = QTransform()
        transform.scale(9.0, 9.0)
        self.view.setTransform(transform)

        # 高亮连接段
        connector_id_list: List[int] = self.junction_data[junction_id]["connector_id_list"]
        self._highlighted_connectors(connector_id_list)

    # 高亮连接段
    def _highlighted_connectors(self, connector_id_list: list):
        self.remove_items()
        for connector_id in connector_id_list:
            connector = self.netiface.findConnector(connector_id)
            polygon = connector.polygon()
            polygon_item = HighLightPathItem(polygon)
            # 将路径项添加到场景中
            self.scene.addItem(polygon_item)
            self.current_items.append(polygon_item)

    # 移除当前的items
    def remove_items(self):
        for item in self.current_items:
            self.scene.removeItem(item)
        self.current_items.clear()

    # 读取连接段数据
    def _read_junction_data(self):
        # 遍历连接段
        for connector in self.netiface.connectors():
            conn_name = connector.name()
            try:
                junction_id = int(conn_name)
            except:
                continue

            if junction_id == -1:
                continue

            if junction_id not in self.junction_data:
                self.junction_data[junction_id] = {
                    "center_point": None,
                    "connector_id_list": [],
                    "temp_point_list": []
                }

            # 添加连接段ID
            conn_id = connector.id()
            self.junction_data[junction_id]["connector_id_list"].append(conn_id)

            # 添加车道中心线点位
            for lane_connector in connector.laneConnectors():
                for point_qt in lane_connector.centerBreakPoints():
                    x, y = point_qt.x(), point_qt.y()
                    self.junction_data[junction_id]["temp_point_list"].append([x, y])

        # 计算中心点
        for junction_id in self.junction_data:
            xs, ys = [], []
            for x, y in self.junction_data[junction_id]["temp_point_list"]:
                xs.append(x)
                ys.append(y)
            x_mean = float(np.mean(xs))
            y_mean = float(np.mean(ys))
            self.junction_data[junction_id]["center_point"] = (x_mean, y_mean)
            self.junction_data[junction_id]["temp_point_list"].clear()

        # 按照junction_id排序
        self.junction_data = dict(sorted(self.junction_data.items(), key=lambda v: v[0]))
