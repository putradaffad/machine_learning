import pandas as pd  # Untuk memanipulasi data dalam bentuk DataFrame
from sklearn.ensemble import RandomForestClassifier  # Model klasifikasi Random Forest
from sklearn.model_selection import train_test_split  # Untuk membagi dataset menjadi train/test
from sklearn.metrics import classification_report  # Untuk evaluasi performa model
import joblib  # Untuk menyimpan dan memuat model ke/dari file

def train_and_save_model():
    # Membaca dataset dari file CSV
    df = pd.read_csv('data/dataset.csv')

    # Membuat kolom target: 1 jika total keterlambatan > 2, else 0
    df['target'] = (df['total_terlambat'] > 2).astype(int)

    # Menentukan fitur input (X) dan target/output (y)
    X = df[['terlambat_1', 'terlambat_2', 'terlambat_3', 'terlambat_4', 'terlambat_5']]
    y = df['target']

    # Membagi dataset menjadi data latih dan data uji (80:20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Inisialisasi model Random Forest dengan parameter yang ditentukan
    model = RandomForestClassifier(
        n_estimators=100,      # Jumlah pohon dalam hutan
        max_depth=4,           # Kedalaman maksimum setiap pohon
        min_samples_leaf=5,    # Minimal jumlah sampel di daun pohon
        random_state=42        # Seed untuk hasil konsisten
    )

    # Melatih model menggunakan data latih
    model.fit(X_train, y_train)

    # Evaluasi model dengan data uji
    y_pred = model.predict(X_test)
    print("=== EVALUASI MODEL ===")
    print(classification_report(y_test, y_pred))  # Tampilkan metrik evaluasi (precision, recall, f1)

    # Simpan model yang telah dilatih ke dalam file
    joblib.dump(model, 'model/model.pkl')

# Jalankan fungsi hanya jika file ini dijalankan secara langsung
if __name__ == '__main__':
    train_and_save_model()