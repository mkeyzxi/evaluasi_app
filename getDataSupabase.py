import json
import os
from dotenv import load_dotenv  # 1. TAMBAHKAN INI
from supabase import create_client, Client

# 2. TAMBAHKAN INI untuk membaca file .env Anda
load_dotenv()

# Kredensial Supabase Anda diambil dari file .env
SUPABASE_URL = os.getenv("SUPABASE_URL")  
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
NAMA_TABEL = "evaluasi"

# 3. Validasi untuk memastikan file .env berhasil terbaca
if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: Gagal membaca SUPABASE_URL atau SUPABASE_KEY dari file .env!")
    print("Pastikan file '.env' ada di folder proyek dan berisi variabel tersebut.")
    exit()

# Inisialisasi klien Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def export_all_supabase_data(table_name: str, output_file: str):
    all_rows = []
    start = 0
    batch_size = 1000  # Mengambil data per 1000 baris agar aman dari limit API
    
    print("Mulai mengunduh data dari Supabase...")
    
    while True:
        try:
            # Ambil data berdasarkan rentang baris (range)
            response = supabase.table(table_name)\
                .select("*")\
                .range(start, start + batch_size - 1)\
                .execute()
                
            data = response.data
            
            if not data:
                break  # Berhenti jika sudah tidak ada data lagi yang tersisa
                
            all_rows.extend(data)
            print(f"Berhasil mengunduh {len(all_rows)} baris...")
            
            start += batch_size
        except Exception as e:
            print(f"❌ Terjadi kesalahan saat mengambil data: {e}")
            break

    if all_rows:
        # Simpan seluruh data ke dalam file JSON lokal
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_rows, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Selesai! Total {len(all_rows)} baris berhasil disimpan ke '{output_file}'")
    else:
        print("⚠ Tidak ada data yang berhasil diunduh.")

# Jalankan fungsi export
export_all_supabase_data(NAMA_TABEL, 'data_supabase.json')
