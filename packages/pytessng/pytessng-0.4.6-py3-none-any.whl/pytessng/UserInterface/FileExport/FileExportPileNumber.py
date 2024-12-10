from PySide2.QtWidgets import QLabel, QRadioButton, QButtonGroup, QPushButton, QTableWidget, QHeaderView, QTableWidgetItem
from PySide2.QtCore import Qt

from ..BaseUI import BaseUserInterface, MyQHBoxLayout, MyQVBoxLayout
from pytessng.Config import UIConfig
from pytessng.ToolInterface import MyOperation


# 整数表格项类
class IntItem(QTableWidgetItem):
    def __init__(self, text=""):
        super().__init__(text)
        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self.setText(text)

    def setData(self, role, value):
        if role == Qt.EditRole:
            try:
                int_value = int(value)
                super().setData(role, int_value)
            except ValueError:
                pass  # 忽略无效输入
        else:
            super().setData(role, value)


# 浮点数表格项类
class FloatItem(QTableWidgetItem):
    def __init__(self, text=""):
        super().__init__(text)
        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self.setText(text)

    def setData(self, role, value):
        if role == Qt.EditRole:
            try:
                float_value = float(value)
                super().setData(role, float_value)
            except ValueError:
                pass  # 忽略无效输入
        else:
            super().setData(role, value)


