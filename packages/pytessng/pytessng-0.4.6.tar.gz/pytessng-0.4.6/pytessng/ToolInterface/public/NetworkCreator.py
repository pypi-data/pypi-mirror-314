import traceback

from ..BaseTool import BaseTool
from .DataClass import Attrs, Link, Connector, VehicleComposition, VehicleInput
from .DataClass import SignalPhase, SignalGroup, SignalHead, DecisionPoint, ReducedSpeedArea, GuidArrow
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class NetworkCreator(BaseTool):
    def __init__(self, netiface, is_road_network: bool = True, move_distance: dict = None, pgd_indexes: tuple = (1, 2)):
        super().__init__(netiface, extension=True)

        # 是否为道路网络
        self.is_road_network: bool = is_road_network
        # 移动距离
        self.move_distance: dict = move_distance if move_distance else {"x_move": 0, "y_move": 0}
        # 进度条相关
        self.pgd_index_start: int = pgd_indexes[0]
        self.pgd_index_max: int = pgd_indexes[1]

        # 路段ID映射字典
        self._link_id_mapping: dict = {}
        # 车辆组成ID映射字典
        self._vehicle_composition_id_mapping: dict = {}
        # 信号相位ID映射字典
        self._signal_phase_id_mapping: dict = {}

        # 对象创建函数映射
        self._create_function_mapping: dict = {
            "links": self.create_links,
            "connectors": self.create_connectors,
            "vehicleCompositions": self.create_vehicle_compositions,
            "vehicleInputs": self.create_vehicle_inputs,
            "signalGroups": self.create_signal_groups,
            "signalHeads": self.create_signal_heads,
            "decisionPoints": self.create_decision_points,
            "reducedSpeedAreas": self.create_reduced_speed_areas,
            "guidArrows": self.create_guid_arrow,
        }

    # 设置路网属性
    def set_attrs(self, attrs: dict):
        # 构建对象
        attrs: Attrs = Attrs(**attrs)
        # 设置属性
        self.netiface.setNetAttrs(f"{attrs.data_source} Network", otherAttrsJson=attrs.dict())

    # 创建路网
    def create_network(self, network_data: dict, update_scene_size: bool = True) -> dict:
        result_create_network = dict()
        # 创建路网
        for object_type, objects_data in network_data.items():
            create_func = self._create_function_mapping.get(object_type)
            if create_func:
                result_create_objects = create_func(objects_data)
                result_create_network[object_type] = result_create_objects
            else:
                logger.logger_pytessng.error(f"Failed to find the function of create {object_type}!")
                result_create_network[object_type] = None

        # 如果是道路网络就更新场景尺寸
        if self.is_road_network and update_scene_size:
            self.update_scene_size()

        return result_create_network

    # 创建路段
    def create_links(self, links_data: list) -> dict:
        result_create = {}

        # 按照ID排序
        try:
            links_data = sorted(links_data, key=lambda x: int(x["id"]))
        except:
            pass

        for link_data in pgd.progress(links_data, f"路段创建中({self.pgd_index_start}/{self.pgd_index_max})"):
            link_id = -1
            try:
                # 构建路段对象
                link = Link(**link_data)
                link_id = link.id

                points = link.points
                lane_count = link.lane_count
                lanes_width = [self._m2p(width) for width in link.lanes_width]
                lanes_points = link.lanes_points
                lanes_type = link.lanes_type
                limit_speed = self._m2p(link.limit_speed)
                name = link.name

                point_value_num = len(points[0])
                points = self._list2qtpoint(points, self.move_distance)

                # 用车道点位
                if lanes_points:
                    for lane_point in lanes_points:
                        for location in ["left", "center", "right"]:
                            lane_point[location] = self._list2qtpoint(lane_point[location], self.move_distance)
                    link_obj = self.netiface.createLink3DWithLanePoints(points, lanes_points, name)
                # 用车道宽度
                elif lanes_width:
                    if point_value_num == 2:
                        link_obj = self.netiface.createLinkWithLaneWidth(points, lanes_width, name)
                    else:
                        link_obj = self.netiface.createLink3DWithLaneWidth(points, lanes_width, name)
                # 用车道数量
                else:
                    if point_value_num == 2:
                        link_obj = self.netiface.createLink(points, lane_count, name)
                    else:
                        link_obj = self.netiface.createLink3D(points, lane_count, name)

                # 如果创建成功，设置限速和车道类型
                if link_obj:
                    # 限速
                    if limit_speed:
                        link_obj.setLimitSpeed(limit_speed)
                    # 车道类型
                    for lane, lane_type in zip(link_obj.lanes(), lanes_type):
                        lane.setLaneType(lane_type)
                    # 保存对应关系
                    self._link_id_mapping[link_id] = link_obj.id()
                    result_create[link_id] = link_obj.id()
                else:
                    self._handle_error("Link", link_id, result_create)

            except:
                self._handle_error("Link", link_id, result_create, traceback.format_exc())

        return result_create

    # 创建连接段
    def create_connectors(self, connectors_data: list) -> dict:
        result_create = {}

        for connector_data in pgd.progress(connectors_data, f"连接段创建中({self.pgd_index_start + 1}/{self.pgd_index_max})"):
            connector_id = -1
            try:
                # 构建连接段对象
                connector = Connector(**connector_data)

                from_link_id = self._link_id_mapping.get(connector.from_link_id) or int(connector.from_link_id)
                to_link_id = self._link_id_mapping.get(connector.to_link_id) or int(connector.to_link_id)
                from_lane_numbers = connector.from_lane_numbers
                to_lane_numbers = connector.to_lane_numbers
                lanes_points = None  # TODO SXH: 暂时不支持
                # lanes_points = connector.lanes_points
                name = connector.name

                connector_id = f"{from_link_id}-{to_link_id}"

                # 不给点位
                if not lanes_points:
                    connector_obj = self.netiface.createConnector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers, connName=name)
                # 给点位
                else:
                    for lane_point in lanes_points:
                        for location in ["left", "center", "right"]:
                            lane_point[location] = self._list2qtpoint(lane_point[location])
                    connector_obj = self.netiface.createConnector3DWithPoints(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers, lanes_points, connName=name)

                if connector_obj:
                    # 保存对应关系
                    result_create[connector_id] = connector_obj.id()
                else:
                    self._handle_error("Connector", connector_id, result_create)
            except:
                self._handle_error("Connector", connector_id, result_create, traceback.format_exc())

        return result_create

    # 创建车辆组成
    def create_vehicle_compositions(self, vehicle_compositions_data: list) -> dict:
        result_create = {}

        for vehicle_composition_data in pgd.progress(vehicle_compositions_data, "车辆组成创建中"):
            vehicle_composition_id = -1
            try:
                # 构建车辆组成对象
                vehicle_composition = VehicleComposition(**vehicle_composition_data)

                vehicle_composition_id = vehicle_composition.id
                vehicle_composition_name = vehicle_composition.id
                vehi_type_code_list = vehicle_composition.vehi_type_code_list
                vehi_type_ratio_list = vehicle_composition.vehi_type_ratio_list

                vehicle_data_list = [
                    self.Online.VehiComposition(vehi_type_code, vehi_type_ratio)
                    for vehi_type_code, vehi_type_ratio in zip(vehi_type_code_list, vehi_type_ratio_list)
                ]
                vehicle_composition_actual_id = self.netiface.createVehicleComposition(vehicle_composition_name, vehicle_data_list)

                # 如果创建成功
                if vehicle_composition_actual_id:
                    # 保存对应关系
                    result_create[vehicle_composition_id] = vehicle_composition_actual_id
                else:
                    self._handle_error("VehicleComposition", vehicle_composition_id, result_create)
            except:
                self._handle_error("VehicleComposition", vehicle_composition_id, result_create, traceback.format_exc())

        return result_create

    # 创建发车点
    def create_vehicle_inputs(self, vehicle_inputs_data: list) -> dict:
        result_create = {}

        for vehicle_input_data in pgd.progress(vehicle_inputs_data, "车辆输入创建中"):
            vehicle_input_id = -1
            try:
                # 构建发车点对象
                vehicle_input = VehicleInput(**vehicle_input_data)

                vehicle_input_id = vehicle_input.id
                vehicle_input_name = vehicle_input_id
                vehicle_compose_id = self._vehicle_composition_id_mapping.get(vehicle_input.vehicle_compose_id, vehicle_input.vehicle_compose_id)
                link_id = self._link_id_mapping.get(vehicle_input.link_id, vehicle_input.link_id)
                volumes = vehicle_input.volumes
                durations = vehicle_input.durations

                link = self.netiface.findLink(link_id)
                if link:
                    dp = self.netiface.createDispatchPoint(link, dpName=vehicle_input_name)
                    if dp:
                        for volume, duration in zip(volumes, durations):
                            dp.addDispatchInterval(int(vehicle_compose_id), duration, volume)  # 车辆组成、时间间隔、车辆数
                        result_create[vehicle_input_id] = dp.id()
                    else:
                        self._handle_error("VehicleInput", vehicle_input_id, result_create, f"No find Link {link_id}!")
                else:
                    self._handle_error("VehicleInput", vehicle_input_id, result_create)
            except:
                self._handle_error("VehicleInput", vehicle_input_id, result_create, traceback.format_exc())

        return result_create

    # 创建信号灯组及相位
    def create_signal_groups(self, signal_groups_data: list) -> dict:
        result_create = {}

        for signal_group_data in pgd.progress(signal_groups_data, "信号灯组创建中"):
            try:
                # 构建信号相位对象
                signal_group_data["phases"] = [
                    SignalPhase(**phase_data)
                    for phase_data in signal_group_data["phases"]
                ]
                # 构建信号灯组对象
                signal_group = SignalGroup(**signal_group_data)

                signal_group_name = signal_group.name
                cycle_time = signal_group.cycle_time  # 周期时间
                phases = signal_group.phases  # 相位
                duration = signal_group.duration  # 持续时间

                signal_group_obj = self.netiface.createSignalGroup(signal_group_name, cycle_time, 0, duration)
                # 创建信号相位
                for phase in phases:
                    phase_id = phase.id
                    phase_name = phase.name
                    colors = phase.colors
                    durations = phase.durations
                    try:
                        signal_phase = [
                            self.Online.ColorInterval(color, duration)
                            for color, duration in zip(colors, durations)
                        ]
                        signal_phase_obj = self.netiface.createSignalPhase(signal_group_obj, phase_name, signal_phase)

                        # 如果创建成功
                        if signal_phase_obj:
                            self._signal_phase_id_mapping[phase_id] = signal_phase_obj.id()
                            result_create[phase_id] = signal_phase_obj.id()
                        else:
                            self._handle_error("SignalPhase", phase_id, result_create)
                    except:
                        self._handle_error("SignalPhase", phase_id, result_create, traceback.format_exc())
            except:
                signal_group_id = "-1"
                self._handle_error("SignalGroup", signal_group_id, result_create, traceback.format_exc())
        return result_create

    # 创建信号灯头
    def create_signal_heads(self, signal_heads_data: list) -> dict:
        result_create = {}

        for signal_head_data in pgd.progress(signal_heads_data, "信号灯头创建中"):
            try:
                # 构建信号灯头对象
                signal_head = SignalHead(**signal_head_data)

                signal_head_id: str = signal_head.id
                signal_head_name: str = str(signal_head_id)
                phase_id: int = self._signal_phase_id_mapping.get(str(signal_head.phase_id)) or int(signal_head.phase_id)
                link_id: int = self._link_id_mapping.get(signal_head.link_id) or int(signal_head.link_id)
                lane_numer: int = signal_head.lane_number
                dist: float = self._m2p(signal_head.dist) if int(signal_head.dist) != -1 else None
                to_link_id: int = self._link_id_mapping.get(signal_head.to_link_id) or int(signal_head.to_link_id)
                to_lane_number: int = signal_head.to_lane_number
                lane_number_is_from_right: bool = signal_head.lane_number_is_from_right
                lane_id: int = int(signal_head.lane_id)
                to_lane_id: int = int(signal_head.to_lane_id)

                signal_phase = self.netiface.findSignalPhase(phase_id)

                # 给的路段ID和车道序号
                if lane_id == 0:
                    link = self.netiface.findLink(link_id)
                    # lane_id
                    if lane_number_is_from_right:
                        lane = [lane for i, lane in enumerate(link.lanes()) if i + 1 == lane_numer][0]
                    else:
                        lane = [lane for i, lane in enumerate(link.lanes()) if link.laneCount() - i == lane_numer][0]
                    lane_id = lane.id()

                    # to_lane_id
                    if to_link_id == 0:  # 路段
                        to_lane_id = 0
                    else:  # 连接段
                        to_link = self.netiface.findLink(to_link_id)
                        if lane_number_is_from_right:
                            to_lane = [lane for i, lane in enumerate(to_link.lanes()) if i + 1 == to_lane_number][0]
                        else:
                            to_lane = [lane for i, lane in enumerate(to_link.lanes()) if to_link.laneCount() - i == to_lane_number][0]
                        to_lane_id = to_lane.id()
                # 直接给的车道ID
                else:
                    lane = self.netiface.findLane(lane_id)

                # 所在路段的距离
                if to_link_id == 0:  # 路段
                    if dist is None:
                        dist = lane.length()  # 不需要转换单位
                else:  # 连接段
                    if dist is None:
                        dist = 0

                signal_lamp = self.netiface.createSignalLamp(signal_phase, signal_head_name, lane_id, to_lane_id, dist)

                # 如果创建成功
                if signal_lamp:
                    result_create[signal_head_id] = signal_lamp.id()
                else:
                    self._handle_error("SignalHead", signal_head_id, result_create)

            except:
                signal_head_id = "-1"
                self._handle_error("SignalHead", signal_head_id, result_create, traceback.format_exc())

        return result_create

    # 创建决策点
    def create_decision_points(self, decision_points_data: list) -> dict:
        result_create = {}

        _DecisionPoint = self.private_class["_DecisionPoint"]
        _RoutingFLowRatio = self.private_class["_RoutingFLowRatio"]

        # 更新决策点添加路径
        def _update_decision_point(decision_point_actual_id_: int, hour_: int, routings_flow_: dict):
            decisionPoint = _DecisionPoint()
            decisionPoint.deciPointID = decision_point_actual_id_
            decisionPoint.deciPointName = f"{decision_point_actual_id_}"
            decisionPoint.X = 0
            decisionPoint.Y = 0
            decisionPoint.Z = 0

            ratio_data = []
            for routing_id_, flow_ in routings_flow_.items():
                r = _RoutingFLowRatio()
                r.startDateTime = 0
                r.endDateTime = 3600 * hour_
                r.ratio = flow_
                r.routingID = routing_id_
                ratio_data.append(r)

            decisionPoint = self.netiface.updateDecipointPoint(decisionPoint, ratio_data)
            return decisionPoint

        for decision_point_data in pgd.progress(decision_points_data, "决策点创建中"):
            decision_point_id = -1
            try:
                # 构建决策点对象
                decision_point = DecisionPoint(**decision_point_data)

                decision_point_id = decision_point.id
                decision_point_name = decision_point_id
                link_id = self._link_id_mapping.get(decision_point.link_id, decision_point.link_id)
                dist = self._m2p(decision_point.dist)
                routings = decision_point.routings
                ratios = decision_point.ratios
                duration = decision_point.duration

                link = self.netiface.findLink(link_id)
                # 创建决策点
                decision_point_obj = self.netiface.createDecisionPoint(link, dist, decision_point_name)
                decision_point_actual_id = decision_point_obj.id()
                routings_flow = {}
                # 创建决策路径
                for routing, ratio in zip(routings, ratios):
                    routing_ = [
                        self.netiface.findLink(int(self._link_id_mapping[link_id]))
                        for link_id in routing
                        if link_id in self._link_id_mapping
                    ]
                    routing_object = self.netiface.createDeciRouting(decision_point_obj, routing_)
                    routing_id = routing_object.id()
                    routings_flow[routing_id] = ratio
                # 更新路径流量
                decision_point_obj = _update_decision_point(decision_point_actual_id, duration, routings_flow)

                # 如果创建成功
                if decision_point_obj:
                    result_create[decision_point_id] = decision_point_actual_id
                else:
                    self._handle_error("DecisionPoint", decision_point_id, result_create)
            except:
                self._handle_error("DecisionPoint", decision_point_id, result_create, traceback.format_exc())

        return result_create

    # 创建减速区
    def create_reduced_speed_areas(self, reduced_speed_areas_data: list) -> dict:
        result_create = {}

        SPEED_STANDARD_DEVIATION = 1

        def _get_reduceSpeedVehicleType_list(speed):
            reduceSpeedVehicleType_list = []
            for vehicleTypeCode in range(1, 12):
                rsvt = self.Online.ReduceSpeedVehicleType()
                rsvt.avgSpeed = speed
                rsvt.speedSD = SPEED_STANDARD_DEVIATION
                rsvt.vehicleTypeCode = vehicleTypeCode
                reduceSpeedVehicleType_list.append(rsvt)
            return reduceSpeedVehicleType_list

        for reducedSpeedArea_data in pgd.progress(reduced_speed_areas_data, "减速区创建中"):
            reduced_speed_area_id = -1
            try:
                # 构建减速区对象
                reducedSpeedArea = ReducedSpeedArea(**reducedSpeedArea_data)

                reduced_speed_area_id = reducedSpeedArea.id
                reduced_speed_area_name = reduced_speed_area_id
                speed = self._m2p(reducedSpeedArea.speed)
                link_id = self._link_id_mapping.get(reducedSpeedArea.link_id, reducedSpeedArea.link_id)
                lane_number = reducedSpeedArea.lane_number
                dist = self._m2p(reducedSpeedArea.dist)
                length = self._m2p(reducedSpeedArea.length)
                to_time = reducedSpeedArea.to_time
                reduceSpeedVehicleType_list = _get_reduceSpeedVehicleType_list(speed)

                reduceSpeedArea = self.netiface.createReduceSpeedArea(reduced_speed_area_name, dist, length, link_id, lane_number, -1, 0, to_time, reduceSpeedVehicleType_list)

                # 如果创建成功
                if reduceSpeedArea:
                    result_create[reduced_speed_area_id] = reduceSpeedArea.id()
                else:
                    self._handle_error("ReduceSpeedArea", reduced_speed_area_id, result_create)
            except:
                self._handle_error("ReduceSpeedArea", reduced_speed_area_id, result_create, traceback.format_exc())

        return result_create

    # 创建导向箭头
    def create_guid_arrow(self, guid_arrows_data: list) -> None:
        guid_arrow_type_mapping = {
            1: self.Online.GuideArrowType.Straight,
            2: self.Online.GuideArrowType.Left,
            3: self.Online.GuideArrowType.Right,
            4: self.Online.GuideArrowType.StraightLeft,
            5: self.Online.GuideArrowType.StraightRight,
            6: self.Online.GuideArrowType.StraightLeftRight,
            7: self.Online.GuideArrowType.LeftRight,
            8: self.Online.GuideArrowType.Uturn,
            9: self.Online.GuideArrowType.StraightUturn,
            10: self.Online.GuideArrowType.LeftUturn,
        }

        for guid_arrow_data in pgd.progress(guid_arrows_data, "导向箭头创建中"):
            try:
                # 构建发车点对象
                guid_arrow = GuidArrow(**guid_arrow_data)

                lane_id: int = int(guid_arrow.lane_id)
                turn_arrow_type = guid_arrow.turn_arrow_type
                length = self._m2p(guid_arrow.length)
                dist_to_end = self._m2p(guid_arrow.dist_to_end)

                lane = self.netiface.findLane(lane_id)
                turn_arrow_type_tessng = guid_arrow_type_mapping[turn_arrow_type]
                self.netiface.createGuidArrow(lane, length, dist_to_end, turn_arrow_type_tessng)

            except:
                print(traceback.format_exc())

        return None

    # 错误处理
    def _handle_error(self, object_name: str, object_id: str, result_create: dict, error_message: str = None) -> None:
        logger.logger_pytessng.error(f"Failed to create {object_name} {object_id}!")
        if error_message:
            logger.logger_pytessng.error(error_message)
        result_create[object_id] = None
