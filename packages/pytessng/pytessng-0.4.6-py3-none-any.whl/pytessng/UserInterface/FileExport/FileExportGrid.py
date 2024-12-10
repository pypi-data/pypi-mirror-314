import copy
from PySide2.QtWidgets import QLabel, QRadioButton, QPushButton, QComboBox, QAction, QTextBrowser
from PySide2.QtWidgets import QDockWidget
from PySide2.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QGraphicsEllipseItem, QGraphicsLineItem
from PySide2.QtGui import QFont, QPen, QBrush, QColor
from PySide2.QtGui import Qt

from ..BaseUI import BaseUserInterface, MyQHBoxLayout, MyQVBoxLayout
from ..BaseMouse import BaseMouse
from pytessng.GlobalVar import GlobalVar
from pytessng.ToolInterface import MyOperation


class FileExportGrid(BaseUserInterface):
    name: str = "生成城市推演雷达区域文件"
    mode: str = "grid"
    format: tuple = ("Json", "json")

    # 单例模式
    _instance = None
    _init = False

    def __new__(cls, ):
        if FileExportGrid._instance is None:
            FileExportGrid._instance = super().__new__(cls)
        return FileExportGrid._instance

    def __init__(self, *args, **kwargs):
        if FileExportGrid._init:
            return
        FileExportGrid._init = True

        super().__init__(*args, **kwargs)
        # TESSNG接口
        self.netiface = self.iface.netInterface()

        # 按钮
        self.action: QAction = GlobalVar.actions_related_to_mouse_event["grid"]
        # 当前是否需要鼠标事件
        self.is_need_select_file: bool = False

        # 浮动面板组件
        self.dock_widget = None
        # 区域数据
        self.zone_data = ZoneData()
        # 表格
        self.table = None
        # 画布
        self.scene = None

    # 重写抽象父类BaseUserInterface的方法
    def load(self):
        if self.action.isChecked():
            # 更改按钮状态
            self.action.setChecked(True)
            # 设置界面布局
            self.set_widget_layout()
            # 设置组件监测关系
            self.set_monitor_connect()
            # 设置按钮关联关系
            self.set_button_connect()
            # 设置默认状态
            self.set_default_state()
        else:
            self.exit()

    # 重写父类QWidget的方法
    def show(self):
        if self.action.isChecked():
            win = self.guiiface.mainWindow()
            self.dock_widget = QDockWidget(self.name, win)
            # self.dock_widget.setTitleBarWidget(QWidget())  # 隐藏标题栏
            self.dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)  # 不能浮动
            self.dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea)  # 只能停靠在左侧区域
            self.dock_widget.setWidget(self)
            self.guiiface.addDockWidgetToMainWindow(Qt.DockWidgetArea(1), self.dock_widget)

    # 重写父类QWidget的方法
    def close(self, actual_close: bool = False):
        # 因为执行完操作时，MyOeration会调用close方法，但这时并不想关闭界面，所以这里需要判断是否是实际关闭
        if actual_close:
            # 父类方法关闭界面
            super().close()
            # 移除左侧界面
            if self.dock_widget:
                self.guiiface.removeDockWidgetFromMainWindow(self.dock_widget)

    def set_widget_layout(self):
        # 1.文本
        text = "\n【交叉口雷达区域选择工具】\n\n  — 左键点击生成点\n  — 右键点击将点连成多边形\n\n"
        self.label_caption = QLabel(text)
        self.label_caption.setFont(QFont(u"微软雅黑", 12))
        # 2.按钮
        self.button_load = QPushButton("加载路口")
        self.button_close = QPushButton("关闭窗口")
        # 3.文本、下拉框
        self.label_intersection = QLabel("路口名称：")
        self.combo_intersection = QComboBox()
        # 4.文本、单选框
        self.label_size = QLabel("区域类型：")
        self.radio_small = QRadioButton('小区域')
        self.radio_big = QRadioButton('大区域')
        # 5.按钮
        self.button_select = QPushButton("选择")
        self.button_clear = QPushButton("清除")
        self.button_select.setDisabled(True)
        self.button_clear.setDisabled(True)
        # 6.表格
        self.table = MyTable(self.zone_data)
        # 7.按钮
        self.button_clear_all = QPushButton("清空全部")
        self.button_clear_all.setDisabled(True)
        # 8.文本、下拉框
        self.label_grid = QLabel("网格化大小：")
        self.combo_grid = QComboBox()
        self.combo_grid.addItems(["0.5 m", "1 m", "2 m", "5 m"])
        self.combo_grid.setCurrentIndex(1)
        # 9.按钮
        self.button_export_grid = QPushButton("生成 grid.json")
        self.button_export_grid.setDisabled(True)
        # 10.信息窗
        self.message = QTextBrowser()

        # 总体布局
        layout = MyQVBoxLayout([
            self.label_caption,
            MyQHBoxLayout([self.button_load, self.button_close]),
            MyQHBoxLayout([self.label_intersection, self.combo_intersection]),
            MyQHBoxLayout([self.label_size, self.radio_small, self.radio_big]),
            MyQHBoxLayout([self.button_select, self.button_clear]),
            self.table,
            self.button_clear_all,
            MyQHBoxLayout([self.label_grid, self.combo_grid]),
            self.button_export_grid,
            self.message,
        ])
        self.setLayout(layout)

    def set_monitor_connect(self):
        self.combo_intersection.currentIndexChanged.connect(self.apply_monitor_state)
        self.radio_small.clicked.connect(self.apply_monitor_state)
        self.radio_big.clicked.connect(self.apply_monitor_state)
        self.table.itemChanged.connect(self.apply_monitor_state)

    def set_button_connect(self):
        self.button_load.clicked.connect(self.load_intersections)
        self.button_close.clicked.connect(self.exit)
        self.button_select.clicked.connect(self.start_select_points)
        self.button_clear.clicked.connect(self.clear_points)
        self.button_clear_all.clicked.connect(self.clear_all_points)
        self.button_export_grid.clicked.connect(self.apply_button_action)

        def disconnect() -> None:
            if self.scene and self.scene.is_selecting:
                # 选择【取消工具】
                self.guiiface.actionNullGMapTool().trigger()
                # 重新添加myNet观察者
                GlobalVar.attach_observer_of_my_net(self.scene)
                self.utils.show_info_box("请先选择完毕！")

        # 把其他关联上
        for actions in [self.guiiface.netToolBar().actions(), self.guiiface.operToolBar().actions()]:
            for action in actions:
                if action.text() == "取消工具":
                    continue
                action.triggered.connect(disconnect)

    def set_default_state(self):
        # 单选框状态
        self.radio_small.setChecked(True)

    def apply_monitor_state(self):
        intersection_name = self.combo_intersection.currentText()
        if not intersection_name:
            return
        zone_type = "small" if self.radio_small.isChecked() else "big"

        # 选择按钮和清除按钮
        point_list = self.table.zone_data.get_value(intersection_name, zone_type)
        if point_list is None:
            self.button_select.setDisabled(False)
            self.button_clear.setDisabled(True)
            self.update_message("")
        else:
            self.button_select.setDisabled(True)
            self.button_clear.setDisabled(False)
            message = "\n".join([str([round(x, 3), round(y, 3)]) for x, y in point_list])
            self.update_message(f"多边形: \n{message}")

        # 清空按钮和生成按钮
        is_empty = self.table.zone_data.empty()
        if is_empty:
            self.button_clear_all.setDisabled(True)
            self.button_export_grid.setDisabled(True)
        else:
            self.button_clear_all.setDisabled(False)
            self.button_export_grid.setDisabled(False)

    def apply_button_action(self):
        length = float(self.combo_grid.currentText().split(" ")[0])
        params = {"length": length, "data": self.zone_data.data}

        # 执行导出
        MyOperation.apply_other_operation(self, params)

    # =================================================================================

    # 槽函数：加载按钮
    def load_intersections(self):
        # 读取交叉口名称
        intersections = [signalGroup.groupName() for signalGroup in self.netiface.signalGroups()]
        # 更新数据
        self.zone_data.init(intersections)
        # 更新表格
        self.table.init(intersections)
        # 设置下拉框元素
        self.combo_intersection.clear()
        self.combo_intersection.addItems(intersections)
        # 显示信息
        self.utils.show_info_box("加载成功！")

    # 槽函数：退出关闭界面
    def exit(self):
        # 更改按钮状态
        self.action.setChecked(False)
        # 关闭：移除界面
        self.close(True)

    # 槽函数：选择按钮
    def start_select_points(self):
        # 当前为True说明是结束选择
        if self.is_need_select_file:
            if self.scene.is_selecting:
                self.utils.show_info_box("请先选择完毕！")
                return

            self.is_need_select_file = False

            # 设置按钮文字
            self.button_select.setText("选择")
            # 清空按钮设置可点击
            self.button_clear_all.setDisabled(False)
            # 生成按钮设置可点击
            self.button_export_grid.setDisabled(False)

        # 当前为False说明是开始选择
        else:
            self.is_need_select_file = True

            # 设置按钮文字
            self.button_select.setText("取消选择")
            # 清空按钮设置不可点击
            self.button_clear_all.setDisabled(True)
            # 生成按钮设置不可点击
            self.button_export_grid.setDisabled(True)

            # 设置为取消选择按钮
            self.guiiface.actionNullGMapTool().trigger()

            # 添加MyNet观察者
            self.scene = Scene(self)
            GlobalVar.attach_observer_of_my_net(self.scene)

    # 槽函数：清除按钮
    def clear_points(self):
        intersection_name = self.combo_intersection.currentText()
        zone_type = "small" if self.radio_small.isChecked() else "big"

        # 更新数据
        self.zone_data.del_value(intersection_name, zone_type)
        # 更新表格
        self.table.update_table_element(intersection_name, zone_type, False)
        # 删除元素
        self.scene.remove_items([(intersection_name, zone_type)])
        # 显示信息
        self.update_message("")
        self.utils.show_info_box("清除成功！")

    # 槽函数：清空按钮
    def clear_all_points(self):
        keys = []
        for intersection_name in self.zone_data.data.keys():
            for zone_type in ["small", "big"]:
                keys.append((intersection_name, zone_type))
                # 更新数据
                self.zone_data.del_value(intersection_name, zone_type)
                # 更新表格
                self.table.update_table_element(intersection_name, zone_type, False)
        # 删除元素
        self.scene.remove_items(keys)
        # 显示信息
        self.update_message("")
        self.utils.show_info_box("全部清除成功！")

    # 鼠标事件后函数
    def after_select_points(self, intersection_name: str, zone_type: str, point_list: list):
        # 更新数据
        self.zone_data.set_value(intersection_name, zone_type, point_list)
        # 更新表格
        self.table.update_table_element(intersection_name, zone_type, True)
        # 更新状态
        self.start_select_points()
        # 显示信息
        message = "\n".join([str([round(x, 3), round(y, 3)]) for x, y in self.scene.temp_point_list])
        self.update_message(f"多边形: \n{message}")
        self.utils.show_info_box("选点成功！")

    # 信息窗显示函数
    def update_message(self, message):
        self.message.clear()
        self.message.setText(message)


