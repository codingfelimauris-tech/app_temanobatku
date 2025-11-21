#!/usr/bin/env python3
"""
TemanObatKu v2.0 - Advanced CLI
- Konsultasi obat sederhana sesuai rancangan user (educational only)
- Riwayat lengkap dengan manajemen (tampil, hapus, cari, ekspor)
"""

import json
import os
import csv
from datetime import datetime
from textwrap import fill

# -------------------------
# Konstanta / Data (sesuai rancangan)
# -------------------------
RIWAYAT_FILE = "riwayat.json"

OBAT = {
    "Flu": [
        {"nama": "CTM", "dosis": "Dewasa 4mg 2-3x/hari; Anak 6-12 th: 2mg 2-3x/hari",
         "aturan": "Setelah makan / bisa menyebabkan kantuk", "efek": "Ngantuk, mulut kering", "ket": "Antihistamin"},
        {"nama": "Loratadine", "dosis": "Dewasa 10mg 1x/hari; Anak 6-12th: 5mg 1x/hari",
         "aturan": "Bisa kapan saja", "efek": "Pusing, mulut kering ringan", "ket": "Tidak bikin ngantuk"},
        {"nama": "Pseudoephedrine", "dosis": "Dewasa 60mg 2x/hari; Anak 6-12th: 30mg 2x/hari",
         "aturan": "Hindari malam hari", "efek": "Berdebar, susah tidur", "ket": "Dekongestan"},
    ],
    "Demam": [
        {"nama": "Paracetamol", "dosis": "Dewasa 500-1000mg tiap 6-8 jam; Anak 10-15 mg/kgBB",
         "aturan": "Bisa sebelum/ sesudah makan", "efek": "Aman, jarang efek samping", "ket": "Pilihan pertama"},
        {"nama": "Ibuprofen", "dosis": "Dewasa 200-400mg/8 jam; Anak 5-10mg/kgBB",
         "aturan": "Setelah makan", "efek": "Nyeri lambung", "ket": "Hindari maag"},
        {"nama": "Asam mefenamat", "dosis": "500mg awal, lanjut 250mg tiap 6 jam",
         "aturan": "Setelah makan", "efek": "Perih lambung", "ket": "Jangan pada maag berat"},
    ],
    "Pusing": [  # sama obatnya seperti Demam menurut rancangan
        {"nama": "Paracetamol", "dosis": "Dewasa 500-1000mg tiap 6-8 jam; Anak 10-15 mg/kgBB",
         "aturan": "Bisa sebelum/ sesudah makan", "efek": "Aman, jarang efek samping", "ket": "Pilihan pertama"},
        {"nama": "Ibuprofen", "dosis": "Dewasa 200-400mg/8 jam; Anak 5-10mg/kgBB",
         "aturan": "Setelah makan", "efek": "Nyeri lambung", "ket": "Hindari maag"},
        {"nama": "Asam mefenamat", "dosis": "500mg awal, lanjut 250mg tiap 6 jam",
         "aturan": "Setelah makan", "efek": "Perih lambung", "ket": "Jangan pada maag berat"},
    ],
    "Batuk": [
        {"nama": "Dextromethorphan", "dosis": "Dewasa 10-20mg/6 jam; Anak 5-10mg/6 jam",
         "aturan": "Jangan >4x/hari", "efek": "Ngantuk", "ket": "Penekan batuk"},
        {"nama": "Guaifenesin", "dosis": "Dewasa 200-400mg/4 jam; Anak 100-200mg/4 jam",
         "aturan": "Minum air banyak", "efek": "Mual ringan", "ket": "Pengencer dahak"},
        {"nama": "Bromhexine / Ambroxol", "dosis": "Dewasa 8-16mg 3x/hari; Anak 4mg 3x/hari",
         "aturan": "Setelah makan", "efek": "Mulas, mual", "ket": "Mukolitik"},
    ],
    "Mual": [
        {"nama": "Antasida", "dosis": "1-2 tablet / 5-10ml sirup 3x/hari",
         "aturan": "Sebelum makan", "efek": "Diare/konstipasi", "ket": "Menetralkan asam"},
        {"nama": "Domperidone", "dosis": "Dewasa 10mg 3x/hari",
         "aturan": "30 menit sebelum makan", "efek": "Kram perut", "ket": "Untuk mual dan muntah"},
    ],
    "Diare": [
        {"nama": "Oralit", "dosis": "1 sachet/200ml, minum bertahap",
         "aturan": "Sedikit-sedikit", "efek": "Tidak ada", "ket": "Wajib untuk semua diare"},
        {"nama": "Attapulgite", "dosis": "Dewasa 2 tablet awal, lalu 1 tiap BAB; Anak ½-1 tablet",
         "aturan": "Saat diare", "efek": "Konstipasi ringan", "ket": "Menyerap racun"},
        {"nama": "Loperamide", "dosis": "Awal 2mg, lanjut 1mg tiap BAB (maks 8mg/hari)",
         "aturan": "Hindari pada diare berdarah", "efek": "Sembelit", "ket": "Menghentikan pergerakan usus"},
    ],
    "Radang tenggorokan": [
        {"nama": "Lozenges", "dosis": "1 butir tiap 3-4 jam",
         "aturan": "Isap perlahan", "efek": "Kebas ringan", "ket": "Melembutkan tenggorokan"},
        {"nama": "Benzidamine / Dequalinium", "dosis": "3-4x/hari",
         "aturan": "Semprot / tablet isap", "efek": "Rasa panas ringan", "ket": "Antiseptik tenggorokan"},
    ],
    "Maag": [
        {"nama": "Antasida", "dosis": "1-2 tablet / 5-10ml sirup 3x/hari",
         "aturan": "Sebelum makan", "efek": "Diare/konstipasi", "ket": "Menetralisir asam"},
        {"nama": "Sukralfat", "dosis": "1g 3-4x/hari",
         "aturan": "Sebelum makan", "efek": "Konstipasi", "ket": "Melapisi lambung"},
        {"nama": "Ranitidine / Famotidine", "dosis": "Ranitidine 150mg 2x/hari; Famotidine 20mg 1-2x/hari",
         "aturan": "Sebelum tidur / sebelum makan", "efek": "Pusing", "ket": "Mengurangi produksi asam"},
    ],
    "Nyeri haid": [
        {"nama": "Paracetamol", "dosis": "500-1000mg/6-8 jam",
         "aturan": "Sesuai kebutuhan", "efek": "Aman", "ket": "Untuk nyeri ringan"},
        {"nama": "Ibuprofen", "dosis": "200-400mg/8 jam",
         "aturan": "Setelah makan", "efek": "Perih lambung", "ket": "Anti nyeri haid umum"},
        {"nama": "Asam mefenamat", "dosis": "500mg awal, 250mg/6 jam",
         "aturan": "Setelah makan", "efek": "Nyeri lambung", "ket": "Sering digunakan untuk haid"},
    ],
}

