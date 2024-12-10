import os
import time
import traceback
from typing import Union
from PySide2.QtWidgets import QWidget, QMessageBox
from PySide2.QtCore import QPointF

from .BaseTool import BaseTool
# 1-路网数据导入
from .NetworkImport.Other2TessngFactory import Other2TessngFactory
# 2-路网数据导出
from .NetworkExport.Tessng2OtherFactory import Tessng2OtherFactory
# 3-路段编辑
from .LinkEdit.LinkEditorFactory import LinkEditorFactory
# 4.1-轨迹数据导入
from .SimuImport.SimuImportTrajectoryActor import SimuImportTrajectoryActor
# 5.1-轨迹数据导出
from .SimuExport.trajectory.SimuExportTrajectoryActor import SimuExportTrajectoryActor
# 5.2-信号灯数据导出
from .SimuExport.signalLight.SimuExportSignalLightActor import SimuExportSignalLightActor
# 6.1-桩号数据导出
from .FileExport.PileNumberDataSaver import PileNumberDataSaver
# 6.2-选区数据导出
from .FileExport.GridDataSaver import GridDataSaver
# x.1-核验shapefile
from .NetworkImport.shape2tessng.ShapefileChecker import ShapefileChecker
# x.2-核验kafka
from .public.communication.KafkaChecker import KafkaChecker
# 公共工具
from pytessng.DLLs.Tessng import tessngIFace, Online
from pytessng.Config import PathConfig
from pytessng.GlobalVar import GlobalVar
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass


