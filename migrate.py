# migrate.py
# Skrip migrasi: mengisi tabel 'evaluasi' di Supabase dari file evaluasi_model.json
# Jalankan sekali saja setelah tabel dibuat di Supabase.

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

# Konversi data dari format JSON lama ke format tabel Supabase
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

# Insert dalam batch (Supabase mendukung bulk insert)
# Bagi ke batch 500 baris agar tidak melebihi payload limit
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
