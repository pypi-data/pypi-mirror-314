from pytessng.DLLs.Tessng import PyCustomerSimulator


class MySimulator(PyCustomerSimulator):
    def __init__(self):
        super().__init__()
        # 当前观察者字典
        self._observers: dict = dict()

    # 自定义方法：添加观察者
    def attach_observer(self, observer_name: str, observer_obj):
        self._observers[observer_name] = observer_obj

    # 自定义方法：移除观察者
    def detach_observer(self, observer_name: str):
        self._observers.pop(observer_name, None)

    # 重写方法：每次仿真前执行
    def beforeStart(self, ref_keep_on: bool):
        for observer in self._observers.values():
            observer.ready()

    # 重写方法：每帧仿真后执行
    def afterOneStep(self):
        for observer in self._observers.values():
            observer.operate()

    # 重写方法：每次仿真后执行
    def afterStop(self):
        for observer in self._observers.values():
            observer.finish()
