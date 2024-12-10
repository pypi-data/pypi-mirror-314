import os
from functools import reduce
from PySide2.QtWidgets import QLineEdit, QPushButton, QLabel, QComboBox, QRadioButton, QButtonGroup

from .BaseNetworkImport import BaseNetworkImport, MyQHBoxLayout, MyQVBoxLayout
from pytessng.ToolInterface import MyOperation


class NetworkImportShape(BaseNetworkImport):
    name: str = "导入Shape"
    mode: str = "shape"
    format = None

    # 标签信息 (Shape独有)
    info_need_file = "待选择文件"
    info_no_file = "该路径下无合法文件"
    info_not_need_file = "不选择文件"
    proj_modes = (
        "prj文件投影",
        "高斯克吕格投影(tmerc)",
        "通用横轴墨卡托投影(utm)",
        "Web墨卡托投影(web)",
    )

    def set_widget_layout(self):
        # 第一行：文本框和按钮
        self.line_edit = QLineEdit()
        self.line_edit.setFixedWidth(500)
        self.button_select = QPushButton('文件夹选择')
        # 第二行：单选框
        self.label_select_coordType = QLabel("读取坐标类型：")
        self.radio_coordType_dke = QRadioButton('笛卡尔坐标')
        self.radio_coordType_jwd = QRadioButton('经纬度坐标')
        self.radio_group_coordType = QButtonGroup(self)
        self.radio_group_coordType.addButton(self.radio_coordType_dke)
        self.radio_group_coordType.addButton(self.radio_coordType_jwd)
        # 第三行：单选框
        self.label_select_laneDataType = QLabel("导入车道数据类型：")
        self.radio_laneDataType_center = QRadioButton('车道中心线')
        self.radio_laneDataType_boundary = QRadioButton('车道边界线')
        self.radio_group_laneDataType = QButtonGroup(self)
        self.radio_group_laneDataType.addButton(self.radio_laneDataType_center)
        self.radio_group_laneDataType.addButton(self.radio_laneDataType_boundary)
        # 第四行：下拉框
        self.label_selcet_laneFileName = QLabel("路段车道文件名称：")
        self.combo_laneFileName = QComboBox()
        self.combo_laneFileName.addItems((self.info_need_file,))
        # 第五行：下拉框
        self.label_select_laneConnFileName = QLabel("连接段车道文件名称：")
        self.combo_laneConnFileName = QComboBox()
        self.combo_laneConnFileName.addItems((self.info_need_file,))
        # 第六行：下拉框
        self.label_select_proj = QLabel("投影方式：")
        self.combo_proj = QComboBox()
        self.combo_proj.addItems(self.proj_modes)
        # 第七行：按钮
        self.button_import = QPushButton('生成路网')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.line_edit, self.button_select]),
            MyQHBoxLayout([self.label_select_coordType, self.radio_coordType_dke, self.radio_coordType_jwd]),
            MyQHBoxLayout([self.label_select_laneDataType, self.radio_laneDataType_center, self.radio_laneDataType_boundary]),
            MyQHBoxLayout([self.label_selcet_laneFileName, self.combo_laneFileName]),
            MyQHBoxLayout([self.label_select_laneConnFileName, self.combo_laneConnFileName]),
            MyQHBoxLayout([self.label_select_proj, self.combo_proj]),
            self.button_import,
        ])
        self.setLayout(layout)

    def set_monitor_connect(self):
        self.line_edit.textChanged.connect(self.apply_monitor_state)
        self.radio_coordType_dke.toggled.connect(self.apply_monitor_state_radio_coordType)
        self.radio_laneDataType_center.toggled.connect(self.apply_monitor_state_radio_laneDataType)

    def set_button_connect(self) -> None:
        self.button_select.clicked.connect(self.select_folder)
        self.button_import.clicked.connect(self.apply_button_action)

    def set_default_state(self):
        self.radio_coordType_dke.setChecked(True)
        self.radio_laneDataType_center.setChecked(True)
        self.apply_monitor_state()

    def apply_monitor_state(self):
        # 获取文件夹路径
        folder_path = self.line_edit.text()
        # 判断文件夹是否存在
        is_dir = os.path.isdir(folder_path)
        # 设置下拉框状态
        self.set_combo(folder_path, is_dir)

        # 获取下拉框状态
        combo = all(
            combo_text not in [self.info_need_file, self.info_no_file]
            for combo_text in [self.combo_laneFileName.currentText(), self.combo_laneConnFileName.currentText()]
        )

        # 设置可用状态
        enabled = all([is_dir, combo])
        self.button_import.setEnabled(enabled)

    # 重写父类方法
    def get_params(self) -> dict:
        # 获取路径
        folder_path = self.line_edit.text()
        # 获取坐标类型
        is_use_lon_and_lat = self.radio_coordType_jwd.isChecked()
        # 获取车道数据类型
        is_use_center_line = self.radio_laneDataType_center.isChecked()
        # 获取车道文件名称
        laneFileName = self.combo_laneFileName.currentText()
        # 获取车道连接文件名称
        laneConnectorFileName = self.combo_laneConnFileName.currentText()
        # 获取投影方式
        proj_mode = self.combo_proj.currentText()

        # 核查shape文件
        is_ok, prompt_information = MyOperation.apply_check_data(
            "shapefile",
            folder_path,
            laneFileName,
            is_use_lon_and_lat
        )

        # 执行创建
        if is_ok:
            return {
                "folder_path": folder_path,
                "is_use_lon_and_lat": is_use_lon_and_lat,
                "is_use_center_line": is_use_center_line,
                "lane_file_name": laneFileName,
                "lane_connector_file_name": laneConnectorFileName,
                "proj_mode": proj_mode,
            }
        else:
            self.utils.show_info_box(prompt_information, "warning")
            return {}

    # 特有方法：根据坐标类型设置下拉框状态
    def apply_monitor_state_radio_coordType(self):
        # 笛卡尔还是经纬度
        is_use_lon_and_lat = self.radio_coordType_jwd.isChecked()
        # 下拉框状态
        self.combo_proj.setEnabled(is_use_lon_and_lat)

    # 特有方法：根据车道数据类型设置下拉框状态
    def apply_monitor_state_radio_laneDataType(self):
        # 车道数据类型
        is_use_center_line = self.radio_laneDataType_center.isChecked()
        # 下拉框状态
        self.combo_laneConnFileName.setEnabled(is_use_center_line)

    # 特有方法：设置下拉框状态
    def set_combo(self, folder_path, isdir):
        # 车道文件和车道连接文件
        if not folder_path:
            new_items_laneFileName = new_items_laneConnFileName = (self.info_need_file,)
        elif isdir:
            public_file = self.read_public_files(folder_path)
            if public_file:
                new_items_laneFileName = tuple(public_file)
                new_items_laneConnFileName = (self.info_not_need_file,) + tuple(public_file)
            else:
                new_items_laneFileName = new_items_laneConnFileName = (self.info_no_file,)
        else:
            new_items_laneFileName = new_items_laneConnFileName = (self.info_no_file,)

        # 重新设置QComboBox
        self.combo_laneFileName.clear()
        self.combo_laneConnFileName.clear()
        self.combo_laneFileName.addItems(new_items_laneFileName)
        self.combo_laneConnFileName.addItems(new_items_laneConnFileName)
        if "lane" in new_items_laneFileName:
            self.combo_laneFileName.setCurrentText("lane")
        if "laneConnector" in new_items_laneConnFileName:
            self.combo_laneConnFileName.setCurrentText("laneConnector")

        # 投影文件
        is_have_prj_file = False
        if folder_path and isdir:
            laneFileName = self.combo_laneFileName.currentText()
            filePath_prj = os.path.join(folder_path, f"{laneFileName}.prj")
            if os.path.exists(filePath_prj):
                # 读取投影文件
                proj_string_file = open(filePath_prj, "r").read()
                if "PROJCS" in proj_string_file:
                    is_have_prj_file = True
        if not is_have_prj_file:
            self.combo_proj.setItemText(0, "（无自带投影）")
            if self.combo_proj.currentIndex() == 0:
                self.combo_proj.setCurrentIndex(1)
            self.combo_proj.model().item(0).setEnabled(False)
        else:
            self.combo_proj.setItemText(0, self.proj_modes[0])
            self.combo_proj.setCurrentIndex(0)
            self.combo_proj.model().item(0).setEnabled(True)

    # 特有方法：读取文件夹里的公共文件
    def read_public_files(self, folder_path):
        items = os.listdir(folder_path)
        # file_dict = {".cpg": [], ".dbf": [], ".shp": [], ".shx": []}
        file_dict = {".dbf": [], ".shp": []}
        # 遍历每个文件和文件夹
        for item in items:
            item_path = os.path.join(folder_path, item)
            # 如果是文件
            if os.path.isfile(item_path):
                file_name, extension = os.path.splitext(item)
                if extension in file_dict:
                    file_dict[extension].append(file_name)
        public_file = reduce(set.intersection, map(set, file_dict.values())) or None
        return sorted(public_file)
