import math
from typing import List, Optional, Callable
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsItem, QMessageBox, QLabel, QComboBox, QPushButton, QDialog
from PySide2.QtCore import QPointF
from PySide2.QtGui import QBrush, QColor, QPen, QMouseEvent, Qt

from ..BaseMouse import BaseMouse
from ..BaseUI import BaseUserInterface, MyQVBoxLayout, MyQHBoxLayout
from ..public.ComboBoxWithCheckBoxes import ComboBoxWithCheckBoxes


# 计算射线与y轴的夹角
def calculate_angle(point1: QPointF, point2: QPointF) -> float:
    # 计算线段的方向向量
    dx = point2.x() - point1.x()
    dy = -(point2.y() - point1.y())
    angle_radians = math.atan2(dx, dy)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees


class DesiredSpeedDecisionPointCreator(BaseMouse):
    def __init__(self):
        super().__init__()

        # 车辆型号列表
        self.vehicle_type_code_list: List[str] = []
        # 当前面板
        self.current_panel: Optional[BaseUserInterface] = None

        # 初始化数据
        self._init_data()

    def _init_data(self):
        # 网格化
        self.netiface.buildNetGrid(50)

        # 获取当前车辆型号列表
        self.vehicle_type_code_list = [
            f"{vehicle_type.vehicleTypeCode}: {vehicle_type.vehicleTypeName}"
            for vehicle_type in self.netiface.vehicleTypes()
        ]
        self.vehicle_type_code_list = sorted(self.vehicle_type_code_list, key=lambda x: int(x.split(":")[0]))

    def handle_mouse_press_event(self, event: QMouseEvent) -> None:
        # 判断按下的是不是右键
        if event.button() != Qt.RightButton:
            return

        # 鼠标位置
        mouse_pos = event.pos()
        # 检查按下的位置是否有图形项
        item = self.view.itemAt(mouse_pos)
        if isinstance(item, DecisionPointRect):
            # 是拖拽模式
            item.draggable = True
            return

        # 是创建模式
        self._is_dragging = False
        # 鼠标坐标转场景坐标
        scene_pos = self.view.mapToScene(mouse_pos)
        # 定位车道
        locations = self.netiface.locateOnCrid(scene_pos, 9)
        if not locations:
            return
        location = locations[0]
        dist = location.leastDist
        if dist > 3:
            return
        # 点坐标
        point = location.point
        x, y = point.x(), point.y()
        # 车道对象
        lane = location.pLaneObject
        # 车道ID
        lane_id = lane.id()
        # 车道宽度
        width = lane.width() if lane.isLane() else 3.5
        # 创建矩形
        rect_item = DecisionPointRect(x, y, width, self._locate_on_crid)
        # 设置属性
        rect_item.setData(0, lane_id)
        rect_item.setData(1, location.distToStart)
        self.scene.addItem(rect_item)

        # 检测重合
        if self._check_overlap(rect_item, mouse_pos):
            QMessageBox.warning(self.view, "重叠检测", "新创建的矩形与已有的矩形重叠！")
            self.scene.removeItem(rect_item)

    def handle_mouse_double_click_event(self, event: QMouseEvent) -> None:
        if event.button() != Qt.LeftButton:
            return

        # 鼠标位置
        mouse_pos = event.pos()
        # 检查按下的位置是否有图形项
        item = self.view.itemAt(mouse_pos)
        if isinstance(item, DecisionPointRect):
            # 获取车道数据
            lane_id = item.data(0)
            dist = item.data(1)
            # 显示配置面板
            self.current_panel = ConfigurePanel(self.vehicle_type_code_list)
            self.current_panel.load()
            self.current_panel.show()

    # 自定义方法：检测新矩形与已有矩形是否重叠
    def _check_overlap(self, current_item, mouse_pos: QPointF) -> bool:
        for item in self.scene.items(mouse_pos):
            if isinstance(item, DecisionPointRect) and item != current_item:
                if current_item.collidesWithItem(item):
                    return True  # 存在重叠
        return False  # 无重叠

    # 自定义方法：根据坐标定位车道
    def _locate_on_crid(self, scene_pos: QPointF) -> Optional[list]:
        locations = self.netiface.locateOnCrid(scene_pos, 9)
        if not locations:
            return None
        location = locations[0]
        dist = location.leastDist
        if dist > 3:
            return None
        # 获取点
        point = location.point
        # 获取角度
        index = location.segmIndex
        lane = location.pLaneObject
        lane_points = lane.centerBreakPoints()
        point1, point2 = lane_points[index], lane_points[index + 1]
        # 使用公式计算角度
        angle = calculate_angle(point1, point2)
        # 车道数据
        lane_id = lane.id()
        dist = location.distToStart
        return [(point.x(), point.y()), angle, lane_id, dist]


