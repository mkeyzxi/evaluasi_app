# migrate.py
# Skrip migrasi: mengisi tabel 'evaluasi' di Supabase dari file evaluasi_model.json
# AMAN dijalankan berulang kali — data lama akan dihapus terlebih dahulu.

import json
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL dan SUPABASE_KEY harus diisi di file .env")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

with open("evaluasi_model.json", encoding="utf-8") as f:
    data = json.load(f)

# ─── Langkah 1: Hapus seluruh data lama agar tidak duplikat ───
print("Menghapus data lama di tabel 'evaluasi'...")
try:
    # Supabase memerlukan filter untuk delete; gunakan id > 0 untuk match semua baris
    supabase.table("evaluasi").delete().gt("id", 0).execute()
    print("  Data lama berhasil dihapus.")
except Exception as e:
    print(f"  WARNING: Gagal menghapus data lama: {e}")
    print("  Melanjutkan proses insert...")

# ─── Langkah 2: Konversi data dari format JSON ke format tabel Supabase ───
rows = []
for item in data:
    # Ambil skor relevansi yang sudah ada (jika sudah dalam format JSONB baru)
    existing_skor = item.get("Skor_Relevansi")

    if isinstance(existing_skor, dict):
        # Sudah format JSONB baru: {"mhs1": ..., "mhs2": ..., "dsn3": ...}
        skor = existing_skor
    else:
        # Format lama: kolom terpisah Skor_Relevansi, Skor_Relevansi_2, Skor_Relevansi_3
        skor = {
            "mhs1": item.get("Skor_Relevansi"),
            "mhs2": item.get("Skor_Relevansi_2"),
            "dsn3": item.get("Skor_Relevansi_3")
        }

    rows.append({
        "query_id":       item["Query_ID"],
        "query_text":     item["Query_Text"],
        "metode":         item["Metode"],
        "rank":           item["Rank"],
        "file_source":    item.get("File_Source", ""),
        "judul_skripsi":  item.get("Judul_Skripsi", ""),
        "abstrak_murni":  item.get("Abstrak_Murni", ""),
        "skor_relevansi": skor
    })

# ─── Langkah 3: Validasi — pastikan tidak ada duplikat di sumber JSON ───
seen_keys = set()
duplicates = 0
for r in rows:
    key = (r["query_id"], r["metode"], r["rank"])
    if key in seen_keys:
        duplicates += 1
        print(f"  WARNING: Duplikat ditemukan di JSON: {key}")
    seen_keys.add(key)

if duplicates > 0:
    print(f"\n  Ditemukan {duplicates} duplikat di file JSON. Periksa evaluasi_model.json!")
else:
    print(f"\n  Validasi OK: {len(rows)} baris unik dari JSON.")

# ─── Langkah 4: Insert dalam batch ───
BATCH_SIZE = 500
total_inserted = 0

for i in range(0, len(rows), BATCH_SIZE):
    batch = rows[i:i + BATCH_SIZE]
    try:
        supabase.table("evaluasi").insert(batch).execute()
        total_inserted += len(batch)
        print(f"  Batch {i // BATCH_SIZE + 1}: {len(batch)} baris berhasil dimasukkan.")
    except Exception as e:
        print(f"  ERROR pada batch {i // BATCH_SIZE + 1}: {e}")

print(f"\nSelesai! Total {total_inserted} dari {len(rows)} baris berhasil dimasukkan ke tabel 'evaluasi'.")

# --- Langkah 5: Verifikasi data di Supabase ---
print("\n--- Verifikasi Data ---")
try:
    result = supabase.table("evaluasi").select("query_id", count="exact").execute()
    total_in_db = result.count if result.count is not None else len(result.data)
    print(f"  Total baris di tabel Supabase: {total_in_db}")

    # Hitung jumlah query unik
    unique_queries = set(r["query_id"] for r in result.data)
    print(f"  Jumlah query unik: {len(unique_queries)}")

    if total_in_db != len(rows):
        print(f"  WARNING: Jumlah baris tidak cocok! JSON={len(rows)}, DB={total_in_db}")
    else:
        print(f"  OK: Jumlah baris cocok ({total_in_db}).")
except Exception as e:
    print(f"  Gagal memverifikasi: {e}")
