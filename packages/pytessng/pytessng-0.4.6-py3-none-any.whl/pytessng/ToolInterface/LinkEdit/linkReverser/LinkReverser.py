from typing import Union, Callable
from shapely.geometry import LineString, Polygon
from PySide2.QtCore import QPointF

from ..BaseLinkEditor import BaseLinkEditor
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class LinkReverser(BaseLinkEditor):
    def edit(self, p1: QPointF, p2: QPointF, confirm_function: Callable, highlight_function: Callable, restore_function: Callable) -> Union[None, int]:
        x1, y1 = self._p2m(p1.x()), -self._p2m(p1.y())
        x2, y2 = self._p2m(p2.x()), -self._p2m(p2.y())

        mode = 1 if x1 < x2 else 2  # 1:全部框住, 2:部分框住

        left, right = sorted([x1, x2])
        bottom, top = sorted([y1, y2])

        # 定义多边形
        polygon = Polygon([(left, bottom), (right, bottom), (right, top), (left, top)])

        # ========================================
        # 判断哪些路段在框内
        reverse_links = []
        for link in self.netiface.links():
            # 全框住
            if mode == 1:
                line = LineString(self._qtpoint2list(link.polygon()))
                # 检查多段线是否在多边形内
                is_within = line.within(polygon)
                if is_within:
                    reverse_links.append(link)
            # 部分框住
            else:
                for lane in link.lanes():
                    line = LineString(self._qtpoint2list(lane.centerBreakPoints()))
                    # 检查多段线是否与多边形相交
                    is_within = line.intersects(polygon)
                    if is_within:
                        reverse_links.append(link)
                        break
        # 高亮路段
        highlight_function(reverse_links)

        # ========================================
        # 要反转的路段数
        link_count = len(reverse_links)
        # 如果选中了
        if link_count > 0:
            # 弹出确认框
            confirm = confirm_function(len(reverse_links), mode)
            # 如果确认了
            if confirm:
                # 反转路段
                links_data = {
                    reverse_link.id(): self.get_reverse_points(reverse_link)
                    for reverse_link in pgd.progress(reverse_links, "路段新点位计算中")
                }
                # 更新点位
                self.network_updater(self.netiface).update_links_points(links_data)
                logger.logger_pytessng.info(f"{link_count} links have been reversed.")
                # 还原画布
                restore_function()
                return None

        # 还原画布
        restore_function()

        return 0

    # 反转路段
    def get_reverse_points(self, link):
        center_points = self._qtpoint2list(link.centerBreakPoint3Ds())
        lanes_points = [
            {
                "left": self._qtpoint2list(lane.leftBreakPoint3Ds()),
                "center": self._qtpoint2list(lane.centerBreakPoint3Ds()),
                "right": self._qtpoint2list(lane.rightBreakPoint3Ds()),
            }
            for lane in link.lanes()
        ]

        new_center_points = center_points[::-1]
        new_lanes_points = [
            {
                "left": lane_points["right"][::-1],
                "center": lane_points["center"][::-1],
                "right": lane_points["left"][::-1],
            }
            for lane_points in lanes_points[::-1]
        ]

        return {
            "points": new_center_points,
            "lanes_points": new_lanes_points,
        }
