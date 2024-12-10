from typing import Callable
from PySide2.QtWidgets import QLabel, QAction, QLineEdit, QPushButton
from PySide2.QtGui import QDoubleValidator

from .BaseLinkEdit import BaseLinkEdit, MyQHBoxLayout, MyQVBoxLayout
from ..BaseMouse import BaseMouseLocator
from pytessng.ToolInterface import MyOperation
from pytessng.Config import LinkEditConfig
from pytessng.GlobalVar import GlobalVar


class LinkEditSplit(BaseLinkEdit):
    name: str = "通过坐标打断路段"
    mode: str = "split"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 按钮
        self.action: QAction = GlobalVar.actions_related_to_mouse_event["split"]
        # 将按钮与状态改变函数关联
        self.action.toggled.connect(self.monitor_check_state)

    # 重写抽象父类BaseUserInterface的方法
    def load(self):
        # 被勾选状态才load
        if self.action.isChecked():
            super().load()

    # 重写父类QWidget的方法
    def show(self):
        # 被勾选状态才show
        if self.action.isChecked():
            # 只有点击了确认才能到勾选状态
            self.action.setChecked(False)
            super().show()

    def set_widget_layout(self):
        # 第一行：文本、下拉框、文本、输入框
        self.label_length = QLabel('连接段最小长度（m）：')
        self.line_edit_length = QLineEdit()
        # self.line_edit_length.setFixedWidth(100)
        # 第二行：按钮
        self.button = QPushButton('确定')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.label_length, self.line_edit_length]),
            self.button
        ])
        self.setLayout(layout)

        # 限制输入框内容
        validator = QDoubleValidator()
        self.line_edit_length.setValidator(validator)

        # 设置提示信息
        min_min_connector_length = LinkEditConfig.MIN_MIN_CONNECTOR_LENGTH
        max_min_connector_length = LinkEditConfig.MAX_MIN_CONNECTOR_LENGTH
        self.line_edit_length.setToolTip(f'{min_min_connector_length} <= length <= {max_min_connector_length}')

    def set_monitor_connect(self):
        self.line_edit_length.textChanged.connect(self.apply_monitor_state)

    def set_default_state(self):
        default_min_connector_length = LinkEditConfig.DEFAULT_MIN_CONNECTOR_LENGTH
        self.line_edit_length.setText(f"{default_min_connector_length}")

    def apply_monitor_state(self):
        length = float(self.line_edit_length.text())
        min_min_connector_length = LinkEditConfig.MIN_MIN_CONNECTOR_LENGTH
        max_min_connector_length = LinkEditConfig.MAX_MIN_CONNECTOR_LENGTH
        enabled_button = (min_min_connector_length <= float(length) <= max_min_connector_length)

        # 设置可用状态
        self.button.setEnabled(enabled_button)

    # 重写父类方法
    def apply_button_action(self):
        # 修改勾选状态
        self.action.setChecked(True)
        # 关闭窗口
        self.close()
        # 显示提示信息
        self.utils.show_info_box("请右击需要打断的位置来打断路段！")

    # 鼠标事件相关特有方法
    def monitor_check_state(self, checked):
        if checked:
            # 修改按钮为【取消工具】
            self.guiiface.actionNullGMapTool().trigger()

            # 其他按钮取消勾选
            for action in GlobalVar.actions_related_to_mouse_event.values():
                if action.text() not in ["打断路段", "取消选中打断路段"]:
                    action.setChecked(False)

            # 修改文字
            self.action.setText("取消选中打断路段")

            # 添加MyNet观察者
            mouse_locate = BaseMouseLocator("打断路段", self.apply_split_link, self.action)
            GlobalVar.attach_observer_of_my_net(mouse_locate)

        else:
            # 修改文字
            self.action.setText("打断路段")

            # 移除MyNet观察者
            GlobalVar.detach_observer_of_my_net()

    # 特有方法：编辑路段
    def apply_split_link(self, params: dict, on_success: Callable = None):
        # 回调函数，用于关闭菜单栏
        if on_success is not None:
            on_success()

        params = {
            **params,
            "min_connector_length": float(self.line_edit_length.text())
        }
        # 执行路段编辑
        MyOperation.apply_link_edit_operation(self, params)
