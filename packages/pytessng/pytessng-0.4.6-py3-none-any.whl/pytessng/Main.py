import os
from shutil import copy, copytree
from warnings import filterwarnings
from PySide2.QtWidgets import QApplication

from pytessng.DLLs.Tessng import TessngFactory
from pytessng.Tessng.MyPlugin import MyPlugin
from pytessng.Config import PathConfig
from pytessng.GlobalVar import GlobalVar


# TODO list
# (1) 导入路网元素（车辆组成、发车点、车辆路径、减速区）
# (2) 导入轨迹数据
# (3) 导出桩号数据（经纬度坐标模式）
# (4) 导入shp（路段级）

class TessngObject:
    def __init__(self, extension: bool = False):
        # 是否为拓展版
        GlobalVar.extension = extension

        # 加载之前
        self.before_run()
        # 加载
        self.run()

    def before_run(self):
        # 创建工作空间文件夹
        os.makedirs(PathConfig.WORKSPACE_PATH, exist_ok=True)

        # =============== 1. 移动试用版key ===============
        # 试用版key的位置
        cert_file_path = os.path.join(PathConfig.THIS_FILE_PATH, "Files", "Cert", "JidaTraffic_key")
        # 移动后的位置
        cert_folder_path = os.path.join(PathConfig.WORKSPACE_PATH, "Cert")
        new_cert_file_path = os.path.join(cert_folder_path, "可使用本试用版密钥激活TESSNG")
        # 如果不存在就复制移动
        if not os.path.exists(cert_folder_path):
            os.makedirs(cert_folder_path, exist_ok=True)
            copy(cert_file_path, new_cert_file_path)

        # =============== 2. 移动导入样例 ===============
        # 导入样例的位置
        examples_file_path = os.path.join(PathConfig.THIS_FILE_PATH, "Files", "Examples")
        # 移动后的位置
        new_examples_file_path = os.path.join(PathConfig.WORKSPACE_PATH, "Examples")
        try:
            copytree(examples_file_path, new_examples_file_path)
        except:
            pass

        # =============== 3. 忽略警告 ===============
        filterwarnings("ignore")

    def run(self):
        app = QApplication()
        config = {
            '__workspace': PathConfig.WORKSPACE_PATH,  # 工作空间
            '__simuafterload': False,  # 加载路网后是否自动启动仿真
            '__custsimubysteps': True,  # 是否自定义仿真调用频率
            '__allowspopup': False,  # 禁止弹窗
            '__cacheid': True,  # 快速创建路段
            '__showOnlineMap': False,  # 关闭在线地图
        }
        plugin = MyPlugin()
        factory = TessngFactory()
        tessng = factory.build(plugin, config)
        if tessng is not None:
            app.exec_()
