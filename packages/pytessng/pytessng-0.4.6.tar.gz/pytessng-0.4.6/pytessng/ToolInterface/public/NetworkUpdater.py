import traceback

from ..BaseTool import BaseTool
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class NetworkUpdater(BaseTool):
    # 更新路段点位
    def update_links_points(self, links_data: dict, pgd_index: int = 1) -> None:
        for link_id, link_data in pgd.progress(links_data.items(), f"路段点位更新中({pgd_index}/{pgd_index})"):
            link = self.netiface.findLink(link_id)
            if link:
                new_points = self._list2qtpoint(link_data["points"])
                new_lanes_points = [
                    {
                        "left": self._list2qtpoint(lane_points["left"]),
                        "center": self._list2qtpoint(lane_points["center"]),
                        "right": self._list2qtpoint(lane_points["right"]),
                    }
                    for lane_points in link_data["lanes_points"]
                ]

                try:
                    self.netiface.updateLinkAndLane3DWithPoints(link, new_points, new_lanes_points)
                except:
                    traceback.print_exc()
