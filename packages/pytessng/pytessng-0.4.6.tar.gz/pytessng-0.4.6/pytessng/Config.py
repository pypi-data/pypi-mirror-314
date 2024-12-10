import os
import logging
from pyautogui import size as scene_size


# ==================== 日志等级配置 ====================
class LoggingConfig:
    # 记录到文件
    FILE_LOGS_LEVEL = logging.DEBUG
    # 打印在控制台
    CONSOLE_LOGS_LEVEL = logging.DEBUG


# ==================== 路径配置 ====================
class PathConfig:
    # 文件所在文件夹的路径
    THIS_FILE_PATH: str = os.path.dirname(__file__)
    # 进程(工作空间)的路径
    WORKSPACE_PATH: str = os.path.join(os.getcwd(), "WorkSpace")

    # (1) UUID的路径（固定）
    UUID_FILE_PATH: str = os.path.join(os.environ['USERPROFILE'], ".pytessng")
    # (2) ico图标的路径（固定）
    ICON_FILE_PATH: str = os.path.join(THIS_FILE_PATH, "Files", "Ico", "TESSNG.ico")
    # (3) 说明书的路径（固定）
    INSTRUCTION_FILE_PATH: str = os.path.join(THIS_FILE_PATH, "Files", "Doc", "用户使用手册.pdf")
    # (4) 版本信息文件的路径（固定）
    VERSION_FILE_PATH: str = os.path.join(THIS_FILE_PATH, "Files", "Doc", "version.json")
    # (5) 样例文件的路径（固定）
    EXAMPLES_DIR_PATH: str = "file:\\" + os.path.join(WORKSPACE_PATH, "Examples")
    # (6) 日志文件的路径（固定）
    LOG_DIR_PATH: str = os.path.join(WORKSPACE_PATH, "Log")
    # (7) OSM数据保存的路径（基本固定）
    DEFAULT_OSM_DATA_SAVE_DIR_PATH: str = os.path.join(WORKSPACE_PATH, "Data", "osm_data")
    # (8) 导出仿真数据（轨迹、信号灯）保存为Json的路径
    # DEFAULT_SIMU_DATA_SAVE_DIR_PATH: str = os.path.join(WORKSPACE_PATH, "Data", "traj_data")
    DEFAULT_SIMU_DATA_SAVE_DIR_PATH: str = os.path.join(os.environ['USERPROFILE'], "Desktop")  # 在电脑桌面
    # (9) 默认创建路网打开文件和导出路网保存数据的路径（会有更改）
    # OPEN_DIR_PATH: str = os.path.join(WORKSPACE_PATH, "Examples")  # 在样例文件夹
    OPEN_DIR_PATH: str = os.path.join(os.environ['USERPROFILE'], "Desktop")  # 在电脑桌面

    DSDP_ICON_FILE_PATH = os.path.join(THIS_FILE_PATH, "Files", "Ico", "dsdp.ico")


# ==================== 路网数据导入配置 ====================
class NetworkImportConfig:
    # 车道类型映射 for OpenDrive/Shape
    LANE_TYPE_MAPPING = {
        'driving': '机动车道',
        'biking': '非机动车道',
        'sidewalk': '非机动车道',
        'stop': '应急车道',
        # OpenDrive
        'onRamp': '机动车道',
        'offRamp': '机动车道',
        'entry': '机动车道',
        'exit': '机动车道',
        'connectingRamp': '机动车道',
        'shoulder': '应急车道',
        'parking': '停车带',
    }

    # 车辆输入、决策路径、信号灯组的生效时长（s）
    VALID_DURATION: int = 12 * 3600

    class OpenDrive:
        # 如果是opendrive导入的路网，会主动进行简化(仅路段)，避免创建过慢
        simplify_network_force = True

        # 当前后几个点的向量夹角小于 default_angle 且点距小于 max_length(除非夹角为0) 时，抹除过渡点
        default_angle = 1
        max_length = 50

        # 连续次数后可视为正常车道，或者连续次数后可视为连接段,最小值为2
        POINT_REQUIRE = 2

        # 当opendrive连接段的首尾连接长度低于此值时，抛弃原有的点序列，使用自动连接
        MIN_CONNECTOR_LENGTH = None

        # 需要被处理的车道类型及处理参数
        WIDTH_LIMIT = {
            '机动车道': {
                'split': 2,  # 作为正常的最窄距离
                'join': 1.5,  # 被忽略时的最宽距离
            },
            '非机动车道': {
                'split': 2,
                'join': 0.5,
            },
        }

        # 拓宽连接段时的路段裁剪长度
        SPLIT_LENGTH = 2

    class Shape:
        # 车道默认宽度
        DEFAULT_LANE_WIDTH_MAPPING = {
            "driving": 3.5,
            "biking": 1.5,
            "sidewalk": 1.5,
            "stop": 3.5
        }
        # 小于该宽度的车道要删除
        MIN_LANE_WIDTH = 2.0  # m

        # 检查最长的车道与最短的车道的长度差是否在一定范围内
        MAX_LENGTH_DIFF = 20  # m
        # 各条车道的起终点距离上下限
        MAX_DISTANCE_LANE_POINTS = 9  # m
        MIN_DISTANCE_LANE_POINTS = 0  # m
        # 寻点距离
        MAX_DISTANCE_SEARCH_POINTS = 2.8  # m

    class OSM:
        # 默认道路等级
        DEFAULT_ROAD_CLASS = 3

        # 拉取的路段类型
        ROAD_CLASS2TYPE_MAPPING = {
            1: [
                "motorway", "motorway_link"
            ],
            2: [
                "motorway", "motorway_link",
                "trunk", "trunk_link",
                "primary", "primary_link",
                "secondary", "secondary_link",
                "tertiary", "tertiary_link"
            ],
        }

        # 不同道路类型的默认车道数
        DEFAULT_LANE_COUNT_MAPPING = {
            "motorway": 3,
            "motorway_link": 2,
            "trunk": 3,
            "trunk_link": 2,
            "primary": 3,
            "primary_link": 1,
            "secondary": 2,
            "secondary_link": 1,
            "tertiary": 2,
            "tertiary_link": 1,
            "other": 1,
        }

        # 默认车道宽度
        DEFAULT_LANE_WIDTH = 3.5

    class Aidaroe:
        # 去除超窄车道的阈值（m）
        THRESHOLD_LANE_WIDTH = 0.5

        # 去除超短路段的阈值（m）
        THRESHOLD_LINK_LENGTH = 2

        # 车辆类型映射
        VEHI_TYPE_CODE_MAPPING = {100: 1, 200: 2, 300: 4}


