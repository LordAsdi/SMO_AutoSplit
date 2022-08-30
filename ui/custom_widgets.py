from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from ui.fonts import *
from ui.colors import Color
from ui.styles import Style


def get_icon_path(component_name):
    icon_path = "ui/resources/icons/"
    if component_name == "moon_get":
        icon_path += "moon_alt.png"
    elif component_name == "moon_story":
        icon_path += "moon_story.png"
    elif component_name == "moon_multi":
        icon_path += "moon_multi.png"
    elif component_name == "cutscene_skip":
        icon_path += "cutscene.png"
    elif component_name == "subarea":
        icon_path += "door.png"
    elif component_name == "black_screen":
        icon_path += "monitor.png"
    elif component_name == "kingdom_end":
        icon_path += "castle.png"
    elif component_name == "world_map_fadeout":
        icon_path += "globe.png"
    elif component_name == "compass":
        icon_path += "compass.png"
    elif component_name == "odyssey":
        icon_path += "odyssey.png"
    elif component_name == "cap_end":
        icon_path += "castle_cap.png"
    elif component_name == "moon_end":
        icon_path += "castle_moon.png"
    else:
        icon_path += ""

    return icon_path


class PreviewLabel(QLabel):
    sig_clicked = pyqtSignal()

    def __init__(self, text):
        super().__init__(text)
        self.installEventFilter(self)
        self.overlay = False
        self.enabled = True

        self.setFont(font_12pt)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(QSize(160, 90))
        self.setMaximumSize(QSize(640, 360))
        self.setStyleSheet("background-color: rgba(27, 29, 35, 200); color: rgb(44, 49, 60);")

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Resize:
            self.setFixedHeight(int(self.width() / 16 * 9))
        return super(QLabel, self).eventFilter(source, event)

    def enterEvent(self, a0: QtCore.QEvent):
        self.overlay = True
        self.update_overlay()

    def leaveEvent(self, a0: QtCore.QEvent):
        self.overlay = False

    def mouseReleaseEvent(self, ev: QMouseEvent):
        self.sig_clicked.emit()

    def update_overlay(self):
        if self.enabled:
            self.setText("Click to disable preview")
        else:
            self.setText("Click to enable preview")


class SplitWidget(QWidget):
    def __init__(self, icon_path, text):
        super().__init__()
        self.setFixedHeight(36)
        layout = QHBoxLayout()
        layout.setSpacing(6)
        layout.setContentsMargins(6, 0, 6, 0)

        self.icon = QLabel()
        self.icon.setPixmap(QPixmap(icon_path))
        self.icon.setScaledContents(True)
        self.icon.setFixedSize(QSize(24, 24))

        label = QLabel(text)
        label.setFont(font_10pt)

        layout.addWidget(self.icon)
        layout.addWidget(label)

        self.setLayout(layout)
        self.setStyleSheet("background-color: transparent;")

    def set_not_active(self):
        self.icon.setPixmap(QPixmap("ui/resources/icons/location_outline.png"))

    def set_active(self):
        self.icon.setPixmap(QPixmap("ui/resources/icons/location.png"))

    def set_complete(self):
        self.icon.setPixmap(QPixmap("ui/resources/icons/location_checkmark.png"))


class RouteSplitWidget(QWidget):
    def __init__(self, list_widget_item, split):
        super().__init__()
        self.list_widget_item = list_widget_item
        self.split = split
        self.setFixedHeight(36)

        layout = QHBoxLayout()
        layout.setSpacing(6)
        layout.setContentsMargins(6, 0, 6, 0)

        self.icon = QLabel()
        self.icon.setScaledContents(True)
        self.icon.setFixedSize(QSize(24, 24))
        self.update_icon()

        self.label = QLabel(split.name)
        self.label.setFont(font_10pt)

        self.delete_button = QPushButton()
        self.delete_button.setFixedSize(QSize(28, 28))
        self.delete_button.setStyleSheet(Style.btn_rounded)
        self.delete_button.setToolTip("Delete")
        self.delete_button.setIcon(QIcon(QPixmap("ui/resources/icons/delete.png")))
        self.delete_button.setIconSize(QtCore.QSize(22, 22))

        self.duplicate_button = QPushButton()
        self.duplicate_button.setFixedSize(QSize(28, 28))
        self.duplicate_button.setStyleSheet(Style.btn_rounded)
        self.duplicate_button.setToolTip("Duplicate")
        self.duplicate_button.setIcon(QIcon(QPixmap("ui/resources/icons/copy.png")))
        self.duplicate_button.setIconSize(QtCore.QSize(22, 22))

        handle = QLabel()
        handle.setPixmap(QPixmap("ui/resources/icons/handle.png"))
        handle.setScaledContents(True)
        handle.setFixedSize(QSize(28, 28))
        handle.setToolTip("Move")

        layout.addWidget(self.icon)
        layout.addWidget(self.label)
        layout.addWidget(self.duplicate_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(handle)

        self.setLayout(layout)
        self.setStyleSheet("background-color: transparent;")

    def set_text(self, text):
        self.label.setText(text)

    def update_icon(self):
        icon_path = get_icon_path(self.split.type)

        self.icon.setPixmap(QPixmap(icon_path))


class SplitList(QListWidget):
    def __init__(self):
        super().__init__()

    # Ignore mouse events
    def mousePressEvent(self, *args, **kwargs):
        pass

    def mouseReleaseEvent(self, *args, **kwargs):
        pass

    def mouseDoubleClickEvent(self, *args, **kwargs):
        pass

    def mouseMoveEvent(self, *args, **kwargs):
        pass

    # Ignore keyboard events
    def keyPressEvent(self, e: QKeyEvent):
        pass


class CustomDropIndicator(QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget=None):
        if element == self.PE_IndicatorItemViewItemDrop and not option.rect.isNull():
            option_new = QStyleOption(option)
            option_new.rect.setLeft(0)
            if widget:
                option_new.rect.setRight(widget.width())
            option = option_new
        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(2)
        painter.setPen(pen)
        super().drawPrimitive(element, option, painter, widget)


class RouteSplitList(QListWidget):
    sig_dropped = pyqtSignal()

    def __init__(self):
        super().__init__()

    def dropEvent(self, event):
        super(RouteSplitList, self).dropEvent(event)
        event.accept()
        self.sig_dropped.emit()


class FlowLayout(QLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(QMargins(0, 0, 0, 0))

        self._item_list = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]

        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._do_layout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()

        for item in self._item_list:
            style = item.widget().style()
            layout_spacing_x = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal
            )
            layout_spacing_y = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical
            )
            space_x = spacing + layout_spacing_x
            space_y = spacing + layout_spacing_y
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()


class SingleBoxWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.frame_layout = QHBoxLayout()
        self.frame_layout.setContentsMargins(6, 0, 6, 0)
        self.frame_layout.setSpacing(4)

        frame = QFrame()
        frame.setStyleSheet(f"background-color: {Color.foreground};")
        frame.setLayout(self.frame_layout)

        layout.addWidget(frame)

        self.setFixedHeight(36)
        self.setLayout(layout)

    def add_widget(self, widget, stretch=0):
        self.frame_layout.addWidget(widget, stretch)


class DualBoxWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.left_layout = QHBoxLayout()
        self.left_layout.setContentsMargins(6, 0, 6, 0)

        frame_left = QFrame()
        frame_left.setStyleSheet(f"background-color: {Color.foreground};")
        frame_left.setLayout(self.left_layout)

        self.right_layout = QHBoxLayout()
        self.right_layout.setSpacing(6)
        self.right_layout.setContentsMargins(6, 0, 6, 0)

        frame_right = QFrame()
        frame_right.setStyleSheet(f"background-color: {Color.foreground};")
        frame_right.setLayout(self.right_layout)

        layout.addWidget(frame_left, 1)
        layout.addWidget(frame_right, 1)

        self.setFixedHeight(36)
        self.setLayout(layout)

    def add_widget_left(self, widget):
        self.left_layout.addWidget(widget)

    def add_widget_right(self, widget):
        self.right_layout.addWidget(widget)


class TextInputWide(DualBoxWidget):
    def __init__(self, text):
        super().__init__()

        label = QLabel(text)
        label.setFont(font_8pt)

        self.add_widget_left(label)

        self.input_field = QLineEdit()
        self.input_field.setFixedHeight(32)
        self.input_field.setFont(font_8pt)
        self.input_field.setStyleSheet(Style.input_field)

        self.add_widget_right(self.input_field)

    def focus(self):
        self.input_field.setFocus()

    def set_text(self, text):
        if text is not None:
            self.input_field.setText(text)

    def get_text(self):
        return self.input_field.text()


class DropdownWide(DualBoxWidget):
    def __init__(self, text):
        super().__init__()
        self.options = None

        label = QLabel(text)
        label.setFont(font_8pt)

        self.add_widget_left(label)

        self.dropdown = QComboBox()
        self.dropdown.setFixedHeight(32)
        self.dropdown.setFont(font_8pt)
        self.dropdown.setStyleSheet(Style.dropdown)
        self.dropdown.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        self.add_widget_right(self.dropdown)

    def set_options(self, options):
        if not isinstance(options, dict):
            return
        elif len(options) < 1:
            return

        self.options = options

        for option in self.options.values():
            self.dropdown.addItem(option)

        self.dropdown.setCurrentIndex(0)

    def clear_options(self):
        self.dropdown.clear()

    def set_index(self, index):
        if self.options is not None and isinstance(index, int) and 0 <= index < len(self.options):
            self.dropdown.setCurrentIndex(index)

    def get_index(self):
        return self.dropdown.currentIndex()

    def set_current_key(self, key):
        if self.options is not None and key in list(self.options.keys()):
            self.dropdown.setCurrentIndex(list(self.options.keys()).index(key))

    def get_current_key(self):
        if self.options is not None:
            return list(self.options.keys())[self.get_index()]
        else:
            return None

    def set_current_name(self, name):
        if self.options is not None and name in list(self.options.values()):
            self.dropdown.setCurrentIndex(list(self.options.values()).index(name))

    def get_current_name(self):
        if self.options is not None:
            return list(self.options.values())[self.get_index()]
        else:
            return None


