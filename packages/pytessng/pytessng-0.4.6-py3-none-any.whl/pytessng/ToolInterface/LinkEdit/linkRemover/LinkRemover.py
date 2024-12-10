from typing import Union, Callable
from shapely.geometry import LineString, Polygon
from PySide2.QtCore import QPointF

from ..BaseLinkEditor import BaseLinkEditor
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class LinkRemover(BaseLinkEditor):
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
        remove_links = []
        for link in self.netiface.links():
            # 全框住
            if mode == 1:
                line = LineString(self._qtpoint2list(link.polygon()))
                # 检查多段线是否在多边形内
                is_within = line.within(polygon)
                if is_within:
                    remove_links.append(link)
            # 部分框住
            else:
                for lane in link.lanes():
                    line = LineString(self._qtpoint2list(lane.centerBreakPoints()))
                    # 检查多段线是否与多边形相交
                    is_within = line.intersects(polygon)
                    if is_within:
                        remove_links.append(link)
                        break
        # 高亮路段
        highlight_function(remove_links)

        # ========================================
        # 要删除的路段数
        link_count = len(remove_links)
        # 如果选中了
        if link_count > 0:
            # 弹出确认框
            confirm = confirm_function(len(remove_links), mode)
            # 如果确认了
            if confirm:
                # 删除路段
                for remove_link in pgd.progress(remove_links, "路段删除中"):
                    self.netiface.removeLink(remove_link)
                logger.logger_pytessng.info(f"{link_count} links have been removed.")
                # 还原画布
                restore_function()
                return None

        # 还原画布
        restore_function()

        return 0
