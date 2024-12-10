from typing import List
from PySide2.QtWidgets import QStyledItemDelegate, QCheckBox, QComboBox, QStyleOptionViewItem
from PySide2.QtCore import Qt, QSize, QModelIndex, QEvent
from PySide2.QtGui import QStandardItemModel, QStandardItem, QFontMetrics


class ComboBoxWithCheckBoxes(QComboBox):
    def __init__(self, items: List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items: List[str] = items

        # 设置下拉框的模型
        model = self._create_model()
        self.setModel(model)
        # 设置项的委托: 控制如何在下拉框中显示和编辑复选框
        self.setItemDelegate(CheckBoxDelegate(self))

    # 获取被勾选的行
    def checked_items(self) -> List[str]:
        checked_items = []
        for row in range(self.model().rowCount()):
            item = self.model().item(row)
            if item.checkState() == Qt.Checked:  # 如果复选框被勾选
                checked_items.append(item.text())
        return checked_items

    def _create_model(self):
        model = QStandardItemModel()
        for item in self.items:
            checkable_item = QStandardItem(item)
            checkable_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkable_item.setData(Qt.Unchecked, Qt.CheckStateRole)
            model.appendRow(checkable_item)
        return model

    # 设置下拉框的宽度
    def showPopup(self):
        view = self.view()
        # 字体宽度
        font_metrics = QFontMetrics(view.font())
        # 最低的宽度
        width = 100
        # 根据文本宽度计算宽度
        for row in range(self.model().rowCount()):
            item = self.model().item(row)
            text_width = font_metrics.width(item.text())
            width = max(width, text_width)
        # 设置宽度
        finial_width = max(width + 60, self.width())
        view.setFixedWidth(finial_width)

        # 动态调整高度，计算所有项的总高度
        item_height = view.sizeHintForRow(0)
        total_height = item_height * self.model().rowCount() + 2 * view.frameWidth()
        # 获取屏幕可用的高度
        max_height = 500
        view.setFixedHeight(min(total_height, max_height))

        super(ComboBoxWithCheckBoxes, self).showPopup()


class CheckBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent: QComboBox = None) -> None:
        super().__init__(parent)
        # 标记鼠标是否按下
        self.mouse_pressed: bool = False
        # 记录开始时的选中状态
        self.start_check_state = None

    def createEditor(self, parent: QComboBox, option: QStyleOptionViewItem, index: QModelIndex) -> QCheckBox:
        # 创建编辑器组件，在这里创建一个复选框（QCheckBox）并返回
        checkbox = QCheckBox(parent)
        return checkbox

    def setEditorData(self, editor: QCheckBox, index: QModelIndex) -> None:
        # 设置编辑器中的数据，判断当前项的选中状态并设置到复选框
        editor.setChecked(index.data(Qt.CheckStateRole) == Qt.Checked)

    def setModelData(self, editor: QCheckBox, model: QStandardItemModel, index: QModelIndex) -> None:
        # 当编辑完成后，将复选框中的选中状态更新到数据模型中
        model.setData(index, editor.isChecked(), Qt.CheckStateRole)

    def updateEditorGeometry(self, editor: QCheckBox, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        # 更新编辑器的几何形状，确保复选框的位置和大小与列表项的区域一致
        editor.setGeometry(option.rect)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        # 获取父类提供的默认大小
        size = super(CheckBoxDelegate, self).sizeHint(option, index)
        # 调整行高
        return QSize(size.width(), size.height() + 12)

    def editorEvent(self, event: QEvent, model: QStandardItemModel, option: QStyleOptionViewItem, index: QModelIndex) -> bool:
        # 处理编辑器的事件，在这里监听鼠标点击事件，点击后切换复选框的选中状态
        if event.type() == event.MouseButtonPress and option.rect.contains(event.pos()):
            # 标记鼠标按下
            self.mouse_pressed = True
            # 获取当前项的选中状态
            self.start_check_state = index.data(Qt.CheckStateRole)  # 记录开始时的选中状态
            # 如果当前未选中，则改为选中；如果已选中，则改为未选中
            new_check_state = Qt.Checked if self.start_check_state == Qt.Unchecked else Qt.Unchecked
            # 更新数据模型中的选中状态
            model.setData(index, new_check_state, Qt.CheckStateRole)
            return True

        elif event.type() == QEvent.MouseMove and self.mouse_pressed:
            # 如果鼠标按住并移动，切换被扫过项的选中状态
            if option.rect.contains(event.pos()):
                current_check_state = index.data(Qt.CheckStateRole)
                if current_check_state == self.start_check_state:
                    new_check_state = Qt.Checked if self.start_check_state == Qt.Unchecked else Qt.Unchecked
                    model.setData(index, new_check_state, Qt.CheckStateRole)
            return True

        elif event.type() == QEvent.MouseButtonRelease:
            # 如果鼠标释放，结束切换状态
            self.mouse_pressed = False  # 取消标记
            self.start_check_state = None  # 重置初始状态
            return True

        # 如果事件未被处理，调用父类的事件处理方法
        return super(CheckBoxDelegate, self).editorEvent(event, model, option, index)