class TextInput(SingleBoxWidget):
    def __init__(self, text):
        super().__init__()

        label = QLabel(text)
        label.setFont(font_8pt)

        self.input_field = QLineEdit()
        self.input_field.setFixedHeight(32)
        self.input_field.setFont(font_8pt)
        self.input_field.setStyleSheet(Style.input_field)

        self.add_widget(label)
        self.add_widget(self.input_field)

    def focus(self):
        self.input_field.setFocus()

    def set_text(self, text):
        if text is not None:
            self.input_field.setText(text)

    def get_text(self):
        return self.input_field.text()


class NumberInput(SingleBoxWidget):
    def __init__(self, text, default, min, max):
        super().__init__()

        label = QLabel(text)
        label.setFont(font_8pt)

        self.spin_box = QSpinBox()
        self.spin_box.setFixedHeight(32)
        self.spin_box.setFont(font_8pt)
        self.spin_box.setStyleSheet(Style.spin_box)
        self.spin_box.setValue(default)
        self.spin_box.setRange(min, max)
        self.spin_box.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.add_widget(label)
        self.frame_layout.addStretch()
        self.add_widget(self.spin_box)

    def focus(self):
        self.spin_box.setFocus()

    def set_value(self, value):
        if value is not None:
            self.spin_box.setValue(value)

    def get_value(self):
        return self.spin_box.value()


class Checkbox(SingleBoxWidget):
    def __init__(self, text):
        super().__init__()

        self.checkbox = QCheckBox()
        self.checkbox.setFixedSize(QSize(32, 32))
        self.checkbox.setFont(font_8pt)
        self.checkbox.setStyleSheet(Style.checkbox)
        self.checkbox.setTristate(False)

        label = QLabel(text)
        label.setFont(font_8pt)

        self.add_widget(self.checkbox)
        self.add_widget(label)

    def get_state(self):
        return self.checkbox.isChecked()

    def set_state(self, state):
        self.checkbox.setChecked(state)


class Dropdown(SingleBoxWidget):
    def __init__(self, text):
        super().__init__()
        self.options = None

        label = QLabel(text)
        label.setFont(font_8pt)

        self.dropdown = QComboBox()
        self.dropdown.setFixedHeight(32)
        self.dropdown.setFont(font_8pt)
        self.dropdown.setStyleSheet(Style.dropdown)
        self.dropdown.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        self.add_widget(label, 1)
        self.add_widget(self.dropdown, 1)

    def set_options(self, options):
        if not isinstance(options, dict):
            return
        elif len(options) < 1:
            return

        self.options = options

        for option in self.options.values():
            self.dropdown.addItem(option)

        self.dropdown.setCurrentIndex(0)

    def clear_options(self):
        self.dropdown.clear()

    def set_index(self, index):
        if isinstance(index, int) and 0 <= index < len(self.options):
            self.dropdown.setCurrentIndex(index)

    def get_index(self):
        return self.dropdown.currentIndex()

    def set_current_key(self, key):
        if self.options is not None and key in list(self.options.keys()):
            self.dropdown.setCurrentIndex(list(self.options.keys()).index(key))

    def get_current_key(self):
        if self.options is not None:
            return list(self.options.keys())[self.get_index()]
        else:
            return None

    def set_current_name(self, name):
        if self.options is not None and name in list(self.options.values()):
            self.dropdown.setCurrentIndex(list(self.options.values()).index(name))

    def get_current_name(self):
        if self.options is not None:
            return list(self.options.values())[self.get_index()]
        else:
            return None

    def wheelEvent(self, a0):
        pass


class Title(QLabel):
    def __init__(self, text, is_top=True):
        super().__init__()

        self.setText(text)
        self.setFont(font_9pt)
        if is_top:
            self.setStyleSheet(Style.title_label)
        else:
            self.setStyleSheet(Style.title_label + "QLabel{margin-top: 10px;}")


class VideoTooltip(QWidget):
    def __init__(self, path):
        super().__init__()
        self.setFixedSize(384, 216)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setStyleSheet("background-color: transparent; border: none;")

        self._scene = QGraphicsScene()
        self._gv = QGraphicsView(self._scene)
        self._gv.setStyleSheet("background-color: transparent;")
        self._gv.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._gv.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self._videoitem = QGraphicsVideoItem()
        self._scene.addItem(self._videoitem)
        self._gv.fitInView(self._videoitem, QtCore.Qt.KeepAspectRatio)

        self._player = QMediaPlayer(
            self, QMediaPlayer.VideoSurface
        )
        self._player.setVideoOutput(self._videoitem)

        file = path
        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.playlist.addMedia(QMediaContent(QtCore.QUrl.fromLocalFile(file)))

        self._player.setPlaylist(self.playlist)

        lay = QVBoxLayout(self)
        lay.addWidget(self._gv)
        lay.setContentsMargins(0, 0, 0, 0)

    def resiezEvent(self, event):
        super().resizeEvent(event)
        self._gv.fitInView(self._videoitem, QtCore.Qt.KeepAspectRatioByExpanding)
        self._videoitem.setSize(QSizeF(384, 216))

    def enable(self):
        self.show()
        self.move(QCursor.pos() + QtCore.QPoint(10, 10))
        self._videoitem.setSize(QSizeF(384, 216))
        self._player.play()

    def disable(self):
        self.hide()
        self._player.stop()


