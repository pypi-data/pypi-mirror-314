import math
import numpy as np
from .utils import clockwise_angle

from pytessng.Config import NetworkExportConfig
from pytessng.ToolInterface.public.line.LinePointsSimplifier import LinePointsSimplifier


class BaseRoad:
    # Road_id = 1

    def __init__(self, qtpoint2point):
        # self.id = BaseRoad.Road_id
        # BaseRoad.Road_id += 1

        # 中心车道
        self.lanes = [
            {
                'width': [],
                'type': 'none',
                'id': 0,
                'direction': 'center',
                'lane': None,
            }
        ]

        self.qtpoint2point = qtpoint2point
        self.road_length = None

    # 参考线计算
    def calc_geometry_line(self, points, simplify_distance=0.3):
        """
        根据左边界线计算参考线
        Args:
            points: 点位坐标序列
            simplify_distance: 简化距离

        Returns:

        """
        # 直线型的参考线必须允许简化，否则点位容易过多
        selected_index = LinePointsSimplifier.simplify_points(points, simplify_distance)
        points = [points[i] for i in selected_index]

        # 为简化计算，每路段只有一 section/dirction/
        geometrys = []
        s = 0
        for index in range(len(points) - 1):
            # 计算参考线段落
            start_point, end_point = points[index], points[index + 1]
            x, y = start_point[0], start_point[1]
            hdg = math.atan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
            length = np.linalg.norm(np.array(start_point[:2]) - np.array(end_point[:2]))
            geometrys.append(
                Curve(s=s, x=x, y=y, hdg=hdg, length=length, lineType='line')  # 也是直线
            )
            s += length

        self.road_length = s
        return geometrys, s

    def calc_geometry_paramPoly3(self, points):
        """
            曲线的参考线计算(三次多项式拟合)
        Args:
            points:

        Returns:

        """
        from .fit import fit
        s = 0
        for index in range(len(points) - 1):
            # 计算参考线段落
            start_point, end_point = points[index], points[index + 1]
            length = np.linalg.norm(np.array(start_point[:2]) - np.array(end_point[:2]))
            s += length
        r_squared, a0, a1, a2, a3, b0, b1, b2, b3 = fit(points)
        hdg = 0
        geometrys = [Curve(**{"aU": a0, "bU": a1, "cU": a2, "dU": a3, "aV": b0, "bV": b1, "cV": b2, "dV": b3,
                              "s": 0, "x": points[0][0], 'y': points[0][1], "hdg": hdg, "length": s, "lineType": "paramPoly3", })]
        # print(f"拟合结果: {r_squared}")
        self.road_length = s
        return geometrys, s

    def calc_elevation(self, points):
        """
        计算 高程曲线列表，含自动简化,必须和参考线用相同序列断点，否则总长度不一致，高程会有误差
        """
        elevations = []
        s = 0
        for index in range(len(points) - 1):
            start_point, end_point = points[index], points[index + 1]
            start_height, end_height = start_point[2], end_point[2]

            distance = np.linalg.norm(np.array(start_point[:2]) - np.array(end_point[:2]))

            a = start_height
            b = round((end_height - start_height) / distance, 3)  # 高程要保持较高精度

            # 如果当前段落斜率和上一段一致，可以进行合并
            if elevations and elevations[-1].b == b:
                # 更新起始位置(s)及起点高程(a)
                elevations.append(Curve(s=elevations[-1].s, a=elevations[-1].a, b=b, c=0, d=0, lineType='line'))  # 直线段 c=0, d=0
                # 移除上一个元素
                elevations.pop()
            else:
                elevations.append(Curve(s=s, a=a, b=b, c=0, d=0, lineType='line'))  # 直线段 c=0, d=0
            s += distance

        # 为了避免车道长度和参考线不一样，需要进行 s 重置
        if s:
            scale = self.road_length / s
            for elevation in elevations:
                elevation.s = elevation.s * scale
        return elevations

    def calc_deviation_curves(self, qt_left_points, qt_right_points, selected_index=None, calc_singal=False):
        """
        计算车道宽度，含自动简化
        Args:
            qt_left_points:
            qt_right_points:
            selected_index:
            calc_singal:

        Returns:

        """
        left_points = self.qtpoint2point(qt_left_points)
        right_points = self.qtpoint2point(qt_right_points)
        if selected_index:
            left_points = [left_points[i] for i in selected_index]
            right_points = [right_points[i] for i in selected_index]

        deviation_curves = []
        # 车道宽度计算，以左侧车道为基础，向右偏移（向 tessng 看齐）,假设所有车道宽度线性变化
        sOffset = 0
        for index in range(len(left_points) - 1):
            left_start_point, left_end_point = left_points[index], left_points[index + 1]
            right_start_point, right_end_point = right_points[index], right_points[index + 1]

            # 向左偏移为正，向右偏移为负
            geometry_vector = Vector(start_point=left_start_point, end_point=left_end_point)
            start_deviation_vector = Vector(start_point=left_start_point, end_point=right_start_point)
            end_deviation_vector = Vector(start_point=left_end_point, end_point=right_end_point)

            # 计算向量夹角 角度在 -pi ~ 0 以内
            start_signal = np.sign(clockwise_angle(geometry_vector, start_deviation_vector))
            end_signal = np.sign(clockwise_angle(geometry_vector, end_deviation_vector))

            # 起终点宽度及行进距离, 此处宽度算有问题, 不应该用相应成对点的距离作为宽度, 有可能发生两点不垂直于中心线, 这样算出的宽度偏大
            start_deviation_distance = (np.linalg.norm(
                np.array(right_start_point[:2]) - np.array(left_start_point[:2]))) * start_signal * -1
            end_deviation_distance = (np.linalg.norm(
                np.array(right_end_point[:2]) - np.array(left_end_point[:2]))) * end_signal * -1
            forward_distance = np.linalg.norm(np.array(left_end_point[:2]) - np.array(left_start_point[:2]))

            a = round(start_deviation_distance, 2)
            b = round((end_deviation_distance - start_deviation_distance) / forward_distance, 2)

            # 如果当前段落斜率和上一段一致，可以进行合并
            if deviation_curves and deviation_curves[-1].b == b:
                # 更新起始位置(s)及起点宽度(a)
                deviation_curves.append(Curve(sOffset=deviation_curves[-1].sOffset, a=deviation_curves[-1].a, b=b, c=0, d=0, lineType='line'))  # 直线段 c=0, d=0
                # 移除上一个元素
                deviation_curves.pop()
            else:
                deviation_curves.append(Curve(sOffset=sOffset, a=a, b=b, c=0, d=0, lineType='line'))  # 直线段 c=0, d=0
            sOffset += forward_distance

        # 为了避免车道长度和参考线不一样，需要进行 s 重置
        if sOffset:
            scale = self.road_length / sOffset
            for deviation_curve in deviation_curves:
                deviation_curve.sOffset = deviation_curve.sOffset * scale
        return deviation_curves

        #     # 如果当前段落斜率和上一段一致，可以进行合并
        #     if deviation_curves and deviation_curves[-1].b == b:
        #         # 更新起点坐标及行驶距离
        #         a = deviation_curves[-1].a
        #         s += forward_distance
        #         # 移除上一个元素
        #         deviation_curves.pop()
        #
        #     # elevations.append(Curve(s=s, a=a, b=b, c=0, d=0, lineType='line'))  # 直线段 c=0, d=0
        #
        #     deviation_curves.append(Curve(s=s, a=a, b=b, c=0, d=0, lineType='line'))  # 车道宽度，用直线表示 c=0, d=0
        #     # s += forward_distance
        #
        # return deviation_curves


