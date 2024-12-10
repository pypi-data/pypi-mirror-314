import collections
import numpy as np
from typing import Dict, List
from PySide2.QtGui import QVector3D

from pytessng.Logger import logger
from pytessng.Config import NetworkImportConfig


LANE_TYPE_MAPPING = NetworkImportConfig.LANE_TYPE_MAPPING
WIDTH_LIMIT = NetworkImportConfig.OpenDrive.WIDTH_LIMIT
POINT_REQUIRE = NetworkImportConfig.OpenDrive.POINT_REQUIRE
max_length = NetworkImportConfig.OpenDrive.max_length

sceneScale = 1

def p2m(x):
    return x * sceneScale

def m2p(x):
    return x / sceneScale


def get_section_childs(section_info: Dict, lengths: List, direction: str) -> List[Dict]:
    """
        处理某 Section 某方向的路网信息
        根据二维信息以及自定义配置，将section 进行再次处理，将宽度过窄的车道所在的路段打断，分配合适的连接段或者抹除车道
    Args:
        section_info:
        lengths: 因为分段时，以road作为最小单位，所以需要提供此 section 对应的长度断点序列
        direction: 沿参考线方向

    Returns:
        被处理后的 小路段列表
    """
    # 分为左右车道，同时过滤tess规则下不同的车道类型
    if direction == 'left':
        lane_ids = [lane_id for lane_id in section_info['lanes'].keys() if
                    lane_id > 0 and lane_id in section_info["tess_lane_ids"]]
    else:
        lane_ids = [lane_id for lane_id in section_info['lanes'].keys() if
                    lane_id < 0 and lane_id in section_info["tess_lane_ids"]]
    # 路段遍历，获取link段，处理异常点
    point_infos = []
    # 查找连接段
    for index, length in enumerate(lengths):
        point_info = {
            'lanes': {},
            'is_link': True,
        }
        for lane_id in lane_ids:
            lane_info = section_info['lanes'][lane_id]
            tess_lane_type = LANE_TYPE_MAPPING.get(lane_info['type'])
            if tess_lane_type not in WIDTH_LIMIT.keys() or lane_info['widths'][index] > \
                    WIDTH_LIMIT[tess_lane_type]['split']:
                point_info['lanes'][lane_id] = lane_info['type']  # 无宽度限制或者宽度足够，正常车道
            elif lane_info['widths'][index] > WIDTH_LIMIT[tess_lane_type]['join']:
                point_info['lanes'][lane_id] = lane_info['type']  # 宽度介于中间，作为连接段
                point_info['is_link'] = False
            # 否则，不加入车道列表
        point_infos.append(point_info)

    # 连续多个点的信息完全一致，可作为同一路段
    childs = []
    child_point = []
    start_index = None  # 分片时，start_index 为None 会视为0
    for index in range(len(lengths)):
        if len(child_point) == 1:
            start_index = index - 1
        point_info = point_infos[index]
        if index < POINT_REQUIRE:  # 首尾必须为link
            child_point.append(point_infos[0])
        elif len(lengths) - index - 1 < POINT_REQUIRE:
            child_point.append(point_infos[-1])
        elif not child_point:  # 原列表为空
            if point_info['is_link']:
                child_point.append(point_info)
            else:
                continue
        else:  # 原列表不为空
            if point_info == child_point[0]:
                child_point.append(point_info)
            elif len(child_point) >= POINT_REQUIRE:
                childs.append(
                    {
                        'start': start_index,
                        'end': index,
                        'lanes': set(child_point[0]['lanes'].keys()) & set(child_point[0]['lanes'].keys()),
                    }
                )
                child_point = []
            else:
                continue

    # 把最后一个存在的点序列导入, 最后一个应该以末尾点为准,但是如果此处包含了首&尾，应该取数据量的交集
    # 这样可能会丢失部分路段，所以在建立连接段时，必须确保 from_lane, to_lane 均存在
    childs.append(
        {
            'start': start_index,
            'end': len(lengths) - 1,
            'lanes': set(child_point[0]['lanes'].keys()) & set(child_point[0]['lanes'].keys())
        }
    )
    # lengths 只是断点序列，标记着与起始点的距离,反向用了同样的lengths
    # 得到link的列表,因为lane的点坐标与方向有关，所以此时的child已经根据方向排序
    return childs


