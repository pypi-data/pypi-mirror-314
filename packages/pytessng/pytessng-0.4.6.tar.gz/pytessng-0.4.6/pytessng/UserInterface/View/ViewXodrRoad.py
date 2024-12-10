from typing import Dict, List
import numpy as np
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide2.QtGui import Qt, QTransform

from ..BaseUI import BaseUserInterface, MyQVBoxLayout
from ..public.HighLightPathItem import HighLightPathItem


class ViewXodrRoad(BaseUserInterface):
    name: str = "查看road"
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
    road_data: dict = {}
    row_mapping: Dict[int, str] = {}

    def __init__(self, netiface):
        super().__init__()
        self.netiface = netiface
        self.scene = self.netiface.graphicsScene()
        self.view = self.netiface.graphicsView()

        # 当前界面上的items
        self.current_items: list = []

        # 读取路段数据
        self._read_road_data()
        # 初始化表格
        self._init_table()

    def _init_table(self):
        # 设置列数
        self.setColumnCount(1)
        # 设置行数
        self.setRowCount(len(self.road_data))

        # 设置表头
        self.setHorizontalHeaderLabels(["ROAD_ID"])
        # 两边无间隙
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设置表格内容
        for index, road_id in enumerate(list(self.road_data.keys())):
            self.row_mapping[index] = road_id
            text_item = self._create_text(str(road_id))
            self.setItem(index, 0, text_item)

        # 表格单元关联槽函数
        self.cellClicked.connect(self._move_to_center)

    def _create_text(self, text: str):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    # 将视图移动到中心
    def _move_to_center(self, row: int, col: int):
        road_id: str = self.row_mapping[row]
        # 获取中心点
        x, y = self.road_data[road_id]["center_point"]

        # 将视图移动到中心点
        self.view.centerOn(x, y)
        # 设置视图的缩放比例
        transform = QTransform()
        transform.scale(9.0, 9.0)
        self.view.setTransform(transform)

        # 高亮路段
        link_id_list: List[int] = self.road_data[road_id]["link_id_list"]
        self._highlighted_links(link_id_list)

    # 高亮路段
    def _highlighted_links(self, link_id_list: list):
        self.remove_items()
        for link_id in link_id_list:
            link = self.netiface.findLink(link_id)
            polygon = link.polygon()
            polygon_item = HighLightPathItem(polygon)
            # 将路径项添加到场景中
            self.scene.addItem(polygon_item)
            self.current_items.append(polygon_item)

    # 移除当前的items
    def remove_items(self):
        for item in self.current_items:
            self.scene.removeItem(item)
        self.current_items.clear()

    # 读取路段数据
    def _read_road_data(self):
        # 遍历路段
        for link in self.netiface.links():
            link_name = link.name()
            try:
                road_id: str = link_name.split("_")[-4]
            except:
                continue

            if road_id not in self.road_data:
                self.road_data[road_id] = {
                    "center_point": None,
                    "link_id_list": [],
                    "temp_point_list": []
                }

            # 添加路段ID
            link_id = link.id()
            self.road_data[road_id]["link_id_list"].append(link_id)

            # 添加车道中心线点位
            for point_qt in link.centerBreakPoints():
                x, y = point_qt.x(), point_qt.y()
                self.road_data[road_id]["temp_point_list"].append([x, y])

        # 计算中心点
        for road_id in self.road_data:
            xs, ys = [], []
            for x, y in self.road_data[road_id]["temp_point_list"]:
                xs.append(x)
                ys.append(y)
            x_mean = float(np.mean(xs))
            y_mean = float(np.mean(ys))
            self.road_data[road_id]["center_point"] = (x_mean, y_mean)
            self.road_data[road_id]["temp_point_list"].clear()

        # 按照road_id排序
        number_list = []
        non_number_list = []
        for road_id in self.road_data:
            try:
                road_id: int = int(road_id)
                number_list.append(road_id)
            except:
                non_number_list.append(road_id)
        number_list = sorted(number_list)
        non_number_list = sorted(non_number_list)
        self.road_data = {
            str(k): self.road_data[str(k)]
            for k in number_list + non_number_list
        }
