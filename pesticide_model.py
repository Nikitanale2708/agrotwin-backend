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

joblib.dump(model, "../model/pesticide_model.pkl")

print("✅ Pesticide model ready")