def get_inter(string: str, roads_info: Dict) -> List:
    """
        根据 opendrive2lanelet 中定义的的车道名判断此车道的合法性，并返回相应的的 road_id,section_id,lane_id, -1
    Args:
        string: 车道名
        roads_info: 路段信息字典

    Returns:
        车道名是否合法，车道名的详细信息
    """
    inter_list = []
    is_true = True
    for i in string.split('.'):
        try:
            inter_list.append(int(i))
        except:
            inter_list.append(None)
            is_true = False

    # 检查 前后续路段 是否存在,不存在可以忽略
    if inter_list[0] not in roads_info.keys():
        is_true = False
    return [is_true, *inter_list]


def connect_childs(links: list, connector_mapping: Dict) -> None:
    """
        因为在section内对过窄车道进行了优化处理，所以可能将section切分成了多个link，需要为每个link在内部建立连接关系
    Args:
        links: section内 同方向子link 顺序列表
        connector_mapping: 全局的路段连接关系表

    Returns:
        无返回值，但路段连接关系表被扩充
    """
    for index in range(len(links) - 1):
        from_link_info = links[index]
        to_link_info = links[index + 1]
        from_link = from_link_info['link']
        to_link = to_link_info['link']
        if not (from_link and to_link and from_link_info['lane_ids'] and to_link_info['lane_ids']):
            continue

        actionTypeMapping = collections.defaultdict(lambda: {"from": set(), 'to': set()})
        for lane_id in from_link_info['lane_ids']:
            actionTypeMapping[from_link_info[lane_id].actionType()]['from'].add(lane_id)
        for lane_id in to_link_info['lane_ids']:
            actionTypeMapping[to_link_info[lane_id].actionType()]['to'].add(lane_id)

        connect_lanes = set()
        for actionType, lanes_info in actionTypeMapping.items():
            for lane_id in set(lanes_info['from'] | lanes_info['to']):
                # 车道原始编号相等，取原始编号对应的车道，否则，取临近车道(lane_ids 是有序的，所以临近车道永远偏向左边区)
                # 因为进行过自优化(人为打断与合并)，可能会导致前后失去连接关系，需要注意
                from_lane_id = min(lanes_info['from'], key=lambda x: abs(x - lane_id)) if lanes_info[
                    'from'] else None
                to_lane_id = min(lanes_info['to'], key=lambda x: abs(x - lane_id)) if lanes_info['to'] else None

                from_lane = from_link_info.get(from_lane_id)
                to_lane = to_link_info.get(to_lane_id)
                if from_lane and to_lane:
                    connect_lanes.add((from_lane.number() + 1, to_lane.number() + 1))

        if connect_lanes:
            connector_mapping[f"{from_link.id()}-{to_link.id()}"]['lFromLaneNumber'] += [i[0] for i in
                                                                                         connect_lanes]
            connector_mapping[f"{from_link.id()}-{to_link.id()}"]['lToLaneNumber'] += [i[1] for i in connect_lanes]
            connector_mapping[f"{from_link.id()}-{to_link.id()}"]['lanesWithPoints3'] += [None for _ in
                                                                                          connect_lanes]
            connector_mapping[f"{from_link.id()}-{to_link.id()}"]['infos'] += []


# 计算两向量间的夹角
def cal_angle_of_vector(v0, v1, is_use_deg=True):
    dot_product = np.dot(v0, v1)
    v0_len = np.linalg.norm(v0)
    v1_len = np.linalg.norm(v1)
    try:
        angle_rad = np.arccos(dot_product / (v0_len * v1_len))
    except ZeroDivisionError as error:
        return None

    if is_use_deg:
        return np.rad2deg(angle_rad)
    return angle_rad


# 根据前后两点坐标绘制向量
def get_vector(start_point, end_point):
    # return np.array([end_point[index] - start_point[index] for index in range(3)])
    return np.array(end_point) - np.array(start_point)


