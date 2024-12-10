from typing import List

from ..BaseLinkEditor import BaseLinkEditor


class LinkAttrsModifier(BaseLinkEditor):
    def edit(self, link_id: int, elevations: List[float], lane_action_type_list: List[str]) -> None:
        # 获取路段对象
        link_obj = self.netiface.findLink(link_id)

        # 更改车道类型
        link_obj.setLaneTypes(lane_action_type_list)

        # 更改路段高程
        elevation_start_point, elevation_end_point = elevations
        current_elevation_start_point: float = link_obj.centerBreakPoint3Ds()[0].z()
        current_elevation_end_point: float = link_obj.centerBreakPoint3Ds()[-1].z()
        link_length = link_obj.length()
        # 有修改才更新高程
        if elevation_start_point != current_elevation_start_point or elevation_end_point != current_elevation_end_point:
            link_points = link_obj.centerBreakPoints()
            dist_to_start_list = [link_obj.distToStartPoint(point) for point in link_points]
            dist_to_start_list = [dist_to_start / link_length for dist_to_start in dist_to_start_list]
            # 根据dist_to_start对高程进行插值
            elevations = [
                elevation_start_point + (elevation_end_point - elevation_start_point) * dist_to_start
                for dist_to_start in
                dist_to_start_list
            ]
            self.netiface.updateLinkV3z(link_obj, elevations)
