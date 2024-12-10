import os
from typing import Callable, List
from PySide2.QtWidgets import QPushButton, QCheckBox, QLineEdit, QLabel
from PySide2.QtCore import Qt
from PySide2.QtGui import QDoubleValidator, QMouseEvent

from .BaseLinkEdit import BaseLinkEdit, MyQHBoxLayout, MyQVBoxLayout
from ..BaseMouse import BaseMouse
from ..public.QuestionMark import QuestionMark
from ..public.HighLightPathItem import HighLightPathItem
from ..public.TextWindowItem import TextWindowItem
from pytessng.ToolInterface import MyOperation
from pytessng.Config import LinkEditConfig, PathConfig
from pytessng.GlobalVar import GlobalVar


class LinkEditMerge(BaseLinkEdit):
    name: str = "合并路段"
    mode: str = "merge"

    def set_widget_layout(self):
        # 第一行：勾选框
        self.checkbox_1 = QCheckBox("是否使用连接段点位")
        # 第二行：勾选框
        self.checkbox_2 = QCheckBox("是否自动简化点位")
        # 第三行：勾选框
        self.checkbox_3 = QCheckBox("是否忽略车道类型不同")
        picture_path_1 = os.path.join(PathConfig.THIS_FILE_PATH, "Files", "Ico", "车道类型不同.png")
        self.question_mark_1 = QuestionMark(picture_path_1)
        # 第四行：勾选框
        self.checkbox_4 = QCheckBox("是否忽略车道连接缺失")
        picture_path_2 = os.path.join(PathConfig.THIS_FILE_PATH, "Files", "Ico", "车道连接缺失.png")
        self.question_mark_2 = QuestionMark(picture_path_2)
        # 第五行：文本、输入框
        self.label_length = QLabel('最大合并长度（m）：')
        self.line_edit_length = QLineEdit()
        # 第六行：按钮
        self.button_all = QPushButton('全部合并')
        self.button_click = QPushButton('点击合并')

        # 总体布局
        layout = MyQVBoxLayout([
            self.checkbox_1,
            self.checkbox_2,
            MyQHBoxLayout([self.checkbox_3, self.question_mark_1]),
            MyQHBoxLayout([self.checkbox_4, self.question_mark_2]),
            MyQHBoxLayout([self.label_length, self.line_edit_length]),
            MyQHBoxLayout([self.button_all, self.button_click]),
        ])
        self.setLayout(layout)

        # 限制输入框内容
        validator = QDoubleValidator()
        self.line_edit_length.setValidator(validator)

        # 设置提示信息
        min_max_length = LinkEditConfig.Merger.MIN_MAX_LENGTH
        max_max_length = LinkEditConfig.Merger.MAX_MAX_LENGTH
        self.line_edit_length.setToolTip(f'{min_max_length} <= length <= {max_max_length}')

    def set_monitor_connect(self):
        self.line_edit_length.textChanged.connect(self.apply_monitor_state)

    def set_button_connect(self):
        self.button_all.clicked.connect(self.apply_button_all_action)
        self.button_click.clicked.connect(self.apply_button_click_action)

    def set_default_state(self):
        self.checkbox_1.setChecked(LinkEditConfig.Merger.DEFAULT_INCLUDE_CONNECTOR)
        self.checkbox_2.setChecked(LinkEditConfig.Merger.DEFAULT_SIMPLIFY_POINTS)
        self.checkbox_3.setChecked(LinkEditConfig.Merger.DEFAULT_IGNORE_LANE_TYPE)
        self.checkbox_4.setChecked(LinkEditConfig.Merger.DEFAULT_IGNORE_MISSING_CONNECTOR)
        default_max_length = LinkEditConfig.Merger.DEFAULT_MAX_LENGTH
        self.line_edit_length.setText(f"{default_max_length}")

    def apply_monitor_state(self):
        max_length = float(self.line_edit_length.text())
        min_max_length = LinkEditConfig.Merger.MIN_MAX_LENGTH
        max_max_length = LinkEditConfig.Merger.MAX_MAX_LENGTH
        enabled_button = min_max_length <= float(max_length) <= max_max_length
        # 设置可用状态
        self.button_all.setEnabled(enabled_button)
        self.button_click.setEnabled(enabled_button)

    def apply_button_all_action(self):
        super().apply_button_action()

    def apply_button_click_action(self):
        # 关闭窗口
        self.close()
        # 提示信息
        message = "请使用鼠标左键依次点击要合并的路段，使用鼠标右键完成合并！"
        self.utils.show_info_box(message)
        # 添加MyNet观察者
        params: dict = self.get_params()
        self.mouse_link_merger = MouseLinkMerger(params, lambda params0: MyOperation.apply_link_edit_operation(self, params0, self.auto_close_window))
        GlobalVar.attach_observer_of_my_net(self.mouse_link_merger)

    # 重写父类方法
    def get_params(self) -> dict:
        include_connector = self.checkbox_1.isChecked()
        simplify_points = self.checkbox_2.isChecked()
        ignore_lane_type = self.checkbox_3.isChecked()
        ignore_missing_connector = self.checkbox_4.isChecked()
        max_length = float(self.line_edit_length.text())
        return {
            "link_groups": [],
            "include_connector": include_connector,
            "simplify_points": simplify_points,
            "ignore_lane_type": ignore_lane_type,
            "ignore_missing_connector": ignore_missing_connector,
            "max_length": max_length,
        }