# ==================== 路网数据导出配置 ====================
class NetworkExportConfig:
    # 车道类型映射 for OpenDrive/Shape
    LANE_TYPE_MAPPING = {
        '机动车道': 'driving',
        '非机动车道': 'biking',
        '人行道': 'sidewalk',
        '应急车道': 'stop',
    }

    class Unity:
        # 属性映射关系
        CONVERT_ATTRIBUTE = {
            "black": "Driving",
            "white": "WhiteLine",
            "yellow": "YellowLine",
        }

        # 线宽
        BORDER_LINE_WIDTH = 0.2  # m
        CENTER_LINE_WIDTH = 0.3  # m

        # # 虚实线长度
        # empty_line_length = 3  # m
        # real_line_length = 4  # m


# ==================== 路段编辑 ====================
class LinkEditConfig:
    # 默认路段最大长度
    DEFAULT_MAX_LINK_LENGTH = 1000  # m
    # 默认连接段最小长度
    DEFAULT_MIN_CONNECTOR_LENGTH = 10  # m

    # UI
    # 路段最大长度的取值范围
    MIN_MAX_LINK_LENGTH = 50  # m
    MAX_MAX_LINK_LENGTH = 5000  # m
    # 连接段最小长度的取值范围
    MIN_MIN_CONNECTOR_LENGTH = 0.1  # m
    MAX_MIN_CONNECTOR_LENGTH = 100  # m

    class Creator:
        # 默认车道宽度
        DEFAULT_LANE_WIDTH = 3.5
        # 车道宽度的取值范围
        MIN_LANE_WIDTH = 0.5
        MAX_LANE_WIDTH = 10

    class Locator:
        # 定位的查找距离
        DIST = 4  # m

    class Merger:
        # 默认是否包含连接段
        DEFAULT_INCLUDE_CONNECTOR = True
        # 默认是否简化点序列
        DEFAULT_SIMPLIFY_POINTS = True
        # 默认是否忽略车道类型不同
        DEFAULT_IGNORE_LANE_TYPE = False
        # 默认是否忽略车道连接缺失
        DEFAULT_IGNORE_MISSING_CONNECTOR = False
        # 默认最大合并长度
        DEFAULT_MAX_LENGTH = 2000  # m

        # UI
        # 合并最大长度的取值范围
        MIN_MAX_LENGTH = 50  # m
        MAX_MAX_LENGTH = 5000  # m

    class Simplifier:
        # 默认割线最远距离
        DEFAULT_MAX_DISTANCE = 0.3  # m
        # 默认遍历最大长度
        DEFAULT_MAX_LENGTH = 1000  # m

        # UI
        # 割线最远距离的取值范围
        MIN_MAX_DISTANCE = 0.05  # m
        MAX_MAX_DISTANCE = 10  # m
        # 遍历最大长度的取值范围
        MIN_MAX_LENGTH = 50  # m
        MAX_MAX_LENGTH = 5000  # m


class SimuExportConfig:
    class Kafka:
        TEST_TOPIC = "pytessng_test"


class UIConfig:
    class Menu:
        # 拓展菜单列表
        extension_list = [
            ("network_import", ["json"]),
            ("network_export", ["unity", "json"]),
            ("link_edit", ["create", "split"]),
            ("file_export", "all")
        ]

    class Base:
        width: int = int(scene_size()[0] / 4)
        height: int = 200

    class BaseLinkEdit:
        width: int = 250
        height: int = 150

    class FileExportPilenumber:
        width: int = int(scene_size()[0] / 2)
