from PySide2.QtCore import QPointF

from ..BaseLinkEditor import BaseLinkEditor


class ConnectorRecalculator(BaseLinkEditor):
    def edit(self) -> None:
        links = self.netiface.links()
        move = QPointF(0, 0)
        self.netiface.moveLinks(links, move)
