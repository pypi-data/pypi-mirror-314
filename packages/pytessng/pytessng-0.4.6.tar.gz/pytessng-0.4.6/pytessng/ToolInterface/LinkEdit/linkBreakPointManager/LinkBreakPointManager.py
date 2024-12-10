from typing import Optional, List, Dict, Tuple
from PySide2.QtCore import QPointF
from PySide2.QtGui import QVector3D

from ..BaseLinkEditor import BaseLinkEditor
from ...public.line.LineBase import LineBase, POINT


class LinkBreakPointManager(BaseLinkEditor):
    def edit(self, mode: str, link_id: int, index: int, pos: Optional[QPointF]) -> None:
        assert mode in ["add", "remove", "move"]

        # 获取路段对象
        link_obj = self.netiface.findLink(link_id)
        if link_obj is None:
            return

        # 获取点位
        link_points = link_obj.centerBreakPoint3Ds()
        lanes_points = [
            {
                "left": lane.leftBreakPoint3Ds(),
                "center": lane.centerBreakPoint3Ds(),
                "right": lane.rightBreakPoint3Ds(),
            }
            for lane in link_obj.lanes()
        ]

        # 更新点位数据
        if mode == "add":
            self.add_break_point(link_points, lanes_points, index, pos)
        elif mode == "remove":
            self.remove_break_point(link_points, lanes_points, index, pos)
        elif mode == "move":
            self.move_break_point(link_points, lanes_points, index, pos)

        # 更新路段断点
        self.netiface.updateLinkAndLane3DWithPoints(link_obj, link_points, lanes_points)

    # 新增断点
    def add_break_point(self, link_points: List[QPointF], lanes_points: List[Dict[str, List[QPointF]]], index: int, pos: Optional[QPointF]) -> None:
        # 路段
        point1, point2 = link_points[index], link_points[index + 1]
        point1, point, point2 = (point1.x(), point1.y(), point1.z()), (pos.x(), pos.y()), (point2.x(), point2.y(), point2.z())
        length_long = LineBase.calculate_distance_between_two_points(point1, point2)
        length_short = LineBase.calculate_distance_between_two_points(point1, point)
        t = length_short / length_long
        point_new = LineBase.calculate_interpolate_point_between_two_points(point1, point2, t)
        point_new = QVector3D(*point_new)
        link_points.insert(index + 1, point_new)
        # 各车道
        for i in range(len(lanes_points)):
            for location in ["left", "center", "right"]:
                point1, point2 = lanes_points[i][location][index], lanes_points[i][location][index + 1]
                point1, point2 = (point1.x(), point1.y(), point1.z()), (point2.x(), point2.y(), point2.z())
                point_new = LineBase.calculate_interpolate_point_between_two_points(point1, point2, t)
                point_new = QVector3D(*point_new)
                lanes_points[i][location].insert(index + 1, point_new)

    # 移除断点
    def remove_break_point(self, link_points: List[QPointF], lanes_points: List[Dict[str, List[QPointF]]], index: int, pos: Optional[QPointF]) -> None:
        point_count = len(link_points)
        if index == 0 or index == point_count - 1:
            return

        # 计算距离
        distance_mapping = self._get_distance_mapping(link_points, lanes_points, index)

        # 路段
        link_points.pop(index)

        # 各车道
        for i in range(len(lanes_points)):
            for location in ["left", "center", "right"]:
                lanes_points[i][location].pop(index)
        # 点位数
        point_count: int = len(link_points)
        # 路段上的点
        last_point_qt: QVector3D = link_points[index - 1]
        last_last_point_qt: QVector3D = link_points[index - 2] if index >= 2 else None
        next_point_qt: QVector3D = link_points[index]
        next_next_point_qt: QVector3D = link_points[index + 1] if index <= point_count - 2 else None
        # 从QVector3D转tuple
        last_point: tuple = (last_point_qt.x(), -last_point_qt.y(), last_point_qt.z())
        last_last_point: tuple = (last_last_point_qt.x(), -last_last_point_qt.y(), last_last_point_qt.z()) if last_last_point_qt else None
        next_point: tuple = (next_point_qt.x(), -next_point_qt.y(), next_point_qt.z())
        next_next_point: tuple = (next_next_point_qt.x(), -next_next_point_qt.y(), next_next_point_qt.z()) if next_next_point_qt else None

        # 遍历各车道
        for i in range(len(lanes_points)):
            for location in ["left", "center", "right"]:
                distance: float = distance_mapping[i][location]
                # 当前点的上一个点
                if index >= 1:
                    pp1, pp2, pp3 = last_last_point, last_point, next_point
                    self._update_lane_point(lanes_points, i, location, index - 1, pp1, pp2, pp3, distance)
                # 当前点的下一个点
                if index <= point_count - 1:
                    pp1, pp2, pp3 = last_point, next_point, next_next_point
                    self._update_lane_point(lanes_points, i, location, index, pp1, pp2, pp3, distance)

    # 移动断点
    def move_break_point(self, link_points: List[QPointF], lanes_points: List[Dict[str, List[QPointF]]], index: int, pos: Optional[QPointF]) -> None:
        # ============================================================
        # 第一步：计算路段中心线与各车道左中右线的距离
        distance_mapping = self._get_distance_mapping(link_points, lanes_points, index)

        # ============================================================
        # 第二步：更新路段点位
        link_point: QVector3D = link_points[index]
        new_link_point: tuple = (link_point.x() + pos.x(), -(link_point.y() + pos.y()), link_point.z())
        new_link_point_qt: QVector3D = QVector3D(new_link_point[0], -new_link_point[1], new_link_point[2])
        link_points[index] = new_link_point_qt

        # ============================================================
        # 第三步：更新各车道点位
        # 点位数
        point_count: int = len(link_points)
        # 路段上的点
        current_point_qt: QVector3D = link_points[index]
        last_point_qt: QVector3D = link_points[index - 1] if index >= 1 else None
        last_last_point_qt: QVector3D = link_points[index - 2] if index >= 2 else None
        next_point_qt: QVector3D = link_points[index + 1] if index < point_count - 1 else None
        next_next_point_qt: QVector3D = link_points[index + 2] if index < point_count - 2 else None
        # 从QVector3D转tuple
        current_point: tuple = (current_point_qt.x(), -current_point_qt.y(), current_point_qt.z())
        last_point: tuple = (last_point_qt.x(), -last_point_qt.y(), last_point_qt.z()) if last_point_qt else None
        last_last_point: tuple = (last_last_point_qt.x(), -last_last_point_qt.y(), last_last_point_qt.z()) if last_last_point_qt else None
        next_point: tuple = (next_point_qt.x(), -next_point_qt.y(), next_point_qt.z()) if next_point_qt else None
        next_next_point: tuple = (next_next_point_qt.x(), -next_next_point_qt.y(), next_next_point_qt.z()) if next_next_point_qt else None

        # 遍历各车道
        for i in range(len(lanes_points)):
            for location in ["left", "center", "right"]:
                distance: float = distance_mapping[i][location]
                # 当前点
                pp1, pp2, pp3 = last_point, current_point, next_point
                self._update_lane_point(lanes_points, i, location, index, pp1, pp2, pp3, distance)
                # 当前点的上一个点
                if index >= 1:
                    pp1, pp2, pp3 = last_last_point, last_point, current_point
                    self._update_lane_point(lanes_points, i, location, index - 1, pp1, pp2, pp3, distance)
                # 当前点的下一个点
                if index <= point_count - 2:
                    pp1, pp2, pp3 = current_point, next_point, next_next_point
                    self._update_lane_point(lanes_points, i, location, index + 1, pp1, pp2, pp3, distance)

    def _get_distance_mapping(self, link_points: List[QVector3D], lanes_points: List[Dict[str, List[QVector3D]]], index: int) -> Dict[int, Dict[str, float]]:
        distance_mapping = {}
        if index == 0:
            p1: QVector3D = link_points[index]
            p2: QVector3D = link_points[index + 1]
        else:
            p1: QVector3D = link_points[index - 1]
            p2: QVector3D = link_points[index]
        p1: tuple = (p1.x(), -p1.y(), p1.z())
        p2: tuple = (p2.x(), -p2.y(), p2.z())
        # 遍历各车道
        for i in range(len(lanes_points)):
            distance_mapping[i] = {}
            for location in ["left", "center", "right"]:
                lane_point: QVector3D = lanes_points[i][location][index]
                lane_point: tuple = (lane_point.x(), -lane_point.y(), lane_point.z())
                # 方位
                direction: str = LineBase.calculate_relative_position_of_point_to_line(p1, p2, lane_point)
                # 距离
                distance: float = LineBase.calculate_distance_from_point_to_line(p1, p2, lane_point)
                distance: float = distance if direction == "left" else -distance
                # 记录
                distance_mapping[i][location] = distance
        return distance_mapping

    def _update_lane_point(self, lanes_points, i: int, location: str, index: int, p1: tuple, p2: tuple, p3: tuple, distance: float) -> None:
        new_lane_point = self._get_new_lane_point(p1, p2, p3, distance)
        lane_point_z: float = lanes_points[i][location][index].z()
        new_lane_point_qt: QVector3D = QVector3D(new_lane_point[0], -new_lane_point[1], lane_point_z)
        lanes_points[i][location][index] = new_lane_point_qt

    def _get_new_lane_point(self, last_point: Optional[tuple], mid_point: tuple, next_point: Optional[tuple], distance: float) -> tuple:
        A1, B1, C1 = LineBase.calculate_line_coefficients_with_left_move(last_point, mid_point, distance) if last_point is not None else (0, 0, 0)
        A2, B2, C2 = LineBase.calculate_line_coefficients_with_left_move(mid_point, next_point, distance) if next_point is not None else (0, 0, 0)

        # 如果是首尾点或两直线平行
        if last_point is None or next_point is None or (A1 == A2 == 0 or B1 == B2 == 0 or round(A1 * B2 - A2 * B1, 5) == 0):
            # 求点到直线的垂足
            (A, B, C) = (A1, B1, C1) if last_point is not None else (A2, B2, C2)
            new_lane_point: tuple = LineBase.calculate_perpendicular_foot_of_point_to_line((A, B, C), mid_point)
        # 如果不平行
        else:
            # 求两直线的交点
            new_lane_point: tuple = LineBase.calculate_intersection_point_from_two_lines((A1, B1, C1), (A2, B2, C2), (None, None))
            assert new_lane_point[0] is not None and new_lane_point[1] is not None

        return new_lane_point
