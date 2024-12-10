from PySide2.QtWidgets import QAction

from ..BaseUI import BaseClass
from ..BaseMouse import BaseMouseSelector
from pytessng.GlobalVar import GlobalVar
from pytessng.ToolInterface import MyOperation


class LinkEditReverse(BaseClass):
    name: str = "框选反转路段"
    mode: str = "reverse"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 按钮
        self.action: QAction = GlobalVar.actions_related_to_mouse_event["reverse"]
        # 将按钮与状态改变函数关联
        self.action.toggled.connect(self.monitor_check_state)

    # 重写抽象父类BaseUserInterface的方法
    def load(self):
        if self.action.isChecked():
            # 为了关联生效
            self.action.setChecked(False)
            self.action.setChecked(True)
            # 显示提示信息
            self.utils.show_info_box("请使用鼠标进行框选来反转路段：\n  -  从左向右框选时，需要框选整个路段；\n  -  从右向左框选时，只需框选路段的一部分即可！")

    # 鼠标事件相关特有方法
    def monitor_check_state(self, checked):
        if checked:
            # 修改按钮为【取消工具】
            self.guiiface.actionNullGMapTool().trigger()

            # 其他按钮取消勾选
            for action in GlobalVar.actions_related_to_mouse_event.values():
                if action.text() not in ["框选反转路段", "取消选中框选反转路段"]:
                    action.setChecked(False)

            # 修改文字
            self.action.setText("取消选中框选反转路段")

            # 添加MyNet观察者
            mouse_reverse = BaseMouseSelector("反转", self.apply_reverse_links, rgb=(0, 255, 0))
            GlobalVar.attach_observer_of_my_net(mouse_reverse)

        else:
            # 修改文字
            self.action.setText("框选反转路段")

            # 移除MyNet观察者
            GlobalVar.detach_observer_of_my_net()

    def apply_reverse_links(self, params: dict):
        MyOperation.apply_link_edit_operation(self, params)
