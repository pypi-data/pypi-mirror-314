import time


class SignalLightDataCalculator:
    @staticmethod
    def get_basic_signal_light_data(simuiface, netiface) -> dict:
        # 当前已仿真时间，单位：毫秒
        simu_time = simuiface.simuTimeIntervalWithAcceMutiples()
        # 当前仿真计算批次
        batch_num = simuiface.batchNumber()

        signal_light_data = {
            "timestamp": int(time.time() * 1000),
            "simuTime": simu_time,
            "batchNum": batch_num,
            "data": dict(),  # 灯组相位：{相位名称：{}}
        }

        # 信号灯组
        signal_group_list: list = netiface.signalGroups()
        # 倒计时映射字典
        count_down_mapping: dict = {
            signal_phase_color.phaseId: int((signal_phase_color.mrIntervalSetted - signal_phase_color.mrIntervalByNow) / 1000)
            for signal_phase_color in simuiface.getSignalPhasesColor()
        }

        # 遍历各灯组
        for signal_group in signal_group_list:
            # 灯组名称
            group_name = signal_group.groupName()
            signal_group_data: dict = dict()

            # 灯组的各相位
            signal_phase_list = signal_group.phases()
            for signal_phase in signal_phase_list:
                # 相位ID
                phase_id = signal_phase.id()
                # 相位名称
                phase_name = signal_phase.phaseName()

                # 相位对应的灯头
                signal_lamp_list = signal_phase.signalLamps()
                # 该相位没有使用过
                if len(signal_lamp_list) == 0:
                    continue

                # 当前灯头颜色
                current_color = signal_lamp_list[0].color()

                # 倒计时，单位：秒
                count_down = count_down_mapping.get(phase_id, -1)
                count_down = min(count_down, 255)

                # 信号相位数据
                signal_phase_data = {
                    "curColor": current_color,
                    "countDown": count_down,
                    # "lampColor": lamp_color,
                    # "duration": duration,
                }
                signal_group_data[phase_name] = signal_phase_data

            signal_light_data["data"][group_name] = signal_group_data

        return signal_light_data

    # 获取完整的信号灯数据
    @staticmethod
    def get_complete_signal_light_data(basic_signal_light_data, netiface) -> None:
        # 信号灯组
        signal_group_list: list = netiface.signalGroups()

        # 遍历各灯组
        for signal_group in signal_group_list:
            # 灯组名称
            group_name = signal_group.groupName()

            # 灯组的各相位
            signal_phase_list = signal_group.phases()
            for signal_phase in signal_phase_list:
                # 相位名称
                phase_name = signal_phase.phaseName()

                if phase_name not in basic_signal_light_data["data"][group_name]:
                    continue

                # 灯色列表
                lamp_color: list = [color_interval.color for color_interval in signal_phase.listColor()]
                # 时长列表
                duration: list = [color_interval.interval for color_interval in signal_phase.listColor()]

                basic_signal_light_data["data"][group_name][phase_name]["lampColor"] = lamp_color
                basic_signal_light_data["data"][group_name][phase_name]["duration"] = duration

    # 直接获取完整的信号灯数据
    @staticmethod
    def get_signal_light_data(simuiface, netiface) -> dict:
        signal_light_data = SignalLightDataCalculator.get_basic_signal_light_data(simuiface, netiface)
        SignalLightDataCalculator.get_complete_signal_light_data(signal_light_data, netiface)
        return signal_light_data
