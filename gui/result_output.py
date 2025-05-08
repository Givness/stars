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
            matched = matches.get(typ, []) if matches else []
            failed = explanations.get(typ, []) if explanations else []
            total = len(matched) + len(failed)
            summary = f" ({len(matched)}/{total})" if total > 0 else ""

            self.output.append(f"<u>Тип {typ}{summary}:</u>")
            for m in matched:
                self.output.append(f"<span style='color:green;'>{m}</span>")
            for reason in failed:
                self.output.append(f"<span style='color:red;'>{reason}</span>")
            self.output.append("<br>")

        self.output.moveCursor(QTextCursor.MoveOperation.Start)