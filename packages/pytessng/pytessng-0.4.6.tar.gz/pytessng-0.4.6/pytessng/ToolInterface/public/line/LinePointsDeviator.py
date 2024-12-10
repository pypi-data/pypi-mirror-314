import numpy as np


# 根据中心点向左右偏移
class LinePointsDeviator:
    @staticmethod
    def deviate_point(coo1, coo2, width: float, right=False, is_last=False):
        signl = 1 if right else -1  # 记录向左向右左右偏移
        x1, y1, z1, x2, y2, z2 = list(coo1) + list(coo2)  # 如果是最后一个点，取第二个点做偏移
        x_base, y_base, z_base = (x1, y1, z1) if not is_last else (x2, y2, z2)
        if not ((x2 - x1) or (y2 - y1)):  # 分母为0
            return [x_base, y_base, z_base]
        X = x_base + signl * width * (y2 - y1) / np.sqrt(np.square(x2 - x1) + np.square((y2 - y1)))
        Y = y_base + signl * width * (x1 - x2) / np.sqrt(np.square(x2 - x1) + np.square((y2 - y1)))
        return [X, Y, z_base]

    @staticmethod
    def deviate_points(base_points: list, move_parameters: dict):
        """
        Args:
            base_points:
            move_parameters:     {
            "right": ['right', 4],
            "center": ['right', 2],
            "left": ['right', 0],
        }
        根据基础点序列，及偏移方向和偏移量进行偏移(['right', 4])
        Returns:

        """
        points = {
            "right": [],
            "center": [],
            "left": [],
        }
        point_count = len(base_points)
        for index in range(point_count):
            if index + 1 == point_count:
                is_last = True
                num = index - 1
            else:
                is_last = False
                num = index

            for position, parameter in move_parameters.items():  # 左/中/右
                direction, width = parameter
                point = LinePointsDeviator.deviate_point(
                    base_points[num],
                    base_points[num + 1],
                    width,
                    right=(direction == 'right'),
                    is_last=is_last
                )
                points[position].append([point[0], point[1], base_points[index][2]])
        return points
