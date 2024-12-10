from ..BaseLinkEditor import BaseLinkEditor
from ...public.line.LineBase import LineBase
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class LinkRecalculator(BaseLinkEditor):
    def edit(self, mode: int) -> None:

        links_data = {
            link.id(): self.get_new_points(link, mode)
            for link in pgd.progress(self.netiface.links(), "路段新点位计算中（1/2）")
        }
        self.network_updater(self.netiface).update_links_points(links_data, pgd_index=2)

    def get_new_points(self, link, mode: int):
        # mode = 1: 通过路段左右边线计算
        # mode = 2: 使用居中的车道中线/边线

        lanes_points = [
            {
                "left": self._qtpoint2list(lane.leftBreakPoint3Ds()),
                "center": self._qtpoint2list(lane.centerBreakPoint3Ds()),
                "right": self._qtpoint2list(lane.rightBreakPoint3Ds()),
            }
            for lane in link.lanes()
        ]

        if mode == 1:
            left_points = lanes_points[-1]["left"]
            right_points = lanes_points[0]["right"]
            new_center_points = LineBase.calculate_merged_line_of_two_lines(left_points, right_points)
        else:
            mid = len(lanes_points) // 2
            # 如果车道数是奇数 使用中间车道的中线
            if len(lanes_points) % 2 == 1:
                new_center_points = lanes_points[mid]["center"]
            # 如果车道数是偶数 使用偏中间车道的右边线
            else:
                new_center_points = lanes_points[mid]["right"]

        return {
            "points": new_center_points,
            "lanes_points": lanes_points,
        }
