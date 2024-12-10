from typing import Optional
from PySide2.QtWidgets import QAction
from PySide2.QtCore import QEvent
from PySide2.QtGui import QMouseEvent, Qt

from ..BaseMouse import BaseMouse
from pytessng.GlobalVar import GlobalVar


class MousePanHandler(BaseMouse):
    def __init__(self):
        super().__init__()
        # 上一个按钮
        self._last_action: Optional[QAction] = None

    def handle_mouse_press_event(self, event: QMouseEvent) -> None:
        if event.button() != Qt.MiddleButton:
            return

        # 记录此时的按钮
        all_actions = [
            self.guiiface.netToolBar().actions(),
            self.guiiface.operToolBar().actions(),
            GlobalVar.actions_related_to_mouse_event.values(),
        ]
        for actions in all_actions:
            for action in actions:
                if action.isChecked():
                    self._last_action = action
                    break

        # 将按钮设置为移动
        self.guiiface.actionPan().trigger()

        # 创建一个左键点击事件
        pos = event.pos()
        left_click_event = QMouseEvent(QEvent.Type.MouseButtonPress, pos, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        # 发送左键点击事件
        self.view.mousePressEvent(left_click_event)

    def handle_mouse_release_event(self, event: QMouseEvent) -> None:
        if event.button() != Qt.MiddleButton:
            return

        # 创建一个左键释放事件
        pos = event.pos()
        left_click_event = QMouseEvent(QEvent.Type.MouseButtonRelease, pos, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        # 发送左键释放事件
        self.view.mouseReleaseEvent(left_click_event)

        # 恢复按钮
        if self._last_action is not None:
            # 设置按钮选中
            self._last_action.setChecked(True)
            self._last_action = None
