from ..BaseSimuExportActor import BaseSimuExportActor
from .SignalLightDataCalculator import SignalLightDataCalculator


class SimuExportSignalLightActor(BaseSimuExportActor):
    # 数据名称
    data_name: str = "信号灯数据"

    def _get_basic_data(self) -> dict:
        basic_signal_light_data = SignalLightDataCalculator.get_basic_signal_light_data(self._simuiface, self._netiface)
        return basic_signal_light_data

    def _get_complete_data(self, basic_data: dict) -> dict:
        SignalLightDataCalculator.get_complete_signal_light_data(basic_data, self._netiface)
        return basic_data
