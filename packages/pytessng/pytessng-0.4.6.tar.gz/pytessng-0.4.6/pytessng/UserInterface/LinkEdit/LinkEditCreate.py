from PySide2.QtWidgets import QLabel, QLineEdit, QComboBox, QPushButton
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator

from .BaseLinkEdit import BaseLinkEdit, MyQHBoxLayout, MyQVBoxLayout
from pytessng.Config import LinkEditConfig


class LinkEditCreate(BaseLinkEdit):
    name: str = "通过坐标创建路段"
    mode: str = "create"

    def set_widget_layout(self):
        # 第一行：文本、下拉框、文本、输入框
        self.label_lane_count = QLabel('车道数：')
        self.combo_lane_count = QComboBox()
        self.combo_lane_count.addItems(("1", "2", "3", "4", "5", "6", "7", "8"))
        self.combo_lane_count.setFixedWidth(100)
        self.label_lane_width = QLabel('    车道宽度（m）：')
        self.line_edit_lane_width = QLineEdit()
        # self.line_edit_lane_width.setFixedWidth(100)
        # 第二行：文本、输入框
        self.label_lane_points = QLabel('路段中心线坐标：')
        self.line_edit_lane_points = QLineEdit()
        # self.lineEdit_lanePoints.setFixedWidth(100)
        # 第三行：按钮
        self.button = QPushButton('创建路段')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.label_lane_count, self.combo_lane_count, self.label_lane_width, self.line_edit_lane_width]),
            MyQHBoxLayout([self.label_lane_points, self.line_edit_lane_points]),
            self.button
        ])
        self.setLayout(layout)

        # 限制输入框内容
        regex = QRegExp("^([0-9](\.[0-9]{0,2})?|10(\.0+)?)$")  # 限制为0~10的浮点数，两位小数
        validator = QRegExpValidator(regex)
        self.line_edit_lane_width.setValidator(validator)

        # 设置提示信息
        min_lane_width = LinkEditConfig.Creator.MIN_LANE_WIDTH
        max_lane_width = LinkEditConfig.Creator.MAX_LANE_WIDTH
        self.line_edit_lane_width.setToolTip(f'{min_lane_width} <= x <= {max_lane_width}')
        self.line_edit_lane_points.setToolTip('x1 , y1 (, z1) ; …… ; xn , yn (, zn)')

    def set_monitor_connect(self):
        self.line_edit_lane_width.textChanged.connect(self.apply_monitor_state)
        self.line_edit_lane_points.textChanged.connect(self.apply_monitor_state)

    def set_default_state(self):
        self.combo_lane_count.setCurrentIndex(2)
        default_lane_width = LinkEditConfig.Creator.DEFAULT_LANE_WIDTH
        self.line_edit_lane_width.setText(f"{default_lane_width}")
        self.apply_monitor_state()

    def apply_monitor_state(self):
        lane_width = self.line_edit_lane_width.text()
        lane_width = bool(lane_width) and float(lane_width) > 0
        # 按钮状态
        enabled_button = False
        try:
            lane_points = self.line_edit_lane_points.text()
            lane_points = lane_points.replace("，", ",").replace("；", ";").replace(" ", "")
            lane_points = lane_points.split(";")
            num = set([len([float(value) for value in point.split(",")]) for point in lane_points])
            if len(lane_points) >= 2 and (num == {2} or num == {3}) and lane_width:
                enabled_button = True
        except:
            pass

        # 设置可用状态
        self.button.setEnabled(enabled_button)

    # 重写父类方法
    def get_params(self) -> dict:
        lane_count = int(self.combo_lane_count.currentText())
        lane_width = float(self.line_edit_lane_width.text())
        lane_points = self.line_edit_lane_points.text().replace("，", ",").replace("；", ";").replace(" ", "")
        return {
            "lane_count": lane_count,
            "lane_width": lane_width,
            "lane_points": lane_points
        }