# 根据角度限制整合中心点，减少绘制路网时的点数
def get_new_point_indexs(center_points, angle):
    new_point_indexs = [0, 1]  # 前两个点是基础
    for index, point in enumerate(center_points[2:-1]):
        real_index = index + 2  # 在 center_points 中的真实索引

        point_0 = center_points[new_point_indexs[-2]]
        point_1 = center_points[new_point_indexs[-1]]
        point_2 = point

        vector_1 = get_vector(point_0, point_1)
        vector_2 = get_vector(point_0, point_2)

        included_angle = cal_angle_of_vector(vector_1, vector_2)
        point_distance = np.sqrt(np.sum((np.array(point_2) - np.array(point_1)) ** 2))

        # 如果两向量夹角变化不大，抹除观测点(不能用连续的两个点比较,即 01 对比 12，容易对缓慢变化的路段判断错误)
        if included_angle is None or included_angle >= angle:
            new_point_indexs.append(real_index)
        # 如果观测点距离上一点过远，且存在角度差异，也不会抹除，不加这个可能会把微小的角度误差放大到明显的地步
        elif point_distance >= max_length and included_angle > 0:
        # elif point_distance >= max_length:  # 存在微小角度偏差的路段 可能会漫延很长
            new_point_indexs.append(real_index)
        else:
            pass
    # 最后一个点需添加
    if len(center_points) - 1 > new_point_indexs[-1]:
        new_point_indexs.append(len(center_points) - 1)

    def is_remove_index_1(center_points, new_point_indexs):
        if len(new_point_indexs) < 3:
            # 只有两个点，无法缩减
            return False
        point_0 = center_points[new_point_indexs[0]]
        point_1 = center_points[new_point_indexs[1]]
        point_2 = center_points[new_point_indexs[2]]

        vector_1 = get_vector(point_0, point_1)
        vector_2 = get_vector(point_0, point_2)

        included_angle = cal_angle_of_vector(vector_1, vector_2)

        # 距离取较小值
        point_distance = np.sqrt(np.sum((np.array(point_1) - np.array(point_0)) ** 2))

        # 如果两向量夹角变化不大，抹除观测点(不能用连续的两个点比较,即 01 对比 12，容易对缓慢变化的路段判断错误)
        if included_angle is None or included_angle >= angle:
            return False
        # 如果观测点距离上一点过远，且存在角度差异，也不会抹除，不加这个可能会把微小的角度误差放大到明显的地步
        elif point_distance >= max_length and included_angle > 0:
            # elif point_distance >= max_length:  # 存在微小角度偏差的路段 可能会蔓延很长
            return False
        else:
            return True

    if is_remove_index_1(center_points, new_point_indexs):
        del new_point_indexs[1]
    return new_point_indexs



# =====================================
# 处理过短连接段

def qtpoint2point(qt_points):
    points = []
    for qt_point in qt_points:
        x = p2m(qt_point.x())
        y = -p2m(qt_point.y())
        z = p2m(qt_point.z())
        points.append([round(x,2), round(y,2), round(z,2)])
    return points


def get_coo_list(vertices):
    list1 = []
    for index in range(0, len(vertices), 1):
        vertice = vertices[index]
        # list1.append(QPointF(m2p((vertice[0])), m2p(-(vertice[1]))))
        list1.append(QVector3D(m2p((vertice[0])), m2p(-(vertice[1])), m2p(vertice[2])))
    if len(list1) < 2:
        raise 3
    return list1


def calculate_section_length(p1, p2):
    dp = np.array(p1) - np.array(p2)
    return np.linalg.norm(dp[:2])

def interpolate_point_on_segment(p1, p2, t):
    return p1 + t * (p2 - p1)

def split_line(line, given_distance, mode):
    total_length = np.sum([calculate_section_length(line[i - 1], line[i]) for i in range(1, len(line))])

    if given_distance >= total_length:
        logger.logger_pytessng.warning(f"OpenDriveWarning: given_distance {given_distance} is greater than the line's total length {total_length}.")

    if mode == "start":
        given_distance = min(given_distance, total_length*0.2)
    elif mode == "end":
        given_distance = max(total_length - given_distance, total_length*0.8)

    all_length = 0
    for i in range(1, len(line)):
        p1 = np.array(line[i - 1])
        p2 = np.array(line[i])
        section_length = calculate_section_length(p1, p2)
        all_length += section_length

        if all_length < given_distance:
            continue
        elif all_length == given_distance:
            line1 = line[:i + 1]
            line2 = line[i:]
            info = (i, None)
            break
        else:
            before_length = all_length - section_length
            ratio = round((given_distance - before_length) / section_length, 3)
            cut_point = interpolate_point_on_segment(p1, p2, ratio)
            line1 = line[:i] + [cut_point.tolist()]
            line2 = [cut_point.tolist()] + line[i:]
            info = (i-1, ratio)
            break

    if mode == "start":
        line = line2
    elif mode == "end":
        line = line1
    return line, info

def split_line_2(line, info, mode):
    index, ratio = info

    if ratio is None:
        line1 = line[:index + 1]
        line2 = line[index:]
    else:
        p1 = np.array(line[index])
        p2 = np.array(line[index+1])
        cut_point = interpolate_point_on_segment(p1, p2, ratio)
        line1 = line[:index+1] + [cut_point.tolist()]
        line2 = [cut_point.tolist()] + line[index+1:]

    if mode == "start":
        return_line = line2
    elif mode == "end":
        return_line = line1
    return return_line
