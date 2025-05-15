import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import numpy as np
import json
import pickle
import os

with open("data/knowledge_base.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

numeric_props = [k for k, v in kb["properties"].items() if v["type"] == "числовой"]
enum_props = [k for k, v in kb["properties"].items() if v["type"] == "перечислимый"]
numeric_ranges = {k: v["options"] for k, v in kb["properties"].items() if v["type"] == "числовой"}
enum_options = {k: v["options"] for k, v in kb["properties"].items() if v["type"] == "перечислимый"}

def normalize(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val)

X = []
y = []

samples_per_class = 2000
missing_prob = 0.25

for star_type, values in kb["values_by_type"].items():
    for _ in range(samples_per_class):
        sample = []

        for prop in numeric_props:
            if np.random.rand() < missing_prob:
                sample.append(0.5)
                sample.append(0.0)
            else:
                val_min, val_max = values[prop]
                val = np.random.uniform(val_min, val_max)
                global_min, global_max = kb["properties"][prop]["options"]
                norm = normalize(val, global_min, global_max)
                sample.append(norm)
                sample.append(1.0)

        for prop in enum_props:
            if np.random.rand() < missing_prob:
                sample.append(0.5)
                sample.append(0.0)
            else:
                val = np.random.choice(values[prop])
                index = enum_options[prop].index(val) / (len(enum_options[prop]) - 1)
                sample.append(index)
                sample.append(1.0)

        X.append(sample)
        y.append(star_type)

X = np.array(X)
le = LabelEncoder()
y_encoded = le.fit_transform(y)
y_onehot = tf.keras.utils.to_categorical(y_encoded)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X.shape[1],)),
    tf.keras.layers.Dense(64),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.ReLU(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(64),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.ReLU(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(y_onehot.shape[1], activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y_onehot, epochs=100, batch_size=32, verbose=1)

os.makedirs("ai", exist_ok=True)
model.save("ai/star_model.keras")
with open("ai/label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("Модель и кодировщик меток сохранены: ai/star_model.keras и ai/label_encoder.pkl")