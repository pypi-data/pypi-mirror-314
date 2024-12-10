from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton, QRadioButton
from PySide2.QtGui import QDoubleValidator

from .BaseLinkEdit import BaseLinkEdit, MyQHBoxLayout, MyQVBoxLayout, MyQGroupBox


class LinkEditMove(BaseLinkEdit):
    name: str = "移动路网"
    mode: str = "move"

    def set_widget_layout(self):
        # 第一行：单选框
        self.radio_1 = QRadioButton('将路网移动到视图中心')
        self.radio_2 = QRadioButton('自定义移动距离')
        # 第二行：文本、输入框
        self.label_move_x = QLabel('横向移动距离（m）：')
        self.line_edit_move_x = QLineEdit()
        # self.line_edit_move_x.setFixedWidth(100)
        # 第三行：文本、输入框
        self.label_move_y = QLabel('纵向移动距离（m）：')
        self.line_edit_move_y = QLineEdit()
        # self.line_edit_move_y.setFixedWidth(100)
        # 第四行：按钮
        self.button = QPushButton('移动路网')

        # 总体布局
        layout = MyQVBoxLayout([
            self.radio_1,
            self.radio_2,
            MyQGroupBox(
                MyQVBoxLayout([
                    MyQHBoxLayout([self.label_move_x, self.line_edit_move_x]),
                    MyQHBoxLayout([self.label_move_y, self.line_edit_move_y]),
                ])
            ),
            self.button
        ])
        self.setLayout(layout)

        # 限制输入框内容
        validator = QDoubleValidator()
        self.line_edit_move_x.setValidator(validator)
        self.line_edit_move_y.setValidator(validator)

    def set_monitor_connect(self):
        self.radio_1.toggled.connect(self.apply_monitor_state)
        self.radio_2.toggled.connect(self.apply_monitor_state)
        self.line_edit_move_x.textChanged.connect(self.apply_monitor_state)
        self.line_edit_move_y.textChanged.connect(self.apply_monitor_state)

    def set_default_state(self):
        self.radio_1.setChecked(True)
        self.apply_monitor_state()

    def apply_monitor_state(self):
        move_to_center = self.radio_1.isChecked()

        # 按钮状态
        enabled_button = False
        if move_to_center:
            enabled_button = True
        else:
            x_move = self.line_edit_move_x.text()
            y_move = self.line_edit_move_y.text()
            try:
                float(x_move)
                float(y_move)
                enabled_button = True
            except:
                pass

        # 设置可用状态
        self.button.setEnabled(enabled_button)

        # 设置可用状态
        self.label_move_x.setEnabled(not move_to_center)
        self.line_edit_move_x.setEnabled(not move_to_center)
        self.label_move_y.setEnabled(not move_to_center)
        self.line_edit_move_y.setEnabled(not move_to_center)

    # 重写父类方法
    def get_params(self) -> dict:
        move_to_center = self.radio_1.isChecked()
        x_move = float(self.line_edit_move_x.text()) if not move_to_center else 0
        y_move = float(self.line_edit_move_y.text()) if not move_to_center else 0
        return {
            "move_to_center": move_to_center,
            "x_move": x_move,
            "y_move": y_move,
        }
