import pandas as pd


# 车辆创建者类
class VehiclesCreator:
    def __init__(self, netiface, simuiface, online):
        self._netiface = netiface
        self._simuiface = simuiface
        self._online = online

        # 路径映射
        self._route_mapping: dict = dict()

    # 创建全部车辆
    def create_vehicles(self, current_vehicles: pd.DataFrame) -> None:
        for vehicle_id, vehicle_series in current_vehicles.iterrows():
            self.create_vehicle(vehicle_series, str(vehicle_id))

    # 创建单个车辆
    def create_vehicle(self, vehicle_series: pd.Series, vehicle_id: str) -> None:
        dvp = self._online.DynaVehiParam()
        dvp.name = f"{vehicle_id}"
        dvp.vehiTypeCode = vehicle_series.type_code
        dvp.roadId = vehicle_series.road_id
        dvp.dist = vehicle_series.dist
        dvp.laneNumber = vehicle_series.lane_number
        if vehicle_series.to_lane_number is not None:
            dvp.toLaneNumber = vehicle_series.to_lane_number

        # 创建车辆
        vehicle = self._simuiface.createGVehicle(dvp)

        # 设置路径
        if vehicle is not None:
            vehicle.setColor("#FFA500")  # 橙色
            route_link_id_list = vehicle_series.route_link_id_list
            route_link_id_tuple = tuple(route_link_id_list)

            # 避免重复创建路径，存储到字典中
            if route_link_id_tuple not in self._route_mapping:
                routing = self.create_vehicle_routing(route_link_id_list)
                if routing is not None:
                    self._route_mapping[route_link_id_tuple] = routing
            else:
                routing = self._route_mapping[route_link_id_tuple]

            if routing is not None:
                vehicle.vehicleDriving().setRouting(routing)
                vehicle.setColor("#87CEFA")  # 天蓝色
                print(f"Vehicle {vehicle_id} has been created and is in routing!")
            else:
                print(f"Failed to set routing for vehicle {vehicle_id}!")
        else:
            print(f"Failed to create vehicle {vehicle_id}!")

    # 创建车辆路径
    def create_vehicle_routing(self, link_id_list: list):
        try:
            links = [self._netiface.findLink(link_id) for link_id in link_id_list]
            routing = self._netiface.createRouting(links)
        except:
            routing = None
        return routing