class MouseLinkMerger(BaseMouse):
    def __init__(self, params: dict, func_apply_merge_link: Callable):
        super().__init__()
        self.params: dict = params
        self.func_apply_merge_link: Callable = func_apply_merge_link

        self.current_link_id_list: List[int] = []
        self.temp_link_id_list: List[int] = []

        self.fixed_item_list = []
        self.temp_item_list = []

        self.text_window_item = None

    def handle_mouse_press_event(self, event: QMouseEvent) -> None:
        # 如果是左击
        if event.button() == Qt.LeftButton:
            if not self.current_link_id_list:
                link_id_list: List[int] = self._get_link_id_list(event)
                if not link_id_list:
                    return
                link_id: int = link_id_list[0]
                # 更新item列表
                self._create_item(link_id, True, is_fixed=True)
                # 更新路段ID列表
                self.current_link_id_list.append(link_id)

                # 新建文本窗口
                self.text_window_item = TextWindowItem()
                self.scene.addItem(self.text_window_item)

            elif self.temp_link_id_list:
                # 更新item列表
                for item in self.temp_item_list:
                    item.set_color("yellow")
                    self.fixed_item_list.append(item)
                self.temp_item_list.clear()
                # 更新路段ID列表
                self.current_link_id_list.extend(self.temp_link_id_list[1:])
                self.temp_link_id_list.clear()

        # 如果是右击
        elif event.button() == Qt.RightButton:
            # 清空item
            self._clear_item_list(is_all=True)
            # 执行合并
            if len(self.current_link_id_list) > 1:
                self.params["link_groups"] = {10000: self.current_link_id_list}
                self.func_apply_merge_link(self.params)
            # 清空路段ID列表
            self.current_link_id_list.clear()
            self.temp_link_id_list.clear()
            # # 移除MyNet观察者
            # GlobalVar.detach_observer_of_my_net()

    def handle_mouse_move_event(self, event: QMouseEvent) -> None:
        # 清空路段ID列表
        self.temp_link_id_list.clear()
        # 清空临时item
        self._clear_item_list()

        # 当前还没有路段
        if not self.current_link_id_list:
            return

        # 当前点不能定位到路段
        link_id_list = self._get_link_id_list(event)
        if not link_id_list:
            if self.text_window_item is not None:
                self.text_window_item.setVisible(False)
            return

        # 搜索路径
        from_link_id = self.current_link_id_list[-1]
        to_link_id: int = link_id_list[0]
        from_link_obj = self.netiface.findLink(from_link_id)
        to_link_obj = self.netiface.findLink(to_link_id)
        routing = self.netiface.shortestRouting(from_link_obj, to_link_obj)
        if not routing:
            if self.text_window_item is not None:
                self.text_window_item.setVisible(False)
            return

        # 迭代获取路段ID
        link_id_list = []
        road_id_list = []
        # 获取当前路段
        current_road = from_link_obj
        # 迭代路径
        while current_road:
            # 加入列表
            is_link = current_road.isLink()
            road_id = current_road.id()
            if is_link:
                if road_id == self.current_link_id_list[0] and len(self.current_link_id_list) > 1:
                    if self.text_window_item is not None:
                        self.text_window_item.setVisible(False)
                    return
                link_id_list.append(road_id)
            road_id_list.append((is_link, road_id))
            # 获取下游路段
            current_road = routing.nextRoad(current_road)

        # 判断连通性
        for link_id_1, link_id_2 in zip(link_id_list[:-1], link_id_list[1:]):
            if not self._get_is_connectible(link_id_1, link_id_2):
                if self.text_window_item is not None:
                    self.text_window_item.setVisible(False)
                return

        # 更新临时路段ID列表
        self.temp_link_id_list: List[int] = link_id_list
        # 创建临时item
        for is_link, road_id in road_id_list:
            self._create_item(road_id, is_link, is_fixed=False)
        if self.text_window_item is not None:
            self.text_window_item.setVisible(True)
            # 更新文本
            # 当前路段长度
            current_length = 0
            for link_id in self.current_link_id_list:
                link_obj = self.netiface.findLink(link_id)
                current_length += link_obj.length()
            # 新增长度
            new_length = 0
            for link_id in self.temp_link_id_list[1:]:
                link_obj = self.netiface.findLink(link_id)
                new_length += link_obj.length()
            # 累计长度
            total_length = current_length + new_length
            # 格式化
            current_length = f"{current_length:.2f}"
            new_length = f"{new_length:.2f}"
            total_length = f"{total_length:.2f}"
            text = f"\n 【各路段长度相加】\n 已有长度：{current_length:>9} m \n 新增长度：{new_length:>9} m \n 累计长度：{total_length:>9} m \n"
            self.text_window_item.set_text(text)
            # 更新位置
            scene_pos = self.view.mapToScene(event.pos())
            self.text_window_item.set_pos(scene_pos.x(), scene_pos.y())

    def before_detach(self) -> None:
        # 清空item
        self._clear_item_list(is_all=True)

    def _get_link_id_list(self, event: QMouseEvent) -> List[int]:
        # 获取坐标
        pos = self.view.mapToScene(event.pos())
        # 定位路段
        class Widget: mode, utils = "locate", self.utils
        params = {"pos": pos}
        link_id_list: List[int] = MyOperation.apply_link_edit_operation(Widget(), params)
        return link_id_list

    def _create_item(self, road_id: int, is_link: bool, is_fixed: bool) -> None:
        if is_link and road_id in self.current_link_id_list:
            return
        road = self.netiface.findLink(road_id) if is_link else self.netiface.findConnector(road_id)
        points = road.polygon()
        color = "yellow" if is_fixed else (239, 104, 32)
        item = HighLightPathItem(points, color=color)
        self.scene.addItem(item)
        if is_fixed:
            self.fixed_item_list.append(item)
        else:
            self.temp_item_list.append(item)

    def _clear_item_list(self, is_all: bool = False) -> None:
        if is_all:
            for item in self.fixed_item_list:
                self.scene.removeItem(item)
            self.fixed_item_list.clear()
            if self.text_window_item is not None:
                self.scene.removeItem(self.text_window_item)
        for item in self.temp_item_list:
            self.scene.removeItem(item)
        self.temp_item_list.clear()

    def _get_is_connectible(self, fist_link_id: int, second_link_id: int) -> bool:
        ignore_lane_type: bool = self.params["ignore_lane_type"]
        ignore_missing_connector: bool = self.params["ignore_missing_connector"]

        # 获取两路段对象, 一定是联通的
        first_link_obj = self.netiface.findLink(fist_link_id)
        second_link_obj = self.netiface.findLink(second_link_id)

        # 上游路段只有一个下游路段
        fist_link_to_connectors = first_link_obj.toConnectors()
        if len(fist_link_to_connectors) != 1:
            return False

        # 下游路段只有一个上游路段
        second_link_from_connectors = second_link_obj.fromConnectors()
        if len(second_link_from_connectors) != 1:
            return False

        # 车道数需要相同
        first_link_lane_count = first_link_obj.laneCount()
        second_link_lane_count = second_link_obj.laneCount()
        if first_link_lane_count != second_link_lane_count:
            return False

        # 各车道类型相同
        first_link_lane_actions = [lane.actionType() for lane in first_link_obj.lanes()]
        second_link_lane_actions = [lane.actionType() for lane in second_link_obj.lanes()]
        if not ignore_lane_type and first_link_lane_actions != second_link_lane_actions:
            return False

        # 车道连接的数量不能缺失
        connector_obj = self.netiface.findConnectorByLinkIds(fist_link_id, second_link_id)
        lane_connector_count = len(connector_obj.laneConnectors())
        if lane_connector_count != first_link_lane_count:
            if not ignore_missing_connector:
                return False
        return True
