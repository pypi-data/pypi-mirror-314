import os
from PySide2.QtWidgets import QLineEdit, QPushButton

from ..BaseUI import BaseUserInterface, MyQHBoxLayout, MyQVBoxLayout
from pytessng.ToolInterface import MyOperation


class BaseNetworkImport(BaseUserInterface):
    # 创建模式
    mode: str = "xxx"
    # 导入文件格式
    format: list = [("Xxxx", "xxxx")]
    # 是不是路网
    is_network: bool = True

    def set_widget_layout(self) -> None:
        # 第一行：文本框和按钮
        self.line_edit = QLineEdit()
        self.line_edit.setFixedWidth(500)
        self.button_select = QPushButton('文件选择')
        # 第二行：按钮
        self.button_import = QPushButton('生成路网')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.line_edit, self.button_select]),
            self.button_import
        ])
        self.setLayout(layout)

    def set_monitor_connect(self) -> None:
        self.line_edit.textChanged.connect(self.apply_monitor_state)

    def set_button_connect(self) -> None:
        self.button_select.clicked.connect(self.select_file)
        self.button_import.clicked.connect(self.apply_button_action)

    def set_default_state(self) -> None:
        self.apply_monitor_state()

    def apply_monitor_state(self) -> None:
        file_path = self.line_edit.text()
        is_file = os.path.isfile(file_path)

        # 设置可用状态
        enabled = all([is_file])
        self.button_import.setEnabled(enabled)

    def apply_button_action(self):
        params = self.get_params()
        if params:
            MyOperation.apply_network_import_operation(self, params)

    # 具体功能
    # 有时候不止一个line_edit特地增加了这个参数来控制在哪显示
    def select_file(self, line_edit=None) -> None:
        file_path = self.utils.open_file(self.format)
        if file_path:
            if line_edit:  # 可能被传入False
                line_edit.setText(file_path)
            else:
                self.line_edit.setText(file_path)

    # 具体功能
    # 有时候不止一个line_edit特地增加了这个参数来控制在哪显示
    def select_folder(self, line_edit=None) -> None:
        folder_path = self.utils.open_folder()
        if folder_path:
            if line_edit:  # 可能被传入False
                line_edit.setText(folder_path)
            else:
                self.line_edit.setText(folder_path)

    # 具体功能
    def get_params(self) -> dict:
        # 获取路径
        file_path = self.line_edit.text()
        # 构建参数
        return {
            "file_path": file_path,
        }
