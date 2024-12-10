from typing import List, Tuple
from PySide2.QtWidgets import QGraphicsProxyWidget, QTextEdit
from PySide2.QtGui import QFontMetrics


class TextWindowItem(QGraphicsProxyWidget):
    def __init__(self, color: Tuple[int, int, int] = (255, 255, 255), transparency: float = 128, font_size: int = 14, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_sheet = ("QTextEdit {"
                       f"font-size: {font_size}pt;  /* 设置字体大小 */ "
                       f"background-color: rgba({color[0]}, {color[1]}, {color[2]}, {transparency});  /* 设置背景颜色为透明 */ "
                       "}")
        self.text_box = QTextEdit()
        self.text_box.setText("")
        self.text_box.setStyleSheet(style_sheet)  # 应用样式表

        # 设置文本框
        self.setWidget(self.text_box)
        # 忽略缩放
        self.setFlag(QGraphicsProxyWidget.ItemIgnoresTransformations)
        # 设置Z值
        self.setZValue(9999+1)

    def set_text(self, text: str) -> None:
        self.text_box.setText(text)

        font = self.text_box.font()
        font_metrics = QFontMetrics(font)
        plain_text: str = self.text_box.toPlainText()
        texts: List[str] = plain_text.split("\n")
        width = max([font_metrics.width(text) for text in texts]) + 20
        height = len(texts) * font_metrics.height() * 1.3
        self.text_box.setFixedSize(width, height)

    def set_pos(self, x: float, y: float) -> None:
        self.setPos(x, y)
