from abc import ABC, abstractmethod
from pyautogui import size as scene_size
from PySide2.QtWidgets import QWidget, QLayout, QHBoxLayout, QVBoxLayout, QGroupBox, QLayoutItem
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QFontMetrics

from .Utils import Utils
from pytessng.DLLs.Tessng import tessngIFace
from pytessng.Config import PathConfig, UIConfig


class BaseUserInterface(QWidget):
    # 界面名称
    name: str = "Xxx"
    # 界面宽度
    width: int = UIConfig.Base.width
    # 界面高度
    height: int = UIConfig.Base.height
    # 在界面中心显示
    show_in_center: bool = True
    # 工具包
    utils = Utils

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iface = tessngIFace()
        self.guiiface = self.iface.guiInterface()
        # 继承子类中只有view系列、路段编辑[合并路段、管理断点、修改路段属性]、导出配置文件会用到iface/netiface

    def load(self):
        # 设置界面布局
        self.set_widget_layout()
        # 设置界面属性*
        self.set_widget_attribution()
        # 设置组件监测关系
        self.set_monitor_connect()
        # 设置按钮关联关系
        self.set_button_connect()
        # 设置默认状态
        self.set_default_state()

    def set_widget_attribution(self):
        # 设置名称
        self.setWindowTitle(self.name)
        # 设置图标
        self.setWindowIcon(QIcon(PathConfig.ICON_FILE_PATH))

        # 获取建议尺寸
        width, height = self.sizeHint().width(), self.sizeHint().height()
        width, height = max(width, self.width), max(height, self.height)
        # 获得屏幕尺寸
        screen_width, screen_height = scene_size()
        # 屏幕中心位置
        if self.show_in_center:
            x, y = (screen_width - width) // 2, (screen_height - height) // 2
        else:
            x, y = (screen_width / 2 - width) // 2, (screen_height - height) // 2
        # 设置位置和尺寸
        self.setGeometry(x, y, width, height)

        # 设置尺寸固定
        # widget.setFixedSize(width, height)
        # 设置窗口标志位，使其永远在最前面
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    @abstractmethod
    def set_widget_layout(self):
        pass

    @abstractmethod
    def set_monitor_connect(self):
        pass

    @abstractmethod
    def set_button_connect(self):
        pass

    @abstractmethod
    def set_default_state(self):
        pass

    @abstractmethod
    def apply_monitor_state(self):
        pass

    @abstractmethod
    def apply_button_action(self):
        pass

    def calc_char_width(self, component, char_number: int) -> int:
        font = component.font()
        font_metrics = QFontMetrics(font)
        item_width = font_metrics.horizontalAdvance("0" * char_number)
        return item_width


class BaseClass(ABC):
    # 界面名称
    name: str = "Xxx"
    # 工具包
    utils = Utils

    def __init__(self, *args, **kwargs):
        self.iface = tessngIFace()  # 继承子类都不会调用
        self.guiiface = self.iface.guiInterface()

    @abstractmethod
    def load(self):
        pass

    def show(self):
        pass

    def close(self):
        pass


class MyQHBoxLayout(QHBoxLayout):
    def __init__(self, elements: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_elements(elements)

    def add_elements(self, elements: list):
        for element in elements:
            if isinstance(element, QWidget):
                self.addWidget(element)
            elif isinstance(element, QLayout):
                self.addLayout(element)
            elif isinstance(element, QLayoutItem):
                self.addItem(element)
            elif isinstance(element, int):
                self.addStretch(element)
            else:
                raise TypeError(f"Unsupported type: {type(element)}. Expected QWidget or QLayout.")


class MyQVBoxLayout(QVBoxLayout):
    def __init__(self, elements: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_elements(elements)

    def add_elements(self, elements: list):
        for element in elements:
            if isinstance(element, QWidget):
                self.addWidget(element)
            elif isinstance(element, QLayout):
                self.addLayout(element)
            elif isinstance(element, QLayoutItem):
                self.addItem(element)
            elif isinstance(element, int):
                self.addStretch(element)
            else:
                raise TypeError(f"Unsupported type: {type(element)}. Expected QWidget or QLayout.")


class MyQGroupBox(QGroupBox):
    def __init__(self, layout, title: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(layout)
        if title:
            self.setTitle(title)
