# GUI Final Lengkap – Pencarian di Dataset & Semua Fungsi Tetap
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Toplevel
from train_model import train_and_save_model
from predict import predict_by_nim, predict_by_nama
from utils import load_dataset, load_riwayat, save_riwayat
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import pandas as pd

FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_TEXT = ("Consolas", 10)
BG_COLOR = "#eef2f7"
BTN_COLOR = "#0d6efd"
BTN_TEXT_COLOR = "white"

prediksi_history = load_riwayat()

root = tk.Tk()
root.title("🎓 Prediksi Keterlambatan Tugas Mahasiswa")
root.geometry("580x600")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

def apply_hover(btn):
    def on_enter(e): btn['bg'] = "#0b5ed7"
    def on_leave(e): btn['bg'] = BTN_COLOR
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

def buat_tombol(text, command):
    btn = tk.Button(frame_button, text=text, width=42, height=2, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
                    font=FONT_LABEL, command=command)
    btn.pack(pady=6)
    apply_hover(btn)

def tampilkan_data():  # Modified: Tambah opsi pilihan kolom pencarian
    df = load_dataset()
    win = Toplevel(root)
    win.title("📄 Data Mahasiswa")
    win.geometry("960x600")
    win.configure(bg=BG_COLOR)

    tk.Label(win, text="📄 Daftar Data Mahasiswa", font=FONT_HEADER, bg=BG_COLOR).pack(pady=10)

    search_frame = tk.Frame(win, bg=BG_COLOR)
    search_frame.pack(pady=(0, 5))

    mode_var = tk.StringVar(value="NIM")
    tk.Label(search_frame, text="Pilih kolom pencarian:", font=FONT_LABEL, bg=BG_COLOR).pack(anchor="w", padx=5, pady=(0, 5))

    radio_frame = tk.Frame(search_frame, bg=BG_COLOR)
    radio_frame.pack(anchor="w", padx=5)
    tk.Radiobutton(radio_frame, text="🔢 NIM", variable=mode_var, value="NIM", bg=BG_COLOR).grid(row=0, column=0, padx=10)
    tk.Radiobutton(radio_frame, text="🧑 Nama", variable=mode_var, value="nama", bg=BG_COLOR).grid(row=0, column=1, padx=10)
    tk.Radiobutton(radio_frame, text="📊 Total Terlambat", variable=mode_var, value="total_terlambat", bg=BG_COLOR).grid(row=0, column=2, padx=10)

    cari_entry = tk.Entry(search_frame, font=FONT_LABEL, width=30)
    cari_entry.pack(pady=(5, 0))

    text = tk.Text(win, wrap="none", font=FONT_TEXT, bg="white", relief="flat", borderwidth=1)
    text.tag_configure("center", justify="center")
    vsb = tk.Scrollbar(win, orient="vertical", command=text.yview)
    hsb = tk.Scrollbar(win, orient="horizontal", command=text.xview)
    text.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    def tampilkan(isi_df):
        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        lines = isi_df.to_string(index=False).split("\n") if not isi_df.empty else ["Tidak ditemukan."]
        max_width = max(len(line) for line in lines)
        centered_lines = [line.center(max_width) for line in lines]
        text.insert(tk.END, "\n".join(centered_lines))
        text.config(state=tk.DISABLED)

    tampilkan(df.drop(columns='target'))

    def filter_data():
        keyword = cari_entry.get().strip().lower()
        if keyword == "":
            tampilkan(df.drop(columns='target'))
        else:
            kolom = mode_var.get()
            if kolom == "total_terlambat":
                hasil = df[df['total_terlambat'].astype(str).str.contains(keyword)]
            elif kolom == "nama":
                hasil = df[df['nama'].str.lower().str.contains(keyword)]
            else:
                hasil = df[df['NIM'].astype(str).str.contains(keyword)]
            tampilkan(hasil.drop(columns='target'))

    tk.Button(search_frame, text="🔍 Cari", font=FONT_LABEL, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=filter_data).pack(side="left", padx=5)

    text.pack(expand=True, fill="both", side="left", padx=(10, 0), pady=10)
    vsb.pack(fill="y", side="left", pady=10)
    hsb.pack(fill="x", side="bottom", padx=10)

    def ekspor():
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            df.drop(columns='target').to_csv(filename, index=False)
            messagebox.showinfo("✅ Ekspor Berhasil", f"Data berhasil disimpan ke {filename}")

    btn = tk.Button(win, text="⬇️ Ekspor CSV", font=FONT_LABEL, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=ekspor)
    btn.pack(pady=5)
    apply_hover(btn)