class ComponentButton(QPushButton):
    def __init__(self, name, components, icon, path):
        super().__init__()
        self.components = components
        self.path = path
        self.initialized = False
        self.setFixedSize(40, 40)
        self.setToolTip(name)

        self.setStyleSheet(Style.video_tooltip_button)
        self.setIcon(QIcon(QPixmap(icon)))
        self.setIconSize(QtCore.QSize(28, 28))

    # def enterEvent(self, a0: QtCore.QEvent) -> None:
    #     if not self.initialized:
    #         self.initialized = True
    #         self.video = VideoTooltip(self.path)
    #         self.video.show()
    #         QtCore.QTimer.singleShot(0, self.video.enable)
    #     else:
    #         self.video.enable()

    # def leaveEvent(self, a0: QtCore.QEvent) -> None:
    #     self.video.disable()

    # def mousePressEvent(self, e: QMouseEvent) -> None:
    #     super().mousePressEvent(e)
    #     self.video.disable()


class ComponentOptionWidget(QWidget):
    def __init__(self, component):
        super(ComponentOptionWidget, self).__init__()
        self.component = component
        self.setFixedHeight(38)

        icon_path = get_icon_path(component.name)

        self.icon = QLabel()
        self.icon.setPixmap(QPixmap(icon_path))
        self.icon.setScaledContents(True)
        self.icon.setFixedSize(QSize(24, 24))
        self.icon.setStyleSheet("background: none;")

        self.activations = NumberInput("Activations", 1, 1, 999)
        self.activations.set_value(component.activations)

        self.min_moons = NumberInput("Minimum Moon Count", 0, 0, 999)
        self.min_moons.set_value(component.min_moons)

        self.delete_button = QPushButton()
        self.delete_button.setFixedSize(QSize(28, 28))
        self.delete_button.setStyleSheet(Style.btn_rounded)
        self.delete_button.setToolTip("Delete")
        self.delete_button.setIcon(QIcon(QPixmap("ui/resources/icons/delete.png")))
        self.delete_button.setIconSize(QtCore.QSize(22, 22))

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(6, 0, 6, 0)
        self.layout.setSpacing(6)
        self.layout.addWidget(self.icon, 0)
        self.layout.addWidget(self.activations, 1)
        self.layout.addWidget(self.min_moons, 1)
        self.layout.addWidget(self.delete_button, 0)

        self.setLayout(self.layout)


class ComponentPreview(QScrollArea):
    def __init__(self):
        super(ComponentPreview, self).__init__()
        self.components = None

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setSpacing(0)

        self.content = QWidget()
        self.content.setFixedHeight(32)
        self.content.setMinimumWidth(100000)
        self.content.setLayout(self.layout)

        self.setMaximumHeight(32)
        self.setStyleSheet("background-color: rgb(27, 29, 35); border: none;")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.content)

    def clear(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i)
            if not isinstance(widget, QSpacerItem):
                widget.widget().deleteLater()
            self.layout.removeItem(widget)

    def set_components(self, components, selected=-1):
        self.components = components
        self.clear()

        if components is None:
            return

        for i, component in enumerate(components):
            icon_path = get_icon_path(component.name)

            if i != 0:
                arrow_label = QLabel()
                arrow_label.setPixmap(QPixmap("ui/resources/icons/right_arrow.png"))
                arrow_label.setScaledContents(True)
                arrow_label.setFixedSize(QSize(20, 20))
                self.layout.addWidget(arrow_label)

            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(icon_path))
            icon_label.setScaledContents(True)
            if i == selected:
                icon_label.setFixedSize(QSize(32, 28))
                icon_label.setStyleSheet(
                    "border: 2px solid white; border-radius: 8px; padding: 2px; margin-right: 4px;")
            else:
                icon_label.setFixedSize(QSize(28, 28))
                icon_label.setStyleSheet(
                    "border: 0px solid white; border-radius: 8px; padding: 4px; margin-right: 0px;")

            activations_label = QLabel(f"x{component.activations}")
            activations_label.setFont(font_8pt)

            self.layout.addWidget(icon_label)
            self.layout.addWidget(activations_label)

        self.layout.addStretch()

    def set_selected(self, index):
        self.set_components(self.components, index)


