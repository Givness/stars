from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QListWidget, QListWidgetItem,
    QFormLayout, QLineEdit, QVBoxLayout, QLabel, QFrame
)
from logic.knowledge_base import KnowledgeBase


class KnowledgeViewerWidget(QWidget):
    def __init__(self, kb):
        super().__init__()
        self.kb = kb

        layout = QHBoxLayout()

        self.type_list = QListWidget()
        self.type_list.itemClicked.connect(self.display_properties)
        layout.addWidget(self.type_list)

        self.detail_layout = QFormLayout()
        self.detail_container = QWidget()
        self.detail_container.setLayout(self.detail_layout)

        right_layout = QVBoxLayout()
        self.title_label = QLabel("Выберите тип звезды слева")
        right_layout.addWidget(self.title_label)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        right_layout.addWidget(line)

        right_layout.addWidget(self.detail_container)
        right_layout.addStretch()

        layout.addLayout(right_layout)
        self.setLayout(layout)
        self.refresh()

    def refresh(self):
        self.type_list.clear()
        for star_type in self.kb.data["types"]:
            item = QListWidgetItem(star_type)
            self.type_list.addItem(item)

        if self.type_list.count() > 0:
            self.type_list.setCurrentRow(0)
            self.display_properties(self.type_list.item(0))
        else:
            self.title_label.setText("Выберите тип звезды слева")
            self.clear_form()

    def display_properties(self, item):
        star_type = item.text()
        self.title_label.setText(f"Тип звезды: {star_type}")
        self.clear_form()

        properties = self.kb.data["type_descriptions"].get(star_type, [])
        values = self.kb.data["values_by_type"].get(star_type, {})
        prop_defs = self.kb.data["properties"]

        for prop in properties:
            val = values.get(prop, "—")
            ptype = prop_defs.get(prop, {}).get("type")

            if ptype == "числовой" and isinstance(val, list) and len(val) == 2:
                from_edit = QLineEdit(str(val[0]))
                to_edit = QLineEdit(str(val[1]))
                for w in [from_edit, to_edit]:
                    w.setReadOnly(True)
                    w.setFixedWidth(70)
                    w.setStyleSheet("margin-top: 0px; margin-bottom: 0px;")

                row_layout = QHBoxLayout()
                row_layout.setContentsMargins(0, 0, 0, 0)
                row_layout.setSpacing(6)
                row_layout.addWidget(QLabel("От"))
                row_layout.addWidget(from_edit)
                row_layout.addSpacing(10)
                row_layout.addWidget(QLabel("До"))
                row_layout.addWidget(to_edit)
                row_layout.addStretch()

                container = QWidget()
                container.setLayout(row_layout)
                self.detail_layout.addRow(QLabel(prop + ":"), container)

            elif ptype == "перечислимый" and isinstance(val, list):
                line = QLineEdit(", ".join(str(v) for v in val))
                line.setReadOnly(True)
                line.setStyleSheet("margin-top: 0px; margin-bottom: 0px;")
                self.detail_layout.addRow(QLabel(prop + ":"), line)

            else:
                line = QLineEdit(str(val))
                line.setReadOnly(True)
                line.setStyleSheet("margin-top: 0px; margin-bottom: 0px;")
                self.detail_layout.addRow(QLabel(prop + ":"), line)

    def clear_form(self):
        while self.detail_layout.rowCount():
            self.detail_layout.removeRow(0)