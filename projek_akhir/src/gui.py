import tkinter as tk
from tkinter import messagebox
from train_model import train_and_save_model
from predict import predict_late
from utils import load_dataset

def tampilkan_data():
    df = load_dataset()
    messagebox.showinfo("Data Mahasiswa", df.to_string())

def latih_model():
    train_and_save_model()
    messagebox.showinfo("Model", "Model berhasil dilatih dan disimpan.")

def prediksi_baru():
    try:
        x1 = int(entry1.get())
        x2 = int(entry2.get())
        x3 = int(entry3.get())

        if x1 not in [0, 1] or x2 not in [0, 1] or x3 not in [0, 1]:
            raise ValueError

        hasil = predict_late([x1, x2, x3])
        teks = "TERLAMBAT" if hasil == 1 else "TEPAT WAKTU"
        messagebox.showinfo("Hasil Prediksi", f"Mahasiswa diprediksi: {teks}")
    except:
        messagebox.showerror("Error", "Input harus 0 atau 1!")

# Buat Window Utama
root = tk.Tk()
root.title("Prediksi Keterlambatan Tugas Mahasiswa")
root.geometry("400x300")

# Label dan Entry
tk.Label(root, text="Tugas 1 (0/1):").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Tugas 2 (0/1):").pack()
entry2 = tk.Entry(root)
entry2.pack()

tk.Label(root, text="Tugas 3 (0/1):").pack()
entry3 = tk.Entry(root)
entry3.pack()

# Tombol
tk.Button(root, text="Tampilkan Data", command=tampilkan_data).pack(pady=5)
tk.Button(root, text="Latih Model", command=latih_model).pack(pady=5)
tk.Button(root, text="Prediksi", command=prediksi_baru).pack(pady=5)
tk.Button(root, text="Keluar", command=root.quit).pack(pady=5)

# Jalankan GUI
root.mainloop()
