from PySide2.QtCore import QPointF
from ..BaseLinkEditor import BaseLinkEditor
from ...public.line.LinePointsDivider import LinkPointsDivider
from ...public.line.LinePointsSplitter import LinkPointsSplitter
from pytessng.Config import LinkEditConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class LinkSplitter(BaseLinkEditor):
    def edit(self, link_id: int, pos: QPointF, min_connector_length: float = LinkEditConfig.DEFAULT_MIN_CONNECTOR_LENGTH) -> None:
        # 模拟进度条
        pgd().update_progress(0, 100, "数据解析中（1/3）")

        # 定位时距离的阈值
        DIST = LinkEditConfig.Locator.DIST

        # TESSNG坐标 (已经取负) (不需要转换比例尺)
        split_pos_x, split_pos_y = pos.x(), pos.y()
        point = QPointF(split_pos_x, split_pos_y)

        # 定位路段
        self.netiface.buildNetGrid(5)
        locations = self.netiface.locateOnCrid(point, 9)
        for location in locations:
            lane = location.pLaneObject
            if lane.isLane() and lane.link().id() == link_id:
                leastDist = location.leastDist
                if leastDist < DIST:
                    dist_to_start = self._p2m(location.distToStart)
                    location_x, location_y = location.point.x(), location.point.y()

                    message = f"""Split message:
                    \r\tThe ID of the nearest link is: [{link_id}]
                    \r\tThe coordinate of the clicked point is：({split_pos_x:.2f}, {split_pos_y:.2f})
                    \r\tThe coordinate of the searched point is：({location_x:.2f}, {location_y:.2f})
                    \r\tThe distance between the two points is：{leastDist:.2f}m"""

                    logger.logger_pytessng.info(message)

                    self.apply_split(link_id, dist_to_start, min_connector_length)
                    break

    def apply_split(self, link_id: int, distToStart: float, min_connector_length: float):
        # 模拟进度条
        pgd().update_progress(10, 100, "数据解析中（1/3）")

        link = self.netiface.findLink(link_id)

        # 获取新路段数据
        new_links_data = self.get_new_links_data(link, distToStart, min_connector_length)
        # 模拟进度条
        pgd().update_progress(60, 100, "数据解析中（1/3）")

        # 获取新连接段数据
        new_connectors_data = self.get_new_connector_data(link)
        # 模拟进度条
        pgd().update_progress(90, 100, "数据解析中（1/3）")

        # 创建新路段和连接段
        network_data = {
            "links": new_links_data,
            "connectors": new_connectors_data
        }
        result_create_links = self.network_creator(
            self.netiface,
            pgd_indexes=(2, 3)
        ).create_network(network_data, update_scene_size=False)

        # 是否所有路段都创建成功
        self.delete_links(link, result_create_links)

    # 获取新路段信息：裁剪
    def get_new_links_data(self, link, distToStart: float, min_connector_length: float) -> list:
        # 路段名称
        link_name = link.name()

        # 路段限速
        link_limit_speed = link.limitSpeed()

        # 路段车道类型
        lanes_type = [
            lane.actionType()
            for lane in link.lanes()
        ]

        # 路段点位
        points = self._qtpoint2list(link.centerBreakPoint3Ds())
        # 车道点位
        lanes_points = [
            {
                "left": self._qtpoint2list(lane.leftBreakPoint3Ds()),
                "center": self._qtpoint2list(lane.centerBreakPoint3Ds()),
                "right": self._qtpoint2list(lane.rightBreakPoint3Ds()),
            }
            for lane in link.lanes()
        ]

        divided_points, divided_lanes_points = LinkPointsDivider.divide_link(points, lanes_points, [distToStart])
        first_half_points, second_half_points = divided_points
        first_half_lanes_points, second_half_lanes_points = divided_lanes_points

        first_half_points, first_half_lanes_points = LinkPointsSplitter.split_link(first_half_points, first_half_lanes_points, min_connector_length / 2, 1)
        second_half_points, second_half_lanes_points = LinkPointsSplitter.split_link(second_half_points, second_half_lanes_points, min_connector_length / 2, 0)

        first_link = {
            "id": "new_1",
            "points": first_half_points,
            "lanes_points": first_half_lanes_points,
            "lanes_type": lanes_type,
            "limit_speed": link_limit_speed,
            "name": link_name,
        }
        second_link = {
            "id": "new_2",
            "points": second_half_points,
            "lanes_points": second_half_lanes_points,
            "lanes_type": lanes_type,
            "limit_speed": link_limit_speed,
            "name": link_name,
        }
        new_links_data = [first_link, second_link]

        return new_links_data

    # 获取新连接段信息：记录上下游连接关系
    def get_new_connector_data(self, link) -> list:
        new_connectors_data = []

        # 本路段
        lane_numbers = [
            lane.number() + 1
            for lane in link.lanes()
        ]
        new_connectors_data.append({
            "from_link_id": "new_1",
            "to_link_id": "new_2",
            "from_lane_numbers": lane_numbers,
            "to_lane_numbers": lane_numbers,
        })

        # 上游连接段
        for from_connector in link.fromConnectors():
            from_link = from_connector.fromLink()
            from_link_id = from_link.id()
            from_lane_numbers = sorted([
                lane_connector.fromLane().number() + 1
                for lane_connector in from_connector.laneConnectors()
            ])
            to_lane_numbers = sorted([
                lane_connector.toLane().number() + 1
                for lane_connector in from_connector.laneConnectors()
            ])
            new_connectors_data.append({
                "from_link_id": from_link_id,
                "to_link_id": "new_1",
                "from_lane_numbers": from_lane_numbers,
                "to_lane_numbers": to_lane_numbers,
            })

        # 下游连接段
        for to_connector in link.toConnectors():
            to_link = to_connector.toLink()
            to_link_id = to_link.id()
            from_lane_numbers = sorted([
                lane_connector.fromLane().number() + 1
                for lane_connector in to_connector.laneConnectors()
            ])
            to_lane_numbers = sorted([
                lane_connector.toLane().number() + 1
                for lane_connector in to_connector.laneConnectors()
            ])
            new_connectors_data.append({
                "from_link_id": "new_2",
                "to_link_id": to_link_id,
                "from_lane_numbers": from_lane_numbers,
                "to_lane_numbers": to_lane_numbers,
            })

        return new_connectors_data

    # 删除原路段
    def delete_links(self, link, result_create_links: dict) -> None:
        if all(result_create_links.values()):
            # 如果路段创建成功，则删除原路段
            self.netiface.removeLink(link)
        else:
            # 如果部分路段创建成功，则删除新创建的连接段
            for link_id in result_create_links.values():
                if link_id:
                    link = self.netiface.findLink(link_id)
                    self.netiface.removeLink(link)
