import math
from typing import List, Tuple, Union
from shapely.geometry import Polygon


POINT = Union[List[float], Tuple[float, float], Tuple[float, float, float]]
LINE = List[POINT]


class LineBase:
    # 计算两点间距
    @staticmethod
    def calculate_distance_between_two_points(p1: POINT, p2: POINT) -> float:
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    # 计算两点连线与y正轴的顺时针角度(0~360)
    @staticmethod
    def calculate_angle_with_y_axis(p1: POINT, p2: POINT) -> float:
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        delta_x: float = x2 - x1
        delta_y: float = y2 - y1
        # 使用 atan2 计算角度（弧度）
        angle_rad: float = math.atan2(delta_x, delta_y)
        # 将弧度转换为角度
        angle_deg: float = math.degrees(angle_rad)
        # 将角度限制在0到360
        angle_deg_with_y_axis: float = (angle_deg + 360) % 360
        return angle_deg_with_y_axis

    # 对两点的线段进行线性插值
    @staticmethod
    def calculate_interpolate_point_between_two_points(p1: POINT, p2: POINT, t: float) -> POINT:
        x: float = p1[0] + (p2[0] - p1[0]) * t
        y: float = p1[1] + (p2[1] - p1[1]) * t
        if len(p1) == 2:
            return x, y
        else:
            z = p1[2] + (p2[2] - p1[2]) * t
            return x, y, z

    # 给两个点算直线参数ABC
    @staticmethod
    def calculate_line_coefficients(p1: POINT, p2: POINT) -> (float, float, float):
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        # 处理垂直线，斜率不存在
        if x1 == x2:
            A, B, C = 1, 0, -x1
        else:
            # 计算斜率
            m = (y2 - y1) / (x2 - x1)
            # 计算截距
            b = y1 - m * x1
            # 转换为Ax + By + C = 0的形式
            A, B, C = -m, 1, -b
        return A, B, C

    # 两点所在直线向左移动移动一定距离之后的ABC
    @staticmethod
    def calculate_line_coefficients_with_left_move(p1: POINT, p2: POINT, move_distance: float) -> (float, float, float):
        A, B, C = LineBase.calculate_line_coefficients(p1, p2)
        length: float = math.sqrt(A ** 2 + B ** 2)
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        delta_x: float = x2 - x1
        delta_y: float = y2 - y1
        flag: int = -1 if delta_x > 0 else (1 if delta_x < 0 else (-1 if delta_y > 0 else 1))
        C_offset: float = C + move_distance * length * flag
        return A, B, C_offset

    # 判断点在直线的左侧、右侧还是其上
    @staticmethod
    def calculate_relative_position_of_point_to_line(p1: POINT, p2: POINT, p3: POINT) -> str:
        x1, y1 = p1[:2]
        x2, y2 = p2[:2]
        x3, y3 = p3[:2]
        # 计算叉积
        cross: float = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        if cross > 0:
            return "left"
        elif cross < 0:
            return "right"
        else:
            return "on"

    # 计算点到直线(用两点表示)的距离
    @staticmethod
    def calculate_distance_from_point_to_line(p1: POINT, p2: POINT, p3: POINT) -> float:
        x1, y1 = p1[:2]
        x2, y2 = p2[:2]
        x3, y3 = p3[:2]
        numerator: float = abs((y2 - y1) * x3 - (x2 - x1) * y3 + x2 * y1 - y2 * x1)
        denominator: float = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        return numerator / denominator

    # 计算点到直线的垂足点坐标
    @staticmethod
    def calculate_perpendicular_foot_of_point_to_line(line_coeff: Tuple[float, float, float], point: POINT) -> POINT:
        A, B, C = line_coeff
        x0, y0 = point[:2]
        denominator: float = A ** 2 + B ** 2
        x: float = (B * (B * x0 - A * y0) - A * C) / denominator
        y: float = (A * (-B * x0 + A * y0) - B * C) / denominator
        if len(point) == 2:
            return [x, y]
        else:
            return [x, y, point[2]]

    # 计算线段长度
    @staticmethod
    def calculate_line_length(line: LINE) -> float:
        return sum([
            LineBase.calculate_distance_between_two_points(line[i - 1], line[i])
            for i in range(1, len(line))
        ])

    @staticmethod
    # 根据首尾段角度计算转向类型
    def calculate_turn_type(line: LINE) -> str:
        start_angle: float = LineBase.calculate_angle_with_y_axis(line[0], line[1])
        end_angle: float = LineBase.calculate_angle_with_y_axis(line[-2], line[-1])
        # 角度差 -180~180
        angle_diff: float = (end_angle - start_angle + 180) % 360 - 180
        # 计算转向
        if -45 < angle_diff < 45:  # 90
            turn_type: str = "直行"
        elif -150 < angle_diff < -45:  # 105
            turn_type: str = "左转"
        elif 45 < angle_diff < 150:  # 105
            turn_type: str = "右转"
        else:  # 60
            turn_type: str = "调头"
        return turn_type

    # 计算两条多义线合并后的线段
    @staticmethod
    def calculate_merged_line_of_two_lines(line1: List[POINT], line2: List[POINT]) -> LINE:
        new_line: LINE = []
        for p1, p2 in zip(line1, line2):
            x: float = (p1[0] + p2[0]) / 2
            y: float = (p1[1] + p2[1]) / 2
            if len(p1) == 3:
                z: float = p1[2] + (p2[2] - p1[2]) / 2
                p: POINT = [x, y, z]
            else:
                p: POINT = [x, y]
            new_line.append(p)
        return new_line

    # 计算两直线交点
    @staticmethod
    def calculate_intersection_point_from_two_lines(first_line_coeff: Tuple[float, float, float], second_line_coeff: Tuple[float, float, float], point: POINT) -> POINT:
        A1, B1, C1 = first_line_coeff
        A2, B2, C2 = second_line_coeff
        # 计算分母
        denominator: float = A1 * B2 - A2 * B1
        # 如果分母接近零，说明直线平行或重合
        if abs(denominator) < 1e-6:
            x, y = point
        else:
            # 计算交点坐标
            x = (B1 * C2 - B2 * C1) / denominator
            y = (A2 * C1 - A1 * C2) / denominator
        return x, y

    # 获取多边形边界点
    @staticmethod
    def calculate_boundary_points(polygon_list: List[List[POINT]]) -> list:
        # 构建多边形对象列表
        polygon_list: List[Polygon] = [Polygon(coords) for coords in polygon_list]
        # 计算多边形的并集
        union_polygon: Polygon = polygon_list[0]
        for polygon in polygon_list[1:]:
            try:
                union_polygon: Polygon = union_polygon.union(polygon)
            except:
                pass
        try:
            # 提取边界点
            union_boundary_coords: List[POINT] = list(union_polygon.exterior.coords)
            return union_boundary_coords
        except:
            pass
