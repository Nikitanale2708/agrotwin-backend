import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ---------------- LOAD DATA ----------------
df = pd.read_excel(r"E:/OneDrive/Documents/Digital_Twin/fertilizer_dataset1.csv.xlsx")

print("Columns:", df.columns)

# ---------------- CLEAN ----------------
df = df.drop(columns=['District_Name', 'Link'], errors='ignore')
df = df.dropna()   # ✅ remove missing

# ---------------- FEATURES ----------------
features = [
    'Soil_color',
    'Nitrogen',
    'Phosphorus',
    'Potassium',
    'pH',
    'Rainfall',
    'Temperature',
    'Crop'
]

target = 'Fertilizer'

# ---------------- ENCODING ----------------
le_soil = LabelEncoder()
le_crop = LabelEncoder()
le_target = LabelEncoder()

df['Soil_color'] = le_soil.fit_transform(df['Soil_color'].astype(str))
df['Crop'] = le_crop.fit_transform(df['Crop'].astype(str))
df['Fertilizer'] = le_target.fit_transform(df['Fertilizer'].astype(str))

# ---------------- SPLIT ----------------
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODEL ----------------
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------- EVALUATION ----------------
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"✅ Model Accuracy: {round(acc * 100, 2)}%")

# ---------------- SAVE ----------------
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model, os.path.join(MODEL_DIR, "fertilizer_model.pkl"))
joblib.dump(le_soil, os.path.join(MODEL_DIR, "le_soil.pkl"))
joblib.dump(le_crop, os.path.join(MODEL_DIR, "le_crop.pkl"))
joblib.dump(le_target, os.path.join(MODEL_DIR, "le_target.pkl"))

print("✅ Fertilizer model trained successfully!")