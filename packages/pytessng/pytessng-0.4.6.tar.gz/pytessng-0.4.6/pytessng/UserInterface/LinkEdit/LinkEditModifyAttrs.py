from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton, QTableWidget, QHeaderView, QComboBox, QTableWidgetItem

from .BaseLinkEdit import BaseLinkEdit, MyQHBoxLayout, MyQVBoxLayout


class LinkEditModifyAttrs(BaseLinkEdit):
    name: str = "修改路段属性"
    width: int = 300
    mode: str = "modify_attrs"
    auto_close_window: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.netiface = self.iface.netInterface()

        # 车道类型列表
        self.lane_action_type_list: list = ["机动车道", "机非共享", "非机动车道", "人行道", "公交专用道", "应急车道"]

    def set_widget_layout(self):
        # 获取路段ID列表
        link_id_list = self.netiface.linkIds()
        link_id_str_list = [str(link_id) for link_id in link_id_list]

        # 第一行：文本、输入框
        self.label_link_id = QLabel('路段ID：')
        self.combo_link_id = QComboBox()
        self.combo_link_id.setFixedWidth(100)
        self.combo_link_id.addItems(link_id_str_list)
        self.label_elevation_start_point = QLabel('  起点高程（m）：')
        self.line_edit_elevation_start_point = QLineEdit()
        self.label_elevation_end_point = QLabel('  终点高程（m）：')
        self.line_edit_elevation_end_point = QLineEdit()
        # 第二行：表格
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 两边无间隙
        self.table.setHorizontalHeaderLabels(["车道编号", "车道ID", "行为类型"])
        # 第三行：按钮
        self.button = QPushButton('更新路段属性')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([
                self.label_link_id,
                self.combo_link_id,
                self.label_elevation_start_point,
                self.line_edit_elevation_start_point,
                self.label_elevation_end_point,
                self.line_edit_elevation_end_point,
            ]),
            self.table,
            self.button
        ])
        self.setLayout(layout)

    def set_monitor_connect(self):
        # 更改时触发
        self.combo_link_id.currentIndexChanged.connect(self.apply_monitor_state)

    def set_default_state(self):
        if self.combo_link_id.count() != 0:
            self.apply_monitor_state()

    def apply_monitor_state(self):
        # 获取路段对象
        link_id = int(self.combo_link_id.currentText())
        link_obj = self.netiface.findLink(link_id)
        # 获取起终点高程
        elevation_start_point: float = link_obj.centerBreakPoint3Ds()[0].z()
        elevation_end_point: float = link_obj.centerBreakPoint3Ds()[-1].z()
        # 获取各车道ID和行为类型
        lanes = link_obj.lanes()
        lane_id_list = [lane.id() for lane in lanes]
        lane_action_type_list = [lane.actionType() for lane in lanes]

        # 更新输入框
        self.line_edit_elevation_start_point.setText(str(elevation_start_point))
        self.line_edit_elevation_end_point.setText(str(elevation_end_point))
        # 更新表格
        self.table.setRowCount(len(lanes))
        for i, lane_id in enumerate(lane_id_list):
            # 第一列
            lane_index = str(i+1)
            self.table.setItem(i, 0, QTableWidgetItem(lane_index))
            lane_id = str(lane_id)
            # 第二列
            self.table.setItem(i, 1, QTableWidgetItem(lane_id))
            # 第三列
            lane_action_type = lane_action_type_list[i]
            combo = QComboBox()
            combo.addItems(self.lane_action_type_list)
            combo_index = self.lane_action_type_list.index(lane_action_type)
            combo.setCurrentIndex(combo_index)
            self.table.setCellWidget(i, 2, combo)

    # 重写父类方法
    def get_params(self) -> dict:
        if self.combo_link_id.count() == 0:
            return dict()

        # 路段ID
        link_id = int(self.combo_link_id.currentText())
        # 高程
        elevation_start_point = float(self.line_edit_elevation_start_point.text())
        elevation_end_point = float(self.line_edit_elevation_end_point.text())
        # 各车道行为类型
        lane_action_type_list = [
            self.table.cellWidget(i, 2).currentText()
            for i in range(self.table.rowCount())
        ]
        return {
            "link_id": link_id,
            "elevations": [elevation_start_point, elevation_end_point],
            "lane_action_type_list": lane_action_type_list
        }
