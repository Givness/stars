from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtGui import QTextCursor


class ResultOutputWidget(QWidget):
    def __init__(self, kb):
        super().__init__()
        self.kb = kb
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
            all_props = self.kb.data["type_descriptions"].get(typ, [])
            match_map = {m.split(" = ")[0]: m for m in matches.get(typ, [])}
            explain_map = {}
            for e in explanations.get(typ, []):
                key = e.split(" = ")[0] if " = " in e else e.split()[0]
                explain_map[key] = e

            # Получаем список всех свойств для данного типа звезды
            all_props = self.kb.data["type_descriptions"].get(typ, [])

            # Создаём отображения совпадений и объяснений по свойствам
            match_map = {m.split(" = ")[0]: m for m in matches.get(typ, [])}

            # Более надёжное сопоставление объяснений по названию свойства
            explain_map = {}
            for e in explanations.get(typ, []):
                for prop in all_props:
                    if prop in e:
                        explain_map[prop] = e
                        break

            # Выводим свойства строго по порядку
            for prop in all_props:
                if prop in match_map:
                    self.output.append(f"<span style='color:green;'>{match_map[prop]}</span>")
                elif prop in explain_map:
                    color = "orange" if "не указано" in explain_map[prop].lower() else "red"
                    self.output.append(f"<span style='color:{color};'>{explain_map[prop]}</span>")
            self.output.append("<br>")

        self.output.moveCursor(QTextCursor.MoveOperation.Start)