class DecisionPointRect(QGraphicsRectItem):
    def __init__(self, x, y, width, func_locate_on_crid):
        # 初始的中心位置
        self.init_pos: QPointF = QPointF(x, y)
        # 初始的角度
        self.init_angle: float = 0
        # 宽度
        self.width: int = width
        # 长度
        self.length: int = 1

        # 定位函数
        self._locate_on_crid: Callable = func_locate_on_crid

        # 父类初始化
        super().__init__(x - self.width / 2, y - self.length / 2, self.width, self.length)
        # 本类初始化
        self._init()

    # 自定义方法：初始化
    def _init(self):
        # 设置颜色和透明度
        brush = QBrush(QColor(100, 100, 250, 222))
        self.setBrush(brush)
        # 设置边框颜色和宽度
        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(0.4)
        self.setPen(pen)
        # 设置旋转中心为矩形中心
        self.setTransformOriginPoint(self.rect().center())
        # 设置可拖动
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)
        # 设置接收鼠标双击事件
        self.setAcceptedMouseButtons(Qt.LeftButton)

        # 设置初始旋转角度
        self.init_angle = self._locate_on_crid(self.init_pos)[1]
        self.setRotation(self.init_angle)

    # 父类方法：当位置被移动后
    def itemChange(self, change, value: QPointF):
        if change != QGraphicsItem.ItemPositionChange:
            return super().itemChange(change, value)

        # 获取矩形的中心点
        change_pos = value
        new_x_center = self.init_pos.x() + change_pos.x()
        new_y_center = self.init_pos.y() + change_pos.y()
        rect_center = QPointF(new_x_center, new_y_center)

        # 获取新点和角度
        result = self._locate_on_crid(rect_center)
        # 如果拖到了路段外面
        if result is None:
            self.setRotation(self.init_angle)
            return QPointF(0, 0)
        point, angle, lane_id, dist = result
        # 点坐标
        change_pos.setX(point[0] - self.init_pos.x())
        change_pos.setY(point[1] - self.init_pos.y())
        # 设置角度
        self.setRotation(angle)
        # 设置属性
        self.setData(0, lane_id)
        self.setData(1, dist)
        return change_pos


class ConfigurePanel(BaseUserInterface):
    name: str = "期望速度决策点配置"
    width: int = 100

    def __init__(self, vehicle_type_code_list):
        super().__init__()
        # 车型列表
        self.vehicle_type_list: List[str] = vehicle_type_code_list
        # 期望速度列表
        self.desired_speed_list: List[str] = [str(i) for i in range(20, 120, 5)]

        self.desired_speed = None

    def set_widget_layout(self):
        # 第一行：文本、下拉框
        self.label_vehicle_type = QLabel('车辆类型：')
        self.combo_vehicle_type = ComboBoxWithCheckBoxes(self.vehicle_type_list)
        # 第二行：文本、下拉框
        self.label_desired_speed = QLabel('期望速度（km/h）：')
        self.combo_desired_speed = QComboBox()
        self.combo_desired_speed.addItems(tuple(self.desired_speed_list))
        # 第三行：按钮
        self.button = QPushButton('确认')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.label_vehicle_type, self.combo_vehicle_type]),
            MyQHBoxLayout([self.label_desired_speed, self.combo_desired_speed]),
            self.button
        ])
        self.setLayout(layout)

    def set_monitor_connect(self):
        pass

    def set_button_connect(self):
        self.button.clicked.connect(self.apply_button_action)

    def set_default_state(self):
        pass

    def apply_monitor_state(self):
        pass

    def apply_button_action(self):
        checked_items = self.combo_vehicle_type.checked_items()
        print(checked_items)

