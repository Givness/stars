from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedLayout, QListWidget, QListWidgetItem, QLineEdit, QListView, QMessageBox, QComboBox,
    QRadioButton, QButtonGroup, QCheckBox, QSpinBox, QDoubleSpinBox, QTextEdit, QFrame, QFormLayout
)
from logic.knowledge_base import KnowledgeBase
from utils.theme import button_style, remove_button_style


class TypeEditor(QWidget):
    def __init__(self, kb):
        super().__init__()
        self.kb = kb
        layout = QVBoxLayout()
        self.type_list = QListWidget()
        self.refresh()
        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Введите название типа звезды")
        self.add_type_btn = QPushButton("Добавить")
        self.add_type_btn.setStyleSheet(button_style())
        self.add_type_btn.clicked.connect(self.add_star_type)
        layout.addWidget(self.type_list)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.type_input)
        input_layout.addWidget(self.add_type_btn)
        layout.addLayout(input_layout)
        self.setLayout(layout)

    def refresh(self):
        self.type_list.clear()
        for t in self.kb.data["types"]:
            item_widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)

            remove_btn = QPushButton("−")
            remove_btn.setStyleSheet(remove_button_style())
            remove_btn.setFixedWidth(30)
            remove_btn.clicked.connect(lambda _, name=t: self.remove_star_type(name))

            label = QLabel(t)

            layout.addWidget(remove_btn)
            layout.addWidget(label)
            layout.addStretch()

            item_widget.setLayout(layout)

            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.type_list.addItem(item)
            self.type_list.setItemWidget(item, item_widget)

    def add_star_type(self):
        name = self.type_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название типа звезды не может быть пустым.")
            return
        self.kb.add_type(name)
        self.refresh()
        self.type_input.clear()

    def remove_star_type(self, name):
        reply = QMessageBox.question(self, "Удалить тип", f"Удалить тип звезды '{name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.kb.remove_type(name)
            self.refresh()


class PropertyEditor(QWidget):
    def __init__(self, kb):
        super().__init__()
        self.kb = kb
        layout = QVBoxLayout()
        self.property_list = QListWidget()
        self.property_name_input = QLineEdit()
        self.property_name_input.setPlaceholderText("Введите название свойства")
        self.property_type_input = QComboBox()
        self.property_type_input.addItems(["числовой", "перечислимый"])
        self.add_property_btn = QPushButton("Добавить")
        self.add_property_btn.setStyleSheet(button_style())
        self.add_property_btn.clicked.connect(self.add_property)

        layout.addWidget(self.property_list)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.property_name_input)
        input_layout.addWidget(self.property_type_input)
        input_layout.addWidget(self.add_property_btn)
        layout.addLayout(input_layout)
        self.setLayout(layout)
        self.refresh()

    def refresh(self):
        self.property_list.clear()
        for name in self.kb.data["properties"]:
            item_widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)

            remove_btn = QPushButton("−")
            remove_btn.setStyleSheet(remove_button_style())
            remove_btn.setFixedWidth(30)
            remove_btn.clicked.connect(lambda _, prop=name: self.remove_property(prop))

            label = QLabel(name)

            layout.addWidget(remove_btn)
            layout.addWidget(label)
            layout.addStretch()

            item_widget.setLayout(layout)

            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.property_list.addItem(item)
            self.property_list.setItemWidget(item, item_widget)

    def add_property(self):
        name = self.property_name_input.text().strip()
        ptype = self.property_type_input.currentText()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название свойства не может быть пустым.")
            return
        self.kb.add_property(name, ptype)
        self.refresh()
        self.property_name_input.clear()

    def remove_property(self, name):
        reply = QMessageBox.question(self, "Удалить свойство", f"Удалить свойство '{name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.kb.remove_property(name)
            self.refresh()


class PossibleValuesEditor(QWidget):
    def __init__(self, kb):
        super().__init__()
        self.kb = kb
        self.current_property = None

        layout = QVBoxLayout()

        self.property_selector = QComboBox()
        self.property_selector.addItems(self.kb.data['properties'].keys())
        self.property_selector.currentTextChanged.connect(self.select_property)
        layout.addWidget(self.property_selector)

        self.type_selector_layout = QHBoxLayout()
        self.enum_radio = QRadioButton("Перечислимые")
        self.numeric_radio = QRadioButton("Числовые")
        self.type_selector_group = QButtonGroup()
        self.type_selector_group.addButton(self.enum_radio)
        self.type_selector_group.addButton(self.numeric_radio)

        self.enum_radio.toggled.connect(self.switch_type)

        self.type_selector_layout.addWidget(self.enum_radio)
        self.type_selector_layout.addWidget(self.numeric_radio)
        layout.addLayout(self.type_selector_layout)

        self.stacked_layout = QStackedLayout()

        self.enum_widget = QWidget()
        enum_layout = QVBoxLayout()
        self.enum_list = QListWidget()
        enum_layout.addWidget(self.enum_list)

        self.enum_input = QLineEdit()
        self.enum_input.setPlaceholderText("Введите значение")
        self.enum_add_btn = QPushButton("Добавить")
        self.enum_add_btn.clicked.connect(self.add_enum_value)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.enum_input)
        input_layout.addWidget(self.enum_add_btn)

        enum_layout.addLayout(input_layout)
        self.enum_widget.setLayout(enum_layout)

        self.numeric_widget = QWidget()
        numeric_layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.min_spin = QDoubleSpinBox()
        self.max_spin = QDoubleSpinBox()
        self.min_spin.setRange(-100000, 100000)
        self.max_spin.setRange(-100000, 100000)

        form_layout.addRow("Минимум:", self.min_spin)
        form_layout.addRow("Максимум:", self.max_spin)

        numeric_layout.addLayout(form_layout)
        numeric_layout.addStretch()

        self.numeric_widget.setLayout(numeric_layout)

        self.stacked_layout.addWidget(self.enum_widget)
        self.stacked_layout.addWidget(self.numeric_widget)

        layout.addLayout(self.stacked_layout)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setStyleSheet(button_style())
        self.save_btn.clicked.connect(self.save_values)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.last_enum_values = {}
        self.last_numeric_values = {}

    def select_property(self, prop):
        if prop not in self.kb.data['properties']:
            return

        self.current_property = prop
        prop_data = self.kb.data['properties'][prop]

        if self.enum_radio.isChecked():
            self.last_enum_values[self.current_property] = [self.enum_list.item(i).text() for i in range(self.enum_list.count())]
        elif self.numeric_radio.isChecked():
            self.last_numeric_values[self.current_property] = [self.min_spin.value(), self.max_spin.value()]

        if prop_data['type'] == "перечислимый":
            self.enum_radio.setChecked(True)
            self.enum_list.clear()
            for val in prop_data['options']:
                self.add_enum_item(val)
            self.stacked_layout.setCurrentIndex(0)

        elif prop_data['type'] == "числовой":
            self.numeric_radio.setChecked(True)
            self.min_spin.setValue(prop_data['options'][0])
            self.max_spin.setValue(prop_data['options'][1])
            self.stacked_layout.setCurrentIndex(1)

    def switch_type(self):
        if not self.current_property:
            return

        current_type = self.kb.data['properties'][self.current_property]['type']

        if self.enum_radio.isChecked():
            self.stacked_layout.setCurrentIndex(0)
            if current_type != "перечислимый":
                self.last_numeric_values[self.current_property] = [self.min_spin.value(), self.max_spin.value()]
                self.enum_list.clear()
        else:
            self.stacked_layout.setCurrentIndex(1)
            if current_type != "числовой":
                self.last_enum_values[self.current_property] = [self.enum_list.item(i).text() for i in range(self.enum_list.count())]
                self.min_spin.setValue(0.0)
                self.max_spin.setValue(100.0)

    def add_enum_value(self):
        val = self.enum_input.text().strip()
        if val:
            existing = [self.enum_list.itemWidget(self.enum_list.item(i)).layout().itemAt(1).widget().text()
                        for i in range(self.enum_list.count())]
            if val in existing:
                QMessageBox.warning(self, "Ошибка", "Такое значение уже существует.")
                return
            self.add_enum_item(val)
            self.enum_input.clear()

    def add_enum_item(self, value):
        item_widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        remove_btn = QPushButton("−")
        remove_btn.setFixedWidth(30)
        remove_btn.setStyleSheet(remove_button_style())
        remove_btn.clicked.connect(lambda: self.remove_enum_value(value))

        label = QLabel(value)

        layout.addWidget(remove_btn)
        layout.addWidget(label)
        layout.addStretch()

        item_widget.setLayout(layout)

        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        self.enum_list.addItem(item)
        self.enum_list.setItemWidget(item, item_widget)

    def remove_enum_value(self, value):
        for i in range(self.enum_list.count()):
            item = self.enum_list.item(i)
            widget = self.enum_list.itemWidget(item)
            label = widget.layout().itemAt(1).widget()
            if label.text() == value:
                self.enum_list.takeItem(i)
                break

    def save_values(self):
        if not self.current_property:
            QMessageBox.warning(self, "Ошибка", "Выберите свойство")
            return

        if self.enum_radio.isChecked():
            options = []
            for i in range(self.enum_list.count()):
                item = self.enum_list.item(i)
                widget = self.enum_list.itemWidget(item)
                label = widget.layout().itemAt(1).widget()
                options.append(label.text())

            self.kb.data['properties'][self.current_property]['type'] = "перечислимый"
            self.kb.data['properties'][self.current_property]['options'] = options
        else:
            min_val = self.min_spin.value()
            max_val = self.max_spin.value()
            self.kb.data['properties'][self.current_property]['type'] = "числовой"
            self.kb.data['properties'][self.current_property]['options'] = [min_val, max_val]

        self.kb.save()
        QMessageBox.information(self, "Успех", "Значения сохранены")

    def refresh(self):
        self.property_selector.clear()
        self.property_selector.addItems(self.kb.data['properties'].keys())


