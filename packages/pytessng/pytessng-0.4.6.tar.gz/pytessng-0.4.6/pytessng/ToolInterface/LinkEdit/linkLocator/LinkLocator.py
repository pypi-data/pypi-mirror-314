from typing import List, Union
from PySide2.QtCore import QPointF

from ..BaseLinkEditor import BaseLinkEditor
from ...public.line.LinePointGetter import LinePointGetter
from pytessng.Config import LinkEditConfig


class LinkLocator(BaseLinkEditor):
    def edit(self, pos: QPointF, in_detail: bool = False) -> List[Union[int, dict]]:
        DIST = LinkEditConfig.Locator.DIST

        # 网格化
        self.netiface.buildNetGrid(5)

        # 路段ID集合
        link_id_set: set = set()
        # 路段数据列表
        link_data: list = []

        # 找到一定距离之内的车道所在路段的ID
        locations = self.netiface.locateOnCrid(pos, 9)
        for location in locations:
            dist = self._p2m(location.leastDist)
            lane = location.pLaneObject
            if not (dist < DIST and lane.isLane()):
                continue
            link = lane.link()
            link_id = int(link.id())
            if link_id in link_id_set:
                continue
            link_id_set.add(link_id)
            if not in_detail:
                link_data.append(link_id)
            else:
                dist_to_start = self._p2m(location.distToStart)
                index = location.segmIndex
                angle = location.angle
                points = self._qtpoint2list(link.centerBreakPoints())
                point = LinePointGetter.get_point_by_dist(points, dist_to_start)
                link_data.append({
                    "link_id": link_id,
                    "index": index,
                    "point": point,
                    "angle": angle,
                    "dist_to_start": dist_to_start,
                })

        return link_data