class MyOperation:
    # 创建路网
    @staticmethod
    def apply_network_import_operation(widget: QWidget, params: dict) -> None:
        # widget.mode / widget.utils / widget.close
        # widget.is_network

        iface = tessngIFace()
        netiface = iface.netInterface()
        simuiface = iface.simuInterface()
        guiiface = iface.guiInterface()

        # 导入模式
        import_mode = widget.mode
        # 导入是否为道路网络
        is_network = widget.is_network

        # 1.更改默认路径
        path = params.get("folder_path") or params.get("file_path")
        if path:
            PathConfig.OPEN_DIR_PATH = os.path.dirname(path)

        # 2.正在仿真中无法导入
        if iface.simuInterface().isRunning() or iface.simuInterface().isPausing():
            widget.utils.show_info_box("请先停止仿真！", "warning")
            return

        # 3.路网上已经有路段进行询问
        link_count = netiface.linkCount()
        if is_network and link_count > 0:
            messages = {
                "title": "是否继续",
                "content": "路网上已有路段，请选择是否继续导入",
                "yes": "继续",
            }
            confirm = widget.utils.show_confirm_dialog(messages)
            if confirm != QMessageBox.Yes:
                return

        # 4.尝试关闭在线地图
        win = guiiface.mainWindow()
        win.showOsmInline(False)

        # 5.关闭窗口
        widget.close()

        # 6.执行转换
        try:
            # 记录日志
            logger.logger_pytessng.info(f"Network import mode: {import_mode}")
            logger.logger_pytessng.info(f"Network import params: {params}")

            # 当前路网上的路段ID
            current_linkIds = netiface.linkIds()

            # 创建路段
            response: dict = Other2TessngFactory.build(netiface, import_mode, params)
            status, message = response["status"], response["message"]

            # 如果有问题
            if not status:
                message, message_mode = message, "warning"
            # 如果没问题，问要不要移动
            else:
                # 新创建的路段
                new_links = [link for link in netiface.links() if link.id() not in current_linkIds]
                xs, ys = [], []
                for link in new_links:
                    points = link.centerBreakPoints()
                    xs.extend([point.x() for point in points])
                    ys.extend([point.y() for point in points])

                # 路网数据不为空
                if xs and ys:
                    # osm自动移动，其他要询问
                    if is_network and import_mode != "osm":
                        x_min, x_max = min(xs), max(xs)
                        y_min, y_max = min(ys), max(ys)
                        message = f"新创建路网的范围：\n    x = [ {x_min:.1f} m , {x_max:.1f} m ]\n    y = [ {y_min:.1f} m , {y_max:.1f} m ]\n"

                        messages = {
                            "title": "是否移动至中心",
                            "content": message + "是否将路网移动到场景中心",
                            "yes": "确定",
                        }
                        confirm = widget.utils.show_confirm_dialog(messages)

                        # 移动
                        attrs = netiface.netAttrs().otherAttrs()
                        if confirm == QMessageBox.Yes:
                            # 比例尺转换
                            scene_scale = netiface.sceneScale()
                            x_move = attrs["move_distance"]["x_move"] / scene_scale
                            y_move = attrs["move_distance"]["y_move"] / scene_scale
                            # 移动路网
                            move = QPointF(x_move, -y_move)
                            netiface.moveLinks(new_links, move)
                        # 不移动
                        else:
                            attrs.update({"move_distance": {"x_move": 0, "y_move": 0}})
                            network_name = netiface.netAttrs().netName()
                            netiface.setNetAttrs(network_name, otherAttrsJson=attrs)

                message, message_mode = "导入成功", "info"
            logger.logger_pytessng.info(f"Network attrs: {netiface.netAttrs().otherAttrs()}")

        except:
            message, message_mode = "导入失败", "warning"
            logger.logger_pytessng.critical(traceback.format_exc())

        # 7.设置场景宽度和高度
        if is_network:
            BaseTool(netiface).update_scene_size()

        # 8.设置不限时长
        if is_network:
            simuiface.setSimuIntervalScheming(0)

        # 9.关闭进度条
        ProgressDialogClass().close()

        # 10.打印属性信息
        time.sleep(1)
        attrs = netiface.netAttrs().otherAttrs()
        print("=" * 66)
        print("Create network! Network attrs:")
        for k, v in attrs.items():
            print(f"\t{k:<15}:{' '*5}{v}")
        print("=" * 66, "\n")

        # 11.弹出提示框
        widget.utils.show_info_box(message, message_mode)

        # 12.记录信息
        widget.utils.send_message("operation", widget.name)

    # 路网导出
    @staticmethod
    def apply_network_export_operation(widget: QWidget) -> None:
        # widget.mode / widget.utils / widget.close
        # widget.file_proj_string / widget.format
        # widget.check_box / widget.radio_coord_2
        # widget.radio_proj_custom / widget.line_edit_proj_custom_lon / widget.line_edit_proj_custom_lat

        iface = tessngIFace()
        netiface = iface.netInterface()
        simuiface = iface.simuInterface()

        # 导出模式
        export_mode = widget.mode

        # 1.正在仿真中无法导出
        if simuiface.isRunning() or simuiface.isPausing():
            widget.utils.show_info_box("请先停止仿真！", "warning")
            return

        # 2.检查路网上是否有路段
        if netiface.linkCount() == 0:
            widget.utils.show_info_box("当前路网没有路段 !", "warning")
            return

        # 3.获取投影
        if hasattr(widget, 'check_box'):  # 勾选框
            isChecked = widget.check_box.isChecked()
        elif hasattr(widget, 'radio_coord_2'):  # 单选框
            isChecked = widget.radio_coord_2.isChecked()
        else:
            isChecked = False
        # 有投影
        if isChecked:
            # 用自定义投影
            if widget.radio_proj_custom.isChecked():
                lon_0 = float(widget.line_edit_proj_custom_lon.text())
                lat_0 = float(widget.line_edit_proj_custom_lat.text())
                proj_string = f'+proj=tmerc +lon_0={lon_0} +lat_0={lat_0} +ellps=WGS84'
            # 用文件自带投影
            else:
                proj_string = widget.file_proj_string
        # 无投影
        else:
            proj_string = ""

        # 4.获取保存路径
        file_path = widget.utils.save_file(widget.format)
        if not file_path:
            return
        # 更改默认路径
        PathConfig.OPEN_DIR_PATH = os.path.dirname(file_path)

        # 5.关闭窗口
        widget.close()

        # 6.执行转换
        try:
            logger.logger_pytessng.info(f"Network export mode: {export_mode}")
            params = {"proj_string": proj_string, "file_path": file_path}
            logger.logger_pytessng.info(f"Network export params: {params}")
            logger.logger_pytessng.info(f"Network attrs: {netiface.netAttrs().otherAttrs()}")
            Tessng2OtherFactory.build(netiface, export_mode, params)
            message, message_mode = "导出成功", "info"
        except:
            message, message_mode = "导出失败", "warning"
            logger.logger_pytessng.critical(traceback.format_exc())

        # 7.关闭进度条
        ProgressDialogClass().close()

        # 8.提示信息
        widget.utils.show_info_box(message, message_mode)

        # 9.记录信息
        widget.utils.send_message("operation", widget.name)

    # 编辑路段
    @staticmethod
    def apply_link_edit_operation(widget: QWidget, params: dict, close_widget: bool = True) -> Union[None, list]:
        # widget.mode / widget.utils / widget.close

        iface = tessngIFace()
        netiface = iface.netInterface()
        simuiface = iface.simuInterface()

        # 编辑模式
        edit_mode = widget.mode

        # 1.正在仿真中无法导出
        if simuiface.isRunning() or simuiface.isPausing():
            widget.utils.show_info_box("请先停止仿真！", "warning")
            return

        # 2.检查有无路段
        edit_mode_list = [
            "merge", "simplify", "limit_c", "limit_l",
            "recalculate_l", "recalculate_c", "modify_limit_speed",
            "move", "rotate"
        ]
        if edit_mode in edit_mode_list:
            # 如果没有路段
            if not netiface.linkCount():
                widget.utils.show_info_box("当前路网没有路段！", "warning")
                return

        # 3.关闭窗口
        if close_widget and hasattr(widget, 'close'):
            widget.close()

        # 4.执行路段编辑
        try:
            # 返回值为0表示无操作
            response: Union[None, list, int] = LinkEditorFactory.build(edit_mode, netiface, params)
            # 如果是定位路段直接返回
            if edit_mode in ["locate", "manage_break_point"]:
                return response
            message, message_mode = "操作成功", "info"
            # 记录日志
            if response != 0:
                logger.logger_pytessng.info(f"Link edit mode: {edit_mode}")
                # 去除函数
                print_params = {
                    k: v
                    for k, v in params.items()
                    if not callable(v)
                }
                logger.logger_pytessng.info(f"Link edit params: {print_params}")
        except:
            response = None
            message, message_mode = "操作失败", "warning"
            # 记录日志
            logger.logger_pytessng.critical(traceback.format_exc())

        # 5.关闭进度条
        ProgressDialogClass().close()

        # 6.提示信息
        if response != 0:
            widget.utils.show_info_box(message, message_mode)

        # 7.记录信息
        if response != 0:
            widget.utils.send_message("operation", widget.name)

    # 仿真数据导入/仿真数据导出
    @staticmethod
    def apply_simu_data_import_or_export_operation(mode: str, params: dict) -> None:
        # 仿真观察者映射表
        simulator_observer_mapping = {
            "simu_import_trajectory": SimuImportTrajectoryActor,
            "simu_export_trajectory": SimuExportTrajectoryActor,
            "simu_export_signal_light": SimuExportSignalLightActor,
        }
        # 如果是非法模式则直接返回
        if mode not in simulator_observer_mapping:
            return

        # 仿真观察者名称
        simulator_observer_name: str = mode

        # 根据参数是否为空判断是添加还是移除
        if bool(params):
            # TESSNG接口
            iface = tessngIFace()
            netiface = iface.netInterface()
            simuiface = iface.simuInterface()

            # 获取仿真观察者
            simulator_observer_obj = simulator_observer_mapping[mode](netiface, simuiface, Online)
            # 初始化数据
            simulator_observer_obj.init_data(params)

            # MySimulator添加观察者
            GlobalVar.attach_observer_of_my_simulator(simulator_observer_name, simulator_observer_obj)
        else:
            # MySimulator移除观察者
            GlobalVar.detach_observer_of_my_simulator(simulator_observer_name)

    # 其他操作
    @staticmethod
    def apply_other_operation(widget: QWidget, params: dict) -> None:
        # widget.mode / widget.utils / widget.close

        # 操作者映射表
        operator_mapping = {
            "pile_number": PileNumberDataSaver,
            "grid": GridDataSaver,
        }

        iface = tessngIFace()
        netiface = iface.netInterface()
        simuiface = iface.simuInterface()
        guiiface = iface.guiInterface()

        # 1.正在仿真中无法导出
        if simuiface.isRunning() or simuiface.isPausing():
            widget.utils.show_info_box("请先停止仿真！", "warning")
            return

        # 2.将按钮修改成【取消工具】
        guiiface.actionNullGMapTool().trigger()

        # 3.获取保存路径
        file_path = widget.utils.save_file(widget.format)
        if not file_path:
            return
        # 更改默认路径
        PathConfig.OPEN_DIR_PATH = os.path.dirname(file_path)

        # 4.关闭窗口
        widget.close()

        # 5.执行操作
        logger.logger_pytessng.info(f"Other operation mode: {widget.mode}")
        logger.logger_pytessng.info(f"Other operation params: {params}")
        # 获取操作者
        operator = operator_mapping.get(widget.mode)
        if not operator:
            return
        try:
            operator(netiface).export(**params, file_path=file_path)
            message, message_mode = "操作完成", "info"
        except:
            logger.logger_pytessng.critical(traceback.format_exc())
            message, message_mode = "操作失败", "warning"

        # 6.关闭进度条
        ProgressDialogClass().close()

        # 7.提示信息
        widget.utils.show_info_box(message, message_mode)

        # 8.记录信息
        widget.utils.send_message("operation", widget.name)

    # 核验数据
    @staticmethod
    def apply_check_data(mode: str, *args, **kwargs):
        # 核验者映射表
        checker_mapping = {
            "shapefile": ShapefileChecker,
            "kafka": KafkaChecker,
        }

        # 获取核验者
        checker = checker_mapping.get(mode)
        if not checker:
            return

        # 核验结果的具体类型根据核验者不同而不同
        check_result = checker.check_data(*args, **kwargs)
        return check_result