class TypeDescriptionEditor(QWidget):
    def __init__(self, kb):
        super().__init__()
        self.kb = kb
        layout = QHBoxLayout()

        self.type_list = QListWidget()
        self.type_list.itemSelectionChanged.connect(self.load_properties_for_type)
        layout.addWidget(self.type_list)

        self.property_checkboxes = []
        self.property_area = QWidget()
        outer_layout = QVBoxLayout()

        self.property_layout = QVBoxLayout()
        self.select_all_btn = QCheckBox("Выбрать всё")
        self.select_all_btn.stateChanged.connect(self.toggle_all_properties)
        self.property_layout.addWidget(self.select_all_btn)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.property_layout.addWidget(line)

        self.property_container = QWidget()
        self.property_container.setLayout(self.property_layout)
        outer_layout.addWidget(self.property_container)

        outer_layout.addStretch()

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setStyleSheet(button_style())
        self.save_btn.clicked.connect(self.save)
        outer_layout.addWidget(self.save_btn)

        self.property_area.setLayout(outer_layout)
        layout.addWidget(self.property_area)

        self.setLayout(layout)
        self.refresh()

    def refresh(self):
        self.type_list.clear()
        for t in self.kb.data["types"]:
            self.type_list.addItem(t)
        self.load_property_list()
        
        if self.type_list.count() > 0:
            self.type_list.setCurrentRow(0)

    def load_property_list(self):
        for cb in self.property_checkboxes:
            self.property_layout.removeWidget(cb)
            cb.deleteLater()
        self.property_checkboxes.clear()

        for name in self.kb.data["properties"]:
            cb = QCheckBox(name)
            cb.stateChanged.connect(self.update_select_all_state)
            self.property_checkboxes.append(cb)
            self.property_layout.addWidget(cb)

    def load_properties_for_type(self):
        selected_items = self.type_list.selectedItems()
        if not selected_items:
            return
        type_name = selected_items[0].text()
        selected_props = self.kb.data["type_descriptions"].get(type_name, [])

        for cb in self.property_checkboxes:
            cb.setChecked(cb.text() in selected_props)

        all_checked = all(cb.isChecked() for cb in self.property_checkboxes)
        self.select_all_btn.setChecked(all_checked)

    def toggle_all_properties(self):
        checked = self.select_all_btn.isChecked()
        for cb in self.property_checkboxes:
            cb.setChecked(checked)

    def update_select_all_state(self):
        all_checked = all(cb.isChecked() for cb in self.property_checkboxes)

        self.select_all_btn.blockSignals(True)
        self.select_all_btn.setChecked(all_checked)
        self.select_all_btn.blockSignals(False)

    def save(self):
        selected_items = self.type_list.selectedItems()
        if not selected_items:
            return
        type_name = selected_items[0].text()
        selected_props = [cb.text() for cb in self.property_checkboxes if cb.isChecked()]
        self.kb.data["type_descriptions"][type_name] = selected_props
        self.kb.save()


