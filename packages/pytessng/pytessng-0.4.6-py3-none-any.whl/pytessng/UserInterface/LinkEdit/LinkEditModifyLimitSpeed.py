from PySide2.QtWidgets import QLabel, QComboBox, QPushButton

from .BaseLinkEdit import BaseLinkEdit, MyQHBoxLayout, MyQVBoxLayout


class LinkEditModifyLimitSpeed(BaseLinkEdit):
    name: str = "修改路段限速"
    mode: str = "modify_limit_speed"

    def set_widget_layout(self):
        # 第一行：文本、下拉框
        self.label_limit_speed = QLabel('路段限速（km/h）：')
        self.combo_limit_speed = QComboBox()
        self.combo_limit_speed.addItems(("40", "50", "60", "70", "80", "90", "100", "110", "120", "140", "160", "180", "200"))
        width = self.calc_char_width(self.combo_limit_speed, 16)
        self.combo_limit_speed.setMinimumWidth(width)
        # 第二行：按钮
        self.button = QPushButton('修改全部路段限速')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.label_limit_speed, self.combo_limit_speed]),
            self.button
        ])
        self.setLayout(layout)

    def set_default_state(self):
        self.combo_limit_speed.setCurrentIndex(4)

    # 重写父类方法
    def get_params(self) -> dict:
        limit_speed = int(self.combo_limit_speed.currentText())
        return {
            "limit_speed": limit_speed,
        }
