import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QPushButton,
    QSlider,
    QComboBox,
    QColorDialog,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QGroupBox,
    QLineEdit,
    QMessageBox,
    QListWidget,
    QLabel,
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from pynput import keyboard

from llama_assistant.shortcut_recorder import ShortcutRecorder
from llama_assistant import config
from llama_assistant.setting_validator import validate_numeric_field

class SettingsDialog(QDialog):
    settingsSaved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.main_layout = QVBoxLayout(self)

        # General Settings Group
        self.create_general_settings_group()

        # Appearance Settings Group
        self.create_appearance_settings_group()

        # Model Settings Group
        self.create_model_settings_group()

        # Voice Activation Settings Group
        self.create_voice_activation_settings_group()

        self.create_rag_settings_group()

        # Create a horizontal layout for the save button
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)

        # Add the button layout to the main layout
        self.main_layout.addLayout(button_layout)

        self.load_settings()

    def create_general_settings_group(self):
        group_box = QGroupBox("General Settings")
        layout = QVBoxLayout()

        shortcut_layout = QHBoxLayout()
        shortcut_label = QLabel("Shortcut:")
        self.shortcut_recorder = ShortcutRecorder()
        shortcut_layout.addWidget(shortcut_label)
        shortcut_layout.addWidget(self.shortcut_recorder)
        shortcut_layout.addStretch()
        layout.addLayout(shortcut_layout)

        self.reset_shortcut_button = QPushButton("Reset Shortcut")
        self.reset_shortcut_button.clicked.connect(self.reset_shortcut)
        layout.addWidget(self.reset_shortcut_button)

        group_box.setLayout(layout)
        self.main_layout.addWidget(group_box)

    def create_appearance_settings_group(self):
        group_box = QGroupBox("Appearance Settings")
        layout = QVBoxLayout()

        color_layout = QHBoxLayout()
        color_label = QLabel("Background Color:")
        self.color_button = QPushButton("Choose Color")
        self.color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_button)
        color_layout.addStretch()
        layout.addLayout(color_layout)

        transparency_layout = QHBoxLayout()
        transparency_label = QLabel("Transparency:")
        self.transparency_slider = QSlider(Qt.Orientation.Horizontal)
        self.transparency_slider.setRange(10, 100)
        self.transparency_slider.setValue(90)
        transparency_layout.addWidget(transparency_label)
        transparency_layout.addWidget(self.transparency_slider)
        layout.addLayout(transparency_layout)

        group_box.setLayout(layout)
        self.main_layout.addWidget(group_box)

    def create_model_settings_group(self):
        group_box = QGroupBox("Model Settings")
        layout = QVBoxLayout()

        text_model_layout = QHBoxLayout()
        text_model_label = QLabel("Text-only Model:")
        self.text_model_combo = QComboBox()
        self.text_model_combo.addItems(self.get_model_names_by_type("text"))
        text_model_layout.addWidget(text_model_label)
        text_model_layout.addWidget(self.text_model_combo)
        text_model_layout.addStretch()
        layout.addLayout(text_model_layout)

        multimodal_model_layout = QHBoxLayout()
        multimodal_model_label = QLabel("Multimodal Model:")
        self.multimodal_model_combo = QComboBox()
        self.multimodal_model_combo.addItems(self.get_model_names_by_type("image"))
        multimodal_model_layout.addWidget(multimodal_model_label)
        multimodal_model_layout.addWidget(self.multimodal_model_combo)
        multimodal_model_layout.addStretch()
        layout.addLayout(multimodal_model_layout)

        context_len_layout = QHBoxLayout()
        context_len_label = QLabel("Context Length:")
        self.context_len_input = QLineEdit()
        context_len_layout.addWidget(context_len_label)
        context_len_layout.addWidget(self.context_len_input)
        layout.addLayout(context_len_layout)

        temperature_layout = QHBoxLayout()
        temperature_label = QLabel("Temperature:")
        self.temperature_input = QLineEdit()
        temperature_layout.addWidget(temperature_label)
        temperature_layout.addWidget(self.temperature_input)
        layout.addLayout(temperature_layout)

        top_p_layout = QHBoxLayout()
        top_p_label = QLabel("Top p:")
        self.top_p_input = QLineEdit()
        top_p_layout.addWidget(top_p_label)
        top_p_layout.addWidget(self.top_p_input)
        layout.addLayout(top_p_layout)

        top_k_layout = QHBoxLayout()
        top_k_label = QLabel("Top k:")
        self.top_k_input = QLineEdit()
        top_k_layout.addWidget(top_k_label)
        top_k_layout.addWidget(self.top_k_input)
        layout.addLayout(top_k_layout)

        self.manage_custom_models_button = QPushButton("Manage Custom Models")
        self.manage_custom_models_button.clicked.connect(self.open_custom_models_dialog)
        layout.addWidget(self.manage_custom_models_button)

        group_box.setLayout(layout)
        self.main_layout.addWidget(group_box)

    def create_voice_activation_settings_group(self):
        group_box = QGroupBox("Voice Activation Settings")
        layout = QVBoxLayout()

        self.hey_llama_chat_checkbox = QCheckBox('Say "Hey Llama" to open chat form')
        self.hey_llama_chat_checkbox.stateChanged.connect(self.update_hey_llama_mic_state)
        layout.addWidget(self.hey_llama_chat_checkbox)

        self.hey_llama_mic_checkbox = QCheckBox('Say "Hey Llama" to activate microphone')
        layout.addWidget(self.hey_llama_mic_checkbox)

        group_box.setLayout(layout)
        self.main_layout.addWidget(group_box)

    def create_rag_settings_group(self):
        group_box = QGroupBox("RAG Settings")
        layout = QVBoxLayout()

        embed_model_layout = QHBoxLayout()
        embed_model_label = QLabel("Text-only Model:")
        self.embed_model_combo = QComboBox()
        self.embed_model_combo.addItems(config.DEFAULT_EMBEDING_MODELS)
        embed_model_layout.addWidget(embed_model_label)
        embed_model_layout.addWidget(self.embed_model_combo)
        embed_model_layout.addStretch()
        layout.addLayout(embed_model_layout)

        chunk_size_layout = QHBoxLayout()
        chunk_size_label = QLabel("Chunk Size:")
        self.chunk_size_input = QLineEdit()
        chunk_size_layout.addWidget(chunk_size_label)
        chunk_size_layout.addWidget(self.chunk_size_input)
        layout.addLayout(chunk_size_layout)

        chunk_overlap_layout = QHBoxLayout()
        chunk_overlap_label = QLabel("Chunk Overlap:")
        self.chunk_overlap_input = QLineEdit()
        chunk_overlap_layout.addWidget(chunk_overlap_label)
        chunk_overlap_layout.addWidget(self.chunk_overlap_input)
        layout.addLayout(chunk_overlap_layout)

        max_retrieval_top_k_layout = QHBoxLayout()
        max_retrieval_top_k_label = QLabel("Max Retrieval Top k:")
        self.max_retrieval_top_k_input = QLineEdit()
        max_retrieval_top_k_layout.addWidget(max_retrieval_top_k_label)
        max_retrieval_top_k_layout.addWidget(self.max_retrieval_top_k_input)
        layout.addLayout(max_retrieval_top_k_layout)

        similarity_threshold_layout = QHBoxLayout()
        similarity_threshold_label = QLabel("Similarity Threshold:")
        self.similarity_threshold_input = QLineEdit()
        similarity_threshold_layout.addWidget(similarity_threshold_label)
        similarity_threshold_layout.addWidget(self.similarity_threshold_input)
        layout.addLayout(similarity_threshold_layout)

        group_box.setLayout(layout)
        self.main_layout.addWidget(group_box)

    def accept(self):
        valid, message = validate_numeric_field("Context Length", self.context_len_input.text(),
                                                 constraints=config.VALIDATOR['generation']['context_len'])
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        valid, message = validate_numeric_field("Temperature", self.temperature_input.text(),
                                                 constraints=config.VALIDATOR['generation']['temperature'])
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        valid, message = validate_numeric_field("Top p", self.top_p_input.text(),
                                                    constraints=config.VALIDATOR['generation']['top_p'])
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        valid, message = validate_numeric_field("Top k", self.top_k_input.text(),
                                                    constraints=config.VALIDATOR['generation']['top_k'])
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        valid, message = validate_numeric_field("Chunk Size", self.chunk_size_input.text(),
                                                    constraints=config.VALIDATOR['rag']['chunk_size'])
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        valid, message = validate_numeric_field("Chunk Overlap", self.chunk_overlap_input.text(),
                                                    constraints=config.VALIDATOR['rag']['chunk_overlap'])
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        valid, message = validate_numeric_field("Max Retrieval Top k", self.max_retrieval_top_k_input.text(),
                                                    constraints=config.VALIDATOR['rag']['max_retrieval_top_k'])
        
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        valid, message = validate_numeric_field("Similarity Threshold", self.similarity_threshold_input.text(),
                                                    constraints=config.VALIDATOR['rag']['similarity_threshold'])
        
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        self.save_settings()
        self.settingsSaved.emit()
        super().accept()

    def get_model_names_by_type(self, model_type):
        return [model["model_id"] for model in config.models if model["model_type"] == model_type]

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

    def reset_shortcut(self):
        self.shortcut_recorder.setText(config.DEFAULT_LAUNCH_SHORTCUT)

    def update_hey_llama_mic_state(self, state):
        self.hey_llama_mic_checkbox.setEnabled(state == Qt.Checked)

    def load_settings(self):
        if config.settings_file.exists():
            with open(config.settings_file, "r") as f:
                settings = json.load(f)
            try:
                keyboard.HotKey(keyboard.HotKey.parse(settings["shortcut"]), lambda: None)
            except ValueError:
                settings["shortcut"] = config.DEFAULT_LAUNCH_SHORTCUT
                self.save_settings(settings)
            self.shortcut_recorder.setText(settings.get("shortcut", config.DEFAULT_LAUNCH_SHORTCUT))
            self.color = QColor(settings.get("color", "#1E1E1E"))
            self.transparency_slider.setValue(int(settings.get("transparency", 90)))

            text_model = settings.get("text_model")
            if text_model in self.get_model_names_by_type("text"):
                self.text_model_combo.setCurrentText(text_model)

            multimodal_model = settings.get("multimodal_model")
            if multimodal_model in self.get_model_names_by_type("image"):
                self.multimodal_model_combo.setCurrentText(multimodal_model)

            self.hey_llama_chat_checkbox.setChecked(settings.get("hey_llama_chat", False))
            self.hey_llama_mic_checkbox.setChecked(settings.get("hey_llama_mic", False))
            self.update_hey_llama_mic_state(settings.get("hey_llama_chat", False))

            # Load new settings
            if "generation" not in settings:
                settings["generation"] = {}
            if "rag" not in settings:
                settings["rag"] = {}

            embed_model = settings["rag"].get("embed_model_name", config.DEFAULT_SETTINGS['rag']['embed_model_name'])
            if embed_model in config.DEFAULT_EMBEDING_MODELS:
                self.embed_model_combo.setCurrentText(embed_model)
            
            self.chunk_size_input.setText(str(settings["rag"].get("chunk_size", config.DEFAULT_SETTINGS['rag']['chunk_size'])))
            self.chunk_overlap_input.setText(
                str(settings["rag"].get("chunk_overlap", config.DEFAULT_SETTINGS['rag']['chunk_overlap']))
            )
            self.max_retrieval_top_k_input.setText(
                str(settings["rag"].get("max_retrieval_top_k", config.DEFAULT_SETTINGS['rag']['max_retrieval_top_k']))
            )
            self.similarity_threshold_input.setText(
                str(settings["rag"].get("similarity_threshold", config.DEFAULT_SETTINGS['rag']['similarity_threshold']))
            )
            self.context_len_input.setText(
                str(settings["generation"].get("context_len", config.DEFAULT_SETTINGS['generation']['context_len']))
            )
            
            self.temperature_input.setText(
                str(settings["generation"].get("temperature", config.DEFAULT_SETTINGS['generation']['temperature']))
            )
            self.top_p_input.setText(str(settings["generation"].get("top_p", config.DEFAULT_SETTINGS['generation']['top_p'])))
            self.top_k_input.setText(str(settings["generation"].get("top_k", config.DEFAULT_SETTINGS['generation']['top_k'])))
        else:
            self.color = QColor("#1E1E1E")
            self.shortcut_recorder.setText("<cmd>+<shift>+<space>")

    def get_settings(self):
        return {
            "shortcut": self.shortcut_recorder.text(),
            "color": self.color.name(),
            "transparency": self.transparency_slider.value(),
            "text_model": self.text_model_combo.currentText(),
            "multimodal_model": self.multimodal_model_combo.currentText(),
            "hey_llama_chat": self.hey_llama_chat_checkbox.isChecked(),
            "hey_llama_mic": self.hey_llama_mic_checkbox.isChecked(),
            "generation": {
                "context_len": int(self.context_len_input.text()),
                "temperature": float(self.temperature_input.text()),
                "top_p": float(self.top_p_input.text()),
                "top_k": int(self.top_k_input.text()),
            },
            "rag": {
                "embed_model_name": self.embed_model_combo.currentText(),
                "chunk_size": int(self.chunk_size_input.text()),
                "chunk_overlap": int(self.chunk_overlap_input.text()),
                "max_retrieval_top_k": int(self.max_retrieval_top_k_input.text()),
                "similarity_threshold": float(self.similarity_threshold_input.text()),
            },
        }

    def save_settings(self, settings=None):
        if settings is None:
            settings = self.get_settings()

        with open(config.settings_file, "w") as f:
            json.dump(settings, f)

    def open_custom_models_dialog(self):
        dialog = CustomModelsDialog(self)
        if dialog.exec():
            # Refresh the model combos after managing custom models
            self.refresh_model_combos()
        self.refresh_model_combos()  # Run refresh_model_combos after closing the custom models editor

    def refresh_model_combos(self):
        current_text_model = self.text_model_combo.currentText()
        current_multimodal_model = self.multimodal_model_combo.currentText()

        self.text_model_combo.clear()
        self.text_model_combo.addItems(self.get_model_names_by_type("text"))
        self.multimodal_model_combo.clear()
        self.multimodal_model_combo.addItems(self.get_model_names_by_type("image"))

        # Restore previously selected models if they still exist
        if current_text_model in self.get_model_names_by_type("text"):
            self.text_model_combo.setCurrentText(current_text_model)
        if current_multimodal_model in self.get_model_names_by_type("image"):
            self.multimodal_model_combo.setCurrentText(current_multimodal_model)


class CustomModelsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Custom Models")
        self.layout = QVBoxLayout(self)

        self.model_list = QListWidget()
        self.model_list.itemSelectionChanged.connect(self.load_selected_model)
        self.layout.addWidget(self.model_list)

        form_layout = QFormLayout()
        self.model_name_input = QLineEdit()
        self.model_id_input = QLineEdit()
        self.model_type_input = QComboBox()
        self.model_type_input.addItems(["text", "image"])
        self.repo_id_input = QLineEdit()
        self.filename_input = QLineEdit()

        form_layout.addRow("Model Name:", self.model_name_input)
        form_layout.addRow("Model ID:", self.model_id_input)
        form_layout.addRow("Model Type:", self.model_type_input)
        form_layout.addRow("Repo ID:", self.repo_id_input)
        form_layout.addRow("Filename:", self.filename_input)

        self.layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Model")
        self.add_button.clicked.connect(self.add_model)
        self.update_button = QPushButton("Update Model")
        self.update_button.clicked.connect(self.update_model)
        self.remove_button = QPushButton("Remove Model")
        self.remove_button.clicked.connect(self.remove_model)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.remove_button)

        self.layout.addLayout(button_layout)

        self.refresh_model_list()

    def refresh_model_list(self):
        self.model_list.clear()
        for model in config.custom_models:
            self.model_list.addItem(f"{model['model_name']} ({model['model_type']})")

    def load_selected_model(self):
        selected_items = self.model_list.selectedItems()
        if selected_items:
            selected_index = self.model_list.row(selected_items[0])
            model = config.custom_models[selected_index]
            self.model_name_input.setText(model["model_name"])
            self.model_id_input.setText(model["model_id"])
            self.model_type_input.setCurrentText(model["model_type"])
            self.repo_id_input.setText(model["repo_id"])
            self.filename_input.setText(model["filename"])

    def add_model(self):
        model_name = self.model_name_input.text()
        model_id = self.model_id_input.text()
        model_type = self.model_type_input.currentText()
        repo_id = self.repo_id_input.text()
        filename = self.filename_input.text()

        if not all([model_name, model_id, model_type, repo_id, filename]):
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        new_model = {
            "model_name": model_name,
            "model_id": model_id,
            "model_type": model_type,
            "model_path": None,
            "repo_id": repo_id,
            "filename": filename,
        }

        config.custom_models.append(new_model)
        config.save_custom_models()
        self.refresh_model_list()
        self.clear_inputs()
        QMessageBox.information(
            self, "Model Added", f"Model '{model_name}' has been added successfully."
        )

    def update_model(self):
        selected_items = self.model_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a model to update.")
            return

        selected_index = self.model_list.row(selected_items[0])
        model_name = self.model_name_input.text()
        model_id = self.model_id_input.text()
        model_type = self.model_type_input.currentText()
        repo_id = self.repo_id_input.text()
        filename = self.filename_input.text()

        if not all([model_name, model_id, model_type, repo_id, filename]):
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        updated_model = {
            "model_name": model_name,
            "model_id": model_id,
            "model_type": model_type,
            "model_path": None,
            "repo_id": repo_id,
            "filename": filename,
        }

        config.custom_models[selected_index] = updated_model
        config.models = config.DEFAULT_MODELS + config.custom_models
        config.save_custom_models()
        self.refresh_model_list()
        self.clear_inputs()
        QMessageBox.information(
            self, "Model Updated", f"Model '{model_name}' has been updated successfully."
        )

    def remove_model(self):
        selected_items = self.model_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a model to remove.")
            return

        selected_index = self.model_list.row(selected_items[0])
        model_name = config.custom_models[selected_index]["model_name"]
        del config.custom_models[selected_index]
        config.models = config.DEFAULT_MODELS + config.custom_models
        config.save_custom_models()
        self.refresh_model_list()
        self.clear_inputs()
        QMessageBox.information(
            self, "Model Removed", f"Model '{model_name}' has been removed successfully."
        )

    def clear_inputs(self):
        self.model_name_input.clear()
        self.model_id_input.clear()
        self.model_type_input.setCurrentIndex(0)
        self.repo_id_input.clear()
        self.filename_input.clear()
