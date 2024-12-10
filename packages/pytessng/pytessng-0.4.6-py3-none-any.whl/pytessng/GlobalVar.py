from typing import Callable, List, Dict
from PySide2.QtWidgets import QAction


class GlobalVar:
    # ========== Main.py ==========
    # 是否是完整版
    extension: bool = False

    # ========== MyMenu.py ==========
    # 与鼠标事件相关的按钮
    actions_related_to_mouse_event: Dict[str, QAction] = {}
    # 只能正式版本使用的按钮
    actions_only_official_version: List[QAction] = []

    # ========== MyNet.py ==========
    # 给MySimulator添加仿真观察者的函数
    attach_observer_of_my_net: Callable = None
    # 给MySimulator移除仿真观察者的函数
    detach_observer_of_my_net: Callable = None

    # ========== MySimulator.py ==========
    # 给MySimulator添加仿真观察者的函数
    attach_observer_of_my_simulator: Callable = None
    # 给MySimulator移除仿真观察者的函数
    detach_observer_of_my_simulator: Callable = None
