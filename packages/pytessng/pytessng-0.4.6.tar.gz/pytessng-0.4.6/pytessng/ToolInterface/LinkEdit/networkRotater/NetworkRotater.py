import math

from ..BaseLinkEditor import BaseLinkEditor
from pytessng.Logger import logger


class NetworkRotater(BaseLinkEditor):
    def edit(self, angle: float) -> None:
        # 将角度转换为弧度
        angle_radians = math.radians(angle)

        # 旋转路网
        links_data = {
            link.id(): self.get_new_points(link, angle_radians)
            for link in self.netiface.links()
        }
        self.network_updater(self.netiface).update_links_points(links_data)

        logger.logger_pytessng.info(f"旋转路网：[{angle:.2f}°]")

    def get_new_points(self, link, angle_radians: float):
        new_center_points = self.rotate_line(self._qtpoint2list(link.centerBreakPoint3Ds()), angle_radians)
        new_lanes_points = [
            {
                "left": self.rotate_line(self._qtpoint2list(lane.leftBreakPoint3Ds()), angle_radians),
                "center": self.rotate_line(self._qtpoint2list(lane.centerBreakPoint3Ds()), angle_radians),
                "right": self.rotate_line(self._qtpoint2list(lane.rightBreakPoint3Ds()), angle_radians),
            }
            for lane in link.lanes()
        ]

        return {
            "points": new_center_points,
            "lanes_points": new_lanes_points,
        }

    def rotate_line(self, line: list, angle_radians: float):
        for point in line:
            point[:2] = self.rotate_point(point[0], point[1], angle_radians)
        return line

    def rotate_point(self, x: float, y: float, angle_radians: float):
        # 计算顺时针旋转后的新坐标
        x_new = x * math.cos(angle_radians) + y * math.sin(angle_radians)
        y_new = -x * math.sin(angle_radians) + y * math.cos(angle_radians)
        return x_new, y_new
