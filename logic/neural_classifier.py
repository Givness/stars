import numpy as np
import pickle
import tensorflow as tf
import json

class NeuralClassifier:
    def __init__(self, model_path="ai/star_model.keras", encoder_path="ai/label_encoder.pkl", kb_path="data/knowledge_base.json"):
        self.model = tf.keras.models.load_model(model_path)
        with open(encoder_path, "rb") as f:
            self.label_encoder = pickle.load(f)

        with open(kb_path, "r", encoding="utf-8") as f:
            kb = json.load(f)

        self.numeric_props = [k for k, v in kb["properties"].items() if v["type"] == "числовой"]
        self.enum_props = [k for k, v in kb["properties"].items() if v["type"] == "перечислимый"]
        self.numeric_ranges = {k: v["options"] for k, v in kb["properties"].items() if v["type"] == "числовой"}
        self.enum_options = {k: v["options"] for k, v in kb["properties"].items() if v["type"] == "перечислимый"}

    def normalize(self, val, min_val, max_val):
        return (val - min_val) / (max_val - min_val)

    def predict(self, features: dict):
        input_vector = []

        # Числовые признаки
        for prop in self.numeric_props:
            val = features.get(prop)
            min_val, max_val = self.numeric_ranges[prop]

            if val is None:
                input_vector.append(0.5)  # заглушка
                input_vector.append(0.0)  # отсутствует
            else:
                norm = self.normalize(val, min_val, max_val)
                input_vector.append(norm)
                input_vector.append(1.0)  # присутствует

        # Перечислимые признаки
        for prop in self.enum_props:
            val = features.get(prop)
            options = self.enum_options[prop]

            if val is None or val == "Не выбрано" or val not in options:
                input_vector.append(0.5)
                input_vector.append(0.0)
            else:
                index = options.index(val) / (len(options) - 1)
                input_vector.append(index)
                input_vector.append(1.0)

        x = np.array([input_vector])
        pred = self.model.predict(x, verbose=0)
        label = self.label_encoder.inverse_transform([np.argmax(pred)])[0]
        confidence = float(np.max(pred))
        return label, confidence