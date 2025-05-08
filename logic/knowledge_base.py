import json
from pathlib import Path


class KnowledgeBase:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.data = {
            "types": [],
            "properties": {},
            "type_descriptions": {},
            "values_by_type": {}
        }
        self.load()

    def load(self):
        if self.filepath.exists():
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

    def save(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def add_type(self, star_type: str):
        if star_type not in self.data["types"]:
            self.data["types"].append(star_type)
            self.data["type_descriptions"][star_type] = []
            self.data["values_by_type"][star_type] = {}
            self.save()

    def remove_type(self, star_type: str):
        if star_type in self.data["types"]:
            self.data["types"].remove(star_type)
            self.data["type_descriptions"].pop(star_type, None)
            self.data["values_by_type"].pop(star_type, None)
            self.save()

    def add_property(self, name: str, value_type: str, options=None):
        self.data["properties"][name] = {
            "type": value_type,
            "options": options or ([] if value_type == "перечислимый" else [0.0, 100.0])
        }
        self.save()

    def remove_property(self, name: str):
        self.data["properties"].pop(name, None)
        for typ in self.data["types"]:
            self.data["values_by_type"][typ].pop(name, None)
            if name in self.data["type_descriptions"][typ]:
                self.data["type_descriptions"][typ].remove(name)
        self.save()

    def set_property_for_type(self, star_type: str, prop: str, value):
        self.data["values_by_type"][star_type][prop] = value
        if prop not in self.data["type_descriptions"][star_type]:
            self.data["type_descriptions"][star_type].append(prop)
        self.save()

    def validate(self):
        errors = []

        for prop_name, prop_data in self.data["properties"].items():
            if "type" not in prop_data or "options" not in prop_data:
                errors.append(f"Свойство '{prop_name}' не имеет типа или списка допустимых значений.")
                continue

            if not prop_data["options"]:
                errors.append(f"Свойство '{prop_name}' не имеет допустимых значений.")

            elif prop_data["type"] == "перечислимый" and not isinstance(prop_data["options"], list):
                errors.append(f"Свойство '{prop_name}': перечислимые значения должны быть списком.")

            elif prop_data["type"] == "числовой":
                if (not isinstance(prop_data["options"], list) or
                    len(prop_data["options"]) != 2 or
                    not all(isinstance(v, (int, float)) for v in prop_data["options"])):
                    errors.append(f"Свойство '{prop_name}': числовой тип должен иметь диапазон из двух чисел.")

        for typ in self.data["types"]:
            desc = self.data["type_descriptions"].get(typ)
            if not desc:
                errors.append(f"Тип '{typ}' не имеет описанных свойств.")
                continue

            for prop in desc:
                if prop not in self.data["properties"]:
                    errors.append(f"Тип '{typ}': свойство '{prop}' отсутствует в общем списке.")
                    continue

                prop_data = self.data["properties"][prop]
                val = self.data["values_by_type"].get(typ, {}).get(prop)

                if val is None:
                    errors.append(f"Тип '{typ}': не задано значение свойства '{prop}'.")
                    continue

                if prop_data["type"] == "перечислимый":
                    if not isinstance(val, list):
                        errors.append(f"Тип '{typ}', свойство '{prop}': значение должно быть списком.")
                    else:
                        for v in val:
                            if v not in prop_data["options"]:
                                errors.append(f"Тип '{typ}', свойство '{prop}': значение '{v}' не входит в список допустимых: {prop_data['options']}")
                elif prop_data["type"] == "числовой":
                    if (not isinstance(val, list) or len(val) != 2):
                        errors.append(f"Тип '{typ}', свойство '{prop}': значение должно быть диапазоном [min, max].")
                    else:
                        min_val, max_val = val
                        min_opt, max_opt = prop_data["options"]
                        if min_val > max_val:
                            errors.append(f"Тип '{typ}', свойство '{prop}': нижняя граница больше верхней.")
                        if min_val < min_opt or max_val > max_opt:
                            errors.append(f"Тип '{typ}', свойство '{prop}': диапазон {val} выходит за пределы допустимого {prop_data['options']}.")
                else:
                    errors.append(f"Свойство '{prop}': неизвестный тип '{prop_data['type']}'.")

        return errors