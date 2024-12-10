from PySide2.QtWidgets import QLabel, QWidget, QApplication
from PySide2.QtCore import Qt, QTimer, QPoint, QEvent
from PySide2.QtGui import QCursor, QPixmap, QPainter


class QuestionMark(QLabel):
    def __init__(self, picture_path: str, parent=None):
        super().__init__(parent)
        self.picture_path: str = picture_path

        # 设置文本
        self.setText('[?]')
        # 设置固定宽度
        self.setFixedWidth(50)
        # 设置居左
        self.setAlignment(Qt.AlignLeft)
        self.setCursor(Qt.PointingHandCursor)

        # 图片窗口
        self.image_window = None

        # 创建定时器，用于定期检查鼠标位置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_mouse_position)
        self.timer.start(250)  # ms

    def enterEvent(self, event: QEvent) -> None:
        self.show_image_window(event)

    def show_image_window(self, event: QEvent):
        if self.image_window is None:
            self.image_window = ImageWindow(self.picture_path)
            self.image_window.show()

    def hide_image_window(self):
        if self.image_window is not None:
            self.image_window.close()
            self.image_window = None

    # 检查鼠标是否在按钮或图片窗口区域内
    def check_mouse_position(self):
        # 获取鼠标位置
        mouse_pos = QCursor.pos()
        # 获取按钮的区域
        x, y = self.mapToGlobal(QPoint(0, 0)).x(), self.mapToGlobal(QPoint(0, 0)).y()
        w, h = self.width(), self.height()
        # 鼠标是否在按钮区域内
        is_inside_rect = (x <= mouse_pos.x() <= x + w and y <= mouse_pos.y() <= y + h)
        # 鼠标不在按钮区域就关闭图片窗口
        if not is_inside_rect:
            self.hide_image_window()


class ImageWindow(QWidget):
    def __init__(self, picture_path: str):
        super().__init__()
        self.setWindowTitle("图片窗口")
        self.setWindowFlags(Qt.ToolTip)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置位置和大小
        self.setGeometry(0, 0, 1600, 1000)
        # 移动窗口到屏幕中央
        self.move_to_center()

        # 加载并缩放图片为窗口的大小
        self.pixmap = QPixmap(picture_path)
        self.scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    # 移动窗口到屏幕中央
    def move_to_center(self):
        # 获取屏幕尺寸
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        # 计算屏幕中心点
        center_point = screen_geometry.center()
        # 计算窗口左上角的坐标使其居中
        x = center_point.x() - self.width() // 2
        y = center_point.y() - self.height() // 2
        # 移动窗口到屏幕中央
        self.move(x, y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect().center() - self.scaled_pixmap.rect().center(), self.scaled_pixmap)
