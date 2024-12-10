from typing import List, Dict, Tuple, Union, Optional
from pydantic import BaseModel, validator, root_validator

PointType = Union[Tuple[float, float], Tuple[float, float, float], List[float]]


# 路网属性
class Attrs(BaseModel):
    data_source: str
    created_time: str
    proj_string: str = ""
    move_distance: dict = {"x_move": 0, "y_move": 0}


# 路段
class Link(BaseModel):
    id: str
    points: List[PointType]  # 2D or 3D
    lane_count: int = 0
    lanes_width: List[float] = []
    lanes_points: List[Dict[str, List[PointType]]] = []
    lanes_type: List[str] = []
    limit_speed: float = 0
    name: str = ""

    @validator('points')
    def validate_points(cls, points):
        assert len(points) >= 2, "At least two points are required."
        assert len(set([len(point) for point in points])) == 1, "The number of coordinates for all points should be consistent."
        return points

    @validator('lane_count')
    def validate_lane_count(cls, lane_count):
        assert lane_count >= 1, "There should be at least one lane."
        return lane_count

    @validator('lanes_width')
    def validate_lanes_width(cls, lanes_width):
        assert len(lanes_width) >= 1, "There should be at least one lane."
        return lanes_width

    @validator('lanes_points')
    def validate_lanes_points(cls, lanes_points):
        assert len(lanes_points) >= 1, "There should be at least one lane."
        for lane_points in lanes_points:
            locations = {"left", "center", "right"}
            assert set(lane_points.keys()) == locations
            for single_points in lane_points.values():
                assert len(single_points) >= 2, "At least two points are required."
                assert len(set([len(point) for point in single_points])) == 1, "The number of coordinates for all points should be consistent."
                for i, point in enumerate(single_points):
                    assert len(point) in [2, 3]
                    if len(point) == 2:
                        single_points[i] = tuple(point) + (0,)
        return lanes_points

    @validator('lanes_type')
    def validate_lanes_type(cls, lanes_type):
        assert len(lanes_type) >= 1, "There should be at least one lane."
        # for lane_type in lanes_type:
        #     assert lane_type in {"driving"}
        return lanes_type

    @root_validator
    def check(cls, values: dict):
        id = values.get('id')
        points = values.get('points')
        lane_count = values.get('lane_count')
        lanes_width = values.get('lanes_width')
        lanes_points = values.get('lanes_points')
        lanes_type = values.get('lanes_type')
        # limit_speed = values.get('limit_speed')
        name = values.get('name')

        assert not (lanes_width and lanes_points), "lanes_width 和 lanes_points 两个字段不能同时存在"
        if lane_count:
            if lanes_width:
                assert len(lanes_width) == lane_count, "lanes_width 的长度必须与 lane_count 匹配"
            elif lanes_points:
                assert len(lanes_points) == lane_count, "lanes_points 的长度必须与 lane_count 匹配"
        else:
            assert lanes_width or lanes_points, "必须提供 lanes_width 或 lanes_points 中的一个"
        if lanes_points:
            if len(points[0]) == 2:
                for i, point in enumerate(points):
                    points[i] = tuple(point) + (0,)

        # 车道类型
        if lanes_type:
            actual_lane_count = lane_count or len(lanes_width) or len(lanes_points)
            assert len(lanes_type) == actual_lane_count, "The number of lanes_type is not consistent with data."

        # 路段名称
        if not name:
            values["name"] = id

        return values


