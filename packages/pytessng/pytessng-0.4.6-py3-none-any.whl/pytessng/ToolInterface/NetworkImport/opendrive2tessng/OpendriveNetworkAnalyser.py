from pytessng.ToolInterface.NetworkImport.BaseNetworkAnalyser import BaseNetworkAnalyser
from .opendrive2lanelet.opendriveparser.parser import parse_opendrive
from .utils.network_utils import Network


class OpendriveNetwokAnalyser(BaseNetworkAnalyser):
    def analyse_all_data(self, network_data, params: dict = None):
        step_length = params["step_length"]
        lane_types = params["lane_types"]

        opendrive = parse_opendrive(network_data)

        network = Network(opendrive)
        network.convert_network(step_length)

        return network, lane_types




        # links = [
        #     Link(
        #         id=link.id,
        #         points=list(link.line.coords),
        #         lane_count=link.lane_count,
        #         name=f"{link.type}: {link.name}"
        #     )
        #     for link_id, link in links_data.items()
        # ]
        # connectors = [
        #     Connector(
        #         from_link_id=connector.from_link_id,
        #         to_link_id=connector.to_link_id,
        #         from_lane_numbers=connector.from_lane_number,
        #         to_lane_numbers=connector.to_lane_number,
        #     )
        #     for connector in connectors_data
        # ]
        #
        # # 更新中心点
        # self.center_point = [-other_data["move_distance"]["x_move"], -other_data["move_distance"]["y_move"]]
        # # 更新投影
        # self.proj_string = other_data["proj_string"]

        # links, connectors = [], []
        #
        # return {
        #     "links": links,
        #     "connectors": connectors,
        # }
