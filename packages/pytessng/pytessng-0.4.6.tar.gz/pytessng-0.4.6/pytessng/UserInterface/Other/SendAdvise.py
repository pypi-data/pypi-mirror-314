from PySide2.QtWidgets import QLabel, QTextEdit, QPushButton

from ..BaseUI import BaseUserInterface, MyQVBoxLayout


class SendAdvise(BaseUserInterface):
    name: str = "提交用户反馈"
    height: int = 100

    def set_widget_layout(self):
        # 第一行：文本
        self.label = QLabel('感谢您使用TESS NG系列产品，欢迎您提出宝贵的建议和意见！')
        # 第二行：输入框
        self.text_edit = QTextEdit()
        self.text_edit.setFixedHeight(6 * self.text_edit.fontMetrics().height())
        # 第三行：按钮
        self.button = QPushButton('提交')

        # 总体布局
        layout = MyQVBoxLayout([
            self.label,
            self.text_edit,
            self.button
        ])
        self.setLayout(layout)

    def set_monitor_connect(self):
        self.text_edit.textChanged.connect(self.apply_monitor_state)

    def set_button_connect(self):
        self.button.clicked.connect(self.apply_button_action)

    def set_default_state(self):
        self.button.setEnabled(False)

    def apply_monitor_state(self):
        text = self.text_edit.toPlainText()
        self.button.setEnabled(bool(text))

    def apply_button_action(self):
        text = self.text_edit.toPlainText()
        status_code = self.utils.send_message("suggestion", text)
        if status_code == 201:
            message = "提交成功，感谢您的反馈！"
        else:
            message = "感谢您的反馈！"
        # 关闭窗口
        self.close()
        # 提示信息
        self.utils.show_info_box(message)
