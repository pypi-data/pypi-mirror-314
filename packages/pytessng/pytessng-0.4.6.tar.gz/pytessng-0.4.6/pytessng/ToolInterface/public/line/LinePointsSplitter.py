from .LineBase import LineBase
from .LinePointsDivider import LinePointsDivider
from pytessng.Logger import logger


class LinePointsSplitter:
    """ 裁切线段 """
    @staticmethod
    def split_line_by_distance_and_mode(line: list, given_distance: float, mode: int):
        assert len(line) >= 2
        assert mode in [0, 1]  # 0: move start, 1: move end

        START_RATIO = 0.45
        END_RATIO = 0.55

        total_length = LineBase.calculate_line_length(line)

        if given_distance >= total_length:
            logger.logger_pytessng.warning(f"PointsSplitter warning: given_distance {given_distance} is greater than the line's total length {total_length}.")

        if mode == 0:
            given_distance = min(given_distance, total_length * START_RATIO)
        elif mode == 1:
            given_distance = max(total_length - given_distance, total_length * END_RATIO)

        divided_points, divide_infos = LinePointsDivider.divide_line_by_distances(line, [given_distance])
        saved_line = divided_points[1] if mode == 0 else divided_points[0]

        return saved_line, divide_infos[0]

    @staticmethod
    def split_line_by_index_and_ratio(line: list, split_info: tuple, mode: int = 1, reference_point: tuple = None):
        assert len(line) >= 2
        divided_points = LinePointsDivider.divide_line_by_indexes_and_ratios(line, [split_info], [reference_point])
        saved_line = divided_points[1] if mode == 0 else divided_points[0]
        return saved_line


class LinkPointsSplitter:
    @staticmethod
    def split_link(points: list, lanes_points: list, given_distance: float, mode: int) -> (list, list):
        # 分割的路段点位，分割信息
        splitted_points, splitted_info = LinePointsSplitter.split_line_by_distance_and_mode(points, given_distance, mode)
        # 参考点 如果是把头部去掉就是选保留线的起点 如果是把尾部去掉就是选保留线的终点
        reference_point = splitted_points[0] if mode == 0 else splitted_points[-1]
        # 分隔的车道点位
        splitted_lanes_points = [
            {
                "left": LinePointsSplitter.split_line_by_index_and_ratio(lane_points["left"], splitted_info, mode, reference_point),
                "center": LinePointsSplitter.split_line_by_index_and_ratio(lane_points["center"], splitted_info, mode, reference_point),
                "right": LinePointsSplitter.split_line_by_index_and_ratio(lane_points["right"], splitted_info, mode, reference_point),
            }
            for lane_points in lanes_points
        ]
        return splitted_points, splitted_lanes_points
