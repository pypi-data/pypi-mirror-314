import os
import uuid
from datetime import datetime
from requests import post
from PySide2.QtWidgets import QFileDialog, QMessageBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, Qt

from pytessng.DLLs.Tessng import tessngIFace
from pytessng.Config import PathConfig


class Utils:
    # 读取.tess文件的属性
    @staticmethod
    def read_file_proj():
        iface = tessngIFace()
        netiface = iface.netInterface()
        attrs = netiface.netAttrs().otherAttrs()
        if attrs.get("proj_string"):  # None or ""
            proj_string = attrs["proj_string"]
            info = proj_string
        else:
            proj_string = ""
            info = "（未在TESS文件中读取到投影信息）"
        return proj_string, info

    # 读取.tess文件的名称
    @staticmethod
    def read_file_name():
        iface = tessngIFace()
        tmpNetPath = iface.netInterface().netFilePath()
        base_name = os.path.basename(tmpNetPath)
        file_name, _ = os.path.splitext(base_name)
        return file_name

    # 获取打开文件的路径
    @staticmethod
    def open_file(formats: list):
        # 指定文件后缀
        xodrSuffix = ";;".join([f"{format} Files (*.{suffix})" for format, suffix in formats])
        # 默认读取位置
        dbDir = PathConfig.OPEN_DIR_PATH
        # 弹出文件选择框
        file_path, filtr = QFileDialog.getOpenFileName(None, "打开文件", dbDir, xodrSuffix)
        return file_path

    # 获取打开文件夹的路径
    @staticmethod
    def open_folder():
        # 默认读取位置
        dbDir = PathConfig.OPEN_DIR_PATH
        # 弹出文件选择框
        folder_path = QFileDialog.getExistingDirectory(None, "打开文件夹", dbDir)
        return folder_path

    # 选择保存文件路径
    @staticmethod
    def save_file(format: tuple, save_dir: str = ""):
        save_dir = save_dir if save_dir else PathConfig.OPEN_DIR_PATH
        # 指定文件后缀
        xodrSuffix = f"{format[0]} Files (*.{format[1]})"
        # 默认保存位置是路径+文件名称
        dbDir = os.path.join(save_dir, Utils.read_file_name())
        # 弹出文件选择框
        file_path, filtr = QFileDialog.getSaveFileName(None, "保存文件", dbDir, xodrSuffix)
        return file_path

    # 弹出警告或提示提示框
    @staticmethod
    def show_info_box(content: str, mode="info"):
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(PathConfig.ICON_FILE_PATH))
        if mode == "warning":
            msg_box.setWindowTitle("警告")
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setWindowTitle("提示")
            msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(content)
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)  # 设置窗口标志，使其显示在最前面
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    # 确认弹窗
    @staticmethod
    def show_confirm_dialog(messages: dict, default_result: str = "cancel"):
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(PathConfig.ICON_FILE_PATH))
        msg_box.setWindowTitle(messages["title"])
        msg_box.setText(messages["content"])

        # 设置按钮
        if messages.get("no"):
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            msg_box.button(QMessageBox.No).setText(messages["no"])
        else:
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        # 设置窗口标志，使其显示在最前面
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
        # 设置默认选项
        default_button = QMessageBox.Cancel if default_result == "cancel" else QMessageBox.Yes
        msg_box.setDefaultButton(default_button)
        # 修改按钮上的文本
        msg_box.button(QMessageBox.Yes).setText(messages["yes"])
        msg_box.button(QMessageBox.Cancel).setText("取消")
        # 获取选择结果
        result = msg_box.exec_()

        return result

    # 发送信息
    @staticmethod
    def send_message(path: str, message: str):
        # 用于唯一标识
        uuid_path = PathConfig.UUID_FILE_PATH
        if os.path.exists(uuid_path):
            UUID = open(uuid_path, "r").read()
        else:
            UUID = str(uuid.uuid4())
            with open(uuid_path, "w") as f:
                f.write(UUID)

        ip = u"\u0031\u0032\u0039\u002e\u0032\u0031\u0031\u002e\u0032\u0038\u002e\u0032\u0033\u0037"
        port = u"\u0035\u0036\u0037\u0038"
        url = f"http://{ip}:{port}/{path}/"
        message = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": os.getlogin(),
            "UUID": UUID,
            "message": message,
        }
        try:
            status_code = post(url, json=message).status_code
        except:
            status_code = 502
        return status_code
