class StarClassifier:
    def __init__(self, kb):
        self.kb = kb

    def classify(self, input_data):
        candidates = []
        explanations = {}

        for star_type in self.kb.data["types"]:
            valid = True
            reasons = []
            for prop in self.kb.data["type_descriptions"].get(star_type, []):
                expected = self.kb.data["values_by_type"][star_type].get(prop)
                given = input_data.get(prop)

                if expected is None or given is None:
                    continue

                if self.kb.data["properties"][prop]["type"] == "числовой":
                    if isinstance(expected, list):
                        if not (expected[0] <= given <= expected[1]):
                            valid = False
                            reasons.append(f"{prop} = {given} вне диапазона {expected}")
                    else:
                        if given != expected:
                            valid = False
                            reasons.append(f"{prop} = {given}, ожидалось {expected}")
                else:
                    if given not in expected:
                        valid = False
                        reasons.append(f"{prop} = {given}, ожидалось {expected}")

            if valid:
                candidates.append(star_type)
            else:
                explanations[star_type] = reasons

        return candidates, explanations

    def matched_properties(self, input_data):
        matches = {}
        for star_type in self.kb.data["types"]:
            matched = []
            for prop in self.kb.data["type_descriptions"].get(star_type, []):
                expected = self.kb.data["values_by_type"][star_type].get(prop)
                given = input_data.get(prop)
                if expected is None or given is None:
                    continue

                if self.kb.data["properties"][prop]["type"] == "числовой":
                    if isinstance(expected, list) and expected[0] <= given <= expected[1]:
                        matched.append(f"{prop} = {given} в пределах {expected}")
                else:
                    if given in expected:
                        matched.append(f"{prop} = {given} допустимо")
            if matched:
                matches[star_type] = matched
        return matches