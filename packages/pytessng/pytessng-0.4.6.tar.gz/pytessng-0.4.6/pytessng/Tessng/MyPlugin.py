from typing import Optional

from pytessng.DLLs.Tessng import TessPlugin
from pytessng.Tessng.MyNet import MyNet
from pytessng.Tessng.MySimulator import MySimulator
from pytessng.UserInterface import MyMenu
from pytessng.GlobalVar import GlobalVar


class MyPlugin(TessPlugin):
    def __init__(self):
        super(MyPlugin, self).__init__()
        # 路网
        self.my_net: Optional[MyNet] = None
        # 仿真
        self.my_simulator: Optional[MySimulator] = None
        # 界面
        self.my_menu: Optional[MyMenu] = None

    # 重写方法，在TESSNG工厂类创建TESSNG对象时调用
    def init(self):
        # 路网
        self.my_net = MyNet()
        GlobalVar.attach_observer_of_my_net = self.my_net.attach_observer
        GlobalVar.detach_observer_of_my_net = self.my_net.detach_observer
        # 仿真
        self.my_simulator = MySimulator()
        GlobalVar.attach_observer_of_my_simulator = self.my_simulator.attach_observer
        GlobalVar.detach_observer_of_my_simulator = self.my_simulator.detach_observer
        # 界面
        self.my_menu = MyMenu()
        GlobalVar.actions_related_to_mouse_event = self.my_menu.actions_related_to_mouse_event
        GlobalVar.actions_only_official_version = self.my_menu.actions_only_official_version

    # 重写方法：返回插件路网子接口
    def customerNet(self):
        return self.my_net

    # 重写方法：返回插件仿真子接口
    def customerSimulator(self):
        return self.my_simulator
