from typing import List, Tuple, Union
from PySide2.QtWidgets import QGraphicsPolygonItem
from PySide2.QtCore import QPointF, Qt
from PySide2.QtGui import QColor, QPen, QBrush, QPolygonF


class HighLightPathItem(QGraphicsPolygonItem):
    def __init__(self, points: Union[QPolygonF, List[QPointF]], color: Union[str, Tuple[int, int, int]] = "yellow", transparency: float = 128, no_line: bool = False, line_width: float = 0.2):
        # 父类初始化
        polygon = QPolygonF(points) if not isinstance(points, QPolygonF) else points
        super().__init__(polygon)
        self.color: Union[str, Tuple[int, int, int]] = color
        self.transparency: float = transparency
        self.no_line: bool = no_line
        self.line_width: float = line_width

        self.init()

    def init(self):
        # 设置填充颜色
        color = self._get_color(self.color)
        fill_color = QColor(*color)
        # 设置透明
        fill_color.setAlpha(self.transparency)
        self.setBrush(QBrush(fill_color, Qt.SolidPattern))

        # 设置边框
        if self.no_line:
            self.setPen(Qt.NoPen)
        else:
            # 设置颜色和宽度
            self.setPen(QPen(Qt.red, self.line_width))

        # 设置Z值
        self.setZValue(9999)

    def set_color(self, color: Union[str, Tuple[int, int, int]]):
        # 设置填充颜色
        color = self._get_color(color)
        fill_color = QColor(*color)
        # 设置透明
        fill_color.setAlpha(self.transparency)
        self.setBrush(QBrush(fill_color, Qt.SolidPattern))

    def _get_color(self, color: Union[str, Tuple[int, int, int]]):
        color_mapping = {
            "red": Qt.red,
            "orange": Qt.darkYellow,
            "yellow": Qt.yellow,
            "green": Qt.green,
            "blue": Qt.blue,
            "black": Qt.black,
            "white": Qt.white,
            "gray": Qt.gray,
        }
        color = color_mapping.get(color, color)
        color = [color] if not isinstance(color, tuple) else color
        return color
