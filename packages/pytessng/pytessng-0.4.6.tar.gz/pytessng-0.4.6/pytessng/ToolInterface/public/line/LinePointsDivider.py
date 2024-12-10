from typing import List

from .LineBase import LineBase


class LinePointsDivider:
    """ 分割路段 """
    # 通过给定的距离列表，将线段分割成若干段
    @staticmethod
    def divide_line_by_distances(line: list, given_distance_list: list) -> (list, list):
        assert len(line) >= 2

        given_distance_list = sorted(given_distance_list)
        assert len(given_distance_list) > 0

        total_length = LineBase.calculate_line_length(line)
        assert given_distance_list[0] > 0 and given_distance_list[-1] < total_length

        # 保留小数的位数
        precision = len(str(int(total_length)))

        all_length = 0
        all_points = [(line[0], False)]
        divide_infos = []
        last_index = -1
        index = 1
        k = 0

        while True:
            if index >= len(line):
                break

            p1, p2 = line[index - 1], line[index]
            dist = given_distance_list[k] if k < len(given_distance_list) else 1e6

            section_length = LineBase.calculate_distance_between_two_points(p1, p2)
            if index != last_index:
                all_length += section_length
                last_index = index

            if all_length < dist:
                if p2 not in [v[0] for v in all_points]:
                    all_points.append((p2, False))
                index += 1
            elif all_length == dist:
                all_points.append([p2, True])
                divide_infos.append([index, None])
                k += 1
            else:
                before_length = all_length - section_length
                ratio = round((dist - before_length) / section_length, precision)
                assert 0 <= ratio <= 1
                cut_point = LineBase.calculate_interpolate_point_between_two_points(p1, p2, ratio)
                all_points.append([cut_point, True])
                if ratio == 0:
                    divide_infos.append([index - 1, None])
                elif ratio == 1:
                    divide_infos.append([index, None])
                else:
                    divide_infos.append([index - 1, ratio])
                k += 1

        divided_points = [[], ]
        for p, flag in all_points:
            divided_points[-1].append(p)
            if flag:
                divided_points.append([p])

        return divided_points, divide_infos

    # 通过给定的索引列表和比例列表，将线段分割成若干段
    @staticmethod
    def divide_line_by_indexes_and_ratios(line: list, divide_infos: list, reference_points: list = None) -> list:
        assert len(line) >= 2
        if reference_points:
            assert len(divide_infos) == len(reference_points)
            # 用垂足
            algorithm = 1
        else:  # 为空或为None
            # 用比例
            algorithm = 2

        # 全部的点
        all_points: List[list] = []
        # 处理第一个点
        all_points.append([line[0], False])
        # 还没加进去的最小值
        max_index: int = 1

        # 分割
        for i in range(len(divide_infos)):
            # 索引和比例
            index, ratio = divide_infos[i]
            assert ratio is None or (0 < ratio < 1), f"{ratio}"

            # 参考点
            reference_point = reference_points[i] if algorithm == 1 else None

            # 添加之前的点
            for j in range(max_index, index + 1):
                all_points.append([line[j], False])
            max_index: int = max(index + 1, max_index)

            # 分割点
            if ratio is None:
                all_points[-1][1] = True

            else:
                p1 = line[index]
                p2 = line[index + 1]

                # 计算分割点
                if algorithm == 1:
                    # 计算直线系数
                    line_coeff = LineBase.calculate_line_coefficients(p1, p2)
                    # 计算垂足点
                    cut_point = LineBase.calculate_perpendicular_foot_of_point_to_line(line_coeff, reference_point)
                else:
                    # 用比例计算
                    cut_point = LineBase.calculate_interpolate_point_between_two_points(p1, p2, ratio)

                all_points.append([cut_point, True])
        else:
            # 添加剩余的点
            for j in range(max_index, len(line)):
                all_points.append([line[j], False])

        # 按照分割点的标记把线段分成多段
        divided_points = [[], ]
        for p, flag in all_points:
            divided_points[-1].append(p)
            if flag:
                divided_points.append([p])

        return divided_points


class LinkPointsDivider:
    @staticmethod
    def divide_link(points: list, lanes_points: list, given_distance_list: list) -> (list, list):
        # 分割的路段点位，分割信息
        divided_points, divide_infos = LinePointsDivider.divide_line_by_distances(points, given_distance_list)

        # 参考点列表
        reference_points: list = [points[-1] for points in divided_points[:-1]]

        # 分割的车道点位
        temp_lanes_points = [
            {
                "left": LinePointsDivider.divide_line_by_indexes_and_ratios(lane_points["left"], divide_infos, reference_points),
                "center": LinePointsDivider.divide_line_by_indexes_and_ratios(lane_points["center"], divide_infos, reference_points),
                "right": LinePointsDivider.divide_line_by_indexes_and_ratios(lane_points["right"], divide_infos, reference_points),
            }
            for lane_points in lanes_points
        ]

        divided_lanes_points = [
            [
                {
                    "left": lane_points["left"][number],
                    "center": lane_points["center"][number],
                    "right": lane_points["right"][number],
                }
                for lane_points in temp_lanes_points
            ]
            for number in range(len(divided_points))
        ]

        return divided_points, divided_lanes_points
