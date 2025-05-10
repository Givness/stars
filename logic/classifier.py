class StarClassifier:
    def __init__(self, kb):
        self.kb = kb

    def classify(self, input_data):
        candidates = []
        explanations = {}
        matches = {}

        for star_type in self.kb.data["types"]:
            reasons = []
            matched = []
            valid = True

            for prop in self.kb.data["type_descriptions"].get(star_type, []):
                expected = self.kb.data["values_by_type"][star_type].get(prop)
                given = input_data.get(prop)

                if expected is None or given is None:
                    reasons.append(f"{prop} не указано")
                    valid = False
                    break

                if self.kb.data["properties"][prop]["type"] == "числовой":
                    if expected[0] <= given <= expected[1]:
                        matched.append(f"{prop} = {given}, в пределах {expected}")
                    else:
                        reasons.append(f"{prop} = {given}, вне диапазона {expected}")
                        valid = False
                        break
                else:
                    if given in expected:
                        matched.append(f"{prop} = {given}, допустимо")
                    else:
                        reasons.append(f"{prop} = {given}, ожидалось одно из {expected}")
                        valid = False
                        break

            if valid:
                candidates.append(star_type)
            if matched:
                matches[star_type] = matched
            if reasons:
                explanations[star_type] = reasons

        return candidates, explanations, matches