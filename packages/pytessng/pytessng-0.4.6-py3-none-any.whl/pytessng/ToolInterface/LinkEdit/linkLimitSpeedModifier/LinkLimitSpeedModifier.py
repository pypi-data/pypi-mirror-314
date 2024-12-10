from ..BaseLinkEditor import BaseLinkEditor
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class LinkLimitSpeedModifier(BaseLinkEditor):
    def edit(self, limit_speed: float) -> None:
        for link in pgd.progress(self.netiface.links(), "路段限速更改中（1/1）"):
            link.setLimitSpeed(limit_speed)
