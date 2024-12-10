import math

from .LineBase import LineBase


class LinePointsSimplifier:
    """ 简化点序列 """
    @staticmethod
    def calculate_length_between_points_in_line(points: list, start_index: int, end_index: int) -> float:
        length = 0
        for i in range(start_index, end_index):
            p1 = points[i]
            p2 = points[i + 1]
            distance = LineBase.calculate_distance_between_two_points(p1, p2)
            length += distance
        return length

    @staticmethod
    def calculate_distance_from_point_to_line(point: tuple, line_point_1: tuple, line_point_2: tuple) -> float:
        x0, y0 = point[:2]
        x1, y1 = line_point_1[:2]
        x2, y2 = line_point_2[:2]
        # 计算点到直线的距离
        if x1 == x2:
            distance = abs(x0 - x1)
        else:
            # 计算直线的斜率和截距
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
            distance = abs(slope * x0 - y0 + intercept) / math.sqrt(slope ** 2 + 1)
        return distance

    @staticmethod
    def simplify_points(points: list, max_distance: float = 0.3, max_length: float = 1000) -> list:
        num = len(points)
        if num <= 2:
            return [k for k in range(num)]

        indexes = [0]
        start_index, end_index = 0, 2

        while end_index < num:
            assert (end_index - start_index) >= 2

            length = LinePointsSimplifier.calculate_length_between_points_in_line(points, start_index, end_index)
            if length > max_length:
                start_index = end_index - 1
                indexes.append(start_index)
            else:
                start_point, end_point = points[start_index], points[end_index]
                for k in range(start_index + 1, end_index):
                    mid_point = points[k]
                    distance = LinePointsSimplifier.calculate_distance_from_point_to_line(mid_point, start_point, end_point)
                    if distance > max_distance:
                        start_index = end_index - 1
                        indexes.append(start_index)
                        break
            end_index += 1
        indexes.append(num - 1)

        return indexes


class LinkPointsSimplifier:
    @staticmethod
    def simplify_link(points: list, lanes_points: list, max_distance: float = 0.3, max_length: float = 1000):
        simplified_index = LinePointsSimplifier.simplify_points(points, max_distance, max_length)

        # 路段点位
        new_points = [
            points[index]
            for index in simplified_index
        ]

        # 车道点位
        new_lanes_points = [
            {
                "left": [
                    lane_points["left"][index]
                    for index in simplified_index
                ],
                "center": [
                    lane_points["center"][index]
                    for index in simplified_index
                ],
                "right": [
                    lane_points["right"][index]
                    for index in simplified_index
                ],
            }
            for lane_points in lanes_points
        ]

        return new_points, new_lanes_points