# 连接段
class Connector(BaseModel):
    from_link_id: str
    to_link_id: str
    from_lane_numbers: List[int]
    to_lane_numbers: List[int]
    lanes_points: Optional[list] = []
    name: str = ""

    @validator('from_lane_numbers')
    def validate_from_lane_numbers(cls, from_lane_numbers):
        return sorted(from_lane_numbers)

    @validator('to_lane_numbers')
    def validate_to_lane_numbers(cls, to_lane_numbers):
        return sorted(to_lane_numbers)

    @root_validator
    def check(cls, values: dict):
        from_link_id = values.get('from_link_id')
        to_link_id = values.get('to_link_id')
        from_lane_numbers = values.get('from_lane_numbers')
        to_lane_numbers = values.get('to_lane_numbers')
        name = values.get('name')

        # 去重
        unique_mappings = set(zip(from_lane_numbers, to_lane_numbers))
        unique_mappings = sorted(unique_mappings, key=lambda x: x[0])
        from_lane_numbers, to_lane_numbers = zip(*unique_mappings) if unique_mappings else ([], [])
        values["from_lane_numbers"] = sorted(from_lane_numbers)
        values["to_lane_numbers"] = sorted(to_lane_numbers)

        # 连接段名称
        if not name:
            try:
                int(from_link_id)
                int(to_link_id)
                values["name"] = f"{from_link_id}-{to_link_id}"
            except:
                values["name"] = ""

        return values


# 车辆组成
class VehicleComposition(BaseModel):
    id: str
    vehi_type_code_list: List[int]
    vehi_type_ratio_list: List[float]
    # vehi_type_speed_list: List[float] = []

    @root_validator
    def check(cls, values: dict):
        vehi_type_code_list = values.get('vehi_type_code_list')
        vehi_type_ratio_list = values.get('vehi_type_ratio_list')
        assert len(vehi_type_code_list) == len(vehi_type_ratio_list), "vehi_type_code_list 和 vehi_type_ratio_list 的长度必须一致"
        return values


# 发车点
class VehicleInput(BaseModel):
    id: str
    link_id: str
    vehicle_compose_id: str
    volumes: List[int]
    durations: List[int]

    @root_validator
    def check(cls, values: dict):
        volumes = values.get('volumes')
        durations = values.get('durations')
        assert len(volumes) == len(durations), "volumes 和 durations 的长度必须一致"
        return values


# 信号相位
class SignalPhase(BaseModel):
    id: str
    name: str = ""
    colors: List[str] = ['红', '绿', '黄', '红']
    durations: List[int]

    @root_validator
    def check(cls, values: dict):
        colors = values.get('colors')
        durations = values.get('durations')
        assert len(colors) == len(durations), "colors 和 durations 的长度必须一致"

        # 排除时长为0的部分
        colors = [color for color, duration in zip(colors, durations) if duration > 0]
        durations = [duration for duration in durations if duration > 0]
        values["colors"] = colors
        values["durations"] = durations

        # 相位名称
        id = values.get('id')
        name = values.get('name')
        if not name:
            values["name"] = id

        return values


# 信号灯组
class SignalGroup(BaseModel):
    id: str
    name: str = ""
    cycle_time: int
    phases: List[SignalPhase]
    duration: int = 24 * 3600

    @root_validator
    def check(cls, values: dict):
        cycle_time = values.get('cycle_time')
        phases = values.get('phases')
        for phase in phases:
            durations = phase.durations
            all_time = sum(durations)
            assert all_time == cycle_time, "相位总时间必须等于周期时间"

        # 灯组名称
        id = values.get('id')
        name = values.get('name')
        if not name:
            values["name"] = id

        return values


# 信号灯头
class SignalHead(BaseModel):
    id: str
    phase_id: str
    dist: float = -1
    # 组合1
    link_id: str = "0"
    to_link_id: str = "0"
    lane_number: int = 0
    to_lane_number: int = 0
    lane_number_is_from_right: bool = True  # 默认从右向左
    # 组合2
    lane_id: str = "0"
    to_lane_id: str = "0"


# 决策点
class DecisionPoint(BaseModel):
    id: str
    link_id: str
    dist: float
    routings: List[List]
    ratios: List[float]
    duration: int = 24 * 3600

    @root_validator
    def check(cls, values: dict):
        routings = values.get('routings')
        ratios = values.get('ratios')
        assert len(routings) == len(ratios), "The length of routing and ratios must be consistent."
        return values


# 减速区
class ReducedSpeedArea(BaseModel):
    id: str
    speed: int
    link_id: str
    lane_number: int
    to_lane_number: int = -1
    dist: float
    length: float
    from_time: int = 0
    to_time: int = 24 * 3600


# 导向箭头
class GuidArrow(BaseModel):
    lane_id: str
    turn_arrow_type: int
    dist_to_end: float = 10
    length: float = 6
