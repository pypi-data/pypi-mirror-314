import traceback

from ...BaseTool import BaseTool
from ...public.line.LineBase import LineBase
from pytessng.Config import NetworkImportConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class SignalDataAnalyzer(BaseTool):
    valid_duration = NetworkImportConfig.VALID_DURATION

    # 解析信号配时数据
    def analyse_signal_data(self, original_signal_groups_data: dict, original_signal_heads_data: dict) -> (list, list):
        # 获取处理过待行区的信号灯组数据
        signal_groups_data = self.get_signal_groups_data(original_signal_groups_data)

        # 获取路网数据，包括进口道与面域ID的映射关系，各面域的各方向的各转向
        link2area_data, areas_data = self.get_areas_data()

        # 获取面域与信号灯组的映射关系
        area2signal_data = self.get_area2signal_data(original_signal_heads_data, link2area_data)

        # 获取信号灯头数据
        signal_heads_data = self.get_signal_heads_data(area2signal_data, areas_data, signal_groups_data)

        # 获取用于创建信号灯组和信号灯头的标准数据
        signal_groups_data, signal_heads_data = self.get_standard_signal_data(signal_groups_data, signal_heads_data)

        return signal_groups_data, signal_heads_data

    def get_signal_groups_data(self, original_signal_groups_data: dict) -> dict:
        # 当Base为True时不限制灯色列表为4个，也不会读取待行区数据，为False时灯色列表只能是4个，并且会读取待行区数据
        BASE = True

        # ============================================================
        def _handle_phase(colors, durations):
            if BASE:
                # if len(colors) == 1:
                #     colors = []
                #     durations = []
                return colors, durations

            if len(colors) == 1:
                colors = []
                durations = []
            elif len(colors) == 2:
                if colors == ["绿", "红"]:
                    colors = ["红", "绿", "黄", "红"]
                    durations = [0, durations[0], 0, durations[1]]
                elif colors == ["红", "绿"]:
                    colors = ["红", "绿", "黄", "红"]
                    durations = durations + [0, 0]
                else:
                    print(colors)
                    raise Exception("No support!")
            elif len(colors) == 3:
                if colors == ["绿", "黄", "红"]:
                    colors = ["红", "绿", "黄", "红"]
                    durations = [0] + durations
                elif colors == ["红", "绿", "黄"]:
                    colors = ["红", "绿", "黄", "红"]
                    durations = durations + [0]
                elif colors == ["红", "绿", "红"]:
                    colors = ["红", "绿", "黄", "红"]
                    durations = durations[:2] + [0] + durations[2:]
                else:
                    print(colors)
                    raise Exception("No support!")
            elif len(colors) == 4:
                if colors == ["红", "绿", "黄", "红"]:
                    pass
                else:
                    print(colors)
                    raise Exception("No support!")
            else:
                print(colors)
                raise Exception("No support!")
            return colors, durations

        # ============================================================
        def _handle_phases(phases, signal_group_name, cycle_time):
            # 处理相位灯色和持续时间
            handled_phases = []
            for phase in phases:
                colors = phase["colors"]
                durations = phase["durations"]
                try:
                    handled_colors, handled_durations = _handle_phase(colors, durations)
                    # 为了过滤全绿相位
                    if handled_colors and handled_durations:
                        phase["colors"], phase["durations"] = handled_colors, handled_durations
                        handled_phases.append(phase)
                except:
                    logger.logger_pytessng.error(f"Failed to handle phase!")
                    logger.logger_pytessng.error(traceback.format_exc())

            # 按第一个灯色（红）时长排序
            phases = sorted(handled_phases, key=lambda x: x["durations"][0])
            # 新相位列表
            waiting_phases = []

            # 根据是否有待行区创建新相位
            for i, phase in enumerate(phases[1:], start=1):
                direction = phase["direction"]
                waiting_area = phase.get("waitingArea", False)
                # 如果有待行区
                if waiting_area:
                    # 找上一个不一样的相位 TODO SXH 第一个就找不到
                    last_phase = None
                    j = i - 1
                    while j >= 0:
                        if phases[j]["durations"] == phase["durations"]:
                            j -= 1
                        else:
                            last_phase = phases[j]
                            break
                    if last_phase is not None:
                        duration0 = last_phase["durations"][0]
                        duration1 = phase["durations"][0] + phase["durations"][1] - duration0
                        duration2 = phase["durations"][2]
                        duration3 = phase["durations"][3]
                        # 添加新相位
                        new_phase = {
                            "id": "",
                            "colors": ["红", "绿", "黄", "红"],
                            "durations": [duration0, duration1, duration2, duration3],
                            "direction": f"{direction}-待行"
                        }
                        waiting_phases.append(new_phase)

            # 按第一个灯色（红）时长排序
            waiting_phases = sorted(waiting_phases, key=lambda x: x["durations"][0])

            # 处理相位的ID
            phase_no = 1
            for phase in phases + waiting_phases:
                direction = phase["direction"]
                # 排除时长不对的相位
                if sum(phase["durations"]) == cycle_time:
                    # 相位ID用灯组名称加相位序号
                    phase["id"] = f"{signal_group_name}-{phase_no}"
                    phase["name"] = direction
                    phase_no += 1
                else:
                    logger.logger_pytessng.warning(f"The duration of each light color is not equal to the duration of the cycle in [{signal_group_name}] [{direction}]!")

            phases_dict = {phase["direction"]: phase for phase in phases if sum(phase["durations"]) == cycle_time}
            waiting_phases_dict = {phase["direction"]: phase for phase in waiting_phases if sum(phase["durations"]) == cycle_time}

            return phases_dict, waiting_phases_dict

        # ============================================================
        signal_groups_data = {}
        for signal_group in original_signal_groups_data:
            signal_group_name = signal_group["name"]
            cycle_time = signal_group["cycleTime"]
            try:
                phases, waiting_phases = _handle_phases(signal_group["phases"], signal_group_name, cycle_time)
                signal_groups_data[signal_group_name] = {
                    "cycle_time": cycle_time,
                    "phases": phases,
                    "waiting_phases": waiting_phases,
                }
            except:
                logger.logger_pytessng.error(f"Error occurred in analyzing signal light group data [{signal_group_name}]!")
                logger.logger_pytessng.error(traceback.format_exc())

        return signal_groups_data

    def get_areas_data(self) -> (dict, dict):
        # 各面域的上游路段ID集合
        area2link_data = dict()
        for connector_area in self.netiface.allConnectorArea():
            all_connector = connector_area.allConnector()
            # 只有少数连接段的面域视为路段中间
            if len(all_connector) >= 2:
                area2link_data[connector_area.id()] = set()
                for connector in connector_area.allConnector():
                    from_link = connector.fromLink()
                    area2link_data[connector_area.id()].add(from_link.id())

        # 进口道路段ID对应的面域
        link2area_data = {
            link_id: connector_area_id
            for connector_area_id, link_id_list in area2link_data.items()
            for link_id in link_id_list
        }

        # 确定每个面域的进口道方向，和进口道的流向
        areas_data = {}
        for connector_area_id, from_link_list in area2link_data.items():
            direction_record = {"东": {}, "南": {}, "西": {}, "北": {}}
            for link_id in from_link_list:
                link = self.netiface.findLink(link_id)
                for to_connector in link.toConnectors():
                    for lane_connector in to_connector.laneConnectors():
                        from_lane = lane_connector.fromLane()
                        to_lane = lane_connector.toLane()
                        from_lane_id = from_lane.id()
                        to_lane_id = to_lane.id()
                        from_lane_points = self._qtpoint2list(from_lane.centerBreakPoint3Ds())
                        to_lane_points = self._qtpoint2list(to_lane.centerBreakPoint3Ds())

                        start_angle = LineBase.calculate_angle_with_y_axis(from_lane_points[-2], from_lane_points[-1])
                        end_angle = LineBase.calculate_angle_with_y_axis(to_lane_points[0], to_lane_points[1])

                        # 进口道方向 -180~180
                        start_angle = (start_angle + 180) % 360 - 180
                        if -45 <= start_angle <= 45:
                            direction = "南"
                        elif 45 <= start_angle <= 135:
                            direction = "西"
                        elif -135 <= start_angle <= -45:
                            direction = "东"
                        else:
                            direction = "北"

                        # 转向角 -180~180
                        turn_angle = (end_angle - start_angle + 180) % 360 - 180
                        if -45 <= turn_angle <= 45:
                            turn_type = "直"
                        elif -135 <= turn_angle <= -45:
                            turn_type = "左"
                        elif 45 <= turn_angle <= 135:
                            turn_type = "右"
                        else:
                            turn_type = "掉"

                        if from_lane_id not in direction_record[direction]:
                            direction_record[direction][from_lane_id] = {}
                        if turn_type not in direction_record[direction][from_lane_id]:
                            direction_record[direction][from_lane_id][turn_type] = []
                        direction_record[direction][from_lane_id][turn_type].append(to_lane_id)

            areas_data[connector_area_id] = direction_record

        return link2area_data, areas_data

    def get_area2signal_data(self, original_signal_heads_data: dict, link2area_data: dict) -> dict:
        area2signal_data = {}
        for signal_head in original_signal_heads_data:
            link_id_list: list = signal_head["roadIds"]
            signal_group_name: str = signal_head["signalGroupName"]
            area_id_set = set([link2area_data[link_id] for link_id in link_id_list if link2area_data.get(link_id)])

            if len(area_id_set) != 1:
                logger.logger_pytessng.warning(f"The roadIds [{link_id_list}] can not match to a unique connector_area [{area_id_set}]!")
                continue

            area_id = area_id_set.pop()
            area2signal_data[area_id] = signal_group_name

        return area2signal_data

    def get_signal_heads_data(self, area2signal_data: dict, areas_data: dict, signal_groups_data: dict) -> list:
        signal_heads_data = []

        # 遍历面域（交叉口）
        for area_id, signal_group_name in area2signal_data.items():
            area_data = areas_data[area_id]
            signal_group_data: dict = signal_groups_data.get(signal_group_name)
            if signal_group_data is None:
                logger.logger_pytessng.warning(f"The signal group [{signal_group_name}] is not found!")
                continue
            phases, waiting_phases = signal_group_data["phases"], signal_group_data["waiting_phases"]

            # 遍历一个交叉口的各个方向
            for direction0, direction_record in area_data.items():
                # 遍历一个方向的各个车道
                for from_lane_id, turn_record in direction_record.items():
                    # 单个车道包含的转向，按直、左、右、掉的顺序排序
                    turn_type_list = sorted(turn_record.keys(), key=lambda x: ["直", "左", "右", "掉"].index(x))

                    # 单车道有多个转向，且包含右转，且右转不在信号灯组中（即不限制）
                    if len(turn_type_list) > 1:
                        if "右" in turn_type_list and f"{direction0}右" not in phases:
                            in_connector = True
                        else:
                            in_connector = True
                    else:
                        in_connector = False

                    # 如果是建在路段上就只取一种
                    turn_type_list = turn_type_list if in_connector else turn_type_list[:1]

                    # 遍历一条车道各个转向
                    for turn_type in turn_type_list:
                        # 去向车道列表
                        to_lane_id_list = turn_record[turn_type]
                        # 构建方向
                        direction = f"{direction0}{turn_type}"
                        # 如果不需要设置信号灯就跳过
                        if direction not in phases:
                            continue

                        # 需要设置待行相位
                        if waiting_phases and f"{direction}-待行" in waiting_phases:
                            this_phase_id = waiting_phases[f"{direction}-待行"]["id"]
                            waiting_phase_id = phases[direction]["id"]
                        # 不需要设置待行相位
                        else:
                            this_phase_id = phases[direction]["id"]
                            waiting_phase_id = None

                        lane_id = str(from_lane_id)
                        to_lane_id_list = to_lane_id_list if in_connector else to_lane_id_list[:1]
                        # 遍历去向车道
                        for to_lane_id in to_lane_id_list:
                            # 不是在连接段
                            if not in_connector:
                                dist = -1
                                to_lane_id_ = "0"
                            # 是在连接段
                            else:
                                dist = 0.1
                                to_lane_id_ = str(to_lane_id)

                            signal_head_data = {
                                "phase_id": this_phase_id,
                                "dist": dist,
                                "lane_id": lane_id,
                                "to_lane_id": to_lane_id_,
                            }
                            signal_heads_data.append(signal_head_data)

                            # 待行相位
                            if waiting_phase_id is not None:
                                # 一定在连接段上
                                lane_connector = self.netiface.findLaneConnector(from_lane_id, to_lane_id)
                                dist = min([8, 0.5 * self._p2m(lane_connector.length())])
                                to_lane_id_ = str(to_lane_id)

                                signal_head_data = {
                                    "phase_id": waiting_phase_id,
                                    "dist": dist,
                                    "lane_id": lane_id,
                                    "to_lane_id": to_lane_id_,
                                }
                                signal_heads_data.append(signal_head_data)

        return signal_heads_data

    def get_standard_signal_data(self, signal_groups_data: dict, signal_heads_data) -> (list, list):
        # 信号灯组
        standard_signal_groups_data = []
        signal_group_id = 1
        for signal_group_name, signal_group_data in signal_groups_data.items():
            phases = list(signal_group_data["phases"].values()) + list(signal_group_data["waiting_phases"].values())
            temp_handle(phases)
            standard_signal_group_data = {
                "id": str(signal_group_id),  # 自增ID
                "name": signal_group_name,  # 是参数
                "cycle_time": signal_group_data["cycle_time"],
                "phases": phases,
                "duration": self.valid_duration
            }
            # 去除多余字段
            for phase in standard_signal_group_data["phases"]:
                if "direction" in phase:
                    phase.pop("direction")
                if "waitingArea" in phase:
                    phase.pop("waitingArea")
            standard_signal_groups_data.append(standard_signal_group_data)
            # ID自增
            signal_group_id += 1

        # 信号灯头
        standard_signal_heads_data = []
        signal_head_id = 1
        for signal_head_data in signal_heads_data:
            # 加上ID字段
            signal_head_data["id"] = str(signal_head_id)
            standard_signal_heads_data.append(signal_head_data)
            signal_head_id += 1

        return standard_signal_groups_data, standard_signal_heads_data


