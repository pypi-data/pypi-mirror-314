from ..BaseUI import BaseClass
from pytessng.ToolInterface import MyOperation


class LinkEditRecalculateC(BaseClass):
    name: str = "重新计算连接段中心线"
    mode: str = "recalculate_c"

    def load(self):
        MyOperation.apply_link_edit_operation(self, dict())
