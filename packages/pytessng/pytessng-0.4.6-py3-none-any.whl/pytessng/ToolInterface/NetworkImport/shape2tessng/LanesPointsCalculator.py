import numpy as np

from ...public.line.LineBase import LineBase
from pytessng.Logger import logger


class LanesPointsCalculator:
    """
    # 计算具有相同点数的车道断点列表
    # calculate_lanes_with_same_points
    # - all_lanes
    # - threshold_length=3
    # - threshold_distance_max=5
    # - threshold_distance_min=1
    # - force=False
    """

    # 对车道起终点之间的距离合理性进行判断
    @staticmethod
    def check_lane_points(all_lanes, threshold_distance_max, threshold_distance_min):
        # 如果该路段只有一条车道
        if len(all_lanes) == 1:
            return True

        # 对每条车道的起点（终点）进行判断，在其他车道中，是否至少有一条车道的起点（终点）与本车道的起点（终点）在一定范围内
        for idx, lane in enumerate(all_lanes):
            start_point = lane[0]
            end_point = lane[-1]

            found_connection_start = False
            found_connection_end = False

            for other_idx, other_lane in enumerate(all_lanes):
                # 不和自己比较
                if idx != other_idx:
                    other_start = other_lane[0]
                    other_end = other_lane[-1]

                    # 判断起点和其他车道的起点是否满足条件
                    distance = LineBase.calculate_distance_between_two_points(start_point, other_start)
                    if distance <= threshold_distance_max:
                        found_connection_start = True

                    # 判断终点和其他车道的终点是否满足条件
                    distance = LineBase.calculate_distance_between_two_points(end_point, other_end)
                    if distance <= threshold_distance_max:
                        found_connection_end = True

                    if found_connection_start and found_connection_end:
                        break

            if not found_connection_start or not found_connection_end:
                logger.logger_pytessng.warning("ShapeWarning: The distance between the starting or ending points of two lanes in a link is too far!")
                return False

        # 车道起终点之间的距离不能过小
        for idx, lane in enumerate(all_lanes):
            start_point = lane[0]
            end_point = lane[-1]

            for other_idx, other_lane in enumerate(all_lanes):
                # 不和自己比较
                if idx != other_idx:
                    other_start = other_lane[0]
                    other_end = other_lane[-1]

                    # 判断起点和其他车道的起点是否满足条件
                    distance = LineBase.calculate_distance_between_two_points(start_point, other_start)
                    if distance < threshold_distance_min:
                        logger.logger_pytessng.warning(f"ShapeWarning: The distance {distance:.1f}m between the starting points of two lanes in a link is too close!")
                        return False

                    # 判断终点和其他车道的终点是否满足条件
                    distance = LineBase.calculate_distance_between_two_points(end_point, other_end)
                    if distance < threshold_distance_min:
                        logger.logger_pytessng.warning(f"ShapeWarning: The distance {distance:.1f}m between the ending points of two lanes in a link is too close!")
                        return False

        return True

    # 检查最长的车道与最短的车道的长度差是否在一定范围内
    @staticmethod
    def check_lane_length(all_lanes, threshold_length):
        lane_lengths = [LineBase.calculate_line_length(lane) for lane in all_lanes]
        min_lane_length = min(lane_lengths)
        max_lane_length = max(lane_lengths)

        if max_lane_length - min_lane_length <= threshold_length:
            return np.mean(lane_lengths)
        else:
            logger.logger_pytessng.warning(f"ShapeWarning: The longest lane is {max_lane_length:.1f}m, and the shortest lane is {min_lane_length:.1f}m.")
            return False

    # 计算每个断点到起点的距离占整个车道长度的比例（%）
    @staticmethod
    def calculate_distance_proportions(one_lane):
        cumulative_distances_to_start = [0]
        for i in range(1, len(one_lane)):
            distance = LineBase.calculate_distance_between_two_points(one_lane[i], one_lane[i - 1])
            cumulative_distances_to_start.append(cumulative_distances_to_start[-1] + distance)
        # 车道总长度
        total_lane_length = cumulative_distances_to_start[-1]

        proportions = [distance / total_lane_length for distance in cumulative_distances_to_start]

        return proportions

    # 计算多条车道的每个断点到起点的距离比例，并合并并去重
    @staticmethod
    def calculate_merged_proportions(all_lanes, mean_length=None):
        merged_proportions = []

        for lane in all_lanes:
            proportions = LanesPointsCalculator.calculate_distance_proportions(lane)
            merged_proportions.extend(proportions)

        # # 使N米一个点
        # new_list = [i/mean_length for i in range(1, int(mean_length), 3)]
        # merged_proportions.extend(new_list)

        # 保留几位小数，去重，排序
        merged_proportions = sorted(list(set([round(num, 4) for num in merged_proportions])))

        return merged_proportions

    # 计算每条车道上相对应比例位置的坐标点
    @staticmethod
    def calculate_interpolated_points(all_lanes, merged_proportions):
        interpolated_lanes_data = []
        for lane in all_lanes:
            interpolated_points = []
            # 每条车道上每个断点到起点的距离比例
            proportions = LanesPointsCalculator.calculate_distance_proportions(lane)
            for proportion in merged_proportions:
                i = 0
                while i < len(proportions) - 1 and proportions[i + 1] < proportion:
                    i += 1
                if proportions[i + 1] == proportions[i]:
                    alpha = 0
                else:
                    alpha = (proportion - proportions[i]) / (proportions[i + 1] - proportions[i])
                interpolated_point = LineBase.calculate_interpolate_point_between_two_points(lane[i], lane[i + 1], alpha)
                interpolated_points.append(interpolated_point)

            interpolated_lanes_data.append(interpolated_points)

        return interpolated_lanes_data

    # 输入多条车道数据，返回有共同断点数量的车道数据
    def calculate_lanes_with_same_points(self, all_lanes, threshold_length=3, threshold_distance_max=5, threshold_distance_min=1, force=False):
        # 检查最长的车道与最短的车道的长度差是否在一定范围内
        mean_length = self.check_lane_length(all_lanes, threshold_length)
        if not mean_length:
            logger.logger_pytessng.warning("ShapeWarning: The difference in length between the longest and shortest lanes exceeds the threshold!")
            if not force:
                return None
            else:
                logger.logger_pytessng.debug("Shape: Forced calculation!")

        # 在其他车道中，是否至少有一条车道的起/终点与本车道的起/终点在一定范围内
        if not self.check_lane_points(all_lanes, threshold_distance_max, threshold_distance_min):
            logger.logger_pytessng.warning("ShapeWarning: The distance between the starting and ending points of a certain lane and those of other lanes is not within a reasonable range!")
            if not force:
                return None
            else:
                logger.logger_pytessng.debug("Shape: Forced calculation!")

        # 计算合并后的距离比例列表
        merged_proportions = self.calculate_merged_proportions(all_lanes)

        # 计算插值后的坐标点
        interpolated_points = self.calculate_interpolated_points(all_lanes, merged_proportions)

        return interpolated_points
