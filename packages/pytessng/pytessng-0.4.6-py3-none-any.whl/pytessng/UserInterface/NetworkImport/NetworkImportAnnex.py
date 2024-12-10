import os
from functools import partial
from PySide2.QtWidgets import QLineEdit, QPushButton, QCheckBox, QLabel

from .BaseNetworkImport import BaseNetworkImport, MyQHBoxLayout, MyQVBoxLayout


class NetworkImportAnnex(BaseNetworkImport):
    name: str = "导入路网附属元素"
    mode: str = "annex"
    format: list = [("Json", "json")]
    is_network: bool = False

    def set_widget_layout(self) -> None:
        # 第一行：文本框和按钮
        self.line_edit = QLineEdit()
        self.line_edit.setFixedWidth(500)
        self.button_select = QPushButton('文件选择')
        # 第二行：多选框
        self.check_boxes = [
            QCheckBox('车辆组成'),
            QCheckBox('车辆输入'),
            QCheckBox('信号灯组及灯头'),
            QCheckBox('决策点'),
            QCheckBox('限速区域'),
        ]
        object_name_list = [
            "vehicle_composition",
            "vehicle_input",
            "signal",
            "decision_point",
            "reduced_speed_area",
        ]
        for check_box, object_name in zip(self.check_boxes, object_name_list):
            check_box.setObjectName(object_name)
        # 第三行：多选框
        self.label_auto = QLabel("自动导入类型：")
        self.check_boxes_auto = [
            QCheckBox('导向箭头'),
        ]
        object_name_list_auto = [
            "guid_arrow"
        ]
        for check_box, object_name in zip(self.check_boxes_auto, object_name_list_auto):
            check_box.setObjectName(object_name)
        # 第四行：按钮
        self.button_import = QPushButton('生成路网元素')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.line_edit, self.button_select]),
            MyQHBoxLayout(self.check_boxes),
            MyQHBoxLayout([self.label_auto] + self.check_boxes_auto),
            self.button_import,
        ])
        self.setLayout(layout)

    def set_monitor_connect(self) -> None:
        self.line_edit.textChanged.connect(self.apply_monitor_state)
        for check_box in self.check_boxes:
            check_box.stateChanged.connect(self.apply_monitor_state)
        for check_box in self.check_boxes_auto:
            check_box.stateChanged.connect(self.apply_monitor_state)

    def set_button_connect(self) -> None:
        self.button_select.clicked.connect(partial(self.select_file, self.line_edit))
        self.button_import.clicked.connect(self.apply_button_action)

    def set_default_state(self) -> None:
        # 多选框默认全选
        for check_box in self.check_boxes:
            check_box.setChecked(True)
        # 多选框默认全不选
        # for check_box in self.check_boxes_auto:
        #     check_box.setChecked(True)
        self.apply_monitor_state()

    def apply_monitor_state(self) -> None:
        file_path = self.line_edit.text()
        is_file = os.path.isfile(file_path)

        check_box_is_checked = any(check_box.isChecked() for check_box in self.check_boxes)
        check_box_auto_is_checked = any(check_box.isChecked() for check_box in self.check_boxes_auto)

        # 设置可用状态
        enabled = all([is_file, check_box_is_checked]) or all([not file_path, check_box_auto_is_checked])
        self.button_import.setEnabled(enabled)

    # 重写父类方法
    def get_params(self) -> dict:
        # 获取文件路径
        file_path = self.line_edit.text()
        # 获取元素类型
        element_types = [checkbox.objectName() for checkbox in self.check_boxes if checkbox.isChecked()]
        # 获取自动导入元素类型
        auto_element_types = [checkbox.objectName() for checkbox in self.check_boxes_auto if checkbox.isChecked()]

        return {
            "file_path": file_path,
            "element_types": element_types,
            "auto_element_types": auto_element_types,
        }
