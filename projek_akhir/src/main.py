from train_model import train_and_save_model
from predict import predict_late
from utils import load_dataset
import os
import pandas as pd

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def tampilkan_judul():
    print("="*50)
    print("  SISTEM PREDIKSI KETERLAMBATAN TUGAS MAHASISWA")
    print("="*50)

def tampilkan_menu():
    print("\nPILIH MENU:")
    print("1. Lihat Data Mahasiswa")
    print("2. Latih Model")
    print("3. Prediksi Mahasiswa Baru")
    print("4. Keluar")

def tampilkan_data():
    df = load_dataset()
    print("\nDATA MAHASISWA:")
    print("-"*50)
    try:
        # Jika tabulate tersedia
        print(df.to_markdown(index=False))
    except ImportError:
        # Jika tidak tersedia
        print(df.to_string(index=False))
    print("-"*50)


def latih_model():
    train_and_save_model()
    print("\n✅ Model berhasil dilatih dan disimpan.")

def prediksi_baru():
    try:
        nama = input("Nama Mahasiswa: ").strip()
        if not nama:
            raise ValueError("Nama tidak boleh kosong.")

        x = []
        for i in range(1, 6):
            while True:
                nilai = input(f"Tugas {i} (0 = Tepat Waktu, 1 = Terlambat): ")
                if nilai in ['0', '1']:
                    x.append(int(nilai))
                    break
                else:
                    print("⚠️  Input harus 0 atau 1!")

        hasil = predict_late(x)
        status = "📌 TERLAMBAT" if hasil == 1 else "✅ TEPAT WAKTU"
        print(f"\nHasil prediksi untuk {nama.upper()}: {status}")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")

def main():
    while True:
        clear_screen()
        tampilkan_judul()
        tampilkan_menu()

        pilihan = input("\nMasukkan pilihan (1-4): ").strip()

        if pilihan == "1":
            clear_screen()
            tampilkan_judul()
            tampilkan_data()
            input("\nTekan ENTER untuk kembali ke menu...")

        elif pilihan == "2":
            clear_screen()
            tampilkan_judul()
            latih_model()
            input("\nTekan ENTER untuk kembali ke menu...")

        elif pilihan == "3":
            clear_screen()
            tampilkan_judul()
            prediksi_baru()
            input("\nTekan ENTER untuk kembali ke menu...")

        elif pilihan == "4":
            print("\nTerima kasih telah menggunakan sistem ini 🙏")
            break

        else:
            print("❌ Pilihan tidak valid!")
            input("Tekan ENTER untuk ulangi...")

if __name__ == "__main__":
    main()
