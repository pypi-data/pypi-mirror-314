from functools import partial
from traceback import print_exc
from typing import Optional, Dict
from PySide2.QtWidgets import QMenu, QAction, QWidget, QMessageBox, QToolBar
from PySide2.QtGui import QIcon

from .Utils import Utils
from .NetworkImport.NetworkImportOpendrive import NetworkImportOpendrive
from .NetworkImport.NetworkImportShape import NetworkImportShape
from .NetworkImport.NetworkImportOpenstreetmap import NetworkImportOpenstreetmap
from .NetworkImport.NetworkImportJson import NetworkImportJson
from .NetworkImport.NetworkImportExcel import NetworkImportExcel
from .NetworkImport.NetworkImportAidaroe import NetworkImportAidaroe
from .NetworkImport.NetworkImportAnnex import NetworkImportAnnex
from .NetworkExport.NetworkExportOpendrive import NetworkExportOpendrive
from .NetworkExport.NetworkExportShape import NetworkExportShape
from .NetworkExport.NetworkExportGeojson import NetworkExportGeojson
from .NetworkExport.NetworkExportUnity import NetworkExportUnity
from .NetworkExport.NetworkExportJson import NetworkExportJson
from .SimuImport.SimuImportTrajectory import SimuImportTrajectory
from .SimuExport.SimuExportTrajectoryAndSignalLight import SimuExportTrajAndSig
from .FileExport.FileExportPileNumber import FileExportPileNumber
from .FileExport.FileExportGrid import FileExportGrid
from .LinkEdit.LinkEditCreate import LinkEditCreate
from .LinkEdit.LinkEditSplit import LinkEditSplit
from .LinkEdit.LinkEditManageBreakPoint import LinkEditManageBreakPoint
from .LinkEdit.LinkEditRemove import LinkEditRemove
from .LinkEdit.LinkEditReverse import LinkEditReverse
from .LinkEdit.LinkEditModifyAttrs import LinkEditModifyAttrs
from .LinkEdit.LinkEditMerge import LinkEditMerge
from .LinkEdit.LinkEditSimplify import LinkEditSimplify
from .LinkEdit.LinkEditLimitC import LinkEditLimitC
from .LinkEdit.LinkEditLimitL import LinkEditLimitL
from .LinkEdit.LinkEditRecalculateL import LinkEditRecalculateL
from .LinkEdit.LinkEditRecalculateC import LinkEditRecalculateC
from .LinkEdit.LinkEditModifyLimitSpeed import LinkEditModifyLimitSpeed
from .LinkEdit.LinkEditMove import LinkEditMove
from .LinkEdit.LinkEditRotate import LinkEditRotate
from .View.ViewAttrs import ViewAttrs
from .View.ViewXodrJunction import ViewXodrJunction
from .View.ViewXodrRoad import ViewXodrRoad
from .Other.OpenInstruction import OpenInstruction
from .Other.OpenExamples import OpenExamples
from .Other.SendAdvise import SendAdvise
from .Other.CheckUpdate import CheckUpdate
from .Mouse.MousePanHandler import MousePanHandler
from .Mouse.MouseZoomHandler import MouseZoomHandler
from .ToolBar.DesiredSpeedDecisionPoint import DesiredSpeedDecisionPoint
from pytessng.DLLs.Tessng import tessngIFace
from pytessng.Config import UIConfig, PathConfig
from pytessng.GlobalVar import GlobalVar


