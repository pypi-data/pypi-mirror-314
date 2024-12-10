from PySide2.QtWidgets import QPushButton

from ..BaseUI import BaseUserInterface, MyQHBoxLayout, MyQVBoxLayout, MyQGroupBox  # 虽然是灰色但不要删除
from pytessng.Config import UIConfig
from pytessng.ToolInterface import MyOperation


class BaseLinkEdit(BaseUserInterface):
    width: int = UIConfig.BaseLinkEdit.width
    height: int = UIConfig.BaseLinkEdit.height
    # 路段编辑模式
    mode: str = "xxx"
    # 点击按钮后关闭窗口
    auto_close_window: bool = True

    def set_widget_layout(self):
        self.button = QPushButton('按钮')
        # MyQHBoxLayout([])
        # MyQVBoxLayout([])

    def set_monitor_connect(self):
        pass

    def set_button_connect(self):
        self.button.clicked.connect(self.apply_button_action)

    def set_default_state(self):
        pass

    def apply_monitor_state(self):
        pass

    def apply_button_action(self):
        params = self.get_params()
        if params:
            MyOperation.apply_link_edit_operation(self, params, self.auto_close_window)

    # 具体功能
    def get_params(self) -> dict:
        return dict()
