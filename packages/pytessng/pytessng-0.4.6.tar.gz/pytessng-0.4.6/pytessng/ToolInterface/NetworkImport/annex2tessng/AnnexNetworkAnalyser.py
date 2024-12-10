from ..BaseNetworkAnalyser import BaseNetworkAnalyser
from .SignalDataAnalyzer import SignalDataAnalyzer
from ...public.line.LineBase import LineBase
from pytessng.Logger import logger


class AnnexNetworkAnalyser(BaseNetworkAnalyser):
    def __init__(self, netiface):
        super().__init__()
        self.netiface = netiface

    def analyse_all_data(self, annex_data: dict, params: dict = None) -> dict:
        # 文件路径
        file_path: str = params["file_path"]
        # 数据导入类型
        element_types: list = params["element_types"]
        # 自动导入类型
        auto_element_types: list = params["auto_element_types"]

        # 解析后的路网数据
        analysed_network_data: dict = dict()

        # 车辆组成 TODO SXH
        if file_path and "vehicle_composition" in element_types:
            original_vehicle_compositions_data = annex_data.get("vehicleCompositions")
            if original_vehicle_compositions_data is not None:
                standard_vehicle_compositions_data = self.analyse_vehicle_compositions(original_vehicle_compositions_data)
                analysed_network_data["vehicleCompositions"] = standard_vehicle_compositions_data
            else:
                logger.logger_pytessng.warning("车辆组成数据为空！")

        # 车辆输入
        if file_path and "vehicle_input" in element_types:
            original_vehicle_inputs_data = annex_data.get("vehicleInputs")
            if original_vehicle_inputs_data is not None:
                standard_vehicle_inputs_data = self.analyse_vehicle_inputs(original_vehicle_inputs_data)
                analysed_network_data["vehicleInputs"] = standard_vehicle_inputs_data
            else:
                logger.logger_pytessng.warning("车辆输入数据为空！")

        # 信号配时
        if file_path and "signal" in element_types:
            original_signal_groups_data = annex_data.get("signalGroups")
            original_signal_heads_data = annex_data.get("signalHeads")
            if original_signal_groups_data is not None and original_signal_heads_data is not None:
                signal_groups_data, signal_heads_data = SignalDataAnalyzer(self.netiface).analyse_signal_data(original_signal_groups_data, original_signal_heads_data)
                analysed_network_data["signalGroups"] = signal_groups_data
                analysed_network_data["signalHeads"] = signal_heads_data
            else:
                logger.logger_pytessng.warning("信号灯组数据或信号灯头数据为空！")

        # 决策点
        if file_path and "decision_point" in element_types:
            original_decision_points_data = annex_data.get("decisionPoints")
            if original_decision_points_data is not None:
                standard_decision_points_data = self.analyse_decision_points(original_decision_points_data)
                analysed_network_data["decisionPoints"] = standard_decision_points_data
            else:
                logger.logger_pytessng.warning("决策点数据为空！")

        # 减速区
        if file_path and "reduced_speed_area" in element_types:
            original_reduced_speed_areas_data = annex_data.get("reducedSpeedAreas")
            if original_reduced_speed_areas_data is not None:
                standard_reduced_speed_areas_data = self.analyse_reduced_speed_areas(original_reduced_speed_areas_data)
                analysed_network_data["reducedSpeedAreas"] = standard_reduced_speed_areas_data
            else:
                logger.logger_pytessng.warning("减速区数据为空！")

        # 导向箭头
        if "guid_arrow" in auto_element_types:
            standard_guid_arrow_data = self.analyse_guid_arrows()
            analysed_network_data["guidArrows"] = standard_guid_arrow_data

        return analysed_network_data

    # 解析车辆组成
    def analyse_vehicle_compositions(self, original_vehicle_compositions_data) -> list:
        pass

    # 解析车辆输入
    def analyse_vehicle_inputs(self, original_vehicle_inputs_data) -> list:
        pass

    # 解析决策点
    def analyse_decision_points(self, original_decision_points_data) -> list:
        pass

    # 解析减速区
    def analyse_reduced_speed_areas(self, original_reduced_speed_areas_data) -> list:
        pass

    # 解析导向箭头
    def analyse_guid_arrows(self) -> list:
        # 现存的导向箭头所在的车道ID
        land_id_set = set([guid_arrow.lane().id() for guid_arrow in self.netiface.guidArrows()])

        # 车道功能映射
        lane_function_mapping: dict = dict()

        # 遍历连接段面域
        for connector_area in self.netiface.allConnectorArea():
            all_connector = connector_area.allConnector()
            # 连接段超过一定数量才认为是交叉口
            if len(all_connector) >= 3:
                for connector in all_connector:
                    for lane_connector in connector.laneConnectors():
                        # 上游车道
                        from_lane = lane_connector.fromLane()
                        # 上游车道ID
                        from_lane_id = from_lane.id()

                        # 如果车道上已经有箭头
                        if from_lane_id in land_id_set:
                            continue

                        # 车道连接的点位
                        lane_connector_points = [(point.x(), -point.y()) for point in lane_connector.centerBreakPoints()]
                        # 计算转向类型
                        turn_type = LineBase.calculate_turn_type(lane_connector_points)
                        # 添加数据
                        if from_lane.id() not in lane_function_mapping:
                            lane_function_mapping[from_lane.id()] = {
                                "turn_type_set": set(),
                                "turn_arrow_type": 0
                            }
                        # 添加转向类型
                        lane_function_mapping[from_lane.id()]["turn_type_set"].add(turn_type)

        # 根据转向类型计算导向箭头类型
        for lane_id, value in lane_function_mapping.items():
            turn_type_set = value["turn_type_set"]

            if turn_type_set == {"直行"}:
                turn_arrow_type = 1
            elif turn_type_set == {"左转"}:
                turn_arrow_type = 2
            elif turn_type_set == {"右转"}:
                turn_arrow_type = 3
            elif turn_type_set == {"直行", "左转"}:
                turn_arrow_type = 4
            elif turn_type_set == {"直行", "右转"}:
                turn_arrow_type = 5
            elif turn_type_set == {"直行", "左转", "右转"}:
                turn_arrow_type = 6
            elif turn_type_set == {"左转", "右转"}:
                turn_arrow_type = 7
            elif turn_type_set == {"调头"}:
                turn_arrow_type = 8
            elif turn_type_set == {"直行", "调头"}:
                turn_arrow_type = 9
            elif turn_type_set == {"左转", "调头"}:
                turn_arrow_type = 10
            else:
                logger.logger_pytessng.warning(f"无法识别的转向类型：{turn_type_set}")
                continue

            value["turn_arrow_type"] = turn_arrow_type

        return [
            {
                "lane_id": lane_id,
                "turn_arrow_type": value["turn_arrow_type"]
            }
            for lane_id, value in lane_function_mapping.items()
            if value["turn_arrow_type"] != 0  # 在类型库里面有的才添加
        ]
