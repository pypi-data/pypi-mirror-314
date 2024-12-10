import itertools
from typing import List
import numpy as np

from ..BaseLinkEditor import BaseLinkEditor
from .LinkGroupsSearcher import LinkGroupsSearcher
from ...public.line.LineBase import LineBase
from ...public.line.LinePointsSimplifier import LinkPointsSimplifier
from pytessng.Config import LinkEditConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class LinkMerger(BaseLinkEditor):
    def __init__(self, netiface):
        super().__init__(netiface)
        network_iterator = self.network_iterator(netiface)
        # 现有路网数据
        self.existing_network_data = network_iterator.get_existing_network_data()
        # 现有路段数据
        self.existing_links_data = self.existing_network_data["links"]
        # 现有连接段数据
        self.existing_connectors_data = self.existing_network_data["connectors"]
        # 现有连接段面域数据
        self.existing_connector_areas_data = self.existing_network_data["connector_areas"]

    def edit(self,
             link_groups: List[List[int]],
             include_connector: bool = LinkEditConfig.Merger.DEFAULT_INCLUDE_CONNECTOR,
             simplify_points: bool = LinkEditConfig.Merger.DEFAULT_SIMPLIFY_POINTS,
             ignore_lane_type: bool = LinkEditConfig.Merger.DEFAULT_IGNORE_LANE_TYPE,
             ignore_missing_connector: bool = LinkEditConfig.Merger.DEFAULT_IGNORE_MISSING_CONNECTOR,
             max_length: float = LinkEditConfig.Merger.DEFAULT_MAX_LENGTH,
             ) -> None:
        # 没给合并路段就需要自行搜索
        if not link_groups:
            # 得到可以合并的路段的统计
            link_groups: dict = LinkGroupsSearcher(
                self.netiface, self.existing_network_data,
                ignore_lane_type, ignore_missing_connector, max_length,
            ).get_link_groups()

        # 记录新的路段数据
        new_links_data = self.get_new_links_data(link_groups, include_connector, simplify_points, ignore_lane_type, ignore_missing_connector)

        # 记录新的连接段数据
        new_connectors_data = self.get_new_connectors_data(link_groups)

        # 路网数据
        network_data = {
            "links": new_links_data,
            "connectors": new_connectors_data
        }
        # 创建新的路段和连接段
        result_create_network = self.network_creator(
            self.netiface,
            pgd_indexes=(4, 6),
        ).create_network(network_data, update_scene_size=False)

        # 删除旧有路段
        self.delete_links(link_groups, result_create_network["links"])

    # 获取新的路段数据
    def get_new_links_data(self, link_groups, include_connector: bool, simplify_points: bool, ignore_lane_type: bool, ignore_missing_connector: bool) -> list:
        new_links_data = []

        for new_link_id, link_group in pgd.progress(link_groups.items(), "新路段点位计算中（2/6）"):
            # 不需要包括连接段点位
            if not include_connector:
                # 获取道路对象
                links = [
                    self.netiface.findLink(link_id)
                    for link_id in link_group
                ]

                # 获取各车道点位
                lanes_points = [
                    {
                        "left": [
                            point
                            for link in links
                            for point in self._qtpoint2list(link.lanes()[lane_number].leftBreakPoint3Ds())
                        ],
                        "center": [
                            point
                            for link in links
                            for point in self._qtpoint2list(link.lanes()[lane_number].centerBreakPoint3Ds())
                        ],
                        "right": [
                            point
                            for link in links
                            for point in self._qtpoint2list(link.lanes()[lane_number].rightBreakPoint3Ds())
                        ],
                    }
                    for lane_number in range(len(links[0].lanes()))
                ]
            # 需要连接段点位
            else:
                # 获取道路对象
                links = []
                lane_count = -1
                for index in range(1, len(link_group)):
                    last_link_id = link_group[index - 1]
                    link_id = link_group[index]
                    if last_link_id == link_id:
                        continue
                    if not links:
                        link = self.netiface.findLink(last_link_id)
                        links.append(link)
                        lane_count: int = link.laneCount()

                    connector = self.netiface.findConnectorByLinkIds(last_link_id, link_id)
                    # 处理连接段的车道缺失
                    lane_connector_count = len(connector.laneConnectors())
                    if lane_connector_count != lane_count:
                        # 删除连接段
                        self.netiface.removeConnector(connector)
                        # 创建连接段
                        lane_numbers = [i + 1 for i in range(lane_count)]
                        connector = self.netiface.createConnector(last_link_id, link_id, lane_numbers, lane_numbers)

                    # 连接段长度不过短才加入
                    if connector.length() > 1:
                        links.append(connector)
                    else:
                        logger.logger_pytessng.warning(
                            f"The length of connector {connector.id()} is too short: {connector.length(): .2f}!")
                    link = self.netiface.findLink(link_id)
                    links.append(link)

                # 获取各车道点位
                lanes_points = [
                    {
                        "left": [],
                        "center": [],
                        "right": [],
                    }
                    for _ in range(len(links[0].lanes()))
                ]
                for road in links:
                    # 各车道对象
                    lanes = road.lanes() if road.isLink() else road.laneConnectors()
                    # 各车道的左右边线点位
                    for index, lane in enumerate(lanes):
                        qt_left_points = lane.leftBreakPoint3Ds()
                        qt_center_points = lane.centerBreakPoint3Ds()
                        qt_right_points = lane.rightBreakPoint3Ds()

                        left_points = self._qtpoint2list(qt_left_points)
                        center_points = self._qtpoint2list(qt_center_points)
                        right_points = self._qtpoint2list(qt_right_points)

                        if not (len(left_points) == len(center_points) == len(right_points)):
                            logger.logger_pytessng.warning(f"The length of left, center and right points of lane {index} of road {road.id()} is not equal!")
                            # center取left和right的中值
                            center_points = [
                                LineBase.calculate_interpolate_point_between_two_points(
                                    left_point, right_point, 0.5)
                                for left_point, right_point in zip(left_points, right_points)
                            ]
                        assert len(center_points) == len(left_points) == len(right_points)

                        lanes_points[index]["left"].extend(left_points)
                        lanes_points[index]["center"].extend(center_points)
                        lanes_points[index]["right"].extend(right_points)

            # 针对平面坐标进行去重
            unique_lanes_points = [
                {
                    "left": [],
                    "center": [],
                    "right": [],
                }
                for _ in range(len(lanes_points))
            ]
            # 车道数量
            lane_count = len(lanes_points)
            # 点的数量
            point_count = min([
                len(lanes_points[i]["center"])
                for i in range(lane_count)
            ])
            # 位置
            locations = list(lanes_points[0].keys())
            # 遍历点
            for index in range(point_count):
                for lane_number, location in itertools.product(range(lane_count), locations):
                    corresponding_points = unique_lanes_points[lane_number][location]
                    current_point = lanes_points[lane_number][location][index]

                    # 判断点是否为无效点
                    x, y = current_point[:2]
                    if np.isnan(x) or np.isnan(y):
                        logger.logger_pytessng.warning("Skip invalid point.")
                        break

                    # 判断是否有重复点
                    if not (not corresponding_points or (corresponding_points and current_point[:2] != corresponding_points[-1][:2])):
                        # 有重复点
                        logger.logger_pytessng.debug("Skip duplicate point.")
                        break

                # 说明没有重复点
                else:
                    for lane_number in range(lane_count):
                        for location in ["left", "center", "right"]:
                            corresponding_points = unique_lanes_points[lane_number][location]
                            current_point = lanes_points[lane_number][location][index]
                            corresponding_points.append(current_point)

            lanes_points = unique_lanes_points

            # 根据左右边线计算路段中心线
            left_points = lanes_points[-1]["left"]
            right_points = lanes_points[0]["right"]
            points = LineBase.calculate_merged_line_of_two_lines(left_points, right_points)

            # 点位简化
            if simplify_points:
                points, lanes_points = LinkPointsSimplifier.simplify_link(points, lanes_points, 0.3)

            # 车道类型
            if ignore_lane_type:
                lanes_type = [
                    "机动车道"
                    for _ in links[0].lanes()
                ]
            else:
                lanes_type = [
                    lane.actionType()
                    for lane in links[0].lanes()
                ]
            # 路段限速
            limit_speed = self._p2m(links[0].limitSpeed())
            # 路段名称
            name = "-".join(set([
                link.name()
                for link in links
                if "-" not in link.name()
            ]))

            new_links_data.append({
                "id": new_link_id,
                "points": points,
                "lanes_points": lanes_points,
                "lanes_type": lanes_type,
                "limit_speed": limit_speed,
                "name": name,
            })

        return new_links_data

    # 获取新的连接段数据
    def get_new_connectors_data(self, link_groups: dict) -> list:
        new_connectors_data = []
        new_link_id_mapping = {
            link_id: new_link_id
            for new_link_id, link_group in link_groups.items()
            for link_id in link_group
        }

        for new_link_id, link_group in pgd.progress(link_groups.items(), "新连接段记录中（3/6）"):
            # 首路段上游的连接段
            start_link_id = link_group[0]
            last_link_ids = self.existing_links_data[start_link_id]["last_link_ids"]
            for last_link_id in last_link_ids:
                connector = self.netiface.findConnectorByLinkIds(last_link_id, start_link_id)
                # 连接段名称
                connector_name = connector.name()
                # 上游路段ID
                last_link_id = new_link_id_mapping.get(last_link_id, last_link_id)
                # 上下游连接关系
                from_lane_numbers = sorted([
                    laneConnector.fromLane().number() + 1
                    for laneConnector in connector.laneConnectors()
                ])
                to_lane_numbers = sorted([
                    laneConnector.toLane().number() + 1
                    for laneConnector in connector.laneConnectors()
                ])
                connectors_data = {
                    "from_link_id": last_link_id,
                    "to_link_id": new_link_id,
                    "from_lane_numbers": from_lane_numbers,
                    "to_lane_numbers": to_lane_numbers,
                    "name": connector_name,
                }
                if connectors_data not in new_connectors_data:
                    new_connectors_data.append(connectors_data)

            # 末路段上游的连接段
            end_link_id = link_group[-1]
            next_link_ids = self.existing_links_data[end_link_id]["next_link_ids"]
            for next_link_id in next_link_ids:
                connector = self.netiface.findConnectorByLinkIds(end_link_id, next_link_id)
                # 连接段名称
                connector_name = connector.name()
                # 下游路段ID
                next_link_id = new_link_id_mapping.get(next_link_id, next_link_id)
                # 上下游连接关系
                from_lane_numbers = sorted(
                    [laneConnector.fromLane().number() + 1
                     for laneConnector in connector.laneConnectors()
                     ])
                to_lane_numbers = sorted(
                    [laneConnector.toLane().number() + 1
                     for laneConnector in connector.laneConnectors()
                     ])
                connectors_data = {
                    "from_link_id": new_link_id,
                    "to_link_id": next_link_id,
                    "from_lane_numbers": from_lane_numbers,
                    "to_lane_numbers": to_lane_numbers,
                    "name": connector_name,
                }
                if connectors_data not in new_connectors_data:
                    new_connectors_data.append(connectors_data)

        return new_connectors_data

    # 删除旧有路段
    def delete_links(self, link_groups: dict, result_create_links: dict) -> None:
        messages = []
        for new_link_id, link_group in pgd.progress(link_groups.items(), "原有路段及连接段删除中（6/6）"):
            create_link_id = result_create_links[str(new_link_id)]

            # 如果创建成功了，删除原有路段
            if create_link_id:
                for link_id in link_group:
                    link = self.netiface.findLink(link_id)
                    if link is not None:
                        self.netiface.removeLink(link)
                messages.append(f"{link_group} -> [{create_link_id}]")
            else:
                messages.append(f"{link_group} failed to be merged")

        logger.logger_pytessng.info("Merge message:\n\t" + "\n\t".join(messages))
