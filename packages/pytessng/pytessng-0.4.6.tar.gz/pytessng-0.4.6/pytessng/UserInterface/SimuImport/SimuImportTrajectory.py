import os
from PySide2.QtWidgets import QLabel, QRadioButton, QLineEdit, QPushButton, QButtonGroup
from PySide2.QtGui import QDoubleValidator

from ..BaseUI import BaseUserInterface, MyQHBoxLayout, MyQVBoxLayout, MyQGroupBox
from pytessng.ToolInterface import MyOperation


class SimuImportTrajectory(BaseUserInterface):
    name = "轨迹数据导入"
    format = [("CSV", "csv"), ("Json", "json")]  # TODO 导入json未开发

    # 记忆参数
    memory_params = {
        "file_path": None,
        "dke_coord": True,
        "custom_proj": True,
        "coord_lon": None,
        "coord_lat": None,
    }

    # 设置界面布局
    def set_widget_layout(self):
        self.file_proj_string, file_proj_info = self.utils.read_file_proj()

        # 第一行：文本框和按钮
        self.line_edit = QLineEdit()
        self.line_edit.setFixedWidth(500)
        self.button_select = QPushButton('文件选择')
        # 第二行：单选框
        self.label_coord = QLabel("坐标类型：")
        self.radio_coord_1 = QRadioButton('笛卡尔坐标')
        self.radio_coord_2 = QRadioButton('经纬度坐标')
        # 加到一组里
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_coord_1)
        self.button_group.addButton(self.radio_coord_2)
        # 第三行：单选框
        self.radio_proj_file = QRadioButton('使用路网创建时的投影')
        # 第四行：文本
        self.line_edit_proj_file = QLineEdit(file_proj_info)
        # 第五行：单选框
        self.radio_proj_custom = QRadioButton('使用自定义高斯克吕格投影')
        # 第六行：文本和输入框，使用水平布局
        self.label_proj_custom_lon = QLabel('投影中心经度：')
        self.lineEdit_proj_custom_lon = QLineEdit()
        # 第七行：文本和输入框，使用水平布局
        self.label_proj_custom_lat = QLabel('投影中心纬度：')
        self.line_edit_proj_custom_lat = QLineEdit()
        # 第八行：按钮
        self.button = QPushButton('确定')

        # 限制输入框内容
        validator_coord = QDoubleValidator()
        self.lineEdit_proj_custom_lon.setValidator(validator_coord)
        self.line_edit_proj_custom_lat.setValidator(validator_coord)

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.line_edit, self.button_select]),
            MyQHBoxLayout([self.label_coord, self.radio_coord_1, self.radio_coord_2]),
            MyQGroupBox(
                MyQVBoxLayout([
                    self.radio_proj_file,
                    self.line_edit_proj_file,
                    self.radio_proj_custom,
                    MyQHBoxLayout([self.label_proj_custom_lon, self.lineEdit_proj_custom_lon]),
                    MyQHBoxLayout([self.label_proj_custom_lat, self.line_edit_proj_custom_lat]),
                ])
            ),
            self.button,
        ])
        self.setLayout(layout)

    def set_monitor_connect(self):
        self.line_edit.textChanged.connect(self.apply_monitor_state)
        self.radio_coord_1.toggled.connect(self.apply_monitor_state)
        self.radio_coord_2.toggled.connect(self.apply_monitor_state)
        self.radio_proj_custom.toggled.connect(self.apply_monitor_state)
        self.lineEdit_proj_custom_lon.textChanged.connect(self.apply_monitor_state)
        self.line_edit_proj_custom_lat.textChanged.connect(self.apply_monitor_state)

    def set_button_connect(self):
        self.button_select.clicked.connect(self.select_file)
        self.button.clicked.connect(self.apply_button_action)

    def set_default_state(self):
        # 各个组件框的状态
        # 文件路径
        if self.memory_params["file_path"]:
            self.line_edit.setText(self.memory_params["file_path"])
        # 笛卡尔还是经纬度
        if self.memory_params["dke_coord"]:
            self.radio_coord_1.setChecked(True)
        else:
            self.radio_coord_2.setChecked(True)
        # 文件投影还是自定义投影
        if bool(self.file_proj_string):
            self.radio_proj_file.setChecked(True)
        else:
            self.radio_proj_custom.setChecked(True)
        self.memory_params["custom_proj"] = bool(self.file_proj_string)
        # 自定义投影的经纬度
        if self.memory_params["coord_lon"] and self.memory_params["coord_lat"]:
            self.lineEdit_proj_custom_lon.setText(str(self.memory_params["coord_lon"]))
            self.line_edit_proj_custom_lat.setText(str(self.memory_params["coord_lat"]))

        self.apply_monitor_state()

    def apply_monitor_state(self):
        # 文件选择
        file_path = self.line_edit.text()
        is_file = os.path.isfile(file_path)
        # 勾选框的状态
        enabled_radio = self.radio_coord_2.isChecked()
        # 文件投影的状态
        enabled_proj_file = bool(self.file_proj_string)
        # 选择投影方式的状态
        enabled_radio_proj = self.radio_proj_custom.isChecked()
        # 投影是否可行
        proj_is_ok = True
        if enabled_radio and enabled_radio_proj:
            lon_0 = self.lineEdit_proj_custom_lon.text()
            lat_0 = self.line_edit_proj_custom_lat.text()
            if not (lon_0 and lat_0 and -180 < float(lon_0) < 180 and -90 < float(lat_0) < 90):
                proj_is_ok = False

        # 按钮状态
        enabled_button = file_path == "" or (is_file and proj_is_ok)

        # 设置可用状态
        self.radio_proj_file.setEnabled(enabled_radio and enabled_proj_file)
        self.line_edit_proj_file.setEnabled(enabled_radio and enabled_proj_file and not enabled_radio_proj)
        self.radio_proj_custom.setEnabled(enabled_radio)
        self.label_proj_custom_lon.setEnabled(enabled_radio and enabled_radio_proj)
        self.label_proj_custom_lat.setEnabled(enabled_radio and enabled_radio_proj)
        self.lineEdit_proj_custom_lon.setEnabled(enabled_radio and enabled_radio_proj)
        self.line_edit_proj_custom_lat.setEnabled(enabled_radio and enabled_radio_proj)
        self.button.setEnabled(enabled_button)

    def apply_button_action(self):
        # 获取路径
        file_path = self.line_edit.text()
        self.memory_params["file_path"] = file_path

        # 获取投影
        if self.radio_coord_1.isChecked():
            self.memory_params["dke_coord"] = True
            proj_string = ""
        else:
            self.memory_params["dke_coord"] = False
            if self.radio_proj_custom.isChecked():
                self.memory_params["custom_proj"] = True
                lon_0 = float(self.lineEdit_proj_custom_lon.text())
                lat_0 = float(self.line_edit_proj_custom_lat.text())
                self.memory_params["coord_lon"] = lon_0
                self.memory_params["coord_lat"] = lat_0
                proj_string = f'+proj=tmerc +lon_0={lon_0} +lat_0={lat_0} +ellps=WGS84'
            else:
                self.memory_params["custom_proj"] = False
                proj_string = self.file_proj_string

        # 如果有文件路径
        if file_path:
            params = {
                "file_path": file_path,
                "proj_string": proj_string,
            }
        # 否则传入空配置
        else:
            params = {}
        MyOperation.apply_simu_data_import_or_export_operation("simu_import_trajectory", params)

        # 关闭窗口
        self.close()

    # 具体功能
    def select_file(self) -> None:
        file_path = self.utils.open_file(self.format)
        if file_path:
            self.line_edit.setText(file_path)