# Source: https://github.com/anjalp/PySide2extn/blob/master/PySide2extn/RoundProgressBar.py
class QRoundProgressBar(QWidget):

    def __init__(self, text, parent=None):
        super(QRoundProgressBar, self).__init__(parent)

        self.position_x = 0
        self.position_y = 0
        self.posFactor = 0

        self.rpb_minimumSize = (0, 0)
        self.rpb_maximumSize = (0, 0)
        self.rpb_dynamicMin = True
        self.rpb_dynamicMax = True
        self.rpb_Size = 0
        self.sizeFactor = 0

        self.rpb_maximum = 100
        self.rpb_minimum = 0

        self.rpb_type = self.BarStyleFlags.Hybrid1
        self.startPosition = self.StartPosFlags.North
        self.rpb_direction = self.RotationFlags.Clockwise

        self.rpb_textType = self.TextFlags.Percentage
        self.rpb_textColor = (255, 255, 255)
        self.rpb_textWidth = self.rpb_Size / 8
        self.rpb_textFont = font_9pt
        self.text = text
        self.rpb_text_value = '0 / 0'
        self.rpb_textRatio = 8
        self.text_factor_x = 0
        self.text_factor_y = 0
        self.dynamicText = True
        self.rpb_textActive = True

        self.lineWidth = 6
        self.pathWidth = 6
        self.scale = 10
        self.rpb_lineStyle = self.LineStyleFlags.SolidLine
        self.rpb_lineCap = self.LineCapFlags.SquareCap
        self.lineColor = (255, 255, 255)
        self.pathColor = (27, 29, 35)

        self.rpb_circleColor = (27, 29, 35)
        self.rpb_circleRatio = 1
        self.rpb_circlePosX = 0
        self.rpb_circlePosY = 0

        self.rpb_pieColor = (255, 255, 255)
        self.rpb_pieRatio = 1
        self.rpb_piePosX = 0
        self.rpb_piePosY = 0

        self.rpb_value = 0

        if self.rpb_dynamicMin:
            self.setMinimumSize(QSize(self.lineWidth * self.scale + self.pathWidth * self.scale,
                                      self.lineWidth * self.scale + self.pathWidth * self.scale))

    # CLASS ENUMERATORS
    class LineStyleFlags:
        SolidLine = Qt.SolidLine
        DotLine = Qt.DotLine
        DashLine = Qt.DashLine

    class LineCapFlags:
        SquareCap = Qt.SquareCap
        RoundCap = Qt.RoundCap

    class BarStyleFlags:
        Donet = 0
        Line = 1
        Pie = 2
        Pizza = 3
        Hybrid1 = 4
        Hybrid2 = 5

    class RotationFlags:
        Clockwise = -1
        AntiClockwise = 1

    class TextFlags:
        Value = 0
        Percentage = 1

    class StartPosFlags:
        North = 90 * 16
        South = -90 * 16
        East = 0 * 16
        West = 180 * 16

    # METHODS FOR CHANGING THE PROPERTY OF THE ROUNDPROGRESSBAR :SOLTS
    def rpb_set_minimum_size(self, width, height):
        if not isinstance(width, int) or not isinstance(height, int):
            raise Exception('Sorry Width/Height should be an int')
        self.rpb_dynamicMin = False
        self.setMinimumSize(width, height)
        self.rpb_minimumSize = (width, height)
        self.update()

    def rpb_set_maximum_size(self, width, height):
        if not isinstance(width, int) or not isinstance(height, int):
            raise Exception('Sorry Width/Height should be an int')
        self.rpb_dynamicMax = False
        self.setMaximumSize(width, height)
        self.rpb_maximumSize = (width, height)
        self.update()

    def rpb_set_maximum(self, maximum):
        if self.rpb_minimum == maximum:  # FOR AVOIDING DIVISION BY ZERO ERROR IN FUTURE
            self.rpb_minimum = maximum - 1
        if self.rpb_maximum != maximum:
            self.rpb_maximum = maximum
            self.convert_input_value(int(self.rpb_get_value()))
            self.update()

    def rpb_set_minimum(self, minimum):
        if self.rpb_maximum == minimum:  # FOR AVOIDING DIVISION BY ZERO ERROR IN FUTURE
            self.rpb_maximum = minimum + 1
        if self.rpb_minimum != minimum:
            self.rpb_minimum = minimum
            self.convert_input_value(int(self.rpb_get_value()))
            self.update()

    def rpb_set_range(self, maximum, minimum):
        if minimum > maximum:
            maximum, minimum = minimum, maximum
        if self.rpb_maximum != maximum:
            self.rpb_maximum = maximum
        if self.rpb_minimum != minimum:
            self.rpb_minimum = minimum
        self.convert_input_value(int(self.rpb_get_value()))
        self.update()

    def rpb_set_initial_pos(self, pos):
        if pos == 'North':
            self.startPosition = self.StartPosFlags.North
        elif pos == 'South':
            self.startPosition = self.StartPosFlags.South
        elif pos == 'East':
            self.startPosition = self.StartPosFlags.East
        elif pos == 'West':
            self.startPosition = self.StartPosFlags.West
        else:
            raise Exception("Initial Position String can be: 'South', 'North'")

    def rpb_set_value(self, value):
        if self.rpb_value != value:
            if value >= self.rpb_maximum:
                self.convert_input_value(self.rpb_maximum)
            elif value < self.rpb_minimum:
                self.convert_input_value(self.rpb_minimum)
            else:
                self.convert_input_value(value)
            self.update()

    def rpb_reset(self):
        self.convert_input_value(self, self.rpb_minimum)
        self.update()

    def rpb_set_geometry(self, pos_x, pos_y):
        if self.position_x != pos_x:
            self.position_x = pos_x
        if self.position_y != pos_y:
            self.position_y = pos_y
        self.update()

    def rpb_set_line_width(self, width):
        if not isinstance(width, int):
            raise Exception('Line Width should be in int')
        if self.lineWidth != width:
            self.lineWidth = width
            self.update()

    def rpb_set_line_color(self, rgb):
        if not isinstance(rgb, tuple):
            raise Exception("Line Color accepts a tuple: (R, G, B).")
        if self.lineColor != rgb:
            self.lineColor = rgb
            self.update()

    def rpb_set_path_color(self, rgb):
        if not isinstance(rgb, tuple):
            raise Exception("Path Color accepts a tuple: (R, G, B).")
        if self.pathColor != rgb:
            self.pathColor = rgb
            self.update()

    def rpb_set_path_width(self, width):
        if not isinstance(width, int):
            raise Exception('Path Width should be in int')
        if self.pathWidth != width:
            self.pathWidth = width
            self.update()

    def rpb_set_direction(self, direction):
        if direction == 'Clockwise' or direction == -1:
            self.rpb_direction = self.RotationFlags.Clockwise
        elif direction == 'AntiClockwise' or direction == 1:
            self.rpb_direction = self.RotationFlags.AntiClockwise
        else:
            raise Exception("Direction can only be: 'Clockwise' and 'AntiClockwise' and Not: " + str(direction))
        self.update()

    def rpb_set_bar_style(self, style):
        if style == 'Donet':
            self.rpb_type = self.BarStyleFlags.Donet
        elif style == 'Line':
            self.rpb_type = self.BarStyleFlags.Line
        elif style == 'Pie':
            self.rpb_type = self.BarStyleFlags.Pie
        elif style == 'Pizza':
            self.rpb_type = self.BarStyleFlags.Pizza
        elif style == 'Hybrid1':
            self.rpb_type = self.BarStyleFlags.Hybrid1
        elif style == 'Hybrid2':
            self.rpb_type = self.BarStyleFlags.Hybrid2
        else:
            raise Exception(
                "Round Progress Bar has only the following styles: 'Line', 'Donet', " +
                "'Hybrid1', 'Pizza', 'Pie' and 'Hybrid2'")
        self.update()

    def rpb_set_line_style(self, style):
        if style == 'SolidLine':
            self.rpb_lineStyle = self.LineStyleFlags.SolidLine
        elif style == 'DotLine':
            self.rpb_lineStyle = self.LineStyleFlags.DotLine
        elif style == 'DashLine':
            self.rpb_lineStyle = self.LineStyleFlags.DashLine
        else:
            self.rpb_lineStyle = self.LineStyleFlags.SolidLine

    def rpb_set_line_cap(self, cap):
        if cap == 'SquareCap':
            self.rpb_lineCap = self.LineCapFlags.SquareCap
        elif cap == 'RoundCap':
            self.rpb_lineCap = self.LineCapFlags.RoundCap

    def rpb_set_text_color(self, rgb):
        if self.rpb_textColor != rgb:
            self.rpb_textColor = rgb
            self.update()

    def rpb_set_text_font(self, font):
        if self.rpb_textFont != font:
            self.rpb_textFont = font
            self.update()

    def rpb_set_text_format(self, text_typ):
        if text_typ == 'Value':
            self.rpb_textType = self.TextFlags.Value
        elif text_typ == 'Percentage':
            self.rpb_textType = self.TextFlags.Percentage
        else:
            self.rpb_textType = self.TextFlags.Percentage

    def rpb_set_text_ratio(self, ratio):
        if self.rpb_textRatio != ratio:
            if ratio < 3:
                ratio = 3
            elif ratio > 50:
                ratio = 50
            self.rpb_textRatio = ratio
            self.update()

    def rpb_set_text_width(self, width):
        self.dynamicText = False
        if width > 0:
            self.rpb_textWidth = width
            self.update()

    def rpb_set_circle_color(self, rgb):
        if self.rpb_circleColor != rgb:
            self.rpb_circleColor = rgb
            self.update()

    def rpb_set_circle_ratio(self, ratio):
        if self.rpb_circleRatio != ratio:
            self.rpb_circleRatio = ratio
            self.update()

    def rpb_set_pie_color(self, rgb):
        if self.rpb_pieColor != rgb:
            self.rpb_pieColor = rgb
            self.update()

    def rpb_set_pie_ratio(self, ratio):
        if self.rpb_pieRatio != ratio:
            self.rpb_pieRatio = ratio
            self.update()

    def rpb_enable_text(self, enable):
        if enable:
            self.rpb_textActive = enable
        else:
            self.rpb_textActive = enable
        self.update()

    # METHODS FOR GETTING THE PROPERTY OF ROUNDPROGRESSBAR SLOTS
    def rpb_get_size(self):
        return self.rpb_Size

    def rpb_get_value(self):
        return self.rpb_value / 16

    def rpb_get_range(self):
        return self.rpb_minimum, self.rpb_maximum

    def rpb_get_text_width(self):
        return self.rpb_textWidth

    # ENGINE: WHERE ALL THE REAL STUFF TAKE PLACE: WORKING OF THE ROUNDPROGRESSBA
    def rpb_minimum_size(self, dynamic_max, minimum, maximum):
        """
        Minimum size calculating code: Takes consideration of the width of the line/path/circle/pie and the user defined
        width and also the size of the frame/window of the application.
        """

        rpb_height = self.height()
        rpb_width = self.width()
        if dynamic_max:
            if rpb_width >= rpb_height >= minimum[1]:
                self.rpb_Size = rpb_height
            elif rpb_height > rpb_width >= minimum[0]:
                self.rpb_Size = rpb_width
        else:
            if rpb_width >= rpb_height and rpb_height <= maximum[1]:
                self.rpb_Size = rpb_height
            elif rpb_width < rpb_height and rpb_width <= maximum[0]:
                self.rpb_Size = rpb_width

    def convert_input_value(self, value):
        """
        CONVERTS ANY INPUT VALUE TO THE 0*16-360*16 DEGREE REFERENCE OF THE QPainter.drawArc NEEDED.
        """
        try:
            self.rpb_value = ((value - self.rpb_minimum) / (self.rpb_maximum - self.rpb_minimum)) * 360 * 16
            self.rpb_value = self.rpb_direction * self.rpb_value
        except:
            self.rpb_value = 0
            value = 0
        if self.rpb_textType == QRoundProgressBar.TextFlags.Percentage:
            self.rpb_text_value = f"{value} / {self.rpb_maximum}"
        else:
            self.rpb_text_value = str(value)

    # SINCE THE THICKNESS OF THE LINE OR THE PATH CAUSES THE WIDGET TO WRONGLY FIT INSIDE THE SIZE OF THE WIDGET
    # DESIGNED IN THE QTDESIGNER, THE CORRECTION FACTOR IS NECESSERY CALLED THE GEOMETRYFACTOR, WHICH CALCULATE
    # THE TWO FACTORS CALLED THE self.posFactor AND THE self.sizeFactor, CALCULATION THIS IS NECESSERY AS THE
    def geometry_factor(self):
        if self.lineWidth > self.pathWidth:
            self.posFactor = self.lineWidth / 2 + 1
            self.sizeFactor = self.lineWidth + 1
        else:
            self.posFactor = self.pathWidth / 2 + 1
            self.sizeFactor = self.pathWidth + 1

    def rpb_text_factor(self):
        if self.dynamicText:
            self.rpb_textWidth = self.rpb_Size / self.rpb_textRatio
        self.text_factor_x = self.posFactor + (self.rpb_Size - self.sizeFactor) / 2 - self.rpb_textWidth * 0.75 * (
                len(self.rpb_text_value) / 2) - 2
        self.text_factor_y = self.rpb_textWidth / 2 + self.rpb_Size / 2

    def rpb_circle_factor(self):
        self.rpb_circlePosX = self.position_x + self.posFactor + (self.rpb_Size * (1 - self.rpb_circleRatio)) / 2
        self.rpb_circlePosY = self.position_y + self.posFactor + (self.rpb_Size * (1 - self.rpb_circleRatio)) / 2

    def rpb_pie_factor(self):
        self.rpb_piePosX = self.position_x + self.posFactor + (self.rpb_Size * (1 - self.rpb_pieRatio)) / 2
        self.rpb_piePosY = self.position_y + self.posFactor + (self.rpb_Size * (1 - self.rpb_pieRatio)) / 2

    def paintEvent(self, event: QPaintEvent):

        # THIS BELOW CODE AMKE SURE THAT THE SIZE OF THE ROUNDPROGRESSBAR DOESNOT REDUCES TO ZERO WHEN THE USER RESIZES
        # THE WINDOW
        if self.rpb_dynamicMin:
            self.setMinimumSize(QSize(self.lineWidth * self.scale + self.pathWidth * self.scale,
                                      self.lineWidth * self.scale + self.pathWidth * self.scale))

        self.rpb_minimum_size(self.rpb_dynamicMax, self.rpb_minimumSize, self.rpb_maximumSize)
        self.geometry_factor()
        self.rpb_text_factor()
        self.rpb_circle_factor()
        self.rpb_pie_factor()

        if self.rpb_type == 0:  # DONET TYPE
            self.path_component()
            self.line_component()
            self.text_component()
        elif self.rpb_type == 1:  # LINE TYPE
            self.line_component()
            self.text_component()
        elif self.rpb_type == 2:  # Pie
            self.pie_component()
            self.text_component()
        elif self.rpb_type == 3:  # PIZZA
            self.circle_component()
            self.line_component()
            self.text_component()
        elif self.rpb_type == 4:  # HYBRID1
            self.circle_component()
            self.path_component()
            self.line_component()
            self.text_component()
        elif self.rpb_type == 5:  # HYBRID2
            self.pie_component()
            self.line_component()
            self.text_component()

    def line_component(self):
        line_painter = QPainter(self)
        line_painter.setRenderHint(QPainter.Antialiasing)
        pen_linpen_line = QPen()
        pen_linpen_line.setStyle(self.rpb_lineStyle)
        pen_linpen_line.setWidth(self.lineWidth)
        pen_linpen_line.setBrush(QColor(self.lineColor[0], self.lineColor[1], self.lineColor[2]))
        pen_linpen_line.setCapStyle(self.rpb_lineCap)
        pen_linpen_line.setJoinStyle(Qt.RoundJoin)
        line_painter.setPen(pen_linpen_line)
        line_painter.drawArc(int(self.position_x + self.posFactor), int(self.position_y + self.posFactor),
                             int(self.rpb_Size - self.sizeFactor), int(self.rpb_Size - self.sizeFactor),
                             int(self.startPosition), int(self.rpb_value))
        line_painter.end()

    def path_component(self):
        path_painter = QPainter(self)
        path_painter.setRenderHint(QPainter.Antialiasing)
        pen_path = QPen()
        pen_path.setStyle(Qt.SolidLine)
        pen_path.setWidth(self.pathWidth)
        pen_path.setBrush(QColor(self.pathColor[0], self.pathColor[1], self.pathColor[2]))
        pen_path.setCapStyle(Qt.RoundCap)
        pen_path.setJoinStyle(Qt.RoundJoin)
        path_painter.setPen(pen_path)
        path_painter.drawArc(int(self.position_x + self.posFactor), int(self.position_y + self.posFactor),
                             int(self.rpb_Size - self.sizeFactor), int(self.rpb_Size - self.sizeFactor), 0, 360 * 16)
        path_painter.end()

    def text_component(self):
        if self.rpb_textActive:
            text_painter = QPainter(self)
            pen_text = QPen()
            pen_text.setColor(QColor(self.rpb_textColor[0], self.rpb_textColor[1], self.rpb_textColor[2]))
            text_painter.setPen(pen_text)

            font_text = QFont()
            font_text.setFamily(self.rpb_textFont.family())
            font_text.setPointSize(9)
            text_painter.setFont(font_text)
            text_painter.drawText(
                QRectF(self.rpb_circlePosX - 1, self.rpb_circlePosY - 10,
                       (self.rpb_Size - self.sizeFactor) * self.rpb_circleRatio,
                       (self.rpb_Size - self.sizeFactor) * self.rpb_circleRatio),
                Qt.AlignCenter | Qt.AlignVCenter | Qt.AlignHCenter, self.text)

            font_text = QFont()
            font_text.setFamily(self.rpb_textFont.family())
            font_text.setPointSize(11)
            text_painter.setFont(font_text)
            text_painter.drawText(QRectF(self.rpb_circlePosX - 10, self.rpb_circlePosY + 10,
                                         (self.rpb_Size - self.sizeFactor) * self.rpb_circleRatio + 20,
                                         (self.rpb_Size - self.sizeFactor) * self.rpb_circleRatio),
                                  Qt.AlignCenter | Qt.AlignVCenter | Qt.AlignHCenter, self.rpb_text_value)
            text_painter.end()

    def circle_component(self):
        circle_painter = QPainter(self)
        pen_circle = QPen()
        pen_circle.setWidth(0)
        pen_circle.setColor(QColor(self.rpb_circleColor[0], self.rpb_circleColor[1], self.rpb_circleColor[2]))
        circle_painter.setRenderHint(QPainter.Antialiasing)
        circle_painter.setPen(pen_circle)
        circle_painter.setBrush(QColor(self.rpb_circleColor[0], self.rpb_circleColor[1], self.rpb_circleColor[2]))
        circle_painter.drawEllipse(int(self.rpb_circlePosX), int(self.rpb_circlePosY),
                                   int((self.rpb_Size - self.sizeFactor) * self.rpb_circleRatio),
                                   int((self.rpb_Size - self.sizeFactor) * self.rpb_circleRatio))

    def pie_component(self):
        pie_painter = QPainter(self)
        pen_pie = QPen()
        pen_pie.setWidth(0)
        pen_pie.setColor(QColor(self.rpb_pieColor[0], self.rpb_pieColor[1], self.rpb_pieColor[2]))
        pie_painter.setRenderHint(QPainter.Antialiasing)
        pie_painter.setPen(pen_pie)
        pie_painter.setBrush(QColor(self.rpb_pieColor[0], self.rpb_pieColor[1], self.rpb_pieColor[2]))
        pie_painter.drawPie(self.rpb_piePosX, self.rpb_piePosY, (self.rpb_Size - self.sizeFactor) * self.rpb_pieRatio,
                            (self.rpb_Size - self.sizeFactor) * self.rpb_pieRatio, self.startPosition, self.rpb_value)