class FileExportPileNumber(BaseUserInterface):
    name: str = "生成高速桩号文件"
    width: int = UIConfig.FileExportPilenumber.width
    mode: str = "pile_number"
    format: tuple = ("Json", "json")

    # 方向编号ID
    direction_id = 1
    # 之前选择的模式
    current_mode = None
    # 表数据
    data: dict = {
        "link": [],
        "coord_dke": [],
        "coord_jwd": [],
    }
    # 表头
    labels = {
        "link": [
            "方向(str)",
            "起始桩号(float/m)", "结束桩号(float/m)",
            "起始路段ID(int)", "起始路段距离(float/m)",
            "结束路段ID(int)", "结束路段距离(float/m)"
        ],
        "coord_dke": [
            "方向(str)",
            "起始桩号(float/m)", "结束桩号(float/m)",
            "起始点横坐标(float/m)", "起始点纵坐标(float/m)",
            "结束点横坐标(float/m)", "结束点纵坐标(float/m)"
        ],
        "coord_jwd": [
            "方向(str)",
            "起始桩号(float/m)", "结束桩号(float/m)",
            "起始点经度(float)", "起始点纬度(float)",
            "结束点经度(float)", "结束点纬度(float)"
        ],
    }
    # 表格数据类型
    items = {
        "link": [QTableWidgetItem, FloatItem, FloatItem, IntItem, FloatItem, IntItem, FloatItem],
        "coord_dke": [QTableWidgetItem] + [FloatItem for _ in range(6)],
        "coord_jwd": [QTableWidgetItem] + [FloatItem for _ in range(6)],
    }

    def set_widget_layout(self):
        # 第一行：文本、下拉框、文本、输入框
        self.label_mode = QLabel('桩号文件生成模式：')
        self.radio_mode_link = QRadioButton('按照路段ID和距离')
        self.radio_mode_coord_dke = QRadioButton('按照笛卡尔坐标')
        self.radio_mode_coord_jwd = QRadioButton('按照经纬度坐标')
        self.radio_group_mode = QButtonGroup(self)
        self.radio_group_mode.addButton(self.radio_mode_link)
        self.radio_group_mode.addButton(self.radio_mode_coord_dke)
        self.radio_group_mode.addButton(self.radio_mode_coord_jwd)
        # 第二行：表格
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # 设置列数
        self.table.setRowCount(2)  # 设置行数
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 两边无间隙
        self.table.setHorizontalHeaderLabels(["方向(str)", "起始桩号(int)", "结束桩号(int)", "起始路段ID(int)", "起始路段距离(float)", "结束路段ID(int)", "结束路段距离(float)", "删除方向"])
        self.button_add = QPushButton('新增方向')
        self.button_remove = QPushButton('删除方向')
        # 第三行：按钮
        self.button_export = QPushButton('生成配置文件')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.label_mode, self.radio_mode_link, self.radio_mode_coord_dke, self.radio_mode_coord_jwd]),
            MyQHBoxLayout([self.table, MyQVBoxLayout([self.button_add, self.button_remove, self.button_export])]),
        ])
        self.setLayout(layout)

    def set_monitor_connect(self):
        # 单选按钮
        self.radio_mode_link.toggled.connect(self.apply_monitor_state_ratio)
        self.radio_mode_coord_dke.toggled.connect(self.apply_monitor_state_ratio)
        self.radio_mode_coord_jwd.toggled.connect(self.apply_monitor_state_ratio)
        # 表格
        self.table.itemChanged.connect(self.apply_monitor_state)

    def set_button_connect(self):
        self.button_add.clicked.connect(self.add_row)
        self.button_remove.clicked.connect(self.remove_row)
        self.button_export.clicked.connect(self.apply_button_action)

    def set_default_state(self):
        # 如果有上一次的记忆
        if self.current_mode is not None:
            if self.current_mode == "link":
                self.radio_mode_link.setChecked(True)
            elif self.current_mode == "coord_dke":
                self.radio_mode_coord_dke.setChecked(True)
            elif self.current_mode == "coord_jwd":
                self.radio_mode_coord_jwd.setChecked(True)
        # 如果是第一次就选link
        else:
            self.radio_mode_link.setChecked(True)
        # 设置禁用 TODO SXH
        self.radio_mode_coord_jwd.setEnabled(False)

    def apply_monitor_state(self):
        mode = self.get_current_mode()

        # 保存已有数据
        table_data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(7):
                item = self.table.item(row, col)
                if item is not None:
                    text = item.text()
                else:
                    text = ""
                row_data.append(text)
            table_data.append(row_data)
        self.data[mode] = table_data

        # 按钮状态
        condition1 = (self.table.rowCount() >= 1)  # 至少有一行
        condition2 = all([self.table.item(row, 0).text() for row in range(self.table.rowCount()) if self.table.item(row, 0) is not None])  # 方向列不为空
        enabled_button = all([condition1, condition2])
        # 设置可用状态
        self.button_export.setEnabled(enabled_button)

    # 特有方法：单选框变动
    def apply_monitor_state_ratio(self):
        mode = self.get_current_mode()

        # 更新表格行头
        labels = self.labels[mode]
        self.table.setHorizontalHeaderLabels(labels)

        # 更新表格数据
        saved_data = self.data[mode]
        self.table.setRowCount(len(saved_data))  # 设置行数
        for r in range(len(saved_data)):
            values = saved_data[r]
            items = self.get_items(mode, values)
            for c in range(7):
                self.table.setItem(r, c, items[c])

    # 特有方法：新增行
    def add_row(self):
        current_row_count = self.table.rowCount()
        new_row_count = current_row_count + 1
        new_row_index = new_row_count - 1
        self.table.setRowCount(new_row_count)  # 设置行数

        mode = self.get_current_mode()
        # 第一列
        self.table.setItem(new_row_index, 0, QTableWidgetItem(f"新方向[{self.direction_id}]"))
        self.direction_id += 1
        # 第二列到第七列
        items = self.get_items(mode, [0 for _ in range(6)])
        for c in range(6):
            self.table.setItem(new_row_index, c+1, items[c])

    # 特有方法：删除行
    def remove_row(self):
        current_row_index = self.table.currentRow()
        self.table.removeRow(current_row_index)
        # 更新存储数据
        mode = self.get_current_mode()
        if current_row_index >= 0:
            self.data[mode].pop(current_row_index)

    # 特有方法：获取当前模式
    def get_current_mode(self):
        if self.radio_mode_link.isChecked():
            mode = "link"
        elif self.radio_mode_coord_dke.isChecked():
            mode = "coord_dke"
        else:
            mode = "coord_jwd"
        return mode

    # 特有方法：根据值获取对应的QTableWidgetItem
    def get_items(self, mode, values):
        return [
            item(str(value))
            for value, item in zip(values, self.items[mode])
        ]

    def apply_button_action(self):
        # 模式
        mode = self.get_current_mode()
        self.current_mode = mode
        # 数据
        data = {
            str(self.table.item(row, 0).text()): [
                float(self.table.item(row, col).text())
                for col in range(1, 7)
            ]
            for row in range(self.table.rowCount())
        }
        # 参数
        params = {"mode": mode, "data": data}

        # 执行导出
        MyOperation.apply_other_operation(self, params)
