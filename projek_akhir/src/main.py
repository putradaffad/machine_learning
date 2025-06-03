from train_model import train_and_save_model
from predict import predict_late
from utils import load_dataset

def main():
    while True:
        print("\n=== SISTEM PREDIKSI KETERLAMBATAN TUGAS ===")
        print("1. Lihat Data")
        print("2. Latih Model")
        print("3. Prediksi Baru")
        print("4. Keluar")

        pilihan = input("Pilih menu (1/2/3/4): ")

        if pilihan == "1":
            df = load_dataset()
            print(df)

        elif pilihan == "2":
            train_and_save_model()
            print("Model berhasil dilatih dan disimpan.")

        elif pilihan == "3":
            x1 = int(input("Terlambat tugas 1 (0/1): "))
            x2 = int(input("Terlambat tugas 2 (0/1): "))
            x3 = int(input("Terlambat tugas 3 (0/1): "))
            result = predict_late([x1, x2, x3])
            print(">>> Prediksi:", "Terlambat" if result == 1 else "Tepat Waktu")

        elif pilihan == "4":
            break
        else:
            print("Input tidak valid!")

if __name__ == "__main__":
    main()