class TypeValueEditor(QWidget):
    def __init__(self, kb):
        super().__init__()
        self.kb = kb
        layout = QHBoxLayout()

        self.type_list = QListWidget()
        self.type_list.itemSelectionChanged.connect(self.load_properties)
        layout.addWidget(self.type_list)

        self.property_list = QListWidget()
        self.property_list.itemSelectionChanged.connect(self.load_values)
        layout.addWidget(self.property_list)

        control_layout = QVBoxLayout()

        self.value_stack = QStackedLayout()

        numeric_container = QWidget()
        numeric_layout = QVBoxLayout()
        numeric_layout.setContentsMargins(0, 0, 0, 0)

        form = QFormLayout()
        self.range_min = QDoubleSpinBox()
        self.range_max = QDoubleSpinBox()
        self.range_min.setDecimals(2)
        self.range_max.setDecimals(2)
        self.range_min.setRange(-100000, 100000)
        self.range_max.setRange(-100000, 100000)

        form.addRow("От", self.range_min)
        form.addRow("До", self.range_max)
        numeric_layout.addLayout(form)
        numeric_layout.addStretch()

        numeric_container.setLayout(numeric_layout)
        self.value_stack.addWidget(numeric_container)

        enum_container = QWidget()
        enum_layout = QVBoxLayout()
        enum_layout.setContentsMargins(0, 0, 0, 0)

        self.enum_select_all = QCheckBox("Выбрать всё")
        self.enum_select_all.stateChanged.connect(self.toggle_enum_all)
        enum_layout.addWidget(self.enum_select_all)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        enum_layout.addWidget(line)

        self.enum_checkboxes = []
        self.enum_layout = QVBoxLayout()
        enum_layout.addLayout(self.enum_layout)
        enum_layout.addStretch()

        enum_container.setLayout(enum_layout)
        self.value_stack.addWidget(enum_container)

        control_layout.addLayout(self.value_stack)
        control_layout.addStretch()

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setStyleSheet(button_style())
        self.save_btn.clicked.connect(self.save_value)
        control_layout.addWidget(self.save_btn)

        layout.addLayout(control_layout)
        self.setLayout(layout)
        self.refresh()

    def refresh(self):
        self.type_list.clear()
        for t in self.kb.data["types"]:
            self.type_list.addItem(t)

        if self.type_list.count() > 0:
            self.type_list.setCurrentRow(0)
            self.load_properties()
            if self.property_list.count() > 0:
                self.property_list.setCurrentRow(0)

    def load_properties(self):
        self.property_list.clear()
        items = self.type_list.selectedItems()
        if not items:
            return
        t = items[0].text()
        props = self.kb.data["type_descriptions"].get(t, [])
        for p in props:
            self.property_list.addItem(p)
        if self.property_list.count() > 0:
            self.property_list.setCurrentRow(0)

    def load_values(self):
        type_items = self.type_list.selectedItems()
        prop_items = self.property_list.selectedItems()
        if not type_items or not prop_items:
            return
        t = type_items[0].text()
        p = prop_items[0].text()
        prop_type = self.kb.data["properties"].get(p, {}).get("type")
        self.clear_enum()

        if prop_type == "числовой":
            self.value_stack.setCurrentIndex(0)
            val = self.kb.data["values_by_type"].get(t, {}).get(p, [0, 100])
            try:
                self.range_min.setValue(val[0])
                self.range_max.setValue(val[1])
            except Exception:
                self.range_min.setValue(0)
                self.range_max.setValue(100)

        elif prop_type == "перечислимый":
            self.value_stack.setCurrentIndex(1)
            options = self.kb.data["properties"].get(p, {}).get("options", [])
            selected = self.kb.data["values_by_type"].get(t, {}).get(p, [])
            for val in options:
                cb = QCheckBox(val)
                cb.setChecked(val in selected)
                cb.stateChanged.connect(self.update_enum_select_all)
                self.enum_checkboxes.append(cb)
                self.enum_layout.addWidget(cb)
            self.update_enum_select_all()

    def save_value(self):
        type_items = self.type_list.selectedItems()
        prop_items = self.property_list.selectedItems()
        if not type_items or not prop_items:
            return
        t = type_items[0].text()
        p = prop_items[0].text()
        prop_type = self.kb.data["properties"].get(p, {}).get("type")
        if t not in self.kb.data["values_by_type"]:
            self.kb.data["values_by_type"][t] = {}

        if prop_type == "числовой":
            val = [self.range_min.value(), self.range_max.value()]
            self.kb.data["values_by_type"][t][p] = val
        elif prop_type == "перечислимый":
            selected = [cb.text() for cb in self.enum_checkboxes if cb.isChecked()]
            self.kb.data["values_by_type"][t][p] = selected

        self.kb.save()

    def clear_enum(self):
        for cb in self.enum_checkboxes:
            self.enum_layout.removeWidget(cb)
            cb.deleteLater()
        self.enum_checkboxes.clear()

    def toggle_enum_all(self):
        check = self.enum_select_all.isChecked()
        for cb in self.enum_checkboxes:
            cb.setChecked(check)

    def update_enum_select_all(self):
        if not self.enum_checkboxes:
            self.enum_select_all.setChecked(False)
            return

        all_checked = all(cb.isChecked() for cb in self.enum_checkboxes)

        self.enum_select_all.blockSignals(True)
        self.enum_select_all.setChecked(all_checked)
        self.enum_select_all.blockSignals(False)


