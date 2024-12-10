from ..BaseUI import BaseClass
from .DesiredSpeedDecisionPointCreator import DesiredSpeedDecisionPointCreator
from pytessng.GlobalVar import GlobalVar


class DesiredSpeedDecisionPoint(BaseClass):
    name: str = "期望速度决策点"

    def load(self):
        # 修改按钮为【取消工具】
        self.guiiface.actionNullGMapTool().trigger()

        # 添加MyNet观察者
        desired_speed_decision_point_creator = DesiredSpeedDecisionPointCreator()
        GlobalVar.attach_observer_of_my_net(desired_speed_decision_point_creator)
