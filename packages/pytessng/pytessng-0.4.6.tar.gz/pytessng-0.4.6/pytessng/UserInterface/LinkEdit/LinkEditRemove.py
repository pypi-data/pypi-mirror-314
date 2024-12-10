from PySide2.QtWidgets import QAction

from ..BaseUI import BaseClass
from ..BaseMouse import BaseMouseSelector
from pytessng.GlobalVar import GlobalVar
from pytessng.ToolInterface import MyOperation


class LinkEditRemove(BaseClass):
    name: str = "框选删除路段"
    mode: str = "remove"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 按钮
        self.action: QAction = GlobalVar.actions_related_to_mouse_event["remove"]
        # 将按钮与状态改变函数关联
        self.action.toggled.connect(self.monitor_check_state)

    # 重写抽象父类BaseUserInterface的方法
    def load(self):
        if self.action.isChecked():
            # 为了关联生效
            self.action.setChecked(False)
            self.action.setChecked(True)
            # 显示提示信息
            self.utils.show_info_box("请使用鼠标进行框选来删除路段：\n  -  从左向右框选时，需要框选整个路段；\n  -  从右向左框选时，只需框选路段的一部分即可！")

    # 鼠标事件相关特有方法
    def monitor_check_state(self, checked):
        if checked:
            # 修改按钮为【取消工具】
            self.guiiface.actionNullGMapTool().trigger()

            # 其他按钮取消勾选
            for action in GlobalVar.actions_related_to_mouse_event.values():
                if action.text() not in ["框选删除路段", "取消选中框选删除路段"]:
                    action.setChecked(False)

            # 修改文字
            self.action.setText("取消选中框选删除路段")

            # 添加MyNet观察者
            mouse_remove = BaseMouseSelector("删除", self.apply_remove_links, rgb=(255, 0, 0))
            GlobalVar.attach_observer_of_my_net(mouse_remove)

        else:
            # 修改文字
            self.action.setText("框选删除路段")

            # 移除MyNet观察者
            GlobalVar.detach_observer_of_my_net()

    def apply_remove_links(self, params: dict):
        MyOperation.apply_link_edit_operation(self, params)