class MyMenu:
    """
    添加一个新功能的四个步骤：
        - 导入界面类
        - 添加到按钮名称和类映射表中
        - 创建按钮
        - 添加按钮到菜单栏
    """

    # 工具包
    utils = Utils
    # 按钮名称和类映射
    action_name_and_class_mapping: Dict[str, Dict[str, tuple]] = {
        "network_import": {
            "opendrive": ("action_network_import_opendrive", NetworkImportOpendrive),
            "shape": ("action_network_import_shape", NetworkImportShape),
            "osm": ("action_network_import_openstreetmap", NetworkImportOpenstreetmap),
            "json": ("action_network_import_json", NetworkImportJson),
            "excel": ("action_network_import_excel", NetworkImportExcel),
            "aidaroe": ("action_network_import_aidaroe", NetworkImportAidaroe),
            "annex": ("action_network_import_annex", NetworkImportAnnex),
        },
        "network_export": {
            "opendrive": ("action_network_export_opendrive", NetworkExportOpendrive),
            "shape": ("action_network_export_shape", NetworkExportShape),
            "geojson": ("action_network_export_geojson", NetworkExportGeojson),
            "unity": ("action_network_export_unity", NetworkExportUnity),
            "json": ("action_network_export_json", NetworkExportJson),
        },
        "simu_data_import": {
            "trajectory": ("action_simu_import_trajectory", SimuImportTrajectory),
        },
        "simu_data_export": {
            "traj_and_sig": ("action_simu_export_trajectory_and_signal_light", SimuExportTrajAndSig),
        },
        "config_file_export": {
            "pile_number": ("action_file_export_pile_number", FileExportPileNumber),
            "grid": ("action_file_export_grid", FileExportGrid),
        },
        "link_edit": {
            "create": ("action_link_edit_create", LinkEditCreate),
            "split": ("action_link_edit_split", LinkEditSplit),
            "manage_break_point": ("action_link_edit_manage_break_point", LinkEditManageBreakPoint),
            "remove": ("action_link_edit_remove", LinkEditRemove),
            "reverse": ("action_link_edit_reverse", LinkEditReverse),
            "modify_attrs": ("action_link_edit_modify_attrs", LinkEditModifyAttrs),
            "merge": ("action_link_edit_merge", LinkEditMerge),
            "simplify": ("action_link_edit_simplify", LinkEditSimplify),
            "limit_c": ("action_link_edit_limit_c", LinkEditLimitC),
            "limit_l": ("action_link_edit_limit_l", LinkEditLimitL),
            "recalculate_l": ("action_link_edit_recalculate_l", LinkEditRecalculateL),
            "recalculate_c": ("action_link_edit_recalculate_c", LinkEditRecalculateC),
            "modify_limit_speed": ("action_link_edit_modify_limit_speed", LinkEditModifyLimitSpeed),
            "move": ("action_link_edit_move", LinkEditMove),
            "rotate": ("action_link_edit_rotate", LinkEditRotate),
        },
        "view": {
            "attrs": ("action_view_attrs", ViewAttrs),
            "xodr_junction": ("action_view_xodr_junction", ViewXodrJunction),
            "xodr_road": ("action_view_xodr_road", ViewXodrRoad),
        },
        "other": {
            "instruction": ("action_other_instruction", OpenInstruction),
            "examples": ("action_other_examples", OpenExamples),
            "advise": ("action_other_advise", SendAdvise),
            "update": ("action_other_update", CheckUpdate),
        },
        "tool_bar": {
            "ds_dp": ("action_desired_speed_decision_point", DesiredSpeedDecisionPoint),
        }
    }

    def __init__(self):
        self.iface = tessngIFace()
        self.netiface = self.iface.netInterface()
        self.guiiface = self.iface.guiInterface()
        self.win = self.guiiface.mainWindow()

        # 与鼠标事件相关的按钮
        self.actions_related_to_mouse_event: dict = {}
        # 只能正式版本使用的按钮
        self.actions_only_official_version: list = []

        # 当前菜单
        self.current_dialog: Optional[QWidget] = None
        # 上一菜单
        self.last_dialog: Optional[QWidget] = None

        # 初始化
        self.init()

    def init(self):
        # 创建按钮
        self.create_actions()
        # 创建菜单栏
        self.create_menus()
        # 将按钮添加到菜单栏
        self.add_action_to_menu()
        # 将菜单栏添加到主菜单栏
        self.add_menu_to_menubar()
        # 设置隐藏的部分
        self.set_hidden_sections()
        # 设置特殊按钮
        self.set_special_actions()
        # 关联按钮与函数
        self.connect_action_and_function()

        # 统计用户数量
        self.utils.send_message("operation", "visit")
        # 自动版本检查
        CheckUpdate().load(auto_check=True)

    # 创建按钮
    def create_actions(self):
        # =============== 1.路网数据导入 ===============
        # 1.1.导入OpenDrive
        self.action_network_import_opendrive = QAction('导入OpenDrive (.xodr)')
        # 1.2.导入Shape
        self.action_network_import_shape = QAction('导入Shape')
        # 1.3.导入OpenStreetMap
        self.action_network_import_openstreetmap = QAction('导入OpenStreetMap')
        # 1.4.导入Json
        self.action_network_import_json = QAction('导入Json')
        # 1.5.导入Excel
        self.action_network_import_excel = QAction('导入Excel (.xlsx/.xls/.csv)')
        # 1.6.导入Aidaroe
        self.action_network_import_aidaroe = QAction('导入Aidaroe (.jat)')
        # 1.7.导入路网元素
        self.action_network_import_annex = QAction('导入路网元素 (.json)')

        # =============== 2.路网数据导出 ===============
        # 2.1.导出为OpenDrive
        self.action_network_export_opendrive = QAction('导出为OpenDrive (.xodr)')
        # 2.2.导出为Shape
        self.action_network_export_shape = QAction('导出为Shape')
        # 2.3.导出为GeoJson
        self.action_network_export_geojson = QAction('导出为GeoJson')
        # 2.4.导出为Unity
        self.action_network_export_unity = QAction('导出为Unity (.json)')
        # 2.5.导出为Json
        self.action_network_export_json = QAction('导出为Json')

        # =============== 3.仿真数据导入 ===============
        # 3.1.导入轨迹数据
        self.action_simu_import_trajectory = QAction("导入轨迹数据")

        # =============== 4.仿真数据导出 ===============
        # 4.1.导出轨迹数据
        self.action_simu_export_trajectory_and_signal_light = QAction("导出轨迹和信号灯数据")

        # =============== 5.配置文件导出 ===============
        # 5.1.导出桩号数据
        self.action_file_export_pile_number = QAction('导出桩号数据')
        # 5.2.导出选区数据
        self.action_file_export_grid = QAction("导出选区数据")

        # =============== 6.路段编辑 ===============
        # 6.1.创建路段
        self.action_link_edit_create = QAction('创建路段')
        # 6.2.打断路段
        self.action_link_edit_split = QAction("打断路段")
        # 6.3.管理路段断点
        self.action_link_edit_manage_break_point = QAction("管理路段断点")
        # 6.4.框选删除路段
        self.action_link_edit_remove = QAction("框选删除路段")
        # 6.5.框选逆序路段
        self.action_link_edit_reverse = QAction("框选反转路段")
        # 6.6.修改路段属性
        self.action_link_edit_modify_attrs = QAction('修改路段属性')
        # 6.7.合并路段
        self.action_link_edit_merge = QAction('合并路段')
        # 6.8.简化路段点位
        self.action_link_edit_simplify = QAction('简化路段点位（路网级）')
        # 6.9.限制连接段最小长度
        self.action_link_edit_limit_c = QAction('限制连接段最小长度（路网级）')
        # 6.10.限制路段最大长度
        self.action_link_edit_limit_l = QAction('限制路段最大长度（路网级）')
        # 6.11.重新计算路段中心线
        self.action_link_edit_recalculate_l = QAction('重新计算路段中心线（路网级）')
        # 6.12.重新计算连接段中心线
        self.action_link_edit_recalculate_c = QAction('重新计算连接段中心线（路网级）')
        # 6.13.修改路段限速
        self.action_link_edit_modify_limit_speed = QAction('修改路段限速（路网级）')
        # 6.14.移动路网
        self.action_link_edit_move = QAction('移动路网')
        # 6.15.旋转路网
        self.action_link_edit_rotate = QAction('旋转路网')

        # =============== 7.查看 ===============
        # 7.1.查看路网属性
        self.action_view_attrs = QAction('查看路网属性')
        # 7.2.查看junction
        self.action_view_xodr_junction = QAction('查看junction (xodr)')
        # 7.3.查看road
        self.action_view_xodr_road = QAction('查看road (xodr)')

        # =============== 8.帮助 ===============
        # 8.1.打开说明书
        self.action_other_instruction = QAction("打开说明书")
        # 8.2.打开样例
        self.action_other_examples = QAction("打开数据导入样例")
        # 8.3.提出建议
        self.action_other_advise = QAction("提交用户反馈")
        # 8.4.检查更新
        self.action_other_update = QAction("检查更新")

        # =============== 9.其他 ===============
        icon = QIcon(PathConfig.DSDP_ICON_FILE_PATH)
        self.action_desired_speed_decision_point = QAction(icon, "期望速度决策点")

    # 创建菜单栏
    def create_menus(self):
        # 数据导入导出
        self.menu_data = QMenu("数据导入导出")
        # 路网数据导入
        self.menu_network_import = QMenu('路网数据导入')
        # 路网数据导出
        self.menu_network_export = QMenu('路网数据导出')
        # 仿真数据导入
        self.menu_simu_import = QMenu('仿真数据导入')
        # 仿真数据导出
        self.menu_simu_export = QMenu('仿真数据导出')
        # 配置文件导出
        self.menu_file_export = QMenu('配置文件导出')
        # 路段编辑
        self.menu_link_edit = QMenu('路段编辑')

        # 查看[TESS]
        self.menu_view_tess = self.guiiface.viewMenu()
        # 帮助[TESS]
        self.menu_other_tess = self.guiiface.aboutMenu()
        # 路网工具栏[TESS]
        self.tool_bar_network = self.guiiface.netToolBar()

        # 主界面菜单栏
        self.menu_bar = self.guiiface.menuBar()

    # 将按钮添加到菜单栏
    def add_action_to_menu(self):
        # 数据导入导出
        menu_data_list = [
            self.menu_network_import,
            self.menu_network_export,
            self.menu_simu_import,
            self.menu_simu_export,
            self.menu_file_export,
        ]
        for menu in menu_data_list:
            self.menu_data.addMenu(menu)

        # 路网数据导入
        action_network_import_list = [
            self.action_network_import_opendrive,
            self.action_network_import_shape,
            self.action_network_import_openstreetmap,
            self.action_network_import_json,
            self.action_network_import_excel,
            self.action_network_import_aidaroe,
            self.action_network_import_annex,
        ]
        self.menu_network_import.addActions(action_network_import_list)

        # 路网数据导出
        action_network_export_list = [
            self.action_network_export_opendrive,
            self.action_network_export_shape,
            self.action_network_export_geojson,
            self.action_network_export_unity,
            self.action_network_export_json,
        ]
        self.menu_network_export.addActions(action_network_export_list)

        # 仿真数据导入
        action_simu_import_list = [
            self.action_simu_import_trajectory,
        ]
        self.menu_simu_import.addActions(action_simu_import_list)

        # 仿真数据导出
        action_simu_export_list = [
            self.action_simu_export_trajectory_and_signal_light,
        ]
        self.menu_simu_export.addActions(action_simu_export_list)

        # 配置文件导出
        action_file_export_list = [
            self.action_file_export_pile_number,
            self.action_file_export_grid,
        ]
        self.menu_file_export.addActions(action_file_export_list)

        # 路段编辑
        action_link_edit_list = [
            self.action_link_edit_create,
            self.action_link_edit_split,
            self.action_link_edit_manage_break_point,
            self.action_link_edit_remove,
            self.action_link_edit_reverse,
            self.action_link_edit_modify_attrs,
            self.action_link_edit_merge,
            self.action_link_edit_simplify,
            self.action_link_edit_limit_c,
            self.action_link_edit_limit_l,
            self.action_link_edit_recalculate_l,
            self.action_link_edit_recalculate_c,
            self.action_link_edit_modify_limit_speed,
            self.action_link_edit_move,
            self.action_link_edit_rotate,
        ]
        self.menu_link_edit.addActions(action_link_edit_list[:6])
        self.menu_link_edit.addSeparator()
        self.menu_link_edit.addActions(action_link_edit_list[6:13])
        self.menu_link_edit.addSeparator()
        self.menu_link_edit.addActions(action_link_edit_list[13:])

        # 查看
        action_view_list = [
            self.action_view_attrs,
            self.action_view_xodr_junction,
            self.action_view_xodr_road,
        ]
        self.menu_view_tess.addActions(action_view_list)

        # 更多
        action_other_list = [
            self.action_other_instruction,
            self.action_other_examples,
            self.action_other_advise,
            self.action_other_update,
        ]
        self.menu_other_tess.addSeparator()  # 添加分隔线
        self.menu_other_tess.addActions(action_other_list)

    # 将菜单栏添加到主菜单栏中
    def add_menu_to_menubar(self):
        # 数据导入导出
        self.menu_bar.insertAction(self.menu_bar.actions()[-1], self.menu_data.menuAction())
        # 路段编辑
        self.menu_bar.insertAction(self.menu_bar.actions()[-1], self.menu_link_edit.menuAction())
        # 工具栏
        self.tool_bar_network.insertAction(self.tool_bar_network.actions()[8], self.action_desired_speed_decision_point)

    # 设置隐藏的部分
    def set_hidden_sections(self):
        # 设置按钮或菜单栏隐藏
        # 如果不是完整版
        if not GlobalVar.extension:
            # 设置隐藏按钮
            for first_class, second_class_list in UIConfig.Menu.extension_list:
                # 如果是列表就单个隐藏
                if type(second_class_list) == list:
                    for second_class in second_class_list:
                        action_name = f"action_{first_class}_{second_class}"
                        action = getattr(self, action_name)
                        action.setVisible(False)
                # 如果不是列表就是全部隐藏
                elif second_class_list == "all":
                    menu_name = f"menu_{first_class}"
                    menu = getattr(self, menu_name)
                    menu.menuAction().setVisible(False)

        # 设置工具栏隐藏
        all_toolbars = self.win.findChildren(QToolBar)
        for toolbar in all_toolbars:
            if toolbar.windowTitle() in ["收费站", "toolBar"]:
                toolbar.setVisible(False)

    # 设置特殊按钮
    def set_special_actions(self):
        # =============== 鼠标事件相关 ===============
        # 与鼠标事件相关的按钮
        self.actions_related_to_mouse_event: dict = {
            "grid": self.action_file_export_grid,
            "split": self.action_link_edit_split,
            "remove": self.action_link_edit_remove,
            "reverse": self.action_link_edit_reverse,
            "manage_break_point": self.action_link_edit_manage_break_point,
            "decision": self.action_desired_speed_decision_point
        }
        # 设置按钮为可勾选
        for action in self.actions_related_to_mouse_event.values():
            action.setCheckable(True)

        # =============== 试用版相关 ===============
        # 只能正式版本使用的按钮
        self.actions_only_official_version: list = list(self.actions_related_to_mouse_event.values()) + [
            self.action_simu_import_trajectory,
            self.action_simu_export_trajectory_and_signal_light,
        ]
        # 设置按钮禁用, 若是正版会在afterLoadNet中启用
        for action in self.actions_only_official_version:
            action.setEnabled(False)

    # 关联按钮与函数
    def connect_action_and_function(self):
        # 关联普通按钮与函数
        for first_class, second_class_mapping in self.action_name_and_class_mapping.items():
            for second_class, action_and_class in second_class_mapping.items():
                # 获取按钮名称
                action_name = action_and_class[0]
                # 如果有这个按钮，而且也不是None
                if hasattr(self, action_name):
                    # 获取按钮
                    action = getattr(self, action_name)
                    # 关联函数
                    action.triggered.connect(partial(self.apply_action, first_class, second_class))
                else:
                    print(f"Action name {action_name} not found!")

        # 关联在线地图导入OSM的槽函数
        self.win.forPythonOsmInfo.connect(NetworkImportOpenstreetmap.create_network_online)
        # 关闭在线地图
        self.win.showOsmInline(False)

        # 关联普通按钮与取消MyNet观察者的函数
        def uncheck(set_action_checked: bool):
            # 移除观察者
            GlobalVar.detach_observer_of_my_net()
            # 取消按钮选中
            if set_action_checked:
                for action0 in GlobalVar.actions_related_to_mouse_event.values():
                    action0.setChecked(False)

        for actions in [self.guiiface.netToolBar().actions(), self.guiiface.operToolBar().actions()]:
            for action in actions:
                if not action or action.text() in ["期望速度决策点"]:
                    continue
                action.triggered.connect(partial(uncheck, action.text() != "取消工具"))

        # 打开tess文件函数
        def open_tess_file():
            file_path = self.utils.open_file([("TESSNG", "tess")])
            self.netiface.openNetFle(file_path)

        # 覆盖原有的打开文件按钮
        open_action = self.guiiface.actionOpenFile()
        # 移除原有按钮的触发事件
        open_action.triggered.disconnect()
        # 设置新的触发事件
        open_action.triggered.connect(open_tess_file)

        # 添加到MyNet固定观察者
        mouse_observer_list = [
            MousePanHandler(),
            MouseZoomHandler(),
        ]
        for mouse_observer in mouse_observer_list:
            GlobalVar.attach_observer_of_my_net(mouse_observer, is_fixed=True)

    # 执行操作
    def apply_action(self, first_class: str, second_class: str):
        # =============== 特殊情况特殊处理 ===============
        if first_class == "network_import" and second_class == "osm":
            messages = {
                "title": "OSM导入模式",
                "content": "请选择导入离线文件或获取在线地图",
                "yes": "导入离线文件",
                "no": "获取在线地图",
            }
            result = self.utils.show_confirm_dialog(messages)

            # No键
            if result == QMessageBox.No:
                # 显示在线地图
                self.win.showOsmInline(True)
                return
            # 取消键
            elif result == QMessageBox.Cancel:
                return

        # =============================================
        try:
            # 关闭上一个窗口
            if self.current_dialog:
                self.current_dialog.close()
                self.last_dialog = self.current_dialog
            # 获取对应类
            action_class = self.action_name_and_class_mapping[first_class][second_class][1]
            dialog = action_class()
            # 显示窗口
            if dialog:
                # 如果是同一个窗口则将上一窗口置空
                if type(dialog) is type(self.last_dialog):
                    self.last_dialog = None
                self.current_dialog = dialog
                self.current_dialog.load()
                self.current_dialog.show()
        except:
            self.utils.show_info_box("该功能暂未开放！")
            print_exc()
