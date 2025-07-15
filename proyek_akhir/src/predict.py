from utils import load_dataset  # Memuat fungsi untuk mengambil dataset
import joblib  # Untuk memuat model yang telah disimpan

def predict_by_nim(nim):
    # Memuat dataset mahasiswa
    df = load_dataset()

    # Memuat model machine learning yang sudah dilatih
    model = joblib.load('model/model.pkl')

    # Mencari baris data mahasiswa yang memiliki NIM sesuai input
    mahasiswa = df[df['NIM'] == int(nim)]

    # Jika NIM tidak ditemukan, berikan error
    if mahasiswa.empty:
        raise ValueError("NIM tidak ditemukan dalam dataset.")

    # Mengambil fitur riwayat keterlambatan tugas untuk prediksi
    fitur = mahasiswa[['terlambat_1', 'terlambat_2', 'terlambat_3', 'terlambat_4', 'terlambat_5']]
    nama = mahasiswa.iloc[0]['nama']  # Ambil nama mahasiswa
    riwayat = fitur.iloc[0].tolist()  # Riwayat keterlambatan dalam bentuk list

    # Melakukan prediksi menggunakan model
    prediksi = model.predict(fitur)  # Output: 0 (tepat waktu) atau 1 (terlambat)
    semua_probabilitas = model.predict_proba(fitur)[0]  # Probabilitas untuk semua kelas [tepat, terlambat]
    
    # 🔍 Debug: Menampilkan probabilitas ke terminal (bisa dihapus jika tidak dibutuhkan)
    print("Probabilitas semua kelas:", semua_probabilitas)

    # Mengambil probabilitas dari hasil prediksi (misalnya jika prediksi = 1, ambil index ke-1)
    probabilitas = semua_probabilitas[prediksi[0]]

    # Menghitung persentase tugas yang dikumpulkan tepat waktu dari riwayat
    jumlah_tepat_waktu = riwayat.count(0)
    persentase_tepat_waktu = (jumlah_tepat_waktu / len(riwayat)) * 100

    # Mengembalikan hasil prediksi, nama, probabilitas, riwayat keterlambatan, dan persentase tepat waktu
    return prediksi[0], nama, probabilitas, riwayat, persentase_tepat_waktu


def predict_by_nama(nama):
    df = load_dataset()
    model = joblib.load('model/model.pkl')

    # Cari nama yang cocok (case insensitive)
    mahasiswa = df[df['nama'].str.lower() == nama.lower()]

    if mahasiswa.empty:
        raise ValueError("Nama tidak ditemukan dalam dataset.")

    fitur = mahasiswa[['terlambat_1', 'terlambat_2', 'terlambat_3', 'terlambat_4', 'terlambat_5']]
    nama = mahasiswa.iloc[0]['nama']
    nim = mahasiswa.iloc[0]['NIM']
    riwayat = fitur.iloc[0].tolist()

    prediksi = model.predict(fitur)
    semua_probabilitas = model.predict_proba(fitur)[0]
    probabilitas = semua_probabilitas[prediksi[0]]

    jumlah_tepat_waktu = riwayat.count(0)
    persentase_tepat_waktu = (jumlah_tepat_waktu / len(riwayat)) * 100

    return prediksi[0], nama, nim, probabilitas, riwayat, persentase_tepat_waktu
