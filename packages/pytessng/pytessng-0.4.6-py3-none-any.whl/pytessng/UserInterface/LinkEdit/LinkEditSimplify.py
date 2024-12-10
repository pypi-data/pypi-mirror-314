from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton
from PySide2.QtGui import QDoubleValidator

from .BaseLinkEdit import BaseLinkEdit, MyQHBoxLayout, MyQVBoxLayout
from pytessng.Config import LinkEditConfig


class LinkEditSimplify(BaseLinkEdit):
    name: str = "简化路段点位"
    mode: str = "simplify"

    def set_widget_layout(self):
        # 第一行：文本、输入框
        self.label_dist = QLabel('最大割线距离（m）：')
        self.line_edit_dist = QLineEdit()
        # self.line_edit_dist.setFixedWidth(100)
        # 第二行：文本、输入框
        self.label_length = QLabel('最大遍历长度（m）：')
        self.line_edit_length = QLineEdit()
        # self.line_edit_length.setFixedWidth(100)
        # 第三行：按钮
        self.button = QPushButton('简化路网')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.label_dist, self.line_edit_dist]),
            MyQHBoxLayout([self.label_length, self.line_edit_length]),
            self.button
        ])
        self.setLayout(layout)

        # 限制输入框内容
        validator = QDoubleValidator()
        self.line_edit_dist.setValidator(validator)
        self.line_edit_length.setValidator(validator)

        # 设置提示信息
        min_max_distance = LinkEditConfig.Simplifier.MIN_MAX_DISTANCE
        max_max_distance = LinkEditConfig.Simplifier.MAX_MAX_DISTANCE
        min_max_length = LinkEditConfig.Simplifier.MIN_MAX_LENGTH
        max_max_length = LinkEditConfig.Simplifier.MAX_MAX_LENGTH
        self.line_edit_dist.setToolTip(f'{min_max_distance} <= distance <= {max_max_distance}')
        self.line_edit_length.setToolTip(f'{min_max_length} <= length <= {max_max_length}')

    def set_monitor_connect(self):
        self.line_edit_dist.textChanged.connect(self.apply_monitor_state)
        self.line_edit_length.textChanged.connect(self.apply_monitor_state)

    def set_default_state(self):
        default_max_distance = LinkEditConfig.Simplifier.DEFAULT_MAX_DISTANCE
        default_max_length = LinkEditConfig.Simplifier.DEFAULT_MAX_LENGTH
        self.line_edit_dist.setText(f"{default_max_distance}")
        self.line_edit_length.setText(f"{default_max_length}")
        self.apply_monitor_state()

    def apply_monitor_state(self):
        dist = self.line_edit_dist.text()
        length = self.line_edit_length.text()
        enabled_button = False
        try:
            dist = float(dist)
            length = float(length)
            min_max_distance = LinkEditConfig.Simplifier.MIN_MAX_DISTANCE
            max_max_distance = LinkEditConfig.Simplifier.MAX_MAX_DISTANCE
            min_max_length = LinkEditConfig.Simplifier.MIN_MAX_LENGTH
            max_max_length = LinkEditConfig.Simplifier.MAX_MAX_LENGTH
            if min_max_distance <= dist <= max_max_distance and min_max_length <= length <= max_max_length:
                enabled_button = True
        except:
            pass

        # 设置可用状态
        self.button.setEnabled(enabled_button)

    # 重写父类方法
    def get_params(self) -> dict:
        max_distance = float(self.line_edit_dist.text())
        max_length = float(self.line_edit_length.text())
        return {
            "max_distance": max_distance,
            "max_length": max_length
        }
