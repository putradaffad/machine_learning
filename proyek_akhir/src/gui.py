# ========== Import Modul ==========
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Toplevel
from train_model import train_and_save_model            # Fungsi untuk melatih dan menyimpan model
from predict import predict_by_nim                      # Fungsi untuk prediksi berdasarkan NIM
from utils import load_dataset, load_riwayat, save_riwayat  # Fungsi bantu: load dataset dan riwayat
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# ========== Gaya Tampilan (Konstanta Tampilan) ==========
FONT_HEADER = ("Helvetica", 14, "bold")
FONT_LABEL = ("Helvetica", 11)
FONT_TEXT = ("Courier New", 10)
BG_COLOR = "#f4f9ff"
BTN_COLOR = "#1a73e8"
BTN_TEXT_COLOR = "#ffffff"

# ========== Fungsi: Tampilkan Data Mahasiswa ==========
def tampilkan_data():
    df = load_dataset()  # Load data dari dataset.csv

    window = Toplevel(root)  # Buat jendela baru
    window.title("📄 Data Mahasiswa")
    window.geometry("950x550")
    window.configure(bg=BG_COLOR)

    tk.Label(window, text="📄 Daftar Data Mahasiswa", font=FONT_HEADER, bg=BG_COLOR).pack(pady=10)

    # Area teks untuk menampilkan data
    text_area = tk.Text(window, wrap="none", font=FONT_TEXT, bg="white", relief="solid", borderwidth=1)
    text_area.insert(tk.END, df.drop(columns=['target']).to_string(index=False))  # Hapus kolom target
    text_area.config(state=tk.DISABLED)

    # Scroll bar horizontal dan vertikal
    vsb = tk.Scrollbar(window, orient="vertical", command=text_area.yview)
    hsb = tk.Scrollbar(window, orient="horizontal", command=text_area.xview)
    text_area.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    text_area.pack(expand=True, fill="both", side="left", padx=(10, 0), pady=10)
    vsb.pack(fill="y", side="left", pady=10)
    hsb.pack(fill="x", side="bottom", padx=10)

    # Fungsi untuk ekspor CSV
    def ekspor_csv():
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            df.drop(columns=['target']).to_csv(filename, index=False)
            messagebox.showinfo("✅ Ekspor Berhasil", f"Data berhasil disimpan ke {filename}")

    tk.Button(window, text="⬇️ Ekspor CSV", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_LABEL,
              command=ekspor_csv).pack(pady=5)

# ========== Fungsi: Statistik Dataset ==========
def tampilkan_statistik():
    df = load_dataset()
    total = len(df)
    terlambat = df['target'].sum()
    tepat = total - terlambat

    window = Toplevel(root)
    window.title("📈 Statistik Dataset")
    window.geometry("500x400")
    window.configure(bg="white")

    tk.Label(window, text="📊 Statistik Keterlambatan Tugas", font=FONT_HEADER, bg="white").pack(pady=15)

    # Pie chart distribusi keterlambatan
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie([tepat, terlambat], labels=["Tepat Waktu", "Terlambat"], autopct='%1.1f%%', colors=['#34a853', '#ea4335'])
    ax.set_title("Distribusi Keterlambatan")

    # Embed pie chart ke tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Tampilkan info statistik
    stats = f"👥 Jumlah Mahasiswa : {total}\n🟢 Tepat Waktu: {tepat}\n🔴 Terlambat: {terlambat}"
    tk.Label(window, text=stats, font=FONT_LABEL, bg="white", justify="left").pack(pady=10)

# ========== Fungsi: Latih Ulang Model ==========
def latih_model():
    train_and_save_model()  # Melatih model dan menyimpan ke file model.pkl
    messagebox.showinfo("✅ Model", "Model berhasil dilatih dan disimpan!")

# ========== Inisialisasi Riwayat Prediksi ==========
prediksi_history = load_riwayat()

