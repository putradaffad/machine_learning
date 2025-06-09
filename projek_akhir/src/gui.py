import tkinter as tk
from tkinter import messagebox, Toplevel
from train_model import train_and_save_model
from predict import predict_late
from utils import load_dataset

def tampilkan_data():
    df = load_dataset()

    # Window baru
    window = tk.Toplevel(root)
    window.title("Data Mahasiswa")
    window.geometry("700x400")
    window.configure(bg="#f0f0f0")

    # Text widget
    text_area = tk.Text(window, wrap="none", font=("Courier New", 10))
    text_area.insert(tk.END, df.to_string(index=False))
    text_area.config(state=tk.DISABLED)

    # Scrollbar
    vsb = tk.Scrollbar(window, orient="vertical", command=text_area.yview)
    hsb = tk.Scrollbar(window, orient="horizontal", command=text_area.xview)
    text_area.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Layout
    text_area.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

def latih_model():
    train_and_save_model()
    messagebox.showinfo("Model", "Model berhasil dilatih dan disimpan.")

def prediksi_baru():
    # Form baru untuk prediksi
    window = Toplevel(root)
    window.title("Form Prediksi Baru")
    window.geometry("400x350")
    window.configure(bg="#f9f9f9")

    tk.Label(window, text="Nama Mahasiswa:", bg="#f9f9f9").grid(row=0, column=0, pady=(10,5), padx=10, sticky="w")
    entry_nama = tk.Entry(window, width=30)
    entry_nama.grid(row=0, column=1, pady=(10,5), padx=10)

    tugas_labels = ["Tugas 1", "Tugas 2", "Tugas 3", "Tugas 4", "Tugas 5"]
    entry_tugas = []

    for i, label in enumerate(tugas_labels):
        tk.Label(window, text=f"{label} (0/1):", bg="#f9f9f9").grid(row=i+1, column=0, padx=10, sticky="w")
        entry = tk.Entry(window, width=5)
        entry.grid(row=i+1, column=1, padx=10, pady=3, sticky="w")
        entry_tugas.append(entry)

    def proses_prediksi():
        try:
            nama = entry_nama.get()
            x = [int(ent.get()) for ent in entry_tugas]

            if not nama.strip():
                raise ValueError("Nama harus diisi.")
            if any(i not in [0, 1] for i in x):
                raise ValueError("Semua input tugas harus berupa 0 atau 1.")

            hasil = predict_late(x)
            teks = "TERLAMBAT" if hasil == 1 else "TEPAT WAKTU"
            messagebox.showinfo("Hasil Prediksi", f"{nama} diprediksi: {teks}")

        except ValueError as ve:
            messagebox.showerror("Input Salah", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    tk.Button(window, text="Prediksi", width=20, command=proses_prediksi).grid(row=6, column=0, columnspan=2, pady=20)

# Root window
root = tk.Tk()
root.title("Prediksi Keterlambatan Tugas Mahasiswa")
root.geometry("400x300")
root.configure(bg="#f0f0f0")
root.resizable(False, False)

# Judul
label_judul = tk.Label(root, text="=== SISTEM PREDIKSI KETERLAMBATAN TUGAS ===",
                       font=("Helvetica", 12, "bold"), bg="#f0f0f0", fg="#333")
label_judul.pack(pady=(20, 10))

# Tombol Navigasi
frame_button = tk.Frame(root, pady=10, bg="#f0f0f0")
frame_button.pack()

tk.Button(frame_button, text="1. Lihat Data", width=30, command=tampilkan_data).pack(pady=5)
tk.Button(frame_button, text="2. Latih Model", width=30, command=latih_model).pack(pady=5)
tk.Button(frame_button, text="3. Prediksi Baru", width=30, command=prediksi_baru).pack(pady=5)
tk.Button(frame_button, text="4. Keluar", width=30, command=root.quit).pack(pady=5)

root.mainloop()
