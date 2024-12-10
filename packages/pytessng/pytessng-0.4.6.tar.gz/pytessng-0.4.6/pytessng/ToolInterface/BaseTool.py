from abc import ABC
from typing import Optional, Callable, Dict, List, Union
from numpy import isnan
from PySide2.QtCore import QPointF
from PySide2.QtGui import QVector3D

from pytessng.DLLs.Tessng import Online, _DecisionPoint, _RoutingFLowRatio


class BaseTool(ABC):
    def __init__(self, netiface=None, extension: bool = False):
        self.netiface = netiface
        self.scene_scale = netiface.sceneScale() if netiface else 1

        self.Online = Online if extension else None
        self.private_class: dict = {
            "_DecisionPoint": _DecisionPoint,
            "_RoutingFLowRatio": _RoutingFLowRatio,
        } if extension else None

    def _p2m(self, x: float) -> float:
        return x * self.scene_scale

    def _m2p(self, x: float) -> float:
        return x / self.scene_scale

    def _qtpoint2list(self, qtpoints: List[Union[QPointF, QVector3D]], move: Optional[Dict[str, float]] = None) -> List[List[float]]:
        x_move, y_move = (0, 0) if move is None else (-move["x_move"], -move["y_move"])

        if type(qtpoints[0]) == QPointF:
            return [
                [
                    self._p2m(qt_point.x()) + x_move,
                    -self._p2m(qt_point.y()) + y_move,
                ]
                for qt_point in qtpoints
            ]
        return [
            [
                self._p2m(qt_point.x()) + x_move,
                -self._p2m(qt_point.y()) + y_move,
                self._p2m(qt_point.z()) if not isnan(qt_point.z()) else 0
            ]
            for qt_point in qtpoints
        ]

    def _list2qtpoint(self, points: List[List[float]], move: Optional[Dict[str, float]] = None) -> List[Union[QPointF, QVector3D]]:
        if len(points) < 2:
            raise Exception("The length of points is not valid!")

        x_move, y_move = (0, 0) if move is None else (move["x_move"], move["y_move"])

        if len(points[0]) == 2:
            return [
                QPointF(
                    self._m2p(float(point[0]) + x_move),
                    -(self._m2p(float(point[1]) + y_move)),
                )
                for point in points
            ]
        else:
            return [
                QVector3D(
                    self._m2p(float(point[0]) + x_move),
                    -(self._m2p(float(point[1]) + y_move)),
                    self._m2p(float(point[2])),
                ) for point in points
            ]

    def _xy2lonlat(self, points: List[List[float]], proj_func: Callable) -> list:
        if len(points[0]) == 2:
            return [
                [*proj_func(point[0], point[1], inverse=True)]
                for point in points
            ]
        else:
            return [
                [*proj_func(point[0], point[1], inverse=True), point[2]]
                for point in points
            ]

    # 更新场景大小
    def update_scene_size(self) -> None:
        # 尺寸初始值
        scene_size: List[float] = [300, 200]
        # 尺寸最大值
        max_size: int = 10_0000

        all_links = self.netiface.links()
        if all_links:
            xs, ys = [], []
            for link in all_links:
                points = self._qtpoint2list(link.centerBreakPoints())
                xs.extend([abs(point[0]) for point in points])
                ys.extend([abs(point[1]) for point in points])

                scene_size[0] = max(scene_size[0], max(xs))
                scene_size[1] = max(scene_size[1], max(ys))

            width = min(scene_size[0] * 2 + 10, max_size)
            height = min(scene_size[1] * 2 + 10, max_size)

            # 设置场景大小
            self.netiface.setSceneSize(width, height)  # m
