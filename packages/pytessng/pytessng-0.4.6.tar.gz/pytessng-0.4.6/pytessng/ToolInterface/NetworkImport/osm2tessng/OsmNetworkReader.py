import os
import json
import random
import traceback
from datetime import datetime
from typing import Callable, Optional
from pyproj import Proj
from xml.etree import ElementTree
from networkx import MultiDiGraph
import osmnx as ox

from ...public.coordinate.CoordinateCalculator import CoordinateCalculator
from pytessng.Config import NetworkImportConfig, PathConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class OSMNetworkReader:
    """
    1.Params:
        (1) osm_file_path (str) (optional)
            e.g.
                osm_file_path = "nanjing.osm"
        (2) bounding_box_data (dict) (optional)
            e.g.
                bounding_box_data = {
                    "lon_min": 113.80543,
                    "lon_max": 114.34284,
                    "lat_min": 29.69543,
                    "lat_max": 31.84852,
                }
        (3) center_point_data (dict) (optional)
            e.g.
                center_point_data = {
                    "lon_0": 113.80543,
                    "lat_0": 31.84852,
                    "distance": 5, # (km)
                }
        (4) road_class (int/enum) (optional)
            1: 高速公路
            2: 高速公路和城市主干路
            3: 高速公路、城市主干路和低等级道路 (default)
        (5) proj_mode (str/enum) (optional)
            tmerc: 高斯克吕格投影
            utm: 通用横轴墨卡托投影
            web: Web墨卡托投影 (default)

    2.Public Method (All other methods are private methods):
        (1) read_data

    3.Network Data:
        (1) edges_data;
        (2) nodes_data;
        (3) other_data.
    """

    def __init__(self, params: dict):
        # 入参
        self.params: dict = params

        # 投影函数
        self.proj_func: Optional[Callable] = None

        # 其他信息
        self.other_data: dict = {
            # 数据来源
            "data_source": "OpenStreetMap",
            # 创建时间
            "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # 投影字符串
            "proj_string": "EPSG:3857",
            # 移动距离
            "move_distance": {
                "x_move": 0,
                "y_move": 0
            },
            # 场景中心经纬度
            "scene_center": {
                "lon_0": None,
                "lat_0": None
            },
            # 场景边界经纬度
            "scene_bounding": {
                "lon_min": None,
                "lon_max": None,
                "lat_min": None,
                "lat_max": None
            },
            # 场景尺寸
            "scene_size": {
                "width": None,
                "height": None
            },
        }

    # 获取osm数据
    def read_data(self) -> Optional[dict]:
        # ==================== 初始化配置 ====================
        # 1-取消API限速
        ox.settings.overpass_rate_limit = False

        # 2-设置缓存文件的路径
        dir_path_save_data: str = PathConfig.DEFAULT_OSM_DATA_SAVE_DIR_PATH
        # 拉取到的原始数据的保存路径
        file_path_save_data_before_process: str = os.path.join(dir_path_save_data, "before_process")
        ox.settings.cache_folder = file_path_save_data_before_process
        # 简单处理后的数据的保存路径
        file_path_save_data_after_process: str = os.path.join(dir_path_save_data, "after_process")

        # 3-创建保存缓存文件的文件夹
        os.makedirs(file_path_save_data_before_process, exist_ok=True)
        os.makedirs(file_path_save_data_after_process, exist_ok=True)

        # 4-获取要解析的道路类型参数
        road_type_param: dict = self._get_road_type_param(self.params)

        # ==================== 获取图对象 解析图对象数据 ====================
        # 获取图对象
        graph_object: MultiDiGraph = self._get_osm_graph_object(self.params, road_type_param)

        # 初步解析图对象为JSON数据
        if graph_object is not None:
            logger.logger_pytessng.debug("Graph object obtaining is finished!")

            # 解析图对象为JSON数据
            json_data: dict = self._get_osm_json_data(graph_object)

            # 保存数据
            file_name = self.other_data["created_time"].replace('-', '').replace(':', '').replace(' ', '')
            file_path = os.path.join(file_path_save_data_after_process, f'{file_name}.json')
            with open(file_path, 'w', encoding="utf-8") as json_file:
                json.dump(json_data, json_file, indent=4, ensure_ascii=False)
            logger.logger_pytessng.debug("Data saving is finished!")

            return json_data

        return None

    # 获取图对象
    def _get_osm_graph_object(self, params: dict, road_type_param: dict) -> Optional[MultiDiGraph]:
        # 通过读取osm文件获取
        if params.get("osm_file_path"):
            osm_file_path = params["osm_file_path"]
            graph_object = self._get_osm_graph_object_by_osm_file_path(osm_file_path)

        # 通过指定矩形区域获取
        elif params.get("bounding_box_data"):
            bounding_box_data = params["bounding_box_data"]
            graph_object = self._get_osm_graph_object_by_bounding_box_data(bounding_box_data, road_type_param)

        # 通过指定中心点获取
        elif params.get("center_point_data"):
            center_point_data = params["center_point_data"]
            graph_object = self._get_osm_graph_object_by_center_point_data(center_point_data, road_type_param)

        # 否则获取失败
        else:
            graph_object = None
            logger.logger_pytessng.error("No initialization information!")

        return graph_object

    # 解析osm文件
    def _get_osm_graph_object_by_osm_file_path(self, osm_file_path: str) -> Optional[MultiDiGraph]:
        try:
            # 模拟进度条
            pgd().update_progress(random.randint(10, 20), 100, "数据解析中（1/7）")
            # 解析数据获取图对象
            graph_object = ox.graph_from_xml(osm_file_path)
            # 模拟进度条
            pgd().update_progress(100, 100, "数据解析中（1/7）")
        except:
            logger.logger_pytessng.error(f"The OSM file cannot be parsed with the error: {traceback.format_exc()}!")
            return None

        # 获取地图边界
        try:
            # 试图解析XML文件获取边界坐标
            tree = ElementTree.parse(osm_file_path)
            root = tree.getroot()
            # 获取bounds元素的属性
            bounds_element = root.find('bounds')
            lat_min = float(bounds_element.get('minlat'))
            lon_min = float(bounds_element.get('minlon'))
            lat_max = float(bounds_element.get('maxlat'))
            lon_max = float(bounds_element.get('maxlon'))
        except:
            # 解析文件失败就用数据计算中心位置
            lons, lats = [], []
            for u, v, key, data in graph_object.edges(keys=True, data=True):
                for node_id in [u, v]:
                    lon = graph_object.nodes[node_id]['x']
                    lat = graph_object.nodes[node_id]['y']
                    lons.append(lon)
                    lats.append(lat)
            lon_min, lon_max = min(lons), max(lons)
            lat_min, lat_max = min(lats), max(lats)

        # 边界经纬度
        bounding_box_data = {
            "lon_min": lon_min,
            "lon_max": lon_max,
            "lat_min": lat_min,
            "lat_max": lat_max,
        }

        # 四边界经纬度
        self.other_data["scene_bounding"].update(bounding_box_data)
        # 中心经纬度
        lon_0, lat_0 = CoordinateCalculator.calculate_center_coordinate(**bounding_box_data)
        self.other_data["scene_center"].update({"lon_0": lon_0, "lat_0": lat_0})
        # 投影和移动距离
        self._get_proj_string_and_move_distance(lon_0, lat_0)
        # 场景尺寸
        width, height = CoordinateCalculator.calculate_scene_size(lon_0, lat_0, lon_min, lon_max, lat_min, lat_max, self.proj_func)
        self.other_data["scene_size"].update({"width": width, "height": height})

        return graph_object

    # 指定四边界拉取数据
    def _get_osm_graph_object_by_bounding_box_data(self, bounding_box_data: dict, road_type_param: dict) -> Optional[MultiDiGraph]:
        lon_min = bounding_box_data["lon_min"]
        lon_max = bounding_box_data["lon_max"]
        lat_min = bounding_box_data["lat_min"]
        lat_max = bounding_box_data["lat_max"]

        # 四边界经纬度
        self.other_data["scene_bounding"].update(bounding_box_data)
        # 中心经纬度
        lon_0, lat_0 = CoordinateCalculator.calculate_center_coordinate(**bounding_box_data)
        self.other_data["scene_center"].update({"lon_0": lon_0, "lat_0": lat_0})
        # 投影和移动距离
        self._get_proj_string_and_move_distance(lon_0, lat_0)
        # 场景尺寸
        width, height = CoordinateCalculator.calculate_scene_size(lon_0, lat_0, lon_min, lon_max, lat_min, lat_max, self.proj_func)
        self.other_data["scene_size"].update({"width": width, "height": height})

        try:
            # 模拟进度条
            pgd().update_progress(random.randint(10,20), 100, "数据解析中（1/7）")
            # 解析数据获取图对象
            graph_object = ox.graph_from_bbox(lat_max, lat_min, lon_max, lon_min, **road_type_param)
            # 模拟进度条
            pgd().update_progress(100, 100, "数据解析中（1/7）")
        except:
            logger.logger_pytessng.error(f"Due to network connectivity issues, OpenStreetMap data acquisition failed with the error: {traceback.format_exc()}!")
            return None

        return graph_object

    # 指定中心和半径拉取数据
    def _get_osm_graph_object_by_center_point_data(self, center_point_data: dict, road_type_param: dict) -> Optional[MultiDiGraph]:
        lon_0 = center_point_data["lon_0"]
        lat_0 = center_point_data["lat_0"]
        distance = center_point_data["distance"] * 1000  # m

        # 中心经纬度
        self.other_data["scene_center"].update({"lon_0": lon_0, "lat_0": lat_0})
        # 投影和move
        self._get_proj_string_and_move_distance(lon_0, lat_0)
        # 场景尺寸
        self.other_data["scene_size"].update({"width": round(distance * 2, 1), "height": round(distance * 2, 1)})
        # 四边界经纬度
        lon_min, lon_max, lat_min, lat_max = CoordinateCalculator.calculate_bounding_coordinate(distance, self.proj_func)
        self.other_data["scene_bounding"].update({"lon_min": lon_min, "lon_max": lon_max, "lat_min": lat_min, "lat_max": lat_max})

        try:
            # 模拟进度条
            pgd().update_progress(random.randint(10,20), 100, "数据解析中（1/7）")
            # 解析数据获取图对象
            graph_object = ox.graph_from_point((lat_0, lon_0), distance, **road_type_param)
            # 模拟进度条
            pgd().update_progress(100, 100, "数据解析中（1/7）")
        except:
            logger.logger_pytessng.error(f"Due to network connectivity issues, OpenStreetMap data acquisition failed with the error: {traceback.format_exc()}!")
            return None

        return graph_object

    # 获取应该拉取的路段类型
    def _get_road_type_param(self, params: dict):
        road_class = params.get("road_class", NetworkImportConfig.OSM.DEFAULT_ROAD_CLASS)
        # 只有高速公路
        if road_class == 1:
            road_type_param = {"custom_filter": '["highway"~"motorway|motorway_link"]'}
        # 有高速公路和主干路
        elif road_class == 2:
            road_type_param = {"custom_filter": '["highway"~"motorway|motorway_link|trunk|primary|secondary|tertiary"]'}
        # 所有道路都有
        else:
            road_type_param = {"network_type": "drive"}
        return road_type_param

    # 更新投影字符串、投影函数、移动距离
    def _get_proj_string_and_move_distance(self, lon_0: float, lat_0: float):
        # 投影字符串
        proj_mode = self.params.get("proj_mode")
        if proj_mode == "tmerc":
            self.other_data["proj_string"] = f'+proj=tmerc +lon_0={lon_0} +lat_0={lat_0} +ellps=WGS84'
        elif proj_mode == "utm":
            self.other_data["proj_string"] = f'+proj=utm +zone={lon_0 // 6 + 31} +ellps=WGS84'

        # 投影函数
        proj_string = self.other_data["proj_string"]
        self.proj_func = Proj(proj_string)

        # 移动距离
        x_move, y_move = CoordinateCalculator.calculate_move_distance(lon_0, lat_0, self.proj_func)
        self.other_data["move_distance"].update({"x_move": x_move, "y_move": y_move})

    # 初步解析图对象
    def _get_osm_json_data(self, graph_object: MultiDiGraph) -> dict:
        # 存储边的数据
        edges_data: dict = dict()
        # 存储点的数据
        nodes_data: dict = dict()

        # 不使用原来的点和边的编号 从0开始重新编号
        node_id_mapping: dict = dict()
        global_new_edge_id = 0
        global_new_node_id = 0

        # 用于防止添加同一路段
        edge_id_set: set = set()

        # 道路等级
        road_class = self.params.get("road_class", NetworkImportConfig.OSM.DEFAULT_ROAD_CLASS)

        # u：起始节点编号，v：目标节点编号，key：同一对节点的不同边的编号
        for u, v, key, data in pgd.progress(graph_object.edges(keys=True, data=True), '数据解析中（2/7）'):
            # 给节点从0开始重新编号
            for node_id in [u, v]:
                if node_id not in node_id_mapping:
                    global_new_node_id += 1
                    node_id_mapping[node_id] = global_new_node_id

            # 防止重复添加同一条边
            edge_id = f"{min(u, v)}-{max(u, v)}"
            if edge_id in edge_id_set:
                continue
            else:
                edge_id_set.add(edge_id)

            # 道路类型
            highway = data.get("highway")
            # 如果是列表就取第一个值
            if type(highway) == list:
                highway = highway[0]
            # 当道路等级为1或2时 当前道路类型不在指定类型列表中就跳过
            if NetworkImportConfig.OSM.ROAD_CLASS2TYPE_MAPPING.get(road_class) and highway not in NetworkImportConfig.OSM.ROAD_CLASS2TYPE_MAPPING[road_class]:
                continue

            # 车道数(int or list or None)
            lane_count = data.get("lanes")
            # 道路类型不同，默认车道数不同
            try:
                # 如果为None 就取默认车道数
                if lane_count is None:
                    lane_count = NetworkImportConfig.OSM.DEFAULT_LANE_COUNT_MAPPING.get(str(highway)) or NetworkImportConfig.OSM.DEFAULT_LANE_COUNT_MAPPING["other"]
                # 如果为列表 就取最大值
                elif type(lane_count) == list:
                    lane_count = max(list(map(int, lane_count)))
                # 如果为字符 就转为整数（字符不一定是数字）
                else:
                    lane_count = int(lane_count)
            except:
                logger.logger_pytessng.error(f"Lane Count with the error: {traceback.format_exc()}")
                # 有错误就为1
                lane_count = 1

            # 点位信息
            try:
                # 有点位信息就用点位信息
                geometry = [
                    self.proj_func(x, y)
                    for x, y in list(data.get('geometry').coords)
                ]
            except:
                # 没有点位信息就用起终点的坐标
                point_start = self.proj_func(graph_object.nodes[u]['x'], graph_object.nodes[u]['y'])
                point_end = self.proj_func(graph_object.nodes[v]['x'], graph_object.nodes[v]['y'])
                geometry = [point_start, point_end]

            # 是单向道路(True)还是双向道路(False) （这个字段肯定有）
            oneway = data["oneway"]

            # 路段名称
            name = data.get("name", "")
            # 如果是列表就拼接
            if type(name) == list:
                name = ",".join(name)

            # 记录边的数据
            global_new_edge_id += 1
            edges_data[global_new_edge_id] = {
                "start_node_id": node_id_mapping[u],
                "end_node_id": node_id_mapping[v],
                "geometry": geometry,
                "lane_count": lane_count,
                "highway": highway,
                "is_oneway": oneway,
                "name": name,
            }

            # 小路段的节点不加入节点数据 为了简化后续解析
            if highway not in NetworkImportConfig.OSM.ROAD_CLASS2TYPE_MAPPING[2]:
                continue

            # 记录点的数据
            for old_node_id in [u, v]:
                # 新的节点编号
                new_node_id = node_id_mapping[old_node_id]
                if new_node_id not in nodes_data:
                    loc = self.proj_func(graph_object.nodes[old_node_id]['x'], graph_object.nodes[old_node_id]['y'])
                    nodes_data[new_node_id] = {
                        # 点的位置
                        "loc": loc,
                        # 点的邻边ID列表
                        "adjacent_edge_id_list": []
                    }
                nodes_data[new_node_id]["adjacent_edge_id_list"].append(global_new_edge_id)

        return {
            "edges_data": edges_data,
            "nodes_data": nodes_data,
            "other_data": self.other_data,
        }
