import numpy as np

from ..BaseLinkEditor import BaseLinkEditor
from ...public.line.LinePointsSplitter import LinkPointsSplitter
from pytessng.Config import LinkEditConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class ConnectorLengthLimiter(BaseLinkEditor):
    def edit(self, min_connector_length: float = LinkEditConfig.DEFAULT_MIN_CONNECTOR_LENGTH) -> None:
        # 获取分割信息
        split_information, link_need_split_all = self.get_split_info(min_connector_length)

        # 获取新的路段数据
        new_links_data = self.get_new_links_data(split_information, link_need_split_all)

        # 更新点位
        self.network_updater(self.netiface).update_links_points(new_links_data, pgd_index=3)

    # 获取分割信息
    def get_split_info(self, min_connector_length: float) -> (dict, set):
        split_info = {
            "start": {},
            "end": {}
        }

        # 遍历连接段找到过短连接段
        too_short_connector_count = 0
        for connector in pgd.progress(self.netiface.connectors(), "过短连接段搜索中（1/3）"):
            # 根据车道连接的长度判断是否需要处理
            for lane_connector in connector.laneConnectors():
                lane_length = self._p2m(lane_connector.length())
                if lane_length < min_connector_length:
                    # 记录需要处理的路段信息
                    split_length = (min_connector_length - lane_length) / 2
                    from_link_id = connector.fromLink().id()
                    to_link_id = connector.toLink().id()
                    split_info["start"][to_link_id] = split_length
                    split_info["end"][from_link_id] = split_length
                    # 计数加一
                    too_short_connector_count += 1
                    break

        link_need_split_all = set(split_info["start"].keys()) | set(split_info["end"].keys())
        logger.logger_pytessng.info(f"Find {too_short_connector_count} too short connectors!")

        return split_info, link_need_split_all

    # 获取新的路段数据
    def get_new_links_data(self, split_information: dict, link_need_split_all: set) -> dict:
        new_link_data = {}

        # 遍历路段
        for link in pgd.progress(self.netiface.links(), "路段新点位计算中（2/3）"):
            link_id = link.id()
            if link_id not in link_need_split_all:
                continue

            # 路段点位：防止像OpenDrive一样道路中线不在中心线，所以需要重新计算
            link_points_left = np.array(self._qtpoint2list(link.leftBreakPoint3Ds()))
            link_points_right = np.array(self._qtpoint2list(link.rightBreakPoint3Ds()))
            points = ((link_points_left + link_points_right) / 2).tolist()

            # 车道点位
            lanes_points = [
                {
                    "left": self._qtpoint2list(lane.leftBreakPoint3Ds()),
                    "center": self._qtpoint2list(lane.centerBreakPoint3Ds()),
                    "right": self._qtpoint2list(lane.rightBreakPoint3Ds()),
                }
                for lane in link.lanes()
            ]

            # 裁剪
            if link_id in split_information["end"]:
                split_length = split_information["end"][link_id]
                points, lanes_points = LinkPointsSplitter.split_link(points, lanes_points, split_length, 1)
            if link_id in split_information["start"]:
                split_length = split_information["start"][link_id]
                points, lanes_points = LinkPointsSplitter.split_link(points, lanes_points, split_length, 0)

            new_link_data[link_id] = {
                'points': points,
                'lanes_points': lanes_points,
            }

        return new_link_data
