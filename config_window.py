from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QComboBox, QPushButton, QFormLayout
from PyQt5.QtWidgets import QCheckBox, QScrollArea, QFrame, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings

class ConfigWindow(QDialog):
    def __init__(self, config, parent=None):
        super(ConfigWindow, self).__init__(parent)
        self.config = config
        self.setWindowTitle("Chat.tv Configuration")
        self.setWindowIcon(QIcon("./assets/blanc.png"))
        self.resize(500, 700)
        layout = QVBoxLayout()

        # Load saved settings
        settings = QSettings("blanc_savant", "Chat.tv")
        saved_api_key = settings.value("openai_api_key", "")
        saved_streamer_name = settings.value("streamer_name", config['streamer_name'])
        saved_num_bots = settings.value("num_bots", config['num_bots'], type=int)
        saved_bot_update_interval = settings.value("bot_update_interval", config['bot_update_interval'], type=int)
        saved_tone = settings.value("tone", config['bot_config']['tone'])
        saved_slang_types = settings.value("slang_types", [])
        saved_streamer_current_action = settings.value("streamer_current_action", config['bot_config']['streamer_current_action'])
        saved_max_num_of_responding_bots = settings.value("max_num_of_responding_bots", config['max_num_of_responding_bots'], type=int)
        saved_slang_types = settings.value("slang_types", config['bot_config']['slang_types'], type=str)
        
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
        self.num_bots_input.setMinimum(1)
        self.num_bots_input.setMaximum(99)  # Allow up to four digits for the number of bots
        self.num_bots_input.setValue(config['num_bots'])
        layout.addWidget(QLabel("Number of Bots:"))
        layout.addWidget(self.num_bots_input)

        # Bot update interval input
        self.bot_update_interval_input = QSpinBox()
        self.bot_update_interval_input.setMinimum(1)
        self.bot_update_interval_input.setValue(config['bot_update_interval'])
        layout.addWidget(QLabel("Bot Update Interval (seconds):"))
        layout.addWidget(self.bot_update_interval_input)

        # Max number of responding bots input
        self.max_num_of_responding_bots_input = QSpinBox()
        self.max_num_of_responding_bots_input.setMinimum(1)
        self.max_num_of_responding_bots_input.setMaximum(999)
        self.max_num_of_responding_bots_input.setValue(config['max_num_of_responding_bots'])
        layout.addWidget(QLabel("Max Number of Responding Bots (per interval):"))
        layout.addWidget(self.max_num_of_responding_bots_input)

        # Select Tone
        saved_tones = settings.value("tones", ["casual", "witty", "formal", "funny", "stupid", "random"], type=str)
        self.tone_input = QComboBox()
        self.tone_input.addItems(saved_tones)
        self.tone_input.setCurrentText(config['bot_config']['tone'])
        layout.addWidget(QLabel("Tone:"))
        layout.addWidget(self.tone_input)


        # Add custom tone input and button
        custom_tone_layout = QHBoxLayout()
        self.custom_tone_input = QLineEdit()
        custom_tone_layout.addWidget(self.custom_tone_input)
        self.add_custom_tone_button = QPushButton("Add Tone")
        self.add_custom_tone_button.clicked.connect(self.add_custom_tone)
        custom_tone_layout.addWidget(self.add_custom_tone_button)
        layout.addLayout(custom_tone_layout)


        # Select slang types/personality types
        self.slang_type_checkboxes = []

        self.scroll_area = QScrollArea()
        slang_types_frame = QFrame()
        grid_layout = QGridLayout()
        row = 0
        col = 0

        # slang types from QSettings
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
        self.scroll_area.setWidget(slang_types_frame)
        self.scroll_area.setWidgetResizable(True)

        # Slang types
        layout.addWidget(QLabel("Personality Types:"))
        layout.addWidget(self.scroll_area)

        # Add custom slang type input and button
        custom_slang_layout = QHBoxLayout()
        self.custom_slang_input = QLineEdit()
        custom_slang_layout.addWidget(self.custom_slang_input)
        self.add_custom_slang_button = QPushButton("Add Personality")
        self.add_custom_slang_button.clicked.connect(self.add_custom_slang_type)
        custom_slang_layout.addWidget(self.add_custom_slang_button)
        layout.addLayout(custom_slang_layout)
        
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
        self.tone_input.setCurrentText(saved_tone)
        self.streamer_current_action_input.setText(saved_streamer_current_action)
        self.max_num_of_responding_bots_input.setValue(saved_max_num_of_responding_bots)

    def save_and_close(self):
        # Save to QSettings (saves settings to local storage)
        settings = QSettings("blanc_savant", "Chat.tv")
        settings.setValue("openai_api_key", self.api_key_input.text())
        settings.setValue("streamer_name", self.streamer_name_input.text())
        settings.setValue("num_bots", self.num_bots_input.value())
        settings.setValue("bot_update_interval", self.bot_update_interval_input.value())
        settings.setValue("tone", self.tone_input.currentText())
        settings.setValue("slang_types", [checkbox.text() for checkbox in self.slang_type_checkboxes if checkbox.isChecked()])
        settings.setValue("streamer_current_action", self.streamer_current_action_input.text())
        settings.setValue("max_num_of_responding_bots", self.max_num_of_responding_bots_input.value())

        # Save to config (for use in main.py)
        self.config['streamer_name'] = self.streamer_name_input.text()
        self.config['num_bots'] = self.num_bots_input.value()
        self.config['bot_update_interval'] = self.bot_update_interval_input.value()
        self.config['bot_config']['tone'] = self.tone_input.currentText()
        self.config['bot_config']['slang_types'] = [checkbox.text() for checkbox in self.slang_type_checkboxes if checkbox.isChecked()]
        self.config['bot_config']['streamer_current_action'] = self.streamer_current_action_input.text()
        self.config['max_num_of_responding_bots'] = self.max_num_of_responding_bots_input.value()

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
        self.tone_input.setCurrentText(self.config['bot_config']['tone'])
        self.max_num_of_responding_bots_input.setValue(self.config['max_num_of_responding_bots'])

        for checkbox in self.slang_type_checkboxes:
            checkbox.setChecked(False)

        for checkbox in self.slang_type_checkboxes:
            checkbox.setChecked(False)

    def add_custom_slang_type(self):
        new_slang_type = self.custom_slang_input.text().strip()
        if new_slang_type and new_slang_type not in [checkbox.text() for checkbox in self.slang_type_checkboxes]:
            checkbox = QCheckBox(new_slang_type)
            checkbox.setChecked(True)  # Toggle on the new checkbox
            self.slang_type_checkboxes.append(checkbox)
            row, col = divmod(len(self.slang_type_checkboxes) - 1, 3)  # Assumes a grid with 3 columns
            grid_layout = self.scroll_area.widget().layout()
            grid_layout.addWidget(checkbox, row, col)
            self.custom_slang_input.clear()

            # Save new custom slang type immediately to local storage
            settings = QSettings("blanc_savant", "Chat.tv")
            saved_slang_types = settings.value("slang_types", [], type=str)
            saved_slang_types.append(new_slang_type)
            settings.setValue("slang_types", saved_slang_types)


    def add_custom_tone(self):
        new_tone = self.custom_tone_input.text().strip()
        if new_tone and new_tone not in [self.tone_input.itemText(i) for i in range(self.tone_input.count())]:
            self.tone_input.addItem(new_tone)
            self.custom_tone_input.clear()

            # Save new custom tone immediately to local storage
            settings = QSettings("blanc_savant", "Chat.tv")
            saved_tones = settings.value("tones", ["casual", "witty", "formal", "funny", "stupid", "random"], type=str)
            saved_tones.append(new_tone)
            settings.setValue("tones", saved_tones)
