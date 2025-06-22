import pandas as pd  # Library untuk memproses data tabular
import os  # Library untuk operasi sistem file seperti pengecekan file

# Fungsi untuk memuat dataset utama
def load_dataset():
    # Membaca dataset dari file CSV
    df = pd.read_csv('data/dataset.csv')
    
    # Menambahkan kolom target secara dinamis: 1 jika total keterlambatan > 2, selain itu 0
    df['target'] = (df['total_terlambat'] > 2).astype(int)
    
    return df  # Mengembalikan dataframe

# Fungsi untuk memuat riwayat prediksi dari file CSV
def load_riwayat():
    path = 'data/riwayat.csv'  # Lokasi file riwayat

    # Jika file riwayat ada, baca dan ubah ke list of list
    if os.path.exists(path):
        return pd.read_csv(path).values.tolist()
    
    # Jika tidak ada, kembalikan list kosong
    return []

# Fungsi untuk menyimpan riwayat prediksi ke file CSV
def save_riwayat(data):
    # Buat dataframe dari data dengan nama kolom yang sesuai
    df = pd.DataFrame(data, columns=["NIM", "Nama", "Status", "Keyakinan"])
    
    # Simpan ke file CSV tanpa menyertakan index
    df.to_csv('data/riwayat.csv', index=False)
