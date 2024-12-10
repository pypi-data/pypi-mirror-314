import numpy as np


class LaneNumbersSorter:
    @staticmethod
    def sort_lane_number(lanes_points: list) -> list:
        # 找到一条车道作为基准车道
        base_lane = lanes_points[0]

        # 如果大于等于三个点，就用第二个点和第三个点；否则就用第一个点和第二个点
        if len(base_lane) >= 3:
            num_last, num_next = 1, 2
        else:
            num_last, num_next = 0, 1

        # 计算基准车道的方向向量，使用前两个点
        base_direction = np.array(base_lane[num_next]) - np.array(base_lane[num_last])

        # 计算基准车道的旋转角度（逆时针方向）
        angle_to_rotate = np.arctan2(base_direction[0], base_direction[1])

        # 使用旋转矩阵将所有车道旋转到指向y正轴
        rotation_matrix = np.array(
            [[np.cos(angle_to_rotate), -np.sin(angle_to_rotate)],
            [np.sin(angle_to_rotate), np.cos(angle_to_rotate)]]
        )

        # 获取旋转后的各车道第一个点的x坐标
        x_coordinates = [
            np.dot(rotation_matrix, np.array(lane[num_last][:2]))[0]
            for lane in lanes_points
        ]

        # 获取车道索引，从右向左，从1开始
        sorted_indices = len(x_coordinates) - np.argsort(np.argsort(x_coordinates))

        return list(sorted_indices)