# 区域数据
class ZoneData:
    def __init__(self):
        self.data = dict()

    def init(self, intersections: list) -> None:
        self.data.clear()
        for intersection_name in intersections:
            if intersection_name not in self.data:
                self.data[intersection_name] = dict()
            for zone_type in ["small", "big"]:
                self.set_value(intersection_name, zone_type, None)

    def set_value(self, intersection_name: str, zone_type: str, data: list) -> None:
        self.data[intersection_name][zone_type] = data

    def get_value(self, intersection_name: str, zone_type: str) -> list:
        return self.data[intersection_name][zone_type]

    def del_value(self, intersection_name: str, zone_type: str) -> None:
        self.data[intersection_name][zone_type] = None

    def name_list(self) -> list:
        return list(self.data.keys())

    def empty(self) -> bool:
        for intersection_name, intersection_value in self.data.items():
            for zone_type in ["small", "big"]:
                if intersection_value[zone_type] is not None:
                    return False
        return True


# 表格
class MyTable(QTableWidget):
    def __init__(self, zone_data):
        super().__init__()
        self.zone_data = zone_data

        self.setColumnCount(3)  # 设置列数
        self.setRowCount(0)  # 设置行数
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 两边无间隙
        self.setHorizontalHeaderLabels(["路口名称", "小区域", "大区域"])

    def init(self, intersections: list) -> None:
        # 设置表格
        self.clearContents()  # 清空表格
        self.setRowCount(len(intersections))  # 设置行数
        # 更新元素
        for index, intersection_name in enumerate(intersections):
            # 路口名称
            self.setItem(index, 0, QTableWidgetItem(intersection_name))
            for zone_type in ["small", "big"]:
                # 更新表格
                self.update_table_element(intersection_name, zone_type, False)
        self.resizeColumnsToContents()

    def update_table_element(self, intersection_name: str, zone_type: str, is_have_data: bool):
        row = self.zone_data.name_list().index(intersection_name)
        col = 1 if zone_type == "small" else 2
        if is_have_data is True:
            self.setItem(row, col, QTableWidgetItem("■" * 8))
        else:
            self.setItem(row, col, QTableWidgetItem("□" * 8))