# TODO SXH 为了上海电科项目临时处理，后续需要修改
def temp_handle(phases: list):
    mapping = {
        '北左': 1, '北直': 2, '北右': 3, '北行人1': 4,
        '东左': 5, '东直': 6, '东右': 7, '东行人1': 8,
        '南左': 9, '南直': 10, '南右': 11, '南行人1': 12,
        '西左': 13, '西直': 14, '西右': 15, '西行人1': 16,
        '北掉': 17, '东掉': 18, '南掉': 19, '西掉': 20,
        '北行人2': 21, '东行人2': 22, '南行人2': 23, '西行人2': 24,
        '北非机动车': 25, '东非机动车': 26, '南非机动车': 27, '西非机动车': 28,
        '扩展1': 61, '扩展2': 62, '扩展3': 63, '扩展4': 64,
        '东北左': 33, '东北直': 34, '东北右': 35, '东北行人1': 36,
        '东南左': 37, '东南直': 38, '东南右': 39, '东南行人1': 40,
        '西南左': 41, '西南直': 42, '西南右': 43, '西南行人1': 44,
        '西北左': 45, '西北直': 46, '西北右': 47, '西北行人1': 48,
        '东北掉头': 49, '东南掉头': 50, '西南掉头': 51, '西北掉头': 52,
        '东北行人2': 53, '东南行人2': 54, '西南行人2': 55, '西北行人2': 56,
        '东北非机动车': 57, '东南非机动车': 58, '西南非机动车': 59, '西北非机动车': 60
    }
    for phase in phases:
        try:
            direction = phase["direction"]
            number = mapping[direction]
            phase["name"] = f"{number}-{direction}"
        except:
            pass
