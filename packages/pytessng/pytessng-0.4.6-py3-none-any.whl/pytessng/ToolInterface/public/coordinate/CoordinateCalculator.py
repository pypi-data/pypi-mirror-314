import math
from typing import Callable


class CoordinateCalculator:
    # 计算给定经度下两个纬度点的中心位置的纬度和经度
    @staticmethod
    def calculate_center_coordinate(lon_min: float, lon_max: float, lat_min: float, lat_max: float) -> (float, float):
        # 计算中心位置的经度
        lon_center = (lon_min + lon_max) / 2
        # 将经纬度从度数转换为弧度
        lat1 = math.radians(lat_min)
        lat2 = math.radians(lat_max)
        # 计算中心位置的纬度
        lat_center = (lat1 + lat2) / 2
        # 将中心位置的经纬度从弧度转换为度数
        lat_center = math.degrees(lat_center)
        return lon_center, lat_center

    # 给定半径（米）和投影函数，计算边界经纬度
    @staticmethod
    def calculate_bounding_coordinate(distance: float, proj: Callable) -> (float, float, float, float):
        lon_max, _ = proj(distance, 0, inverse=True)
        lon_min, _ = proj(-distance, 0, inverse=True)
        _, lat_max = proj(0, distance, inverse=True)
        _, lat_min = proj(0, -distance, inverse=True)
        return lon_min, lon_max, lat_min, lat_max

    # 给定中心经纬度、四边界经纬度和投影函数，计算场景尺寸
    @staticmethod
    def calculate_scene_size(lon_0: float, lat_0: float, lon_min: float, lon_max: float, lat_min: float, lat_max: float, proj: Callable) -> (float, float):
        east, _ = proj(lon_max, lat_0)
        west, _ = proj(lon_min, lat_0)
        _, north = proj(lon_0, lat_max)
        _, south = proj(lon_0, lat_min)
        width = round(east - west, 1)
        height = round(north - south, 1)
        return width, height

    # 确定移动场景到中心的距离
    @staticmethod
    def calculate_move_distance(lon_0: float, lat_0: float, proj: Callable) -> (float, float):
        x_0, y_0 = proj(lon_0, lat_0)
        x_move, y_move = -x_0, -y_0
        return x_move, y_move
