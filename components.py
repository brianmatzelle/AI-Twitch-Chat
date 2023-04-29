from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPainter

class HeaderBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.parent.oldPos:
            delta = event.globalPos() - self.parent.oldPos
            self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
            self.parent.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.oldPos = None

class ResizeHandle(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def sizeHint(self):
        return QSize(12, 12)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.drawRect(0, 0, self.width(), self.height())

class RemoveBorderButton(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    def sizeHint(self):
        return QSize(12, 12)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.gray)
        painter.drawRect(0, 0, self.width(), self.height())