from ..BaseLinkEditor import BaseLinkEditor


class LinkCreator(BaseLinkEditor):
    def edit(self, lane_count: int, lane_width: float, lane_points: str) -> None:
        points = [
            point.split(",")
            for point in lane_points.split(";")
        ]
        lanes_width = [
            lane_width
            for _ in range(lane_count)
        ]

        # 路段数据
        links_data = [
            {
                'id': "new",
                'points': points,
                'lanes_width': lanes_width,
            }
        ]

        # 路网数据
        network_data = {"links": links_data}

        # 创建路网
        self.network_creator(self.netiface, pgd_indexes=(1, 1)).create_network(network_data)
