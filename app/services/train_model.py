# train_model.py

import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# 🔹 BASE DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 🔹 DATA PATHS
input_file = os.path.join(BASE_DIR, "data", "processed", "it_jobs_processed.csv")
output_model_file = os.path.join(BASE_DIR, "models", "future_it_model.pkl")

# 🔹 LOAD FILTERED IT DATA
df = pd.read_csv(input_file)
print(f"Loaded IT dataset: {df.shape}")

# 🔹 SKILL COLUMNS
skill_cols = [f"Skill_{i}" for i in range(1, 11)]

# 🔹 CREATE FEATURE SET
# Combine skills + AI/automation features
X = pd.concat([
    df[skill_cols],
    df[["AI_Exposure_Index", "Tech_Growth_Factor", "Automation_Probability_2030"]]
], axis=1)

# Target: future IT role
y = df["Job_Title"]

# 🔹 SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 🔹 TRAIN MODEL
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# 🔹 EVALUATION
y_pred = model.predict(X_test)
print("\n📊 MODEL PERFORMANCE")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# 🔹 SAVE MODEL
os.makedirs(os.path.dirname(output_model_file), exist_ok=True)
joblib.dump(model, output_model_file)
print(f"\n✅ Model saved successfully at: {output_model_file}")