class Road(BaseRoad):
    def __init__(self, link, qtpoint2point):
        super().__init__(qtpoint2point)

        self.id = str(link.id())
        self.type = 'link'
        self.tess_id = str(link.id())
        self.link = link

        # # 计算路段参考线及高程，这种方式可以保留路网原始的中心线作为参考线
        # geometry_points = self.qtpoint2point(self.link.centerBreakPoint3Ds())
        # # 计算中心车道偏移量
        # self.lane_offsets = self.calc_deviation_curves(link.leftBreakPoint3Ds(), link.centerBreakPoint3Ds(), calc_singal=False)

        # 直接用link左侧边界作为参考线，就不需要偏移量了
        geometry_points = qtpoint2point(self.link.leftBreakPoint3Ds())
        self.lane_offsets = []

        self.geometrys, self.length = self.calc_geometry_line(geometry_points)
        self.elevations = self.calc_elevation(qtpoint2point(self.link.leftBreakPoint3Ds()))  # 必须和参考线用同样的点序列计算高程

        # 计算车道及相关信息
        self.add_lane()

    # 添加车道
    def add_lane(self):
        lane_objs = self.link.lanes()[::-1]
        lane_id = -1
        direction = 'right'
        for index in range(0, len(lane_objs)):  # 从中心车道向右侧展开
            lane = lane_objs[index]
            widths = self.calc_deviation_curves(lane.leftBreakPoint3Ds(), lane.rightBreakPoint3Ds(), calc_singal=True)
            self.lanes.append(
                {
                    'width': widths,
                    'type': NetworkExportConfig.LANE_TYPE_MAPPING.get(lane.actionType(), 'driving'),
                    'id': lane_id,
                    'direction': direction,
                    'lane': lane,
                }
            )
            lane_id -= 1
        return


