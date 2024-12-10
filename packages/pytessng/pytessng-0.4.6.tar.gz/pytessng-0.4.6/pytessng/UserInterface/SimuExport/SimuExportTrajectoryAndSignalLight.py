import os
from ipaddress import ip_address
from PySide2.QtWidgets import QLabel, QCheckBox, QRadioButton, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PySide2.QtCore import QRegExp, QCoreApplication
from PySide2.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator, QFont

from ..BaseUI import BaseUserInterface, MyQHBoxLayout, MyQVBoxLayout, MyQGroupBox
from pytessng.ToolInterface import MyOperation
from pytessng.Config import PathConfig


class SimuExportTrajAndSig(BaseUserInterface):
    name = "轨迹和信号灯数据导出"

    # 记忆参数
    memory_params = {
        "check_box": {
            "traj_json": False,
            "traj_kafka": False,
            "sig_json": False,
            "sig_kafka": False,
        },
        "proj": {
            "write_coord": False,
            "is_file_proj": False,
            "custom_lon": None,
            "custom_lat": None,
        },
        "json": {
            "dir_path": PathConfig.DEFAULT_SIMU_DATA_SAVE_DIR_PATH,
        },
        "kafka": {
            "ip": None,
            "port": None,
            "topic_traj": None,
            "topic_sig": None,
        }
    }

    def __init__(self):
        super().__init__()
        # kafka有无问题
        self.kafka_is_ok = False

    # 设置界面布局
    def set_widget_layout(self):
        # 读取文件投影信息
        self.file_proj_string, file_proj_info = self.utils.read_file_proj()
        font = QFont()
        font.setBold(True)  # 设置为粗体

        # 第一行：文本、勾选框、勾选框
        self.label_header_traj = QLabel('\t轨迹数据：')
        self.label_header_traj.setFont(font)
        self.check_box_header_traj_json = QCheckBox('保存为JSON文件')
        self.check_box_header_traj_kafka = QCheckBox('上传至kafka')
        # 第二行：文本、勾选框、勾选框
        self.label_header_sig = QLabel('\t信号灯数据：')
        self.label_header_sig.setFont(font)
        self.check_box_header_sig_json = QCheckBox('保存为JSON文件')
        self.check_box_header_sig_kafka = QCheckBox('上传至kafka')
        # 第三行：勾选框
        self.check_box_config_proj_coord = QCheckBox('轨迹数据写入经纬度坐标')
        # 第四行：单选框
        self.radio_config_proj_file = QRadioButton('使用路网创建时的投影')
        # 第五行：文本
        self.label_config_proj_file = QLabel('文件投影：')
        self.line_edit_config_proj_file = QLineEdit(file_proj_info)
        # 第六行：单选框
        self.radio_config_proj_custom = QRadioButton('使用自定义高斯克吕格投影')
        # 第七行：文本和输入框，使用水平布局
        self.label_config_proj_custom_lon = QLabel('投影中心经度：')
        self.line_edit_config_proj_custom_lon = QLineEdit()
        # 第八行：文本和输入框，使用水平布局
        self.label_config_proj_custom_lat = QLabel('投影中心纬度：')
        self.line_edit_config_proj_custom_lat = QLineEdit()
        # 第九行：文本和按钮
        self.label_config_json = QLabel('保存位置：')
        self.line_edit_config_json = QLineEdit()
        # self.line_edit_config_json.setFixedWidth(500)
        self.button_config_json_save = QPushButton(' 选择保存位置 ')
        # 第十行：文本和输入框
        self.label_config_kafka_ip = QLabel('IP：')
        self.line_edit_config_kafka_ip = QLineEdit()
        self.label_config_kafka_port = QLabel('端口：')
        self.line_edit_config_kafka_port = QLineEdit()
        self.button_config_kafka_check = QPushButton('核验')
        self.label_check_config_kafka_info = QLabel(' 待核验 ')
        # 第十一行：文本和输入框
        self.label_config_kafka_topic_traj = QLabel('traj topic：')
        self.line_edit_config_kafka_topic_traj = QLineEdit()
        self.label_config_kafka_topic_sig = QLabel('sig topic：')
        self.line_edit_config_kafka_topic_sig = QLineEdit()
        # 第十二行：按钮
        self.button = QPushButton('确定')
        self.button.setFixedWidth(60)

        # 总体布局
        layout = MyQVBoxLayout([
            # 空白行
            QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding),
            # 勾选框
            MyQHBoxLayout([self.label_header_traj, self.check_box_header_traj_json, self.check_box_header_traj_kafka]),
            MyQHBoxLayout([self.label_header_sig, self.check_box_header_sig_json, self.check_box_header_sig_kafka]),
            # 空白行
            QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding),
            # 坐标配置
            MyQGroupBox(
                MyQVBoxLayout([
                    self.check_box_config_proj_coord,
                    MyQGroupBox(
                        MyQVBoxLayout([
                            self.radio_config_proj_file,
                            MyQHBoxLayout([
                                self.label_config_proj_file,
                                self.line_edit_config_proj_file
                            ]),
                            self.radio_config_proj_custom,
                            MyQHBoxLayout([
                                self.label_config_proj_custom_lon,
                                self.line_edit_config_proj_custom_lon,
                                self.label_config_proj_custom_lat,
                                self.line_edit_config_proj_custom_lat
                            ]),
                        ])
                    ),
                ]),
                " 坐标配置 "
            ),
            # 空白行
            QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding),
            # JSON配置
            MyQGroupBox(
                MyQVBoxLayout([
                    MyQHBoxLayout([self.label_config_json, self.line_edit_config_json, self.button_config_json_save]),
                ]),
                " JSON配置 "
            ),
            # 空白行
            QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding),
            # kafka配置
            MyQGroupBox(
                MyQVBoxLayout([
                    MyQHBoxLayout([
                        self.label_config_kafka_ip,
                        self.line_edit_config_kafka_ip,
                        self.label_config_kafka_port,
                        self.line_edit_config_kafka_port,
                        self.button_config_kafka_check,
                        self.label_check_config_kafka_info
                    ]),
                    MyQHBoxLayout([
                        self.label_config_kafka_topic_traj,
                        self.line_edit_config_kafka_topic_traj,
                        self.label_config_kafka_topic_sig,
                        self.line_edit_config_kafka_topic_sig,
                    ]),
                ]),
                " kafka配置 ",
            ),
            MyQHBoxLayout([5, self.button, 5]),
        ])
        self.setLayout(layout)

        # 设置只读
        self.line_edit_config_proj_file.setReadOnly(True)

        # 限制输入框内容
        # 限制为浮点数
        validator_coord = QDoubleValidator()
        self.line_edit_config_proj_custom_lon.setValidator(validator_coord)
        self.line_edit_config_proj_custom_lat.setValidator(validator_coord)
        # 限制为整数
        validator_kafka_port = QIntValidator()
        self.line_edit_config_kafka_port.setValidator(validator_kafka_port)
        # 限制为字母开头，字母数字下划线
        regex = QRegExp("^[a-zA-Z][a-zA-Z0-9_]*$")
        validator_kafka_topic = QRegExpValidator(regex)
        self.line_edit_config_kafka_topic_traj.setValidator(validator_kafka_topic)
        self.line_edit_config_kafka_topic_sig.setValidator(validator_kafka_topic)

    def set_monitor_connect(self):
        # 勾选
        self.check_box_header_traj_json.stateChanged.connect(self.apply_monitor_state)
        self.check_box_header_traj_kafka.stateChanged.connect(self.apply_monitor_state)
        self.check_box_header_sig_json.stateChanged.connect(self.apply_monitor_state)
        self.check_box_header_sig_kafka.stateChanged.connect(self.apply_monitor_state)
        # 坐标
        self.check_box_config_proj_coord.stateChanged.connect(self.apply_monitor_state)
        self.radio_config_proj_file.toggled.connect(self.apply_monitor_state)
        self.radio_config_proj_custom.toggled.connect(self.apply_monitor_state)
        self.line_edit_config_proj_file.textChanged.connect(self.apply_monitor_state)
        self.line_edit_config_proj_custom_lon.textChanged.connect(self.apply_monitor_state)
        self.line_edit_config_proj_custom_lat.textChanged.connect(self.apply_monitor_state)
        # JSON
        self.line_edit_config_json.textChanged.connect(self.apply_monitor_state)
        # kafka
        self.line_edit_config_kafka_ip.textChanged.connect(self.apply_monitor_state_kafka)
        self.line_edit_config_kafka_port.textChanged.connect(self.apply_monitor_state_kafka)
        self.line_edit_config_kafka_topic_traj.textChanged.connect(self.apply_monitor_state)
        self.line_edit_config_kafka_topic_sig.textChanged.connect(self.apply_monitor_state)

    def set_button_connect(self):
        self.button_config_json_save.clicked.connect(self.select_folder)
        self.button_config_kafka_check.clicked.connect(self.check_kafka)
        self.button.clicked.connect(self.apply_button_action)

    def set_default_state(self):
        # 勾选框
        self.check_box_header_traj_json.setChecked(self.memory_params["check_box"]["traj_json"])
        self.check_box_header_traj_kafka.setChecked(self.memory_params["check_box"]["traj_kafka"])
        self.check_box_header_sig_json.setChecked(self.memory_params["check_box"]["sig_json"])
        self.check_box_header_sig_kafka.setChecked(self.memory_params["check_box"]["sig_kafka"])

        # 坐标
        self.check_box_config_proj_coord.setChecked(self.memory_params["proj"]["write_coord"])
        if bool(self.file_proj_string):
            self.radio_config_proj_file.setChecked(True)
        else:
            self.radio_config_proj_custom.setChecked(True)
        custom_lon, custom_lat = self.memory_params["proj"]["custom_lon"], self.memory_params["proj"]["custom_lat"]
        if custom_lon is not None and custom_lat is not None:
            self.line_edit_config_proj_custom_lon.setText(str(custom_lon))
            self.line_edit_config_proj_custom_lat.setText(str(custom_lat))

        # json
        dir_path = self.memory_params["json"]["dir_path"]
        self.line_edit_config_json.setText(dir_path)
        # 创建默认保存文件夹
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        # kafka
        ip = self.memory_params["kafka"]["ip"]
        port = self.memory_params["kafka"]["port"]
        topic_traj = self.memory_params["kafka"]["topic_traj"]
        topic_sig = self.memory_params["kafka"]["topic_sig"]
        if ip is not None:
            self.line_edit_config_kafka_ip.setText(str(ip))
            self.line_edit_config_kafka_port.setText(str(port))
            self.line_edit_config_kafka_topic_traj.setText(str(topic_traj))
            self.line_edit_config_kafka_topic_sig.setText(str(topic_sig))

        self.apply_monitor_state()

    def apply_monitor_state(self):
        # 勾选框
        traj_json_is_checked: bool = self.check_box_header_traj_json.isChecked()
        traj_kafka_is_checked: bool = self.check_box_header_traj_kafka.isChecked()
        sig_json_is_checked: bool = self.check_box_header_sig_json.isChecked()
        sig_kafka_is_checked: bool = self.check_box_header_sig_kafka.isChecked()
        traj_is_checked = traj_json_is_checked or traj_kafka_is_checked
        json_is_checked = traj_json_is_checked or sig_json_is_checked
        kafka_is_checked = traj_kafka_is_checked or sig_kafka_is_checked
        # 坐标
        write_coord_is_checked: bool = self.check_box_config_proj_coord.isChecked()
        enabled_file_proj: bool = bool(self.file_proj_string)
        is_file_proj: bool = self.radio_config_proj_file.isChecked()

        # 设置可用状态
        # 坐标
        self.check_box_config_proj_coord.setEnabled(traj_is_checked)
        self.radio_config_proj_file.setEnabled(traj_is_checked and write_coord_is_checked and enabled_file_proj)
        self.radio_config_proj_custom.setEnabled(traj_is_checked and write_coord_is_checked)
        self.label_config_proj_file.setEnabled(traj_is_checked and write_coord_is_checked and enabled_file_proj and is_file_proj)
        self.line_edit_config_proj_file.setEnabled(traj_is_checked and write_coord_is_checked and enabled_file_proj and is_file_proj)
        self.label_config_proj_custom_lon.setEnabled(traj_is_checked and write_coord_is_checked and not is_file_proj)
        self.label_config_proj_custom_lat.setEnabled(traj_is_checked and write_coord_is_checked and not is_file_proj)
        self.line_edit_config_proj_custom_lon.setEnabled(traj_is_checked and write_coord_is_checked and not is_file_proj)
        self.line_edit_config_proj_custom_lat.setEnabled(traj_is_checked and write_coord_is_checked and not is_file_proj)
        # json
        self.label_config_json.setEnabled(json_is_checked)
        self.line_edit_config_json.setEnabled(json_is_checked)
        self.button_config_json_save.setEnabled(json_is_checked)
        # kafka
        self.label_config_kafka_ip.setEnabled(kafka_is_checked)
        self.line_edit_config_kafka_ip.setEnabled(kafka_is_checked)
        self.label_config_kafka_port.setEnabled(kafka_is_checked)
        self.line_edit_config_kafka_port.setEnabled(kafka_is_checked)
        self.button_config_kafka_check.setEnabled(kafka_is_checked)
        self.label_check_config_kafka_info.setEnabled(kafka_is_checked)
        self.label_config_kafka_topic_traj.setEnabled(traj_kafka_is_checked)
        self.line_edit_config_kafka_topic_traj.setEnabled(traj_kafka_is_checked)
        self.label_config_kafka_topic_sig.setEnabled(sig_kafka_is_checked)
        self.line_edit_config_kafka_topic_sig.setEnabled(sig_kafka_is_checked)

        # 设置按钮可用状态
        # 坐标
        proj_state = False
        if (not write_coord_is_checked) or (write_coord_is_checked and is_file_proj):
            proj_state = True
        elif write_coord_is_checked and not is_file_proj:
            lon_0 = self.line_edit_config_proj_custom_lon.text()
            lat_0 = self.line_edit_config_proj_custom_lat.text()
            if lon_0 and lat_0 and -180 < float(lon_0) < 180 and -90 < float(lat_0) < 90:
                proj_state = True
        # json
        folder_path = self.line_edit_config_json.text()
        is_dir = os.path.isdir(folder_path)
        json_state = (not json_is_checked) or (json_is_checked and is_dir)
        # kafka
        kafka_state = (not kafka_is_checked) or (kafka_is_checked and self.kafka_is_ok)
        # 三个都没问题
        self.button.setEnabled(proj_state and json_state and kafka_state)

    # 特有方法：监测各组件状态，切换控件的可用状态
    def apply_monitor_state_kafka(self):
        self.kafka_is_ok = False
        self.label_check_config_kafka_info.setText("待核验")
        # 更新状态
        self.apply_monitor_state()

    def apply_button_action(self):
        # 勾选框
        traj_json_is_checked: bool = self.check_box_header_traj_json.isChecked()
        traj_kafka_is_checked: bool = self.check_box_header_traj_kafka.isChecked()
        sig_json_is_checked: bool = self.check_box_header_sig_json.isChecked()
        sig_kafka_is_checked: bool = self.check_box_header_sig_kafka.isChecked()
        self.memory_params["check_box"] = {
            "traj_json": traj_json_is_checked,
            "traj_kafka": traj_kafka_is_checked,
            "sig_json": sig_json_is_checked,
            "sig_kafka": sig_kafka_is_checked,
        }

        # 坐标
        write_coord_is_checked: bool = self.check_box_config_proj_coord.isChecked()
        is_file_proj: bool = self.radio_config_proj_file.isChecked()
        custom_lon: str = self.line_edit_config_proj_custom_lon.text()
        custom_lat: str = self.line_edit_config_proj_custom_lat.text()
        self.memory_params["proj"]["write_coord"] = write_coord_is_checked
        self.memory_params["proj"]["is_file_proj"] = is_file_proj
        self.memory_params["proj"]["custom_lon"] = float(custom_lon) if custom_lon else None
        self.memory_params["proj"]["custom_lat"] = float(custom_lat) if custom_lat else None

        # json
        dir_path: str = self.line_edit_config_json.text()
        self.memory_params["json"]["dir_path"] = dir_path

        # kafka
        ip: str = self.line_edit_config_kafka_ip.text()
        port: str = self.line_edit_config_kafka_port.text()
        topic_traj: str = self.line_edit_config_kafka_topic_traj.text()
        topic_sig: str = self.line_edit_config_kafka_topic_sig.text()
        self.memory_params["kafka"]["ip"] = ip if ip else None
        self.memory_params["kafka"]["port"] = int(port) if port else None
        self.memory_params["kafka"]["topic_traj"] = topic_traj if topic_traj else None
        self.memory_params["kafka"]["topic_sig"] = topic_sig if topic_sig else None

        # 坐标
        if write_coord_is_checked:
            if is_file_proj:
                traj_proj_string = self.file_proj_string
            else:
                traj_proj_string = f'+proj=tmerc +lon_0={custom_lon} +lat_0={custom_lat} +ellps=WGS84'
        else:
            traj_proj_string = ""

        # 轨迹
        traj_json_config = {"folder_path": dir_path} if traj_json_is_checked else None
        traj_kafka_config = {"ip": ip, "port": port, "topic": topic_traj} if traj_kafka_is_checked else None

        # 信号灯
        sig_json_config = {"folder_path": dir_path} if sig_json_is_checked else None
        sig_kafka_config = {"ip": ip, "port": port, "topic": topic_sig} if sig_kafka_is_checked else None

        # 总结参数
        traj_params = {
            "proj_string": traj_proj_string,
            "json_config": traj_json_config,
            "kafka_config": traj_kafka_config,
        } if traj_json_config or traj_kafka_config else dict()
        sig_params = {
            "json_config": sig_json_config,
            "kafka_config": sig_kafka_config,
        } if sig_json_config or sig_kafka_config else dict()

        # 添加观察者
        MyOperation.apply_simu_data_import_or_export_operation("simu_export_trajectory", traj_params)
        MyOperation.apply_simu_data_import_or_export_operation("simu_export_signal_light", sig_params)

        # 关闭窗口
        self.close()

    # 特有方法：按钮方法，选择JSON保存文件夹
    def select_folder(self):
        folder_path = self.utils.open_folder()
        if folder_path:
            # 显示文件路径在LineEdit中
            self.line_edit_json.setText(folder_path)

    # 特有方法：按钮方法，核验kafka
    def check_kafka(self):
        self.label_check_config_kafka_info.setText("核验中…")
        # 立刻更新界面
        QCoreApplication.processEvents()

        ip = self.line_edit_config_kafka_ip.text()
        port = self.line_edit_config_kafka_port.text()

        # 核验IP
        ip_is_ok = False
        if ip:
            try:
                ip_address(ip)
                ip_is_ok = True
            except:
                self.utils.show_info_box("请输入正确的IPv4地址", "warning")
                self.label_check_config_kafka_info.setText("待核验")
                return
        else:
            self.utils.show_info_box("请输入IPv4地址", "warning")
            self.label_check_config_kafka_info.setText("待核验")
            return
        # 核验端口
        port_is_ok = False
        if port:
            if int(port) > 0:
                port_is_ok = True
            else:
                self.utils.show_info_box("请输入大于0的端口号", "warning")
                self.label_check_config_kafka_info.setText("待核验")
                return
        else:
            self.utils.show_info_box("请输入端口号", "warning")
            self.label_check_config_kafka_info.setText("待核验")
            return

        kafka_pull_is_ok = MyOperation.apply_check_data("kafka", ip, port)

        # 如果都没问题
        if ip_is_ok and port_is_ok and kafka_pull_is_ok:
            self.kafka_is_ok = True
            self.label_check_config_kafka_info.setText("核验成功")
        else:
            self.kafka_is_ok = False
            self.label_check_config_kafka_info.setText("核验失败")

        # 更新状态
        self.apply_monitor_state()