# ========== Fungsi: Form Prediksi Mahasiswa ==========
def prediksi_baru():
    df = load_dataset()
    daftar_nim = sorted(df['NIM'].astype(str).tolist())

    window = Toplevel(root)
    window.title("🔍 Form Prediksi Berdasarkan NIM")
    window.geometry("500x330")
    window.configure(bg="white")

    tk.Label(window, text="Masukkan atau pilih NIM Mahasiswa", font=FONT_LABEL, bg="white").pack(pady=(20, 5))

    frame_input = tk.Frame(window, bg="white")
    frame_input.pack(pady=5)

    # Input manual dan dropdown NIM
    entry_nim = tk.Entry(frame_input, font=FONT_LABEL, width=25)
    entry_nim.grid(row=0, column=0, padx=5)

    combo_nim = ttk.Combobox(frame_input, values=daftar_nim, width=10, state="readonly")
    combo_nim.grid(row=0, column=1, padx=5)
    combo_nim.bind("<<ComboboxSelected>>", lambda e: entry_nim.delete(0, tk.END) or entry_nim.insert(0, combo_nim.get()))

    # Proses prediksi setelah klik tombol
    def proses_prediksi():
        try:
            nim = entry_nim.get().strip()
            if not nim.isdigit():
                raise ValueError("NIM harus berupa angka.")

            # Panggil fungsi prediksi
            hasil, nama, probabilitas, riwayat, persen_tepat = predict_by_nim(nim)
            status = "🟢 TEPAT WAKTU" if hasil == 0 else "🔴 TERLAMBAT"
            warna = "#e6f4ea" if hasil == 0 else "#fdecea"

            # Simpan ke riwayat
            prediksi_history.append((nim, nama, status, f"{probabilitas*100:.2f}%"))
            save_riwayat(prediksi_history)

            # Tampilkan hasil prediksi
            hasil_window = Toplevel(window)
            hasil_window.title("📊 Hasil Prediksi")
            hasil_window.geometry("420x300")
            hasil_window.configure(bg=warna)

            tk.Label(hasil_window, text="📊 Hasil Prediksi Mahasiswa", font=FONT_HEADER, bg=warna).pack(pady=15)

            output = (
                f"👤 Nama Mahasiswa  : {nama}\n"
                f"📝 Riwayat Tugas   : {riwayat}\n"
                f"📌 Prediksi        : {status}\n"
                f"🤖 Keyakinan Model : {probabilitas * 100:.2f}%\n"
                f"📈 Tugas Tepat     : {persen_tepat:.2f}%"
            )

            tk.Label(hasil_window, text=output, font=FONT_LABEL, bg=warna, justify="left", anchor="w").pack(padx=20, pady=10, anchor="w")
            tk.Button(hasil_window, text="❎ Tutup", width=15, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_LABEL,
                      command=hasil_window.destroy).pack(pady=15)

        except ValueError as ve:
            messagebox.showerror("❗ Input Salah", str(ve))
        except Exception as e:
            messagebox.showerror("❗ Error", f"Terjadi kesalahan:\n{str(e)}")

    frame_btn = tk.Frame(window, bg="white")
    frame_btn.pack(pady=20)

    # Tombol prediksi dan clear
    tk.Button(frame_btn, text="🔍 Prediksi", width=18, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
              font=FONT_LABEL, command=proses_prediksi).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="♻️ Clear", width=12, bg="#cccccc", font=FONT_LABEL,
              command=lambda: entry_nim.delete(0, tk.END)).grid(row=0, column=1, padx=5)

# ========== Fungsi: Tampilkan Riwayat Prediksi ==========
def tampilkan_riwayat():
    if not prediksi_history:
        messagebox.showinfo("ℹ️ Riwayat Kosong", "Belum ada riwayat prediksi.")
        return

    window = Toplevel(root)
    window.title("📜 Riwayat Prediksi")
    window.geometry("500x330")
    window.configure(bg="white")

    tk.Label(window, text="📜 Riwayat Prediksi Mahasiswa", font=FONT_HEADER, bg="white").pack(pady=10)

    # Area teks untuk menampilkan riwayat
    text_area = tk.Text(window, font=FONT_TEXT, wrap="none", bg="white")
    header = f"{'NIM':<10} {'Nama':<25} {'Status':<15} {'Keyakinan':<10}\n"
    text_area.insert(tk.END, header + "="*60 + "\n")
    for nim, nama, status, prob in prediksi_history:
        text_area.insert(tk.END, f"{nim:<10} {nama:<25} {status:<15} {prob:<10}\n")
    text_area.config(state=tk.DISABLED)
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    # Tombol hapus riwayat
    def clear_riwayat():
        global prediksi_history
        if messagebox.askyesno("⚠️ Konfirmasi", "Yakin ingin menghapus seluruh riwayat?"):
            prediksi_history = []
            save_riwayat(prediksi_history)
            window.destroy()
            messagebox.showinfo("🧹 Riwayat Dihapus", "Riwayat prediksi berhasil dibersihkan.")

    tk.Button(window, text="🧹 Clear Riwayat", bg="#cccccc", font=FONT_LABEL, command=clear_riwayat).pack(pady=(5, 10))

# ========== Tampilan Utama Aplikasi ==========
root = tk.Tk()
root.title("🎓 Prediksi Keterlambatan Tugas Mahasiswa")
root.geometry("520x520")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# Judul
judul = tk.Label(root, text="SISTEM PREDIKSI KETERLAMBATAN TUGAS MAHASISWA",
                 font=FONT_HEADER, bg=BG_COLOR, fg="#202124", wraplength=420, justify="center")
judul.pack(pady=(30, 20))

frame_button = tk.Frame(root, pady=10, bg=BG_COLOR)
frame_button.pack()

# Fungsi pembuat tombol
def buat_tombol(text, command):
    return tk.Button(frame_button, text=text, width=38, height=2,
                     bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_LABEL, command=command)

# Daftar tombol menu utama
buat_tombol("📄 1. Lihat Data Mahasiswa", tampilkan_data).pack(pady=5)
buat_tombol("📈 2. Statistik Dataset", tampilkan_statistik).pack(pady=5)
buat_tombol("⚙️ 3. Latih Model", latih_model).pack(pady=5)
buat_tombol("🔎 4. Prediksi Mahasiswa", prediksi_baru).pack(pady=5)
buat_tombol("🧾 5. Riwayat Prediksi", tampilkan_riwayat).pack(pady=5)
buat_tombol("❌ 6. Keluar", root.quit).pack(pady=5)

# Jalankan GUI
root.mainloop()
