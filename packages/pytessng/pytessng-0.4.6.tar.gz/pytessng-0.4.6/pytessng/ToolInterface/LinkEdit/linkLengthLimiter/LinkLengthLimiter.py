import numpy as np

from ..BaseLinkEditor import BaseLinkEditor
from ...public.line.LinePointsDivider import LinkPointsDivider
from ...public.line.LinePointsSplitter import LinkPointsSplitter
from pytessng.Config import LinkEditConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class LinkLengthLimiter(BaseLinkEditor):
    def __init__(self, netiface):
        super().__init__(netiface)
        self.existing_links_data = self.network_iterator(netiface).get_existing_links_data()

    def edit(self, max_link_length: float = LinkEditConfig.DEFAULT_MAX_LINK_LENGTH, min_connector_length: float = LinkEditConfig.DEFAULT_MIN_CONNECTOR_LENGTH) -> None:
        # 获取分割信息
        split_information = self.get_split_info(max_link_length)

        # 获取新的路段数据
        new_links_data, link_groups = self.get_new_links_data(split_information, min_connector_length)

        # 获取新的连接段数据
        new_connectors_data = self.get_new_connector_data(link_groups)

        # 路网数据
        network_data = {
            "links": new_links_data,
            "connectors": new_connectors_data
        }

        # 创建新的路段和连接段
        result_create_network = self.network_creator(
            self.netiface,
            pgd_indexes=(5, 7),
        ).create_network(network_data)

        # 根据创建情况删除路段，连接段自动删除
        self.delete_links(link_groups, result_create_network["links"])

    # 获取分割信息
    def get_split_info(self, max_link_length: float) -> dict:
        split_infos = dict()

        # 遍历路段找到过长路段
        for link in pgd.progress(self.netiface.links(), "过长路段搜索中（1/7）"):
            link_id = link.id()
            length = link.length()
            if length > max_link_length:
                num = int(np.ceil(length / max_link_length))
                mean_length = length / num
                split_infos[link_id] = [mean_length * k for k in range(1, num)]

        return split_infos

    # 获取新的路段数据
    def get_new_links_data(self, split_infos: dict, min_connector_length: float) -> (list, dict):
        new_links_data = []
        link_groups = {}

        # 遍历路段
        for link in pgd.progress(self.netiface.links(), "新路段点位计算中（2/7）"):
            link_id = link.id()
            if link_id not in split_infos:
                continue

            # 路段名称
            link_name = link.name()
            # 路段限速
            link_limitSpeed = link.limitSpeed()
            # 车道类型
            lane_types = [lane.actionType() for lane in link.lanes()]

            # 原始路段中心线点位
            points = self._qtpoint2list(link.centerBreakPoint3Ds())
            # 原始车道点位
            lanes_points = [
                {
                    "left": [point for point in self._qtpoint2list(link.lanes()[lane_number].leftBreakPoint3Ds())],
                    "center": [point for point in self._qtpoint2list(link.lanes()[lane_number].centerBreakPoint3Ds())],
                    "right": [point for point in self._qtpoint2list(link.lanes()[lane_number].rightBreakPoint3Ds())],
                }
                for lane_number in range(len(link.lanes()))
            ]

            # 分割的路段点位、车道点位
            dist_list = split_infos[link_id]
            divided_points, divided_lanes_points = LinkPointsDivider.divide_link(points, lanes_points, dist_list)

            link_groups[link_id] = []
            for i, (points, lanes_points) in enumerate(zip(divided_points, divided_lanes_points)):
                new_link_id = f"{link_id}-{i}"

                # 限制连接段的最短长度
                if i == 0:
                    modes = [1]
                    indexes = [0]
                elif i == len(divided_points) - 1:
                    modes = [0]
                    indexes = [1]
                else:
                    modes = [1, 0]
                    indexes = [0, 1]
                # 裁剪路段
                for mode, index in zip(modes, indexes):
                    points, lanes_points = LinkPointsSplitter.split_link(points, lanes_points, min_connector_length / 2, mode)

                new_links_data.append({
                    'id': new_link_id,
                    'points': points,
                    'lanes_points': lanes_points,
                    'lanes_type': lane_types,
                    'limit_speed': link_limitSpeed,
                    'name': link_name,
                })
                link_groups[link_id].append(new_link_id)
        
        return new_links_data, link_groups

    # 获取新的连接段数据
    def get_new_connector_data(self, link_groups: dict) -> list:
        new_connector_data = []

        # 新生成的各路段内部的连接段
        for link_id, link_group in pgd.progress(link_groups.items(), "新连接段记录中（3/7）"):
            link = self.netiface.findLink(link_id)
            lane_numbers = [
                lane.number() + 1
                for lane in link.lanes()
            ]
            for i in range(1, len(link_group)):
                from_link_id = link_group[i - 1]
                to_link_id = link_group[i]
                new_connector_data.append({
                    'from_link_id': from_link_id,
                    'to_link_id': to_link_id,
                    'from_lane_numbers': lane_numbers,
                    'to_lane_numbers': lane_numbers,
                })

        for link_id, link_group in pgd.progress(link_groups.items(), "新连接段记录中（4/7）"):
            # 原有的路段的上游的连接段
            for last_link_id in self.existing_links_data[link_id]["last_link_ids"]:
                connector = self.netiface.findConnectorByLinkIds(last_link_id, link_id)
                # 原有连接段名称
                connector_name = connector.name()
                # 上下游连接关系
                from_lane_numbers = [
                    lane_connector.fromLane().number() + 1
                    for lane_connector in connector.laneConnectors()
                ]
                to_lane_numbers = [
                    lane_connector.toLane().number() + 1
                    for lane_connector in connector.laneConnectors()
                ]
                connector_data = {
                    'from_link_id': link_groups.get(last_link_id, [last_link_id])[-1],
                    'to_link_id': link_group[0],
                    'from_lane_numbers': from_lane_numbers,
                    'to_lane_numbers': to_lane_numbers,
                    'name': connector_name,
                }
                if connector_data not in new_connector_data:
                    new_connector_data.append(connector_data)

            # 原有的路段的下游的连接段
            for next_link_id in self.existing_links_data[link_id]["next_link_ids"]:
                connector = self.netiface.findConnectorByLinkIds(link_id, next_link_id)
                # 原有连接段名称
                connector_name = connector.name()
                # 上下游连接关系
                from_lane_numbers = [
                    lane_connector.fromLane().number() + 1
                    for lane_connector in connector.laneConnectors()
                ]
                to_lane_numbers = [
                    lane_connector.toLane().number() + 1
                    for lane_connector in connector.laneConnectors()
                ]
                connector_data = {
                    'from_link_id': link_group[-1],
                    'to_link_id': link_groups.get(next_link_id, [next_link_id])[0],
                    'from_lane_numbers': from_lane_numbers,
                    'to_lane_numbers': to_lane_numbers,
                    'name': connector_name,
                }
                if connector_data not in new_connector_data:
                    new_connector_data.append(connector_data)

        return new_connector_data

    # 根据创建情况删除路段，连接段自动删除
    def delete_links(self, link_groups: dict, result_create_links: dict) -> None:
        messages = []
        for link_id, link_group in pgd.progress(link_groups.items(), "原有路段及连接段删除中（7/7）"):
            new_link_ids = [
                result_create_links[link_id_]
                for link_id_ in link_group
            ]

            # 如果全部路段创建成功，则删除原路段
            if all(new_link_ids):
                link = self.netiface.findLink(link_id)
                self.netiface.removeLink(link)
                messages.append(f"[{link_id}] -> {new_link_ids}")

            # 如果部分路段创建成功，则删除新创建的连接段
            else:
                for new_link_id in new_link_ids:
                    if new_link_id is not None:
                        link = self.netiface.findLink(new_link_id)
                        self.netiface.removeLink(link)
                messages.append(f"[{link_id}] failed to be divided")

        logger.logger_pytessng.info("Divide message:\n\t" + "\n\t".join(messages))
