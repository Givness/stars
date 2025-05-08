from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QMessageBox, QHBoxLayout, QCheckBox, QFormLayout
)
from PyQt6.QtGui import QShortcut, QKeySequence
from logic.classifier import StarClassifier
from logic.neural_classifier import NeuralClassifier
from utils.validators import is_number, to_float
from utils.theme import button_style
from gui.result_output import ResultOutputWidget
import random



class DataInputWidget(QWidget):
    def __init__(self, kb):
        super().__init__()
        self.kb = kb
        self.classifier = StarClassifier(self.kb)
        self.neural = NeuralClassifier()
        self.inputs = {}

        self.outer_layout = QVBoxLayout(self)
        self.container = QWidget()
        self.container_layout = QVBoxLayout()
        self.container.setLayout(self.container_layout)
        self.outer_layout.addWidget(self.container)

        self.build_ui()

        shortcut = QShortcut(QKeySequence("Ctrl+Alt+R"), self)
        shortcut.activated.connect(self.fill_random_inputs)

    def build_ui(self):
        self.inputs.clear()
        self.container_layout.addWidget(QLabel("Введите характеристики звезды:"))

        form_layout = QFormLayout()
        for prop, info in self.kb.data["properties"].items():
            if info["type"] == "числовой":
                input_field = QLineEdit()
                input_field.setPlaceholderText(f"{info['options'][0]} ... {info['options'][1]}")
            else:
                input_field = QComboBox()
                input_field.addItems(info["options"])
            self.inputs[prop] = input_field
            form_layout.addRow(QLabel(prop), input_field)

        self.container_layout.addLayout(form_layout)

        self.use_neural_checkbox = QCheckBox("Использовать нейросеть")
        self.container_layout.addWidget(self.use_neural_checkbox)

        self.result_view = ResultOutputWidget()
        self.container_layout.addWidget(self.result_view)

        classify_button = QPushButton("Определить тип звезды")
        classify_button.clicked.connect(self.classify_star)
        classify_button.setStyleSheet(button_style())
        self.container_layout.addWidget(classify_button)

    def classify_star(self):
        input_data = {}
        for prop, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                val = widget.text().strip()
                if not is_number(val):
                    QMessageBox.warning(self, "Ошибка", f"Значение свойства '{prop}' должно быть числом.")
                    return
                input_data[prop] = to_float(val)
            else:
                input_data[prop] = widget.currentText()

        self.result_view.output.clear()

        if self.use_neural_checkbox.isChecked():
            try:
                label, confidence = self.neural.predict(input_data)
                self.result_view.output.setPlainText(f"Тип звезды (нейросеть): {label} (уверенность: {confidence:.2%})")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка классификации", str(e))
        else:
            candidates, explanations = self.classifier.classify(input_data)
            matches = self.classifier.matched_properties(input_data)
            self.result_view.display_results(candidates, explanations, matches, self.kb.data["types"])

    def refresh(self):
        self.outer_layout.removeWidget(self.container)
        self.container.deleteLater()

        self.container = QWidget()
        self.container_layout = QVBoxLayout()
        self.container.setLayout(self.container_layout)
        self.outer_layout.addWidget(self.container)

        self.build_ui()

    def fill_random_inputs(self):
        use_consistent_type = random.random() < 0.5

        if use_consistent_type:
            star_type = random.choice(self.kb.data["types"])
            type_values = self.kb.data["values_by_type"].get(star_type, {})
        else:
            type_values = {}

        for prop, widget in self.inputs.items():
            info = self.kb.data["properties"][prop]
            if info["type"] == "числовой":
                if prop in type_values:
                    min_val, max_val = type_values[prop]
                else:
                    min_val, max_val = info["options"]
                value = round(random.uniform(min_val, max_val), 2)
                widget.setText(str(value))
            else:
                if prop in type_values:
                    value = random.choice(type_values[prop])
                else:
                    value = random.choice(info["options"])
                widget.setCurrentText(value)