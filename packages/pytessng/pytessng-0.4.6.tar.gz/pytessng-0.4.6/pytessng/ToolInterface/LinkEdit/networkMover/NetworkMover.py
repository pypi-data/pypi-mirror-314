from PySide2.QtCore import QPointF

from ..BaseLinkEditor import BaseLinkEditor
from pytessng.Logger import logger


class NetworkMover(BaseLinkEditor):
    def edit(self, move_to_center: bool, x_move: float, y_move: float) -> None:
        # 移动路网
        links = self.netiface.links()

        if move_to_center:
            # 计算路网中心点
            xs, ys = [], []
            for link in links:
                points = self._qtpoint2list(link.centerBreakPoint3Ds())
                xs.extend([p[0] for p in points])
                ys.extend([p[1] for p in points])
            x_center, y_center = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
            x_move, y_move = -x_center, -y_center

        move = QPointF(self._m2p(x_move), -self._m2p(y_move))
        self.netiface.moveLinks(links, move)

        logger.logger_pytessng.info(f"移动路网：[横向距离为{x_move:.2f}m] [纵向距离为{y_move:.2f}m]")

        # 更新路网属性
        attrs = self.netiface.netAttrs().otherAttrs()
        if not attrs.get("move_distance"):
            attrs.update({"move_distance": {"x_move": 0, "y_move": 0}})
        attrs["move_distance"]["x_move"] += x_move
        attrs["move_distance"]["y_move"] += y_move
        network_name = self.netiface.netAttrs().netName()
        self.netiface.setNetAttrs(network_name, otherAttrsJson=attrs)

        # 更新场景大小
        self.update_scene_size()
