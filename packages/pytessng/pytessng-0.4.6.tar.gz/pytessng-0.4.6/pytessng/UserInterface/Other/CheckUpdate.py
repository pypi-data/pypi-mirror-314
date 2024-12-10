from datetime import datetime
from functools import partial
import json
import os
import sys
from typing import Callable

import webbrowser
import requests
from PySide2.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QLabel, QDialogButtonBox, QPushButton
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide2.QtGui import QIcon, Qt, QFont

from ..BaseUI import BaseClass
from pytessng.Config import PathConfig


class CheckUpdate(BaseClass):
    name = "检查更新"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = u"\u0031\u0032\u0039\u002e\u0032\u0031\u0031\u002e\u0032\u0038\u002e\u0032\u0033\u0037"
        self.port = u"\u0035\u0036\u0037\u0038"
        self.url_version = f"http://{self.host}:{self.port}/version/"
        self.url_zip = f"http://{self.host}:{self.port}/zip/"

    def load(self, auto_check: bool = False) -> None:
        # =============================================
        # 1.获取本地版本信息
        version_file_path = PathConfig.VERSION_FILE_PATH
        if not os.path.exists(version_file_path):
            new_build_version_info = {
                "content": "",
                "index": 0,
                "time": "2024-01-01 12:00",
                "last_check_date": None,
            }
            with open(version_file_path, "w", encoding="utf-8") as file:
                json.dump(new_build_version_info, file, indent=4, ensure_ascii=False)
        # 当前版本信息
        current_version_info = json.load(open(version_file_path, encoding="utf-8"))

        # =============================================
        # 2.判断是否跳过检查
        # 上一次检查的日期
        last_check_date = current_version_info.get("last_check_date")
        # 如果是自动检查且上一次检查时间不为空
        if auto_check and last_check_date is not None:
            last_check_date = datetime.strptime(last_check_date, '%Y-%m-%d %H:%M')
            # 对比当前日期于读取日期之间的差值是否小于等于3
            if (datetime.now() - last_check_date).days <= 3:
                return

        # =============================================
        # 3.获取最新版本信息
        try:
            newest_version_info = requests.get(self.url_version).json()[0]
        except:
            # 可能由于网络原因，获取失败，直接返回
            if not auto_check:
                self.utils.show_info_box("由于网络原因，无法检测更新！")
            return

        # =============================================
        # 4.对比版本号
        # 当前版本号
        current_index = current_version_info["index"]
        # 最新版本号
        newest_index = newest_version_info["index"]
        # 版本号差异
        index_diff = newest_index - current_index
        # 已经是最新版本
        if index_diff <= 0:
            if not auto_check:
                self.utils.show_info_box("当前已经是最新版本！")
            return

        # =============================================
        # 5.弹出确认框
        # 更新时间
        newest_update_time = newest_version_info["time"]
        # 弹出确认框
        message = f"""
        <div style='line-height: 2;'>
            最新版本更新于<span style='color:red;'><b>[{newest_update_time}]</b></span>，当前版本落后<span style='color:red;'><b>[{index_diff}]</b></span>个版本，是否下载最新版本？
        </div>
        """
        dialog = InquiryWindow(message, partial(self.view_update_content, index_diff + 1))
        result = dialog.exec_()

        # =============================================
        # 6.用户确认是否下载最新版本
        if not result:
            return
        # 使用默认浏览器打开 URL
        webbrowser.open(self.url_zip)
        # 退出程序
        sys.exit()

    # 查看更新的内容
    def view_update_content(self, count: int):
        params = {
            'count': count,
        }
        # 拉取更新内容
        response = requests.get(self.url_version, params=params)
        data = response.json()
        # index time content
        table_window = TableWindow(data)
        table_window.exec_()


class InquiryWindow(QDialog):
    def __init__(self, message, func_view_update_content: Callable):
        super().__init__()
        self.message: str = message
        self.func_view_update_content: Callable = func_view_update_content

        self.init()

    # 初始化数据
    def init(self):
        # 设置标题
        self.setWindowTitle("检查更新")
        # 设置固定宽度
        self.setFixedWidth(500)
        # 设置图标
        self.setWindowIcon(QIcon(PathConfig.ICON_FILE_PATH))
        # 隐藏问号按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 确保窗口总是显示在最前面
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        # 设置布局
        self.setLayout(QVBoxLayout())

        # 第一行：标签
        self.label = QLabel(self.message)
        self.label.setWordWrap(True)  # 启用自动换行
        # 第二行：按钮
        self.button = QPushButton("[点击查看更新内容]")
        self.button.setFlat(True)
        # 第三行：按钮
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # 第四行：勾选框
        self.check_box = QCheckBox("三天内不再自动弹出")

        # 添加到面板
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.button)
        self.layout().addWidget(self.button_box)
        self.layout().addWidget(self.check_box)

        # 关联函数
        # [查看更新内容]按钮
        self.button.clicked.connect(self.func_view_update_content)
        # [确认/取消]按钮
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # [三天内不再自动弹出]勾选框
        self.check_box.stateChanged.connect(self.handle_checkbox_state_changed)

    # 处理三天内不再自动弹出
    def handle_checkbox_state_changed(self, state):
        # 读取文件
        version_file_path = PathConfig.VERSION_FILE_PATH
        current_version_info = json.load(open(version_file_path, encoding="utf-8"))
        # 如果勾选了
        if state == Qt.Checked:
            current_version_info["last_check_date"] = datetime.now().strftime('%Y-%m-%d %H:%M')
        # 如果没勾选
        else:
            current_version_info["last_check_date"] = None
        # 重新写入文件
        with open(version_file_path, "w", encoding="utf-8") as file:
            json.dump(current_version_info, file, indent=4, ensure_ascii=False)


class TableWindow(QDialog):
    def __init__(self, data):
        super().__init__()
        self.data: dict = data

        self.init()

    def init(self):
        # 设置窗口属性
        self.setWindowTitle("更新内容")
        # 设置固定宽度
        self.setFixedWidth(650)
        # 设置图标
        self.setWindowIcon(QIcon(PathConfig.ICON_FILE_PATH))
        # 隐藏问号按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 确保窗口总是显示在最前面
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        # 设置布局
        self.setLayout(QVBoxLayout())

        # 设置表格
        count = len(self.data)
        self.table = QTableWidget(count, 3)
        # 设置表头
        self.table.setHorizontalHeaderLabels(['版本号', '更新时间', '更新内容'])
        # 两边无间隙
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置第一列宽度
        for col, width in zip([0, 1], [70, 180]):
            self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
            self.table.setColumnWidth(col, width)

        # 设置表头字体为粗体
        font = QFont()
        font.setBold(True)
        for col in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(col)
            header_item.setFont(font)

        # 填充表格
        for row, value in enumerate(self.data):
            index = f"+{count-row-1}" if count != row + 1 else "当前"
            time = value['time']
            content = value['content']
            for col, text in enumerate([index, time, content]):
                item = QTableWidgetItem(text)
                item.setText(text)
                # 设置居中自动换行
                if col in [0, 1]:
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                # 设置单元格为只读
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                # 添加元素
                self.table.setItem(row, col, item)

        # 自适应行高
        self.table.resizeRowsToContents()
        # 布局
        self.layout().addWidget(self.table)
