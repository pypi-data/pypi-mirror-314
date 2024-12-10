import numpy as np

from .LineBase import LineBase


class LinePointsShifter:
    """计算向[左]偏移一定距离的线段"""
    @staticmethod
    def shift_single_line_to_left(first_point: tuple, second_point: tuple, width: float) -> (tuple, tuple):
        # 获取坐标
        x1, y1 = first_point
        x2, y2 = second_point
        # 计算法向量的分量
        nx = -(y2 - y1)
        ny = x2 - x1
        # 计算法向量的长度
        length = np.sqrt(nx ** 2 + ny ** 2)
        # 计算单位法向量
        ux = nx / length
        uy = ny / length
        # 计算偏移后的点坐标
        new_first_point = (x1 + ux * width, y1 + uy * width)
        new_second_point = (x2 + ux * width, y2 + uy * width)
        return new_first_point, new_second_point

    # 计算向[左]偏移一定距离的多义线
    @staticmethod
    def shift_line_to_left(lines: list, width: float) -> list:
        if len(lines) < 2:
            raise Exception("Too less points count!")

        shift_lines = []
        for i in range(1, len(lines)):
            # 获取偏移线段
            new_first_point, new_second_point = LinePointsShifter.shift_single_line_to_left(lines[i - 1], lines[i], width)
            # 计算多义线偏移
            if i == 1:
                shift_lines.append(new_first_point)
                line_coeff = LineBase.calculate_line_coefficients(new_first_point, new_second_point)
            else:
                last_line_coeff = line_coeff
                line_coeff = LineBase.calculate_line_coefficients(new_first_point, new_second_point)
                new_point = LineBase.calculate_intersection_point_from_two_lines(last_line_coeff, line_coeff, new_first_point)
                shift_lines.append(new_point)
            if i == len(lines) - 1:
                shift_lines.append(new_second_point)

        return shift_lines
