from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class LinkGroupsSearcher:
    def __init__(self, netiface, existing_network_data: dict, ignore_lane_type: bool, ignore_missing_connector: bool, max_length: float):
        self.netiface = netiface
        # 读取的路网数据
        self.existing_links_data = existing_network_data["links"]
        self.existing_connectors_data = existing_network_data["connectors"]
        self.existing_connector_areas_data = existing_network_data["connector_areas"]
        # 合并参数
        self.ignore_lane_type = ignore_lane_type
        self.ignore_missing_connector = ignore_missing_connector
        self.max_length = max_length

    def get_link_groups(self, ) -> dict:
        link_groups = []
        # 已经查找过的路段ID
        exist_links = []

        for link_id, link_data in pgd.progress(self.existing_links_data.items(), "可合并路段搜索中（1/6）"):
            # 已经查找过了
            if link_id in exist_links:
                continue

            link_group = [link_id]
            self._get_chain_by_next(link_id, link_group)
            self._get_chain_by_last(link_id, link_group)

            if len(link_group) >= 2:
                # 限制最大长度
                temp_link_groups = self._limit_link_length(link_group, self.max_length)
                link_groups.extend(temp_link_groups)
            # 将一组路段ID加到已经查找过的列表中
            exist_links.extend(link_group)

        # 判断是否有路段进行过重复查询，如果有，说明逻辑存在漏洞
        if len(exist_links) != len(set(exist_links)):
            print("出现唯一性错误，请联系开发者！")
            return dict()

        return {
            index: link_groups
            for index, link_groups in enumerate(link_groups, start=10000)
        }

    # 向下游搜索
    def _get_chain_by_next(self, link_id: int, link_group: list) -> None:
        # 本路段只有一个下游路段
        next_link_ids = self.existing_links_data[link_id]["next_link_ids"]
        if len(next_link_ids) == 1:
            next_link_id = next_link_ids[0]
            # 下游路段没有搜索过：如果有说明形成了回路
            if next_link_id not in link_group:
                is_connectible = self._get_is_connectible(link_id, next_link_id)
                # 如果可合并
                if is_connectible:
                    link_group.append(next_link_id)
                    self._get_chain_by_next(next_link_id, link_group)

    # 向上游搜索
    def _get_chain_by_last(self, link_id: int, link_group: list) -> None:
        # 本路段只有一个上游路段
        last_link_ids = self.existing_links_data[link_id]["last_link_ids"]
        if len(last_link_ids) == 1:
            last_link_id = last_link_ids[0]
            # 上游路段没有搜索过：如果有说明形成了回路
            if last_link_id not in link_group:
                is_connectible = self._get_is_connectible(last_link_id, link_id)
                # 如果可合并
                if is_connectible:
                    link_group.insert(0, last_link_id)
                    self._get_chain_by_last(last_link_id, link_group)

    # 判断是否可连接
    def _get_is_connectible(self, fist_link_id: int, second_link_id: int) -> bool:
        # 上游路段只有一个下游路段
        fist_link_next_link_ids = self.existing_links_data[fist_link_id]["next_link_ids"]
        if len(fist_link_next_link_ids) != 1:
            return False

        # 下游路段只有一个上游路段
        second_link_last_link_ids = self.existing_links_data[second_link_id]["last_link_ids"]
        if len(second_link_last_link_ids) != 1:
            return False

        # 车道数需要相同
        first_link_data: dict = self.existing_links_data[fist_link_id]
        second_link_data: dict = self.existing_links_data[second_link_id]
        first_link_lane_count = first_link_data["lane_count"]
        second_link_lane_count = second_link_data["lane_count"]
        if first_link_lane_count != second_link_lane_count:
            return False

        # 各车道类型相同
        first_link_lane_actions = first_link_data["lane_type_list"]
        second_link_lane_actions = second_link_data["lane_type_list"]
        if not self.ignore_lane_type and first_link_lane_actions != second_link_lane_actions:
            return False

        # 车道连接的数量不能缺失
        connector_data = self.existing_connectors_data[(fist_link_id, second_link_id)]
        connector_lane_count = connector_data["lane_count"]
        if connector_lane_count != first_link_lane_count:
            if not self.ignore_missing_connector:
                return False
            # 在实际的合并阶段再处理连接段缺失

        # 即使路段只有一个上游，连接段所属面域中存在多个连接段，仍然不允许合并
        connector_id = connector_data["connector_id"]
        for value in self.existing_connector_areas_data.values():
            if connector_id in value and len(value) >= 3:
                if "非机动车道" in first_link_lane_actions:
                    logger.logger_pytessng.debug(f"Warning: 面域内连接段过多, 进入交叉口区域, 不再继续: {value}")
                    return False
                else:
                    logger.logger_pytessng.debug(f"IgnoreWarning: 面域内连接段过多, 但是还要继续: {value}")
        return True

    # 限制一组路段的长度
    def _limit_link_length(self, link_group: list, max_link_length: float) -> list:
        first_link_id = link_group[0]
        first_link_data: dict = self.existing_links_data[first_link_id]
        first_link_length = first_link_data["length"]

        link_groups = []
        current_link_group = [first_link_id]

        current_length = first_link_length
        for i in range(1, len(link_group)):
            # 连接段长度
            from_link_id = link_group[i - 1]
            link_id = link_group[i]
            connector_data = self.existing_connectors_data[(from_link_id, link_id)]
            connector_length = connector_data["length"]
            # 路段长度
            link_data: dict = self.existing_links_data[link_id]
            link_length = link_data["length"]

            if current_length + connector_length + link_length <= max_link_length:
                current_link_group.append(link_id)
            else:
                link_groups.append(current_link_group.copy())
                current_link_group.clear()

        # 把最后一组加入列表
        link_groups.append(current_link_group)

        # 排除长度小于1的组
        link_groups = [link_group for link_group in link_groups if len(link_group) > 1]

        return link_groups
