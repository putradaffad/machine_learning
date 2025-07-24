# src/core/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def train_and_save_model():
    # Load dataset
    df = pd.read_csv('data/raw/dataset.csv')

    # Validasi nilai kosong
    if df.isnull().values.any():
        raise ValueError("Dataset mengandung nilai kosong. Harap bersihkan terlebih dahulu.")

    # Tambahkan kolom target: 1 jika total keterlambat > 2
    df['target'] = (df['total_terlambat'] > 2).astype(int)

    # Pisahkan fitur dan target
    X = df[[f'terlambat_{i}' for i in range(1, 6)]]
    y = df['target']

    # Split data latih dan uji
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inisialisasi model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=4,
        min_samples_leaf=5,
        random_state=42
    )

    # Latih model
    model.fit(X_train, y_train)

    # Evaluasi
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print("=== EVALUASI MODEL ===")
    print(report)

    # Simpan hasil evaluasi ke file log
    os.makedirs("model", exist_ok=True)
    with open("model/evaluasi.txt", "w") as f:
        f.write(report)
