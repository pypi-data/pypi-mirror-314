from pyproj import Proj
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton
from PySide2.QtGui import QDoubleValidator

from ..BaseUI import BaseUserInterface, MyQHBoxLayout, MyQVBoxLayout


class ViewAttrs(BaseUserInterface):
    name: str = "查看路网属性"

    def set_widget_layout(self):
        # 第一行：文本、输入框
        self.label_proj_string = QLabel('投影字符串：')
        self.line_edit_proj_string = QLineEdit()
        # 第二行：文本、输入框
        self.label_move_distance = QLabel('移动距离（m）：')
        self.line_edit_move_distance_x = QLineEdit()
        self.line_edit_move_distance_y = QLineEdit()
        # 第三行：按钮
        self.button = QPushButton('确定')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.label_proj_string, self.line_edit_proj_string]),
            MyQHBoxLayout([self.label_move_distance, self.line_edit_move_distance_x, self.line_edit_move_distance_y]),
            self.button
        ])
        self.setLayout(layout)

        # 限制输入框内容
        validator = QDoubleValidator()
        self.line_edit_move_distance_x.setValidator(validator)
        self.line_edit_move_distance_y.setValidator(validator)

    def set_monitor_connect(self):
        self.line_edit_proj_string.textChanged.connect(self.apply_monitor_state)
        self.line_edit_move_distance_x.textChanged.connect(self.apply_monitor_state)
        self.line_edit_move_distance_y.textChanged.connect(self.apply_monitor_state)

    def set_button_connect(self):
        self.button.clicked.connect(self.apply_button_action)

    def set_default_state(self):
        # 读取路网属性
        netiface = self.iface.netInterface()
        attrs = netiface.netAttrs().otherAttrs()
        # 显示投影字符串
        proj_string = attrs.get("proj_string") or "无"
        self.line_edit_proj_string.setText(proj_string)
        # 显示移动距离
        move_distance = attrs.get("move_distance", {"x_move": 0, "y_move": 0})
        self.line_edit_move_distance_x.setText(str(round(move_distance["x_move"], 2)))
        self.line_edit_move_distance_y.setText(str(round(move_distance["y_move"], 2)))
        # 按钮文本
        self.button.setText('确定')

    def apply_monitor_state(self):
        # 按钮文本
        self.button.setText('保存')

        # 投影字符串
        proj_string = self.line_edit_proj_string.text()
        # 验证投影字符串
        proj_string_is_ok = False
        try:
            if proj_string != "无":
                Proj(proj_string)
            proj_string_is_ok = True
        except:
            pass

        # 设置可用状态
        self.button.setEnabled(proj_string_is_ok)

    def apply_button_action(self):
        # 投影字符串
        proj_string = self.line_edit_proj_string.text()

        # 移动距离
        x_move = float(self.line_edit_move_distance_x.text())
        y_move = float(self.line_edit_move_distance_y.text())

        # 设置路网属性
        netiface = self.iface.netInterface()
        attrs = netiface.netAttrs().otherAttrs()
        attrs["proj_string"] = proj_string
        attrs["move_distance"] = {"x_move": x_move, "y_move": y_move}
        network_name = netiface.netAttrs().netName()
        netiface.setNetAttrs(network_name, otherAttrsJson=attrs)

        # 关闭窗口
        self.close()
