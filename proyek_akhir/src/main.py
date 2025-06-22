import os
from train_model import train_and_save_model  # Fungsi untuk melatih dan menyimpan model
from predict import predict_by_nim  # Fungsi untuk melakukan prediksi berdasarkan NIM
from utils import load_dataset, load_riwayat, save_riwayat  # Fungsi utilitas untuk data dan riwayat

# ========== Riwayat Prediksi ==========
prediksi_history = load_riwayat()  # Memuat riwayat prediksi yang tersimpan

# ========== Gaya Tampilan CLI ==========
def garis():
    print("=" * 60)  # Menampilkan garis horizontal sebagai pembatas

def tampilkan_judul():
    garis()
    print("📚 SISTEM PREDIKSI KETERLAMBATAN TUGAS MAHASISWA".center(60))  # Judul utama program
    garis()

def tampilkan_menu():
    # Menampilkan menu pilihan ke pengguna
    print("\n📋 PILIH MENU:")
    print("1. 📄 Lihat Data Mahasiswa")
    print("2. 📈 Statistik Dataset")
    print("3. ⚙️ Latih Model")
    print("4. 🔍 Prediksi Berdasarkan NIM")
    print("5. 🧾 Lihat Riwayat Prediksi")
    print("6. 🧹 Hapus Riwayat Prediksi")
    print("7. ❌ Keluar")

# ========== Fungsi Menu ==========
def tampilkan_data():
    # Menampilkan data mahasiswa tanpa kolom target
    df = load_dataset()
    print("\n📄 DATA MAHASISWA:")
    print("-" * 60)
    try:
        from tabulate import tabulate  # Untuk tampilan tabel yang lebih rapi
        print(tabulate(df.drop(columns=['target']), headers='keys', tablefmt='fancy_grid', showindex=False))
    except ImportError:
        # Jika tabulate tidak tersedia, tampilkan dengan format default
        print(df.drop(columns=['target']).to_string(index=False))
    print("-" * 60)

def tampilkan_statistik():
    # Menampilkan ringkasan statistik dataset
    df = load_dataset()
    total = len(df)  # Total data mahasiswa
    terlambat = df['target'].sum()  # Jumlah mahasiswa yang terlambat
    tepat = total - terlambat  # Jumlah mahasiswa tepat waktu
    persen_terlambat = (terlambat / total) * 100
    persen_tepat = 100 - persen_terlambat

    print("\n📊 STATISTIK DATASET:")
    print("-" * 60)
    print(f"👥 Jumlah Mahasiswa : {total}")
    print(f"🟢 Tepat Waktu      : {tepat} mahasiswa ({persen_tepat:.2f}%)")
    print(f"🔴 Terlambat        : {terlambat} mahasiswa ({persen_terlambat:.2f}%)")
    print("-" * 60)

def latih_model():
    # Melatih ulang model dan menyimpannya
    train_and_save_model()
    print("\n✅ Model berhasil dilatih dan disimpan!")

def prediksi_baru():
    # Fungsi untuk memproses prediksi berdasarkan input NIM
    global prediksi_history
    try:
        nim = input("🆔 Masukkan NIM Mahasiswa: ").strip()
        if not nim.isdigit():
            raise ValueError("NIM harus berupa angka.")

        # Lakukan prediksi dan ambil hasilnya
        hasil, nama, probabilitas, riwayat, persen_tepat = predict_by_nim(nim)
        status = "🟢 TEPAT WAKTU" if hasil == 0 else "🔴 TERLAMBAT"

        # Tampilkan hasil prediksi ke pengguna
        print("\n📊 HASIL PREDIKSI")
        print("-" * 60)
        print(f"👤 Nama Mahasiswa     : {nama}")
        print(f"📝 Riwayat Tugas      : {riwayat}")
        print(f"📌 Prediksi           : {status}")
        print(f"🤖 Keyakinan Model    : {probabilitas * 100:.2f}%")
        print(f"📈 Tugas Tepat Waktu  : {persen_tepat:.2f}%")
        print("-" * 60)

        # Simpan hasil ke dalam riwayat
        prediksi_history.append((nim, nama, status, f"{probabilitas * 100:.2f}%"))
        save_riwayat(prediksi_history)

    except Exception as e:
        # Tampilkan pesan kesalahan jika terjadi error
        print(f"❌ Terjadi kesalahan: {e}")

def tampilkan_riwayat():
    # Menampilkan riwayat prediksi yang telah dilakukan
    if not prediksi_history:
        print("\nℹ️ Riwayat prediksi masih kosong.")
        return

    print("\n📜 RIWAYAT PREDIKSI:")
    print("-" * 60)
    print(f"{'NIM':<10} {'Nama':<25} {'Status':<15} {'Keyakinan':<10}")
    print("-" * 60)
    for nim, nama, status, prob in prediksi_history:
        print(f"{nim:<10} {nama:<25} {status:<15} {prob:<10}")
    print("-" * 60)

def hapus_riwayat():
    # Menghapus semua riwayat prediksi dengan konfirmasi
    global prediksi_history
    konfirmasi = input("⚠️ Yakin ingin menghapus semua riwayat? (y/n): ").lower()
    if konfirmasi == 'y':
        prediksi_history = []
        save_riwayat(prediksi_history)
        print("✅ Riwayat prediksi berhasil dihapus.")
    else:
        print("❎ Penghapusan dibatalkan.")

# ========== Program Utama ==========
def main():
    # Fungsi utama untuk menjalankan aplikasi CLI
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Membersihkan layar
        tampilkan_judul()
        tampilkan_menu()

        pilihan = input("\n🕓 Masukkan pilihan (1-7): ").strip()

        if pilihan == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            tampilkan_judul()
            tampilkan_data()
            input("\n🔙 Tekan ENTER untuk kembali ke menu...")

        elif pilihan == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            tampilkan_judul()
            tampilkan_statistik()
            input("\n🔙 Tekan ENTER untuk kembali ke menu...")

        elif pilihan == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            tampilkan_judul()
            latih_model()
            input("\n🔙 Tekan ENTER untuk kembali ke menu...")

        elif pilihan == "4":
            os.system('cls' if os.name == 'nt' else 'clear')
            tampilkan_judul()
            prediksi_baru()
            input("\n🔙 Tekan ENTER untuk kembali ke menu...")

        elif pilihan == "5":
            os.system('cls' if os.name == 'nt' else 'clear')
            tampilkan_judul()
            tampilkan_riwayat()
            input("\n🔙 Tekan ENTER untuk kembali ke menu...")

        elif pilihan == "6":
            hapus_riwayat()
            input("\n🔙 Tekan ENTER untuk kembali ke menu...")

        elif pilihan == "7":
            # Keluar dari program
            print("\n🙏 Terima kasih telah menggunakan sistem ini!")
            break

        else:
            # Penanganan jika input tidak valid
            print("❌ Pilihan tidak valid!")
            input("🔁 Tekan ENTER untuk ulangi...")

# Menjalankan program utama jika file ini dijalankan langsung
if __name__ == "__main__":
    main()
