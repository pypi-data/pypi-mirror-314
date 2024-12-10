from math import ceil, sqrt


# 根据左右点序列创建三角形
def create_curve(left_points, right_points, split=False) -> list:
    triangles = []
    for i in range(len(left_points) - 1):  # 两两组合，最后一个不可作为首位
        # 断线时，需要细分路段，做到步长均匀
        # 虚线受步长(断点列表)和虚实比例影响，需要额外处理
        # if split and index % 10 in [0, 1, 2, 3]:
        #     # 断线 3:2 虚线长度由步长和比例共同控制
        #     continue

        left_start, left_end = left_points[i], left_points[i + 1]
        right_start, right_end = right_points[i], right_points[i + 1]

        triangle1 = [left_start, left_end, right_start]
        triangle2 = [left_end, right_end, right_start]

        triangles.append(triangle1)
        triangles.append(triangle2)

    return triangles


def deviation_point(coo1, coo2, width, right=False, is_last=False):
    # 记录向左向右左右偏移
    sign = 1 if right else -1
    x1, y1, z1 = coo1
    x2, y2, z2 = coo2

    # 如果是最后一个点，取第二个点做偏移
    x_base, y_base, z_base = coo1 if not is_last else coo2

    dx, dy = x2 - x1, y2 - y1
    # 分母为0，直接返回基准点
    if dx == 0 and dy == 0:
        return [x_base, y_base, z_base]

    dist = sqrt(dx ** 2 + dy ** 2)
    X = x_base + sign * width * dy / dist
    Y = y_base + sign * width * -dx / dist

    return [X, Y, z_base]


def calc_boundary(base_points, border_line_width):
    left_points, right_points = [], []
    point_count = len(base_points)

    for index in range(point_count):
        is_last = True if index + 1 == point_count else False
        num = index - 1 if index + 1 == point_count else index
        left_point = deviation_point(base_points[num], base_points[num + 1], border_line_width / 2, right=False, is_last=is_last)
        right_point = deviation_point(base_points[num], base_points[num + 1], border_line_width / 2, right=True, is_last=is_last)
        left_points.append(left_point)
        right_points.append(right_point)

    return left_points, right_points


def xyz2xzy(array):
    return [array[0], array[2], array[1]]


def chunk(lst, size):
    num_chunks = ceil(len(lst) / size)
    return [lst[i * size:(i + 1) * size] for i in range(num_chunks)]