# 场景画布
class Scene(BaseMouse):
    def __init__(self, GUI):
        super().__init__()
        self.GUI = GUI

        # 点的列表
        self.temp_point_list: list = []
        # 是否正在选择
        self.is_selecting = True

    def handle_mouse_press_event(self, event):
        intersection_name = self.GUI.combo_intersection.currentText()
        zone_type = "small" if self.GUI.radio_small.isChecked() else "big"

        # 左击
        if event.button() == Qt.LeftButton:
            self.handle_mouse_left_press_event(event, intersection_name, zone_type)
        # 右击
        elif event.button() == Qt.RightButton:
            self.handle_mouse_right_press_event(intersection_name, zone_type)

    def handle_mouse_left_press_event(self, event, intersection_name: str, zone_type: str):
        # 获取坐标
        pos = self.view.mapToScene(event.pos())
        x, y = pos.x(), pos.y()
        self.temp_point_list.append([x, y])

        # 加点
        radius = 2
        item = QGraphicsEllipseItem(x - radius / 2, y - radius / 2, radius, radius)
        item.setBrush(QBrush(QColor(Qt.red)))
        self.add_item((intersection_name, zone_type), item)

    def handle_mouse_right_press_event(self, intersection_name: str, zone_type: str):
        if len(self.temp_point_list) <= 2:
            self.GUI.utils.show_info_box("请选择至少三个点！")
            return

        # 修改状态
        self.is_selecting = False
        # 移除MyNet观察者
        GlobalVar.detach_observer_of_my_net()

        # 连线
        for i in range(len(self.temp_point_list)):
            this, next = i, (i + 1) % len(self.temp_point_list)
            x1, y1 = self.temp_point_list[this]
            x2, y2 = self.temp_point_list[next]

            item = QGraphicsLineItem(x1, y1, x2, y2)
            item.setPen(QPen(Qt.blue))
            self.add_item((intersection_name, zone_type), item)

        # 取负
        self.temp_point_list = [[x, -y] for x, y in self.temp_point_list]

        point_list = copy.copy(self.temp_point_list)
        # 更新数据
        self.GUI.after_select_points(intersection_name, zone_type, point_list)
        # 清空列表
        self.temp_point_list.clear()

    def handle_key_press_event(self, event) -> None:
        if event.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
            intersection_name = self.GUI.combo_intersection.currentText()
            zone_type = "small" if self.GUI.radio_small.isChecked() else "big"
            self.handle_mouse_right_press_event(intersection_name, zone_type)

    # 自定义方法：创建item
    def add_item(self, key: tuple, item):
        item.setZValue(10000)
        item.setData(1, key[0])  # intersection_name
        item.setData(2, key[1])  # zone_type
        self.scene.addItem(item)

    # 自定义方法：移除item
    def remove_items(self, keys: list):
        for i, item in enumerate(self.scene.items()):
            if (item.data(1), item.data(2)) in keys:
                self.scene.removeItem(item)