class KnowledgeValidationWidget(QWidget):
    def __init__(self, kb):
        super().__init__()
        self.kb = kb

        layout = QVBoxLayout()

        self.label = QLabel("Проверка полноты знаний")
        layout.addWidget(self.label)

        self.check_btn = QPushButton("Проверить")
        self.check_btn.setStyleSheet(button_style())
        self.check_btn.clicked.connect(self.validate_knowledge)
        layout.addWidget(self.check_btn)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        self.setLayout(layout)

    def validate_knowledge(self):
        errors = self.kb.validate()
        self.result_output.clear()
        if errors:
            self.result_output.append("Найдены ошибки:")
            for error in errors:
                self.result_output.append(f"- {error}")
        else:
            self.result_output.append("Все данные корректны. Ошибок не найдено.")


class KnowledgeEditorWidget(QWidget):
    def __init__(self, kb):
        super().__init__()
        self.kb = kb

        main_layout = QHBoxLayout()
        self.menu = QListWidget()
        self.menu.setFixedWidth(200)
        self.pages = ["Типы звёзд", "Свойства", "Возможные значения", "Описание свойств типа", "Значения для типа", "Проверка полноты знаний"]
        for name in self.pages:
            QListWidgetItem(name, self.menu)
        self.menu.currentRowChanged.connect(self.display_page)

        self.stack = QStackedLayout()
        self.type_editor = TypeEditor(self.kb)
        self.property_editor = PropertyEditor(self.kb)
        self.values_editor = PossibleValuesEditor(self.kb)
        self.type_desc_editor = TypeDescriptionEditor(self.kb)
        self.type_value_editor = TypeValueEditor(self.kb)
        self.validation_widget = KnowledgeValidationWidget(self.kb)
        self.stack.addWidget(self.type_editor)
        self.stack.addWidget(self.property_editor)
        self.stack.addWidget(self.values_editor)
        self.stack.addWidget(self.type_desc_editor)
        self.stack.addWidget(self.type_value_editor)
        self.stack.addWidget(self.validation_widget)

        main_layout.addWidget(self.menu)
        right_widget = QWidget()
        right_widget.setLayout(self.stack)
        main_layout.addWidget(right_widget)
        self.setLayout(main_layout)
        self.menu.setCurrentRow(0)

    def display_page(self, index):
        self.stack.setCurrentIndex(index)
        if index == 0:
            self.type_editor.refresh()
        elif index == 1:
            self.property_editor.refresh()
        elif index == 2:
            self.values_editor.refresh()
        elif index == 3:
            self.type_desc_editor.refresh()
        elif index == 4:
            self.type_value_editor.refresh()

    def _placeholder(self, text):
        w = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Раздел: {text}"))
        w.setLayout(layout)
        return w