def tampilkan_statistik():
    df = load_dataset()
    total, terlambat = len(df), df['target'].sum()
    tepat = total - terlambat

    win = Toplevel(root)
    win.title("📈 Statistik Dataset")
    win.geometry("500x400")
    win.configure(bg="white")

    tk.Label(win, text="📊 Statistik Keterlambatan Tugas", font=FONT_HEADER, bg="white").pack(pady=15)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie([tepat, terlambat], labels=["Tepat Waktu", "Terlambat"], autopct='%1.1f%%', colors=['#198754', '#dc3545'])
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack()

    info = f"👥 Total Mahasiswa : {total}\n🟢 Tepat Waktu     : {tepat}\n🔴 Terlambat       : {terlambat}"
    tk.Label(win, text=info, font=FONT_LABEL, bg="white").pack(pady=10)

def latih_model():
    train_and_save_model()
    messagebox.showinfo("✅ Model", "Model berhasil dilatih dan disimpan!")

def prediksi_baru():
    df = load_dataset()
    daftar_nim = sorted(df['NIM'].astype(str).tolist())
    daftar_nama = sorted(df['nama'].tolist())

    win = Toplevel(root)
    win.title("🔍 Form Prediksi Mahasiswa")
    win.geometry("520x400")
    win.configure(bg="white")

    tk.Label(win, text="Pilih metode pencarian:", font=FONT_LABEL, bg="white").pack(pady=(15, 5))

    mode_var = tk.StringVar(value="NIM")
    opsi_frame = tk.Frame(win, bg="white")
    opsi_frame.pack()
    tk.Radiobutton(opsi_frame, text="🔢 Berdasarkan NIM", variable=mode_var, value="NIM", bg="white").grid(row=0, column=0, padx=10)
    tk.Radiobutton(opsi_frame, text="🧑 Berdasarkan Nama", variable=mode_var, value="Nama", bg="white").grid(row=0, column=1, padx=10)

    input_frame = tk.Frame(win, bg="white")
    input_frame.pack(pady=10)
    entry_input = tk.Entry(input_frame, font=FONT_LABEL, width=25)
    entry_input.grid(row=0, column=0, padx=5)
    combo_input = ttk.Combobox(input_frame, values=daftar_nim, width=15, state="readonly")
    combo_input.grid(row=0, column=1, padx=5)
    combo_input.bind("<<ComboboxSelected>>", lambda e: entry_input.delete(0, tk.END) or entry_input.insert(0, combo_input.get()))

    def update_dropdown(*args):
        combo_input.config(values=daftar_nim if mode_var.get() == "NIM" else daftar_nama)
        entry_input.delete(0, tk.END)

    mode_var.trace_add("write", update_dropdown)

    def proses_prediksi():
        try:
            input_val = entry_input.get().strip()
            if not input_val:
                raise ValueError("Input tidak boleh kosong.")

            if mode_var.get() == "NIM":
                if not input_val.isdigit():
                    raise ValueError("NIM harus berupa angka.")
                hasil, nama, probabilitas, riwayat, persen_tepat = predict_by_nim(input_val)
                nim = input_val
            else:
                hasil, nama, nim, probabilitas, riwayat, persen_tepat = predict_by_nama(input_val)

            status = "🟢 TEPAT WAKTU" if hasil == 0 else "🔴 TERLAMBAT"
            warna = "#e6f4ea" if hasil == 0 else "#fdecea"
            prediksi_history.append((nim, nama, status, f"{probabilitas*100:.2f}%"))
            save_riwayat(prediksi_history)

            out = Toplevel(win); out.title("📊 Hasil Prediksi")
            out.geometry("420x300"); out.configure(bg=warna)
            hasil_text = (
                f"👤 Nama: {nama}\n"
                f"🆔 NIM: {nim}\n"
                f"📝 Riwayat: {riwayat}\n"
                f"📌 Prediksi: {status}\n"
                f"🤖 Keyakinan: {probabilitas * 100:.2f}%\n"
                f"📈 Tugas Tepat: {persen_tepat:.2f}%"
            )
            tk.Label(out, text=hasil_text, font=FONT_LABEL, bg=warna, justify="left").pack(padx=20, pady=15)
            tk.Button(out, text="❎ Tutup", width=15, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_LABEL, command=out.destroy).pack(pady=10)
        except ValueError as ve:
            messagebox.showerror("❗ Input Salah", str(ve))
        except Exception as e:
            messagebox.showerror("❗ Error", f"Terjadi kesalahan:\n{str(e)}")

    btn_frame = tk.Frame(win, bg="white")
    btn_frame.pack(pady=20)
    btn_pred = tk.Button(btn_frame, text="🔍 Prediksi", width=18, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT_LABEL, command=proses_prediksi)
    btn_pred.grid(row=0, column=0, padx=5)
    btn_clear = tk.Button(btn_frame, text="♻️ Clear", width=12, bg="#cccccc", font=FONT_LABEL, command=lambda: entry_input.delete(0, tk.END))
    btn_clear.grid(row=0, column=1, padx=5)
    apply_hover(btn_pred)

