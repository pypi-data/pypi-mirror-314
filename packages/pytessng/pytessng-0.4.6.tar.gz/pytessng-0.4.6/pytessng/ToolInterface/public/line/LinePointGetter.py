from .LineBase import LineBase
from pytessng.Logger import logger


class LinePointGetter:
    """ 根据距离计算线上的点的位置 """
    @staticmethod
    def get_point_by_dist(line: list, target_distance: float) -> list:
        target_location = []

        if target_distance < 0:
            logger.logger_pytessng.warning(f"LinkPointGetter waring 1: [target_distance: {target_distance}]")
            return target_location

        current_distance = 0.0
        for i in range(len(line) - 1):
            current_point = line[i]
            next_point = line[i + 1]
            segment_distance = LineBase.calculate_distance_between_two_points(current_point, next_point)

            if current_distance + segment_distance >= target_distance:
                t = (target_distance - current_distance) / segment_distance
                target_location = LineBase.calculate_interpolate_point_between_two_points(current_point, next_point, t)
                break

            current_distance += segment_distance

        # 超出范围
        if target_location == []:
            logger.logger_pytessng.warning(f"LinePointGetter waring 2: [current_distance: {current_distance:.3f}] [target_distance: {target_distance:.3f}]")
            if abs(target_distance - current_distance) <= 2:
                target_location = line[-1]

        return target_location
