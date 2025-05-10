from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtGui import QTextCursor


class ResultOutputWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)
        self.setLayout(self.layout)

    def display_results(self, candidates, explanations, matches=None, ordered_types=None):
        self.output.clear()

        if candidates:
            self.output.append("<b>Подходящие типы звёзд:</b>")
            for c in candidates:
                self.output.append(f"<span style='color:green;'>{c}</span>")
        else:
            self.output.append("<b>Тип звезды не определён.</b>")

        self.output.append("<br><b>Анализ по каждому типу:</b>")

        all_types = ordered_types or sorted(set((matches or {}).keys()) | set((explanations or {}).keys()))
        for typ in all_types:
            self.output.append(f"<u>Тип {typ}:</u>")
            for m in matches.get(typ, []):
                self.output.append(f"<span style='color:green;'>{m}</span>")
            for r in explanations.get(typ, []):
                self.output.append(f"<span style='color:red;'>{r}</span>")
            self.output.append("<br>")

        self.output.moveCursor(QTextCursor.MoveOperation.Start)