def tampilkan_riwayat():
    if not prediksi_history:
        messagebox.showinfo("ℹ️ Riwayat Kosong", "Belum ada riwayat prediksi.")
        return

    win = Toplevel(root)
    win.title("📜 Riwayat Prediksi")
    win.geometry("500x330")
    win.configure(bg="white")

    tk.Label(win, text="📜 Riwayat Prediksi Mahasiswa", font=FONT_HEADER, bg="white").pack(pady=10)
    text = tk.Text(win, font=FONT_TEXT, wrap="none", bg="white")
    header = f"{'NIM':<10} {'Nama':<25} {'Status':<15} {'Keyakinan':<10}\n{'='*60}\n"
    text.insert(tk.END, header)
    for nim, nama, status, prob in prediksi_history:
        text.insert(tk.END, f"{nim:<10} {nama:<25} {status:<15} {prob:<10}\n")
    text.config(state=tk.DISABLED)
    text.pack(expand=True, fill="both", padx=10, pady=10)

    def clear_riwayat():
        global prediksi_history
        if messagebox.askyesno("⚠️ Konfirmasi", "Yakin ingin menghapus seluruh riwayat?"):
            prediksi_history = []
            save_riwayat(prediksi_history)
            win.destroy()
            messagebox.showinfo("🧹 Riwayat Dihapus", "Riwayat prediksi berhasil dibersihkan.")

    btn = tk.Button(win, text="🧹 Clear Riwayat", bg="#cccccc", font=FONT_LABEL, command=clear_riwayat)
    btn.pack(pady=(5, 10))

judul = tk.Label(root, text="SISTEM PREDIKSI KETERLAMBATAN TUGAS MAHASISWA", font=FONT_HEADER, bg=BG_COLOR, wraplength=480, justify="center")
judul.pack(pady=(20, 15))
frame_button = tk.Frame(root, bg=BG_COLOR); frame_button.pack()
buat_tombol("📄 Lihat Data Mahasiswa", tampilkan_data)
buat_tombol("📈 Statistik Dataset", tampilkan_statistik)
buat_tombol("⚙️ Latih Model", latih_model)
buat_tombol("🔎 Prediksi Mahasiswa", prediksi_baru)
buat_tombol("🧾 Riwayat Prediksi", tampilkan_riwayat)
buat_tombol("❌ Keluar", root.quit)
root.mainloop()
