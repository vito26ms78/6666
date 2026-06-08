from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, pyqtSignal

from .overlay_renderer import OverlayRenderer


class OverlayWindow(QWidget):

    update_items_signal = pyqtSignal(list)
    clear_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.items = []
        self.renderer = OverlayRenderer()

        self.setWindowTitle("Anber Overlay")

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        self.update_items_signal.connect(
            self._update_items_gui_thread
        )

        self.clear_signal.connect(
            self._clear_gui_thread
        )

        self.showFullScreen()

    def update_items(self, items):

        self.update_items_signal.emit(items)

    def clear(self):

        self.clear_signal.emit()

    def _update_items_gui_thread(self, items):

        if items == self.items:
            return

        self.items = items
        self.update()

    def _clear_gui_thread(self):

        self.items = []
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(1)

        painter.setPen(pen)

        self.renderer.render(
            painter,
            self.items
        )