NON_MEDIS = {
    "Flu": ["Banyak minum air hangat", "Istirahat cukup", "Hirup uap air hangat (steam inhalation)", "Gunakan humidifier atau ruangan lembap", "Makan sup hangat / makanan bergizi"],
    "Demam": ["Kompres hangat di ketiak atau dahi", "Minum air lebih banyak", "Gunakan pakaian tipis dan nyaman", "Istirahat total", "Mandi air hangat (tidak terlalu panas)"],
    "Pusing": ["Minum air putih, hindari dehidrasi", "Istirahat di ruangan gelap dan tenang", "Kompres dingin di dahi / belakang leher", "Pijat ringan pelipis dan leher", "Hindari layar HP berlebihan"],
    "Batuk": ["Minum air hangat / madu + lemon", "Hirup uap air hangat", "Istirahat cukup", "Jaga ruangan tetap lembap", "Hindari rokok / asap"],
    "Mual": ["Minum air sedikit tapi sering", "Hindari gerakan tiba-tiba", "Jangan langsung baring setelah makan", "Makan makanan ringan (roti, biskuit, pisang)", "Hindari makanan berminyak, pedas, atau asam"],
    "Diare": ["Minum oralit / air putih lebih sering", "Konsumsi makanan rendah serat sementara (bubur, pisang, roti)", "Hindari susu, makanan pedas, minuman manis", "Cuci tangan sering untuk cegah infeksi", "Istirahat"],
    "Radang tenggorokan": ["Minum air hangat", "Kumur air garam hangat 3x sehari", "Hindari makanan goreng / pedas", "Minum madu + lemon", "Istirahat suara"],
    "Maag": ["Makan porsi kecil tapi sering", "Hindari makanan pemicu (pedas, asam, gorengan, kopi)", "Minum air hangat perlahan", "Kompres hangat di ulu hati", "Jangan langsung berbaring setelah makan (tunggu 2-3 jam)"],
    "Nyeri haid": ["Kompres hangat di perut bawah", "Lakukan peregangan ringan", "Minum air hangat dan hindari kafein", "Istirahat cukup dan kelola stress", "Konsumsi makanan pereda nyeri (jahe, cokelat hitam, pisang)"],
}