# 为每个车道连接建立 connector，仅一条车道
class Connector(BaseRoad):
    def __init__(self, laneConnector, junction, qtpoint2point):
        super().__init__(qtpoint2point)

        self.type = 'connector'
        self.junction = junction
        self.laneConnector = laneConnector
        self.fromLink = laneConnector.fromLane().link()
        self.toLink = laneConnector.toLane().link()
        self.tess_id = f"{laneConnector.fromLane().id()}_{laneConnector.toLane().id()}"
        self.id = laneConnector.id() + 100000

        self.lane_offsets = []  # 连接段选取左侧点序列作为参考线，不会有offset

        self.geometry_points = qtpoint2point(laneConnector.leftBreakPoint3Ds())
        selected_index = None

        # 如果点数 >= 4，用参数三次多项式，否则用直线
        if len(self.geometry_points) >= 4:
            try:
                self.geometrys, self.length = self.calc_geometry_paramPoly3(self.geometry_points)
            except:
                print(f"参数三次多项式生成失败!")
                self.geometrys, self.length = self.calc_geometry_line(self.geometry_points)
        else:
            self.geometrys, self.length = self.calc_geometry_line(self.geometry_points)

        # self.geometrys, self.length = self.calc_geometry_line(self.geometry_points)

        # 默认车道方向即参考线方向
        self.add_lane(selected_index)

        self.elevations = self.calc_elevation(qtpoint2point(laneConnector.leftBreakPoint3Ds()))  # 必须和参考线用同样的点序列计算高程

    # 添加车道, junction 仅一条右侧车道 + 中心车道
    def add_lane(self, selected_index):
        # 计算所有的车道
        lane_id = -1
        direction = 'right'
        widths = self.calc_deviation_curves(self.laneConnector.leftBreakPoint3Ds(),
                                            self.laneConnector.rightBreakPoint3Ds(), selected_index, calc_singal=True)

        self.lanes.append(
            {
                'width': widths,
                'type': NetworkExportConfig.LANE_TYPE_MAPPING.get(self.laneConnector.fromLane().actionType(), 'driving'),
                'id': lane_id,
                'direction': direction,
                'lane': None,
                'fromLaneId': self.laneConnector.fromLane().number() - self.laneConnector.fromLane().link().laneCount(),
                'toLaneId': self.laneConnector.toLane().number() - self.laneConnector.toLane().link().laneCount(),
            }
        )


class Junction:
    def __init__(self, ConnectorArea):
        self.id = str(ConnectorArea.id() + 100000000)
        self.tess_id = ConnectorArea.id()
        self.ConnectorArea = ConnectorArea
        self.connection_count = 0


# opendrive 中的所有曲线对象
class Curve:
    """
        以参考线为基础，曲线对象分为四种，分别为 line, spiral, arc, paramPoly3
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, kwargs[key])
        return
        parameters = ["road", "section", "lane", "s", "x", "y", "hdg", "a", "b", "c", "d", "offset", 'direction',
                      "lineType",
                      'level', 'length'] + list(kwargs.keys())
        for key in parameters:
            if key in kwargs:
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, None)


class Vector:
    def __init__(self, start_point, end_point):
        start_point, end_point = list(start_point), list(end_point)
        self.x = end_point[0] - start_point[0]
        self.y = end_point[1] - start_point[1]
        self.z = end_point[2] - start_point[2]
