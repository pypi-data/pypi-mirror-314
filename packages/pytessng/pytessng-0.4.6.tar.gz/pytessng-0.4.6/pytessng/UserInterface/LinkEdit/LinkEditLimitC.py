from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton
from PySide2.QtGui import QDoubleValidator

from .BaseLinkEdit import BaseLinkEdit, MyQHBoxLayout, MyQVBoxLayout
from pytessng.Config import LinkEditConfig


class LinkEditLimitC(BaseLinkEdit):
    name: str = "限制连接段最小长度"
    mode: str = "limit_c"

    def set_widget_layout(self):
        # 第一行：文本、输入框
        self.label_length = QLabel('连接段最小长度（m）：')
        self.line_edit_length = QLineEdit()
        # self.line_edit_length.setFixedWidth(100)
        # 第二行：按钮
        self.button = QPushButton('重构路网')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.label_length, self.line_edit_length]),
            self.button
        ])
        self.setLayout(layout)

        # 限制输入框内容
        validator = QDoubleValidator()
        self.line_edit_length.setValidator(validator)

        # 设置提示信息
        min_min_connector_length = LinkEditConfig.MIN_MIN_CONNECTOR_LENGTH
        max_min_connector_length = LinkEditConfig.MAX_MIN_CONNECTOR_LENGTH
        self.line_edit_length.setToolTip(f'{min_min_connector_length} <= length <= {max_min_connector_length}')

    def set_monitor_connect(self):
        self.line_edit_length.textChanged.connect(self.apply_monitor_state)

    def set_default_state(self):
        default_min_connector_length = LinkEditConfig.DEFAULT_MIN_CONNECTOR_LENGTH
        self.line_edit_length.setText(f"{default_min_connector_length}")
        self.apply_monitor_state()

    def apply_monitor_state(self):
        length = self.line_edit_length.text()
        # 按钮状态
        enabled_button = False
        try:
            length = float(length)
            min_min_connector_length = LinkEditConfig.MIN_MIN_CONNECTOR_LENGTH
            max_min_connector_length = LinkEditConfig.MAX_MIN_CONNECTOR_LENGTH
            if min_min_connector_length <= float(length) <= max_min_connector_length:
                enabled_button = True
        except:
            pass

        # 设置可用状态
        self.button.setEnabled(enabled_button)

    # 重写父类方法
    def get_params(self) -> dict:
        min_connector_length = float(self.line_edit_length.text())
        return {
            "min_connector_length": min_connector_length
        }
