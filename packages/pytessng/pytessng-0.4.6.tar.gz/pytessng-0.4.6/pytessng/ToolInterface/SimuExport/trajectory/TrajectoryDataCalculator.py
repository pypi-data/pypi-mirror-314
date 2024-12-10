import time
import math
from typing import Callable


class TrajectoryDataCalculator:
    # 获取基础的轨迹数据，不含经纬度
    @staticmethod
    def get_basic_trajectory_data(simuiface, p2m: Callable = lambda x: x) -> dict:
        # 当前已仿真时间，单位：毫秒
        simu_time = simuiface.simuTimeIntervalWithAcceMutiples()
        # 开始仿真的现实时间戳，单位：毫秒
        start_time = simuiface.startMSecsSinceEpoch()
        # 当前仿真计算批次
        batch_num = simuiface.batchNumber()
        # 当前正在运行车辆列表
        all_vehicles = simuiface.allVehiStarted()

        traj_data = {
            "timestamp": int(time.time() * 1000),
            "simuTime": simu_time,
            'startSimuTime': start_time,
            "batchNum": batch_num,
            "count": len(all_vehicles),
            "objs": [],
        }

        for vehicle in all_vehicles:
            x = p2m(vehicle.pos().x())
            y = -p2m(vehicle.pos().y())
            if math.isnan(x) or math.isnan(y):
                continue

            in_link = vehicle.roadIsLink()

            # 车辆寻找异常，跳过
            if (in_link and not vehicle.lane()) or (not in_link and not vehicle.laneConnector()):
                continue

            lane = vehicle.lane()
            angle = vehicle.angle()
            veh_data = {
                'id': vehicle.id(),
                'name': vehicle.name(),
                'typeCode': vehicle.vehicleTypeCode(),
                'roadId': vehicle.roadId(),
                'inLink': in_link,
                'laneCount': in_link and lane.link().laneCount(),
                'laneNumber': in_link and lane.number(),
                'laneTypeName': in_link and lane.actionType(),
                'angle': angle,
                'speed': p2m(vehicle.currSpeed()),  # m/s
                'Speed': p2m(vehicle.currSpeed()) * 3.6,  # km/h
                'size': [p2m(vehicle.length()), p2m(vehicle.width()), 2],
                'color': "",
                'x': x,
                'y': y,
                'z': vehicle.v3z(),
                'longitude': None,
                'latitude': None,
                'eulerX': -angle / 180 * math.pi + math.pi / 2,
                'eulerY': -angle / 180 * math.pi + math.pi / 2,
                'eulerZ': -angle / 180 * math.pi + math.pi / 2,
            }

            traj_data['objs'].append(veh_data)

        return traj_data

    # 获取完整的轨迹数据，含经纬度
    @staticmethod
    def get_complete_trajectory_data(basic_traj_data, proj_func: Callable, move_distance: dict) -> None:
        for veh in basic_traj_data['objs']:
            x, y = veh['x'], veh['y']
            lon, lat = proj_func(x + move_distance["x_move"], y + move_distance["y_move"], inverse=True)
            veh["longitude"], veh["latitude"] = lon, lat

    # 直接获取完整的轨迹数据
    @staticmethod
    def get_trajectory_data(simuiface, p2m: Callable, proj: Callable, move_distance: dict) -> dict:
        traj_data = TrajectoryDataCalculator.get_basic_trajectory_data(simuiface, p2m)
        TrajectoryDataCalculator.get_complete_trajectory_data(traj_data, proj, move_distance)
        return traj_data
