from typing import Callable, List, Optional
from PySide2.QtWidgets import QAction, QGraphicsItem, QGraphicsEllipseItem, QGraphicsObject, QGraphicsProxyWidget, QTextEdit
from PySide2.QtCore import QPointF
from PySide2.QtGui import QMouseEvent, QKeyEvent, QBrush, QColor, QPen, Qt

from ..BaseUI import BaseClass
from ..BaseMouse import BaseMouse
from ..public.TextWindowItem import TextWindowItem
from pytessng.ToolInterface import MyOperation
from pytessng.GlobalVar import GlobalVar


class LinkEditManageBreakPoint(BaseClass):
    name: str = "管理路段断点"
    mode: str = "manage_break_point"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 按钮
        self.action: QAction = GlobalVar.actions_related_to_mouse_event["manage_break_point"]
        # 将按钮与状态改变函数关联
        self.action.toggled.connect(self.monitor_check_state)

        # 观察者
        self.mouse_break_point_manager = None

    # 重写抽象父类BaseUserInterface的方法
    def load(self):
        if self.action.isChecked():
            # 为了关联生效
            self.action.setChecked(False)
            self.action.setChecked(True)
            # 显示提示信息
            message = """已经开启路段断点管理模式，选中路段才会显示路段断点！
            \n - (1) 拖拽断点：选中断点后，鼠标左键拖拽；
            \n - (2) 新增断点：选中路段后，鼠标右键点击新增；
            \n - (3) 删除断点：选中断点后，按下[BackSpace]键。
            """
            self.utils.show_info_box(message)

    # 鼠标事件相关特有方法
    def monitor_check_state(self, checked):
        if checked:
            # 修改按钮为【取消工具】
            self.guiiface.actionNullGMapTool().trigger()

            # 其他按钮取消勾选
            for action in GlobalVar.actions_related_to_mouse_event.values():
                if action.text() not in ["管理路段断点", "退出管理路段断点"]:
                    action.setChecked(False)

            # 修改文字
            self.action.setText("退出管理路段断点")

            # 添加MyNet观察者
            self.mouse_break_point_manager = MouseBreakPointManager(self.apply_manage_break_point)
            GlobalVar.attach_observer_of_my_net(self.mouse_break_point_manager)

        else:
            # 修改文字
            self.action.setText("管理路段断点")

            # 移除MyNet观察者
            GlobalVar.detach_observer_of_my_net()

    def apply_manage_break_point(self, params: dict):
        MyOperation.apply_link_edit_operation(self, params)


