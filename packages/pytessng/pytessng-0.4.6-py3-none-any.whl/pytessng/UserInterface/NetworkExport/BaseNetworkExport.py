from PySide2.QtWidgets import QLineEdit, QPushButton, QLabel, QCheckBox, QRadioButton, QButtonGroup
from PySide2.QtGui import QDoubleValidator

from ..BaseUI import BaseUserInterface, MyQHBoxLayout, MyQVBoxLayout, MyQGroupBox
from pytessng.ToolInterface import MyOperation


class BaseNetworkExport(BaseUserInterface):
    # 导出模式
    mode: str = "xxx"
    # 导出文件格式
    format = [("Xxxx", "xxxx")]
    # 界面样式：1是勾选框，2是单选框
    style = 1
    # 勾选框的文本
    box_message = ""

    def set_widget_layout(self):
        self.file_proj_string, file_proj_info = self.utils.read_file_proj()

        # 第一行：勾选框 / 单选框
        if self.style == 1:  # 1/4
            self.check_box = QCheckBox(self.box_message)
            self.first_elements = [self.check_box]
        else:
            self.radio_coord_1 = QRadioButton('笛卡尔坐标')
            self.radio_coord_2 = QRadioButton('经纬度坐标')
            self.first_elements = [self.radio_coord_1, self.radio_coord_2]
            # 加到一组里
            self.button_group = QButtonGroup()
            self.button_group.addButton(self.radio_coord_1)
            self.button_group.addButton(self.radio_coord_2)

        # 第二行：单选框
        self.radio_proj_file = QRadioButton('使用路网创建时的投影')
        # 第三行：文本
        self.line_edit_proj_file = QLineEdit(file_proj_info)
        # 第四行：单选框
        self.radio_proj_custom = QRadioButton('使用自定义高斯克吕格投影')
        # 第五行：文本和输入框，使用水平布局
        self.label_proj_custom_lon = QLabel('投影中心经度：')
        self.line_edit_proj_custom_lon = QLineEdit()
        # 第六行：文本和输入框，使用水平布局
        self.label_proj_custom_lat = QLabel('投影中心纬度：')
        self.line_edit_proj_custom_lat = QLineEdit()
        # 第七行：按钮
        self.button = QPushButton('导出')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQVBoxLayout(self.first_elements),
            MyQGroupBox(
                MyQVBoxLayout([
                    self.radio_proj_file,
                    self.line_edit_proj_file,
                    self.radio_proj_custom,
                    MyQHBoxLayout([self.label_proj_custom_lon, self.line_edit_proj_custom_lon]),
                    MyQHBoxLayout([self.label_proj_custom_lat, self.line_edit_proj_custom_lat]),
                ])
            ),
            self.button,
        ])
        self.setLayout(layout)

        # 限制输入框内容
        validator_coord = QDoubleValidator()
        self.line_edit_proj_custom_lon.setValidator(validator_coord)
        self.line_edit_proj_custom_lat.setValidator(validator_coord)

        # 设置只读
        self.line_edit_proj_file.setReadOnly(True)

    def set_monitor_connect(self):
        if self.style == 1:  # 2/4
            self.check_box.stateChanged.connect(self.apply_monitor_state)
        else:
            self.radio_coord_1.toggled.connect(self.apply_monitor_state)
            self.radio_coord_2.toggled.connect(self.apply_monitor_state)
        self.radio_proj_custom.toggled.connect(self.apply_monitor_state)
        self.line_edit_proj_custom_lon.textChanged.connect(self.apply_monitor_state)
        self.line_edit_proj_custom_lat.textChanged.connect(self.apply_monitor_state)

    def set_button_connect(self):
        self.button.clicked.connect(self.apply_button_action)

    def set_default_state(self):
        if self.style == 2:  # 3/4
            self.radio_coord_1.setChecked(True)
        if bool(self.file_proj_string):
            self.radio_proj_file.setChecked(True)
        else:
            self.radio_proj_custom.setChecked(True)
        self.apply_monitor_state()

    def apply_monitor_state(self):
        # 勾选框的状态
        if self.style == 1:  # 4/4
            enabled_first_element = self.check_box.isChecked()
        else:
            enabled_first_element = self.radio_coord_2.isChecked()
        # 文件投影的状态
        enabled_proj_file = bool(self.file_proj_string)
        # 选择投影方式的状态
        enabled_radio_proj = self.radio_proj_custom.isChecked()
        # 按钮状态
        enabled_button = True
        if enabled_first_element and enabled_radio_proj:
            lon_0 = self.line_edit_proj_custom_lon.text()
            lat_0 = self.line_edit_proj_custom_lat.text()
            if not (lon_0 and lat_0 and -180 < float(lon_0) < 180 and -90 < float(lat_0) < 90):
                enabled_button = False

        # 设置可用状态
        self.radio_proj_file.setEnabled(enabled_first_element and enabled_proj_file)
        self.line_edit_proj_file.setEnabled(enabled_first_element and enabled_proj_file and not enabled_radio_proj)
        self.radio_proj_custom.setEnabled(enabled_first_element)
        self.label_proj_custom_lon.setEnabled(enabled_first_element and enabled_radio_proj)
        self.label_proj_custom_lat.setEnabled(enabled_first_element and enabled_radio_proj)
        self.line_edit_proj_custom_lon.setEnabled(enabled_first_element and enabled_radio_proj)
        self.line_edit_proj_custom_lat.setEnabled(enabled_first_element and enabled_radio_proj)
        self.button.setEnabled(enabled_button)

    def apply_button_action(self):
        MyOperation.apply_network_export_operation(self)
