from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QApplication
from PyQt5.QtCore import pyqtProperty, QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QPainter

class TickerLabel(QLabel):
    def __init__(self, parent=None):
        super(TickerLabel, self).__init__(parent)
        self._text_x = 0

    @pyqtProperty(int)
    def text_x(self):
        return self._text_x

    @text_x.setter
    def text_x(self, val):
        self._text_x = val
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        font_metrics = painter.fontMetrics()
        text_height = font_metrics.height()
        painter.drawText(self._text_x, (self.height() + text_height) // 2, self.text())
        painter.end()

    def reset(self, text):
        self.setText(text)
        self._text_x = self.width()

def LogoIcon():
    label = QLabel()
    label.setFixedSize(32, 32)  # You can adjust the size of the icon
    label.setOpenExternalLinks(True)
    label.setStyleSheet("border: none; padding: 0px; margin: 0px;")
    label.setText('<a href="https://brianmatzelle.com"><img src="blanc32x32.png"/></a>')
    label.setContentsMargins(0, 0, 0, 0)
    return label

def ChatTvLabel(config):
    label = TickerLabel()
    label.setOpenExternalLinks(True)
    label.reset(f"CHAT.TV: {config['streamer_name']}'s chat")
    label.setStyleSheet("background-color: #243049; padding-left: 5px; color: lightgray; font-size: 12px; font-weight: bold; border: none; border-radius: 0px; margin: 0px;")
    label.setContentsMargins(0, 0, 0, 0)

    # create animation
    animation = QPropertyAnimation(label, b'text_x', label)
    animation.setDuration(10000)  # adjust for speed
    animation.setStartValue(label.width())  # Start the animation from the right edge of the label
    # print(-label.fontMetrics().width(label.text()))
    animation.setEndValue(-label.fontMetrics().width(label.text())- (label.fontMetrics().width(label.text()) / 4.666))  # Set the end value to move the text out of the label
    animation.setLoopCount(-1)  # loop indefinitely
    animation.start()

    return label


# Buttons call parent.parent because these are in the HeaderBar class, which is in the ChatWindow class
def MinimizeButton(parent):
    minimize_button = QPushButton("_")
    minimize_button.setStyleSheet("QPushButton {width: 30px; background-color: lightgray;} QPushButton:hover {background-color: gray;}")
    minimize_button.clicked.connect(parent.parent.showMinimized)
    return minimize_button

def MaximizeButton(parent):
    maximize_button = QPushButton("[]")
    maximize_button.setStyleSheet("QPushButton {width: 30px; background-color: lightgray;} QPushButton:hover {background-color: gray;}")
    maximize_button.clicked.connect(parent.parent.toggleMaximized)
    return maximize_button

def ExitButton(parent):
    exit_button = QPushButton("X")
    exit_button.setStyleSheet("QPushButton {width: 30px; background-color: #243049; color: lightgray;} QPushButton:hover {background-color: #e60000;}")
    exit_button.clicked.connect(parent.parent.close)
    return exit_button