class MouseBreakPointManager(BaseMouse):
    def __init__(self, func_apply_manage_break_point: Callable):
        super().__init__()
        # 当前选中的路段ID
        self.link_id: Optional[int] = None
        # 当前选中的断点索引
        self.point_index: Optional[int] = None
        # 现存的点item列表
        self.point_item_list: List[Point] = []
        # 当前文本窗口
        self.current_text_window = None

        # 函数
        self.func_apply_manage_break_point: Callable = func_apply_manage_break_point

    def handle_mouse_press_event(self, event: QMouseEvent) -> None:
        # 网格化
        self.netiface.buildNetGrid(5)
        # 原有所有可移动的item设置为不可见
        self._hide_all_movable_point_items()
        # 置为None
        self.point_index: Optional[int] = None

        # 场景坐标
        scene_pos: QPointF = self.view.mapToScene(event.pos())

        # 左键：选中路段或断点
        if event.button() == Qt.LeftButton:
            # 获取鼠标位置下的项
            items = self.scene.items(scene_pos)
            for item in items:
                if isinstance(item, Point):
                    # 更新路段ID
                    self.link_id: Optional[int] = item.link_id
                    # 重置索引
                    self.point_index: Optional[int] = item.point_index
                    return

            # 获取当前位置的路段数据
            all_link_data: List[dict] = self._get_all_link_data(scene_pos)
            # 没有路段数据
            if not all_link_data:
                # 更新路段ID
                self.link_id: Optional[int] = None
                # 重置索引
                self.point_index: Optional[int] = None
                # 删除之前的图形点
                self._clear_point_item_list()
            # 有路段数据
            else:
                # 判断当前路段是否已经点击过了
                link_data: dict = all_link_data[0]
                link_id: int = link_data["link_id"]
                # 如果路段ID不同
                if link_id != self.link_id:
                    # 更新路段ID
                    self.link_id: Optional[int] = link_id
                    # 重置索引
                    self.point_index: Optional[int] = None
                    # 删除之前的图形点
                    self._clear_point_item_list()
                    # 创建新的图形点
                    self._create_point_item_list(link_id)

        # 右键：新增断点
        elif event.button() == Qt.RightButton:
            if not self.link_id:
                return
            # 获取当前位置的路段数据
            all_link_data: List[dict] = self._get_all_link_data(scene_pos)
            if not all_link_data:
                return

            link_data: dict = all_link_data[0]
            link_id, index, point = link_data["link_id"], link_data["index"], link_data["point"]
            # 执行新增断点
            params = {
                "mode": "add",
                "link_id": link_id,
                "index": index,
                "pos": QPointF(point[0], -point[1]),
            }
            self.func_apply_manage_break_point(params)

            # 新增图形
            point_item: Point = Point(point[0], -point[1], link_id, index+1, self)
            self.scene.addItem(point_item)
            self.point_item_list.insert(index+1, point_item)
            # 更新后面点的索引
            for i, item in enumerate(self.point_item_list[index:], start=index):
                item.point_index = i

    def handle_mouse_release_event(self, event: QMouseEvent) -> None:
        self._remove_info_window()

    def handle_key_press_event(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Backspace:
            # 不满足条件
            if not self.link_id or not self.point_index:
                return

            # 执行删除断点
            params = {
                "mode": "remove",
                "link_id": self.link_id,
                "index": self.point_index,
                "pos": None,
            }
            self.func_apply_manage_break_point(params)

            # 删除图形
            index: int = self.point_index
            self.scene.removeItem(self.point_item_list[index])
            self.point_item_list.pop(index)
            # 重置索引
            self.point_index: Optional[int] = None
            # 更新后面点的索引
            for i, item in enumerate(self.point_item_list[index:], start=index):
                item.point_index = i

        elif event.key() in [Qt.Key_W, Qt.Key_S, Qt.Key_A, Qt.Key_D]:
            if not self.point_item_list or not self.point_index:
                return
            point_item = self.point_item_list[self.point_index]
            x: float = point_item.pos().x()
            y: float = point_item.pos().y()
            if event.key() == Qt.Key_A:
                x -= 0.1
            elif event.key() == Qt.Key_D:
                x += 0.1
            elif event.key() == Qt.Key_W:
                y -= 0.1
            elif event.key() == Qt.Key_S:
                y += 0.1
            point_item.setPos(QPointF(x, y))

    # 开启之前
    def before_attach(self) -> None:
        # 隐藏
        self._hide_all_movable_point_items()

    # 关闭之前
    def before_detach(self) -> None:
        self._remove_info_window()
        self._restore_all_movable_point_items()

    # 获取当前鼠标位置的路段数据
    def _get_all_link_data(self, scene_pos: QPointF) -> List[dict]:
        class Widget: mode, utils = "locate", self.utils
        all_link_data = MyOperation.apply_link_edit_operation(Widget(), {"pos": scene_pos, "in_detail": True})
        return all_link_data

    # 隐藏原有可移动断点item
    def _hide_all_movable_point_items(self):
        # 原有所有可移动的item设置为不可见
        for item in self.scene.items():
            if isinstance(item, QGraphicsObject) and item.flags() & QGraphicsObject.GraphicsItemFlag.ItemIsMovable:
                item.setVisible(False)

    # 恢复原有可移动断点item
    def _restore_all_movable_point_items(self):
        # 原有所有可移动的item设置为可见
        for item in self.scene.items():
            if isinstance(item, QGraphicsObject) and item.flags() & QGraphicsObject.GraphicsItemFlag.ItemIsMovable:
                item.setVisible(True)

    # 创建断点item列表
    def _create_point_item_list(self, link_id: int) -> None:
        link_obj = self.netiface.findLink(link_id)
        link_points: List[QPointF] = link_obj.centerBreakPoints()
        for i, point in enumerate(link_points):
            x, y = point.x(), point.y()
            point_item: Point = Point(x, y, link_id, i, self)
            self.scene.addItem(point_item)
            self.point_item_list.append(point_item)

    # 清除断点item列表
    def _clear_point_item_list(self) -> None:
        for point_item in self.point_item_list:
            self.scene.removeItem(point_item)
        self.point_item_list.clear()

    # 移除信息窗口
    def _remove_info_window(self):
        # 移除信息窗口
        if self.current_text_window is not None:
            self.scene.removeItem(self.current_text_window)
            self.current_text_window = None


class Point(QGraphicsEllipseItem, BaseMouse):
    def __init__(self, x: float, y: float, link_id: int, point_index: int, manager: MouseBreakPointManager):
        # 初始点位置
        self.init_pos: QPointF = QPointF(x, y)
        # 当前点位置
        self.current_pos: QPointF = QPointF(x, y)
        # 路段ID
        self.link_id: int = link_id
        # 点索引
        self.point_index: int = point_index
        # 管理器
        self.manager: MouseBreakPointManager = manager

        # 父类初始化
        BaseMouse.__init__(self)
        self.radius = 1.5
        super().__init__(x - self.radius / 2, y - self.radius / 2, self.radius, self.radius)
        # 设置填充
        self.setBrush(QBrush(QColor(Qt.yellow)))
        # 设置无边框
        self.setPen(QPen(Qt.NoPen))
        # 设置Z
        self.setZValue(10000)
        # 设置可选中和拖动
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)

    # 当位置被移动后
    def itemChange(self, change, value: QPointF):
        # 如果位置发生了改变
        if change == QGraphicsItem.ItemPositionChange:
            change_pos = value
            # 获取中心点
            x_new: float = self.init_pos.x() + change_pos.x()
            y_new: float = self.init_pos.y() + change_pos.y()
            # 计算移动距离
            dx: float = x_new - self.current_pos.x()
            dy: float = y_new - self.current_pos.y()

            # 执行移动断点
            params = {
                "mode": "move",
                "link_id": self.link_id,
                "index": self.point_index,
                "pos": QPointF(dx, dy),
            }
            self.manager.func_apply_manage_break_point(params)

            # 更新周边连接段
            link_obj = self.netiface.findLink(self.link_id)
            move = QPointF(0, 0)
            self.netiface.moveLinks([link_obj], move)

            # 更新当前位置
            self.current_pos = QPointF(x_new, y_new)
            # 更新信息窗口
            self.update_info_window(x_new, y_new)
            return super().itemChange(change, value)

        # 如果选择状态发生了改变
        elif change == QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged:
            selected = bool(value)
            if selected:
                # 设置边框
                pen = QPen(QColor(Qt.red))
                pen.setWidthF(0.2)
                self.setPen(pen)
            else:
                self.setPen(Qt.NoPen)

        return super().itemChange(change, value)

    # 显示信息窗
    def update_info_window(self, x: float, y: float) -> None:
        if self.manager.current_text_window is None:
            item = TextWindowItem()
            self.manager.current_text_window = item
            self.manager.scene.addItem(item)

        # 更新文本
        x_str, y_str = f"{x:.2f}", f"{-y:.2f}"
        link_obj = self.netiface.findLink(self.link_id)
        length = f"{link_obj.length():.2f}"
        message = f"\n 路段ID: {self.link_id:>9} \n 点索引: {self.point_index:>9} \n X-坐标: {x_str:>9} m \n Y-坐标: {y_str:>9} m \n 路段长: {length:>9} m "
        self.manager.current_text_window.set_text(message)
        # 更新位置
        self.manager.current_text_window.set_pos(x, y)