GEJALA_LIST = list(OBAT.keys())


# -------------------------
# Utility: load/save riwayat
# -------------------------
def load_riwayat():
    if not os.path.exists(RIWAYAT_FILE):
        return []
    try:
        with open(RIWAYAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_riwayat(all_entries):
    with open(RIWAYAT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)


def append_riwayat(entry):
    data = load_riwayat()
    data.append(entry)
    save_riwayat(data)


# -------------------------
# Helpers input & formatting
# -------------------------
def input_int(prompt, min_val=None, max_val=None):
    while True:
        s = input(prompt).strip()
        if not s.isdigit():
            print("Masukkan angka yang valid.")
            continue
        v = int(s)
        if min_val is not None and v < min_val:
            print(f"Nilai minimal {min_val}.")
            continue
        if max_val is not None and v > max_val:
            print(f"Nilai maksimal {max_val}.")
            continue
        return v


def confirm(prompt="Yakin? (y/n): "):
    while True:
        c = input(prompt).strip().lower()
        if c in ("y", "ya", "yes", "i", "iya"):
            return True
        if c in ("n", "tidak", "no"):
            return False
        print("Ketik 'y' atau 'n'.")


def wrap(text, width=70):
    return fill(text, width=width)


# -------------------------
# Tampilan hasil rekomendasi
# -------------------------
def tampilkan_rekomendasi(gejala, daftar_obat, alergi_obat=None, hamil=False):
    """
    Menampilkan obat yang sesuai, apply filter alergi dan kehamilan.
    Kembalikan list obat yang ditampilkan (nama saja).
    """
    displayed = []
    print(f" 💊 Rekomendasi Obat untuk: {gejala} 💊")
    print ()
    for obat in daftar_obat:
        nama_lower = obat["nama"].lower()
        if alergi_obat and alergi_obat in nama_lower:
            # skip because allergy
            continue
        if hamil and any(x in nama_lower for x in ["ibuprofen", "mefenamat", "asam mefenamat"]):
            # skip risky meds for pregnancy
            continue

        # tampilkan detail obat
        print(f" 💊 Obat: {obat['nama']}")
        print(f" 🧬 Dosis        : {obat['dosis']}")
        print(f" 📖 Aturan pakai : {obat['aturan']}")
        print(f" ⚠️ Efek samping : {obat['efek']}")
        print(f" 📌 Keterangan   : {obat['ket']}\n")
        displayed.append(obat["nama"])

    if not displayed:
        print("\n(Tidak ada obat yang dapat direkomendasikan karena filter alergi/kehamilan.)")

    return displayed


# -------------------------
# Fitur konsultasi
# -------------------------
def konsultasi():
    print("🔎  MULAI KONSULTASI")
    nama = input("Nama: ").strip() or "-"
    umur = input_int("Umur: ", min_val=0, max_val=150)

    # Pilihan gejala (angka)
    print("\nPilih gejala:")
    for idx, g in enumerate(GEJALA_LIST, start=1):
        print(f"{idx}. {g}")
    pilih = input_int("Masukkan nomor gejala (1-{}): ".format(len(GEJALA_LIST)), min_val=1, max_val=len(GEJALA_LIST))
    gejala = GEJALA_LIST[pilih - 1]

    hari = input_int("Sudah berapa hari mengalami gejala? (tulis angka): ", min_val=0)
    alergi_flag = False
    alergi_obat = None
    resp = input("Ada alergi obat? (iya/tidak): ").strip().lower()
    if resp in ("iya", "ya", "y", "i"):
        alergi_flag = True
        alergi_obat = input("Sebutkan nama obat yang alergi (contoh: Ibuprofen): ").strip().lower()

    hamil = input("Sedang hamil/menyusui? (iya/tidak): ").strip().lower() in ("iya", "ya", "y", "i")

    if hari >= 3:
       print("\n⚠ WARNING: Gejala sudah lebih dari 3 hari!")
       print()


    daftar = OBAT.get(gejala, [])
    rekomendasi_tampil = tampilkan_rekomendasi(gejala, daftar, alergi_obat=alergi_obat, hamil=hamil)

    # Tampilkan saran non-medis
    saran = NON_MEDIS.get(gejala, [])
    if saran:
        print()
        print("🩺 Saran Tindakan Non-Medis 🩺")
        for tip in saran:
            print(f"- {tip}")

    # Simpan riwayat lengkap (simpan rekomendasi yang ditampilkan, dan saran)
    entry = {
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "nama": nama,
        "umur": umur,
        "gejala": gejala,
        "rekomendasi": rekomendasi_tampil if rekomendasi_tampil else [daftar[0]["nama"] if daftar else "-"],
        "saran": saran
    }
    append_riwayat(entry)
    print()
    print(" 𐙚 Rekomendasi telah disimpan ke riwayat.")
    print()


# -------------------------
# Fitur Riwayat (tampil, hapus, cari, ekspor)
# -------------------------
def tampilkan_semua_riwayat():
    data = load_riwayat()
    if not data:
        print("\nBelum ada riwayat.\n")
        return
    print("\n==== DAFTAR RIWAYAT ====")
    for i, item in enumerate(data, start=1):
        print("\n-------------------------------")
        print(f"[{i}]🕰️  Waktu       : {item.get('waktu','-')}")
        print(f"   🪪  Nama        : {item.get('nama','-')}")
        print(f"   ✮  Umur        : {item.get('umur','-')}")
        print(f"   🦠 Gejala      : {item.get('gejala','-')}")
        rekoms = item.get("rekomendasi", [])
        # rekomendasi bisa list atau string
        if isinstance(rekoms, list):
            print("    Rekomendasi :")
            for r in rekoms:
                print(f"      - {r}")
        else:
            print(f"    Rekomendasi : {rekoms}")
        saran = item.get("saran", [])
        if saran:
            print("    Saran non-medis:")
            for s in saran:
                print(f"      - {wrap(s)}")
    print("\n-------------------------------\n")


def hapus_semua_riwayat():
    if not os.path.exists(RIWAYAT_FILE):
        print("\nTidak ada riwayat untuk dihapus.\n")
        return
    if confirm("Yakin ingin menghapus SEMUA riwayat? (y/n): "):
        try:
            os.remove(RIWAYAT_FILE)
            print("Semua riwayat berhasil dihapus.")
        except Exception as e:
            print("Gagal menghapus riwayat:", e)
    else:
        print("Batal menghapus riwayat.")


def hapus_entri_riwayat():
    data = load_riwayat()
    if not data:
        print("\nBelum ada riwayat.\n")
        return
    tampilkan_semua_riwayat()
    idx = input_int("Masukkan nomor entri yang ingin dihapus (0 = batal): ", min_val=0, max_val=len(data))
    if idx == 0:
        print("Batal.")
        return
    pilihan = idx - 1
    item = data[pilihan]
    print(f"Anda akan menghapus entri: {item.get('waktu')} | {item.get('nama')} | {item.get('gejala')}")
    if confirm("Konfirmasi hapus entri ini? (y/n): "):
        data.pop(pilihan)
        save_riwayat(data)
        print("Entri berhasil dihapus.")
    else:
        print("Batal hapus entri.")


def cari_riwayat_nama():
    data = load_riwayat()
    if not data:
        print("\nBelum ada riwayat.\n")
        return
    nama = input("Masukkan nama untuk mencari (case-insensitive): ").strip().lower()
    found = [item for item in data if nama in item.get("nama","").lower()]
    if not found:
        print("Tidak ditemukan riwayat dengan nama tersebut.")
        return
    print(f"\nDitemukan {len(found)} entri:")
    for i, item in enumerate(found, start=1):
        print("\n------------------")
        print(f"{i}. {item.get('waktu')} | {item.get('nama')} | {item.get('gejala')}")
        rekoms = item.get("rekomendasi", [])
        if isinstance(rekoms, list):
            print("   Rekomendasi:")
            for r in rekoms:
                print(f"    - {r}")
        else:
            print(f"   Rekomendasi: {rekoms}")
        print("   Saran non-medis:")
        for s in item.get("saran", []):
            print(f"    - {wrap(s)}")
    print()


def ekspor_riwayat():
    data = load_riwayat()
    if not data:
        print("\nTidak ada riwayat untuk diekspor.\n")
        return
    print("\nPilih format ekspor:")
    print("1. JSON")
    print("2. CSV")
    pilih = input_int("Pilih (1-2): ", min_val=1, max_val=2)
    if pilih == 1:
        filename = input("Nama file JSON (default 'riwayat_export.json'): ").strip() or "riwayat_export.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Riwayat diekspor ke {filename}")
        except Exception as e:
            print("Gagal eksport JSON:", e)
    else:
        filename = input("Nama file CSV (default 'riwayat_export.csv'): ").strip() or "riwayat_export.csv"
        try:
            with open(filename, "w", newline='', encoding="utf-8") as csvfile:
                fieldnames = ["waktu", "nama", "umur", "gejala", "rekomendasi", "saran"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in data:
                    # convert list fields to pipe-separated strings
                    rekom = item.get("rekomendasi")
                    if isinstance(rekom, list):
                        rekom_val = " | ".join(rekom)
                    else:
                        rekom_val = str(rekom)
                    saran_val = " | ".join(item.get("saran", []))
                    writer.writerow({
                        "waktu": item.get("waktu", ""),
                        "nama": item.get("nama", ""),
                        "umur": item.get("umur", ""),
                        "gejala": item.get("gejala", ""),
                        "rekomendasi": rekom_val,
                        "saran": saran_val
                    })
            print(f"Riwayat diekspor ke {filename}")
        except Exception as e:
            print("Gagal eksport CSV:", e)


def menu_riwayat():
    while True:
        print("\n ☘︎ MENU RIWAYAT ☘︎")
        print("1. Tampilkan semua riwayat")
        print("2. Hapus semua riwayat")
        print("3. Hapus entri riwayat tertentu")
        print("4. Cari riwayat berdasarkan nama")
        print("5. Ekspor riwayat (JSON/CSV)")
        print("6. Kembali")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1":
            tampilkan_semua_riwayat()
        elif pilihan == "2":
            hapus_semua_riwayat()
        elif pilihan == "3":
            hapus_entri_riwayat()
        elif pilihan == "4":
            cari_riwayat_nama()
        elif pilihan == "5":
            ekspor_riwayat()
        elif pilihan == "6":
            return
        else:
            print("Pilihan tidak valid.")


# -------------------------
# MAIN MENU
# -------------------------
def main_menu():
    print("            ✿  T E M A N   O B A T   K U  ✿             ")
    print("---------------------------------------------------------")
    print("       Temani kamu jadi lebih sehat setiap hari 💚      ")
    print("---------------------------------------------------------")
    while True:
        print(" 𝜗ৎ MENU UTAMA 𝜗ৎ ")
        print("1. Konsultasi")
        print("2. Riwayat")
        print("3. Keluar")
        choice = input("Pilih menu: ").strip()
        if choice == "1":
            konsultasi()
        elif choice == "2":
            menu_riwayat()
        elif choice == "3":
            print("Terima kasih telah menggunakan TemanObatKu. Jaga kesehatan! 𖹭 ")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main_menu()