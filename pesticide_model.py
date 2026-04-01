import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

df = pd.read_csv("E:\OneDrive\Documents\Digital_Twin\sugarcane_pesticides_dataset.csv")

# Features
X = df[['disease']]
y = df['pesticide_name']

# Encode
X['disease'] = X['disease'].astype('category').cat.codes

model = DecisionTreeClassifier()
model.fit(X, y)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model, os.path.join(MODEL_DIR, "pesticide_model.pkl"))

print("✅ Pesticide model ready")