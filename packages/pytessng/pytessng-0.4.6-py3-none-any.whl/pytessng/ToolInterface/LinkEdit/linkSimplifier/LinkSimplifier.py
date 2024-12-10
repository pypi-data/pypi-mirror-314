from ..BaseLinkEditor import BaseLinkEditor
from ...public.line.LinePointsSimplifier import LinkPointsSimplifier
from pytessng.Config import LinkEditConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class LinkSimplifier(BaseLinkEditor):
    def edit(self, max_distance: float = LinkEditConfig.Simplifier.DEFAULT_MAX_DISTANCE, max_length: float = LinkEditConfig.Simplifier.DEFAULT_MAX_LENGTH) -> None:
        new_links_data = {}

        total_count_points, total_count_new_points = 0, 0
        messages = []

        # 获取当前路段
        for link in pgd.progress(self.netiface.links(), "路段新点位计算中（1/2）"):
            link_id = link.id()
            # 路段点位
            points = self._qtpoint2list(link.centerBreakPoint3Ds())
            # 点位数
            count_points = len(points)
            total_count_points += count_points
            # 车道点位
            lanes_points = [
                {
                    "left": self._qtpoint2list(lane.leftBreakPoint3Ds()),
                    "center": self._qtpoint2list(lane.centerBreakPoint3Ds()),
                    "right": self._qtpoint2list(lane.rightBreakPoint3Ds()),
                }
                for lane in link.lanes()
            ]
            # 简化点位
            new_points, new_lanes_points = LinkPointsSimplifier.simplify_link(points, lanes_points, max_distance, max_length)
            # 点位数
            count_new_points = len(new_points)
            total_count_new_points += count_new_points

            new_links_data[link_id] = {
                'points': new_points,
                'lanes_points': new_lanes_points,
            }
            messages.append(f"link {link_id}: {count_points} -> {count_new_points}")
        messages.append(f"Total count of points: {total_count_points} -> {total_count_new_points}")

        # 更新点位
        self.network_updater(self.netiface).update_links_points(new_links_data, pgd_index=2)

        logger.logger_pytessng.info("Simplify message:\n\t" + "\n\t".join(messages))
