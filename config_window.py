from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QComboBox, QPushButton, QFormLayout
from PyQt5.QtWidgets import QCheckBox, QScrollArea, QFrame, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings

class ConfigWindow(QDialog):
    def __init__(self, config, parent=None):
        super(ConfigWindow, self).__init__(parent)
        self.config = config
        self.setWindowTitle("Chat.tv Configuration")
        self.setWindowIcon(QIcon("./assets/blanc.png"))
        layout = QVBoxLayout()

        settings = QSettings("blanc_savant", "Chat.tv")
        saved_api_key = settings.value("openai_api_key", "")

        form_layout = QFormLayout()
        self.api_key_input = QLineEdit(saved_api_key)
        self.api_key_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("OpenAI API Key:", self.api_key_input)
        layout.addLayout(form_layout)

        delete_key_button = QPushButton("Delete API Key")
        delete_key_button.clicked.connect(self.delete_api_key)
        layout.addWidget(delete_key_button)

        self.streamer_name_input = QLineEdit(config['streamer_name'])
        layout.addWidget(QLabel("Streamer Name:"))
        layout.addWidget(self.streamer_name_input)

        self.num_bots_input = QSpinBox()
        self.num_bots_input.setValue(config['num_bots'])
        layout.addWidget(QLabel("Number of Bots:"))
        layout.addWidget(self.num_bots_input)

        self.bot_update_interval_input = QSpinBox()
        self.bot_update_interval_input.setValue(config['bot_update_interval'])
        layout.addWidget(QLabel("Bot Update Interval (seconds):"))
        layout.addWidget(self.bot_update_interval_input)

        self.slang_level_input = QComboBox()
        self.slang_level_input.addItems(["witty", "casual", "formal"])
        self.slang_level_input.setCurrentText(config['bot_config']['slang_level'])
        layout.addWidget(QLabel("Slang Level:"))
        layout.addWidget(self.slang_level_input)

        self.slang_type_checkboxes = []

        scroll_area = QScrollArea()
        slang_types_frame = QFrame()
        grid_layout = QGridLayout()
        row = 0
        col = 0

        for slang_type in config['bot_config']['slang_types']:
            checkbox = QCheckBox(slang_type)
            checkbox.setChecked(True)
            grid_layout.addWidget(checkbox, row, col)
            self.slang_type_checkboxes.append(checkbox)

            col += 1
            if col == 3:  # Set the number of columns you want in the grid
                col = 0
                row += 1

        slang_types_frame.setLayout(grid_layout)
        scroll_area.setWidget(slang_types_frame)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(QLabel("Slang Types:"))
        layout.addWidget(scroll_area)

        self.save_button = QPushButton("Save and Start")
        self.save_button.clicked.connect(self.save_and_close)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_and_close(self):
        self.config['streamer_name'] = self.streamer_name_input.text()
        self.config['num_bots'] = self.num_bots_input.value()
        self.config['bot_update_interval'] = self.bot_update_interval_input.value()
        self.config['bot_config']['slang_level'] = self.slang_level_input.currentText()
        self.config['bot_config']['slang_types'] = [checkbox.text() for checkbox in self.slang_type_checkboxes if checkbox.isChecked()]
        
        settings = QSettings("blanc_savant", "Chat.tv")
        settings.setValue("openai_api_key", self.api_key_input.text())

        self.accept()

    def delete_api_key(self):
        settings = QSettings("blanc_savant", "Chat.tv")
        settings.remove("openai_api_key")
        self.api_key_input.clear()
