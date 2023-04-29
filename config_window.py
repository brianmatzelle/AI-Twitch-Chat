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
        self.resize(300, 700)
        layout = QVBoxLayout()

        # Load saved settings
        settings = QSettings("blanc_savant", "Chat.tv")
        saved_api_key = settings.value("openai_api_key", "")
        saved_streamer_name = settings.value("streamer_name", config['streamer_name'])
        saved_num_bots = settings.value("num_bots", config['num_bots'], type=int)
        saved_bot_update_interval = settings.value("bot_update_interval", config['bot_update_interval'], type=int)
        saved_slang_level = settings.value("slang_level", config['bot_config']['slang_level'])
        saved_slang_types = settings.value("slang_types", [])
        saved_streamer_current_action = settings.value("streamer_current_action", config['bot_config']['streamer_current_action'])
        
        # OpenAI API Key input
        form_layout = QFormLayout()
        self.api_key_input = QLineEdit(saved_api_key)
        self.api_key_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("OpenAI API Key:", self.api_key_input)
        layout.addLayout(form_layout)

        # Streamer name input
        self.streamer_name_input = QLineEdit(config['streamer_name'])
        layout.addWidget(QLabel("Streamer Name:"))
        layout.addWidget(self.streamer_name_input)

        # Streamer current action input
        self.streamer_current_action_input = QLineEdit(config['bot_config']['streamer_current_action'])
        layout.addWidget(QLabel("Streamer's Current Action:"))
        layout.addWidget(self.streamer_current_action_input)

        # Number of bots input
        self.num_bots_input = QSpinBox()
        self.num_bots_input.setValue(config['num_bots'])
        layout.addWidget(QLabel("Number of Bots:"))
        layout.addWidget(self.num_bots_input)

        # Bot update interval input
        self.bot_update_interval_input = QSpinBox()
        self.bot_update_interval_input.setValue(config['bot_update_interval'])
        layout.addWidget(QLabel("Bot Update Interval (seconds):"))
        layout.addWidget(self.bot_update_interval_input)

        # Bot configuration
        self.slang_level_input = QComboBox()
        self.slang_level_input.addItems(["witty", "casual", "formal", "funny"])
        self.slang_level_input.setCurrentText(config['bot_config']['slang_level'])
        layout.addWidget(QLabel("Slang Level:"))
        layout.addWidget(self.slang_level_input)

        self.slang_type_checkboxes = []

        scroll_area = QScrollArea()
        slang_types_frame = QFrame()
        grid_layout = QGridLayout()
        row = 0
        col = 0

        # Load the saved slang types from QSettings
        saved_slang_types = settings.value("slang_types", [])

        for slang_type in config['bot_config']['slang_types']:
            checkbox = QCheckBox(slang_type)
            if slang_type in saved_slang_types:
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
        
        # Clear All Settings button
        clear_settings_button = QPushButton("Clear All Settings")
        clear_settings_button.clicked.connect(self.clear_all_settings)
        layout.addWidget(clear_settings_button)

        self.save_button = QPushButton("Save and Start")
        self.save_button.clicked.connect(self.save_and_close)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        # Set loaded values to widgets
        self.streamer_name_input.setText(saved_streamer_name)
        self.num_bots_input.setValue(saved_num_bots)
        self.bot_update_interval_input.setValue(saved_bot_update_interval)
        self.slang_level_input.setCurrentText(saved_slang_level)
        self.streamer_current_action_input.setText(saved_streamer_current_action)

    def save_and_close(self):
        settings = QSettings("blanc_savant", "Chat.tv")
        settings.setValue("openai_api_key", self.api_key_input.text())
        settings.setValue("streamer_name", self.streamer_name_input.text())
        settings.setValue("num_bots", self.num_bots_input.value())
        settings.setValue("bot_update_interval", self.bot_update_interval_input.value())
        settings.setValue("slang_level", self.slang_level_input.currentText())
        settings.setValue("slang_types", [checkbox.text() for checkbox in self.slang_type_checkboxes if checkbox.isChecked()])
        settings.setValue("streamer_current_action", self.streamer_current_action_input.text())

        self.config['streamer_name'] = self.streamer_name_input.text()
        self.config['num_bots'] = self.num_bots_input.value()
        self.config['bot_update_interval'] = self.bot_update_interval_input.value()
        self.config['bot_config']['slang_level'] = self.slang_level_input.currentText()
        self.config['bot_config']['slang_types'] = [checkbox.text() for checkbox in self.slang_type_checkboxes if checkbox.isChecked()]
        self.config['bot_config']['streamer_current_action'] = self.streamer_current_action_input.text()

        self.accept()

    def clear_all_settings(self):
        settings = QSettings("blanc_savant", "Chat.tv")
        settings.clear()
        
        # Reset input fields to default values
        self.reset_config_window()

    def reset_config_window(self):
        self.api_key_input.clear()
        self.streamer_name_input.setText(self.config['streamer_name'])
        self.num_bots_input.setValue(self.config['num_bots'])
        self.bot_update_interval_input.setValue(self.config['bot_update_interval'])
        self.slang_level_input.setCurrentText(self.config['bot_config']['slang_level'])

        for checkbox in self.slang_type_checkboxes:
            checkbox.setChecked(False)

        for checkbox in self.slang_type_checkboxes:
            checkbox.setChecked(False)