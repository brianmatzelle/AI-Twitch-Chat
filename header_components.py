from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

def LogoIcon():
    label = QLabel()
    label.setFixedSize(32, 32)  # You can adjust the size of the icon
    label.setOpenExternalLinks(True)
    label.setStyleSheet("border: none; padding: 0px; margin: 0px;")
    label.setText('<a href="https://brianmatzelle.com"><img src="blanc32x32.png"/></a>')
    label.setContentsMargins(0, 0, 0, 0)
    return label

def ChatTvLabel(config):
    label = QLabel()
    label.setOpenExternalLinks(True)
    label.setText(f"CHAT.TV: {config['streamer_name']}'s chat")
    label.setStyleSheet("background-color: #243049; padding-left: 5px; color: lightgray; font-size: 12px; font-weight: bold; border: none; border-radius: 0px; margin: 0px;")
    label.setContentsMargins(0, 0, 0, 0)
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