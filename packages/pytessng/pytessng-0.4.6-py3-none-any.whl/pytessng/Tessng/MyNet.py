from typing import Optional, List
from PySide2.QtGui import QMouseEvent, QKeyEvent, QWheelEvent

from pytessng.DLLs.Tessng import PyCustomerNet, tessngIFace
from pytessng.UserInterface import BaseMouse
from pytessng.GlobalVar import GlobalVar


class MyNet(PyCustomerNet):
    def __init__(self):
        super().__init__()
        self.iface = tessngIFace()
        self.netiface = self.iface.netInterface()

        # 固定观察者对象列表
        self._fixed_observers: List[BaseMouse] = []
        # 临时观察者对象
        self._temp_observer: Optional[BaseMouse] = None

    # 重写方法：加载路网前执行
    def beforeLoadNet(self) -> None:
        # 打印属性信息
        attrs: dict = self.netiface.netAttrs().otherAttrs()
        print("=" * 66)
        print("Load network! Network attrs:")
        if attrs:
            for k, v in attrs.items():
                print(f"\t{k:<15}:{' ' * 5}{v}")
        else:
            print("\t(EMPTY)")
        print("=" * 66, "\n")

    # 重写方法：加载路网后执行
    def afterLoadNet(self) -> None:
        # 能执行这里说明是正版key就开启相关功能
        for action in GlobalVar.actions_only_official_version:
            action.setEnabled(True)

        # # 彩蛋：去除水印
        # scene = self.netiface.graphicsScene()
        # for i, item in enumerate(scene.items()):
        #     if item.zValue() == 100000:
        #         scene.removeItem(item)

    # 重写方法：控制曲率最小距离
    def ref_curvatureMinDist(self, item_type: int, item_id: int, ref_min_dist: float):
        ref_min_dist.value = 0.1
        return True

    # 自定义方法：添加固定或临时观察者
    def attach_observer(self, observer_obj, is_fixed: bool = False):
        observer_obj.before_attach()
        if is_fixed:
            self._fixed_observers.append(observer_obj)
        else:
            self._temp_observer = observer_obj

    # 自定义方法：移除临时观察者
    def detach_observer(self):
        if self._temp_observer is not None:
            self._temp_observer.before_detach()
        self._temp_observer = None

    # 重写方法：鼠标单击后触发
    def afterViewMousePressEvent(self, event: QMouseEvent):
        # 执行观察者的动作
        for observer in self._fixed_observers + [self._temp_observer]:
            if observer is not None:
                observer.handle_mouse_press_event(event)

    # 重写方法：鼠标释放后触发
    def afterViewMouseReleaseEvent(self, event: QMouseEvent):
        # 执行观察者的动作
        for observer in self._fixed_observers + [self._temp_observer]:
            if observer is not None:
                observer.handle_mouse_release_event(event)

    # 重写方法：鼠标移动后触发
    def afterViewMouseMoveEvent(self, event: QMouseEvent) -> None:
        # 执行观察者的动作
        for observer in self._fixed_observers + [self._temp_observer]:
            if observer is not None:
                observer.handle_mouse_move_event(event)

    # 重写方法：鼠标双击后触发
    def afterViewMouseDoubleClickEvent(self, event: QMouseEvent):
        # 执行观察者的动作
        for observer in self._fixed_observers + [self._temp_observer]:
            if observer is not None:
                observer.handle_mouse_double_click_event(event)

    # 重写方法：键盘按下后触发
    def afterViewKeyPressEvent(self, event: QKeyEvent) -> None:
        # 执行观察者的动作
        for observer in self._fixed_observers + [self._temp_observer]:
            if observer is not None:
                observer.handle_key_press_event(event)

    # 重写方法：鼠标滚轮滚动后触发
    def afterViewWheelEvent(self, event: QWheelEvent) -> None:
        # 执行观察者的动作
        for observer in self._fixed_observers + [self._temp_observer]:
            if observer is not None:
                observer.handle_wheel_event(event)
