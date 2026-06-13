cd "C:\belajarku\semester 7\evaluasi_app"

evaluasi_env\Scripts\activate

streamlit run app.py

# Sistem Anotasi Relevansi Dokumen Skripsi

Aplikasi web berbasis **Streamlit** untuk mengevaluasi relevansi dokumen hasil retrieval dari sistem RAG (Retrieval-Augmented Generation) yang digunakan dalam penelitian skripsi. Sistem ini mendukung penilaian multi-penilai (inter-annotator) dengan penyimpanan data terpusat di **Supabase**.

---

## Daftar Isi

- [Gambaran Umum](#gambaran-umum)
- [Fitur Utama](#fitur-utama)
- [Struktur Proyek](#struktur-proyek)
- [Prasyarat](#prasyarat)
- [Instalasi](#instalasi)
- [Konfigurasi Supabase](#konfigurasi-supabase)
- [Struktur Data](#struktur-data)
- [Cara Menjalankan](#cara-menjalankan)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Peran Pengguna](#peran-pengguna)
- [Alur Evaluasi](#alur-evaluasi)
- [Metrik yang Dievaluasi](#metrik-yang-dievaluasi)
- [Troubleshooting](#troubleshooting)

---

## Gambaran Umum

Sistem ini dibangun untuk mendukung proses evaluasi kualitatif dalam penelitian skripsi yang membandingkan performa metode **Standard RAG** vs metode lain dalam me-retrieve dokumen skripsi yang relevan berdasarkan query pengguna.

Setiap dokumen yang di-retrieve dinilai relevansinya oleh **tiga penilai independen** (dua mahasiswa dan satu dosen/mahasiswa ketiga) menggunakan skala biner:

- **Relevan (1)** — Dokumen menjawab kebutuhan query
- **Tidak Relevan (0)** — Dokumen tidak menjawab kebutuhan query

Hasil penilaian disimpan di Supabase sehingga dapat diakses dan diperbarui secara real-time oleh semua penilai tanpa konflik data.

---

## Fitur Utama

- Login berbasis kode akses dengan empat peran berbeda
- Antarmuka evaluasi per-query dengan tampilan judul dan abstrak skripsi
- Indikator progress per query dan per penilai
- Dashboard admin untuk memantau kemajuan penilaian secara keseluruhan
- Penyimpanan data ke Supabase (bukan file JSON statis) sehingga perubahan tersimpan secara persisten
- Struktur `Skor_Relevansi` per penilai (`mhs1`, `mhs2`, `dsn3`) dalam satu objek JSON

---

## Struktur Proyek

```
.
├── app.py                  # Aplikasi Streamlit utama
├── evaluasi_model.json     # Data awal (seed) untuk migrasi ke Supabase
├── requirements.txt        # Dependensi Python
├── .env                    # Variabel lingkungan (tidak di-commit)
├── .env.example            # Contoh variabel lingkungan
└── README.md
```

---

## Prasyarat

- Python 3.9 atau lebih baru
- Akun [Supabase](https://supabase.com) (gratis)
- pip

---

## Instalasi

**1. Clone repositori**

```bash
git clone https://github.com/username/nama-repo.git
cd nama-repo
```

**2. Buat virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

**3. Install dependensi**

```bash
pip install -r requirements.txt
```

Isi `requirements.txt`:

```
streamlit
supabase
pandas
python-dotenv
```

**4. Buat file `.env`**

Salin dari contoh lalu isi dengan kredensial Supabase Anda:

```bash
cp .env.example .env
```

---

## Konfigurasi Supabase

### Langkah 1 — Buat project di Supabase

Masuk ke [supabase.com](https://supabase.com), buat project baru, lalu catat:

- **Project URL** → `https://xxxx.supabase.co`
- **anon/public key** → tersedia di _Settings > API_

### Langkah 2 — Buat tabel `evaluasi`

Jalankan SQL berikut di **Supabase SQL Editor**:

```sql
CREATE TABLE evaluasi (
    id          BIGSERIAL PRIMARY KEY,
    query_id    TEXT NOT NULL,
    query_text  TEXT,
    metode      TEXT,
    rank        INTEGER,
    file_source TEXT,
    judul_skripsi TEXT,
    abstrak_murni TEXT,
    skor_relevansi JSONB DEFAULT '{"mhs1": null, "mhs2": null, "dsn3": null}'::jsonb
);
```

### Langkah 3 — Import data awal

Gunakan skrip migrasi berikut untuk mengisi tabel dari `evaluasi_model.json`:

```python
# migrate.py
import json
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

with open("evaluasi_model.json", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for item in data:
    rows.append({
        "query_id":      item["Query_ID"],
        "query_text":    item["Query_Text"],
        "metode":        item["Metode"],
        "rank":          item["Rank"],
        "file_source":   item["File_Source"],
        "judul_skripsi": item["Judul_Skripsi"],
        "abstrak_murni": item["Abstrak_Murni"],
        "skor_relevansi": {"mhs1": None, "mhs2": None, "dsn3": None}
    })

supabase.table("evaluasi").insert(rows).execute()
print(f"Berhasil memasukkan {len(rows)} baris.")
```

Jalankan sekali:

```bash
python migrate.py
```

### Langkah 4 — Isi file `.env`

```env
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=eyJxxxxxxxxxxxx
```

---

## Struktur Data

Setiap baris di tabel `evaluasi` memiliki kolom `skor_relevansi` bertipe JSONB dengan struktur:

```json
{
  "mhs1": null,
  "mhs2": 1,
  "dsn3": 0
}
```

| Nilai  | Arti          |
| ------ | ------------- |
| `null` | Belum dinilai |
| `1`    | Relevan       |
| `0`    | Tidak Relevan |

Dengan struktur ini, penilaian setiap penilai tersimpan secara terpisah dalam satu kolom dan dapat diperbarui secara independen tanpa menimpa data penilai lain.

---

## Cara Menjalankan

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`.

---

## Panduan Penggunaan

### Login

Masukkan kode akses sesuai peran Anda:

| Kode Akses | Peran               |
| ---------- | ------------------- |
| `MHS1`     | Mahasiswa 1         |
| `MHS2`     | Mahasiswa 2         |
| `DSN3`     | Dosen / Mahasiswa 3 |
| `ADMIN`    | Administrator       |

> **Penting:** Jaga kerahasiaan kode akses Anda. Penilaian yang diberikan merepresentasikan integritas riset.

### Menilai Dokumen (Penilai)

1. Setelah login, pilih **Query** yang ingin dievaluasi dari sidebar kiri.
2. Baca teks query yang tampil di bagian atas halaman.
3. Untuk setiap dokumen, baca **Judul** dan **Abstrak** secara seksama.
4. Pilih salah satu:
   - **Relevan** — Abstrak menjawab atau berkaitan langsung dengan query
   - **Tidak Relevan** — Abstrak tidak menjawab kebutuhan query
   - **Belum Dinilai** — Lewati (penilaian tidak tersimpan)
5. Klik **Simpan Keputusan Relevansi** untuk menyimpan ke Supabase.
6. Progress penilaian per query ditampilkan di sidebar.

### Memantau Progress (Admin)

Dashboard admin menampilkan:

- Jumlah dokumen yang sudah dinilai oleh masing-masing penilai
- Tabel keseluruhan data beserta status penilaian tiap penilai

---

## Peran Pengguna

```
┌──────────┬─────────────────────────────────────────────────────┐
│ Peran    │ Akses                                               │
├──────────┼─────────────────────────────────────────────────────┤
│ MHS1     │ Menilai dokumen, melihat progress sendiri           │
│ MHS2     │ Menilai dokumen, melihat progress sendiri           │
│ DSN3     │ Menilai dokumen, melihat progress sendiri           │
│ ADMIN    │ Melihat semua data & statistik, tidak bisa menilai  │
└──────────┴─────────────────────────────────────────────────────┘
```

Setiap penilai hanya dapat mengubah skor miliknya sendiri. Skor penilai lain tidak terpengaruh.

---

## Alur Evaluasi

```
Penilai Login
     │
     ▼
Pilih Query di Sidebar
     │
     ▼
Baca Query + Dokumen (Judul & Abstrak)
     │
     ▼
Pilih: Relevan / Tidak Relevan / Belum Dinilai
     │
     ▼
Klik Simpan → Data tersimpan ke Supabase
     │
     ▼
(Opsional) Pindah ke Query berikutnya
```

---

## Metrik yang Dievaluasi

Hasil anotasi dari sistem ini digunakan untuk menghitung metrik evaluasi IR (Information Retrieval), antara lain:

- **Precision@K** — Proporsi dokumen relevan dalam K hasil teratas
- **Recall@K** — Proporsi dokumen relevan yang berhasil ditemukan
- **Mean Average Precision (MAP)** — Rata-rata presisi di semua query
- **Normalized Discounted Cumulative Gain (nDCG)** — Mengukur kualitas perankingan

Inter-annotator agreement (misalnya Cohen's Kappa) juga dihitung dari tiga set penilaian untuk mengukur konsistensi antar penilai.

---

## Troubleshooting

**Data tidak tersimpan setelah klik Simpan**

- Pastikan variabel `SUPABASE_URL` dan `SUPABASE_KEY` di `.env` sudah benar.
- Cek apakah tabel `evaluasi` sudah dibuat di Supabase.
- Pastikan Row Level Security (RLS) di Supabase dinonaktifkan atau sudah dikonfigurasi dengan benar untuk tabel ini.

**Error `SUPABASE_URL not found`**

- Pastikan file `.env` ada di direktori yang sama dengan `app.py`.
- Pastikan `python-dotenv` sudah terinstall dan `load_dotenv()` dipanggil di awal `app.py`.

**Tabel kosong di Dashboard Admin**

- Jalankan `migrate.py` terlebih dahulu untuk mengisi data awal dari `evaluasi_model.json`.

**Kode akses tidak dikenali**

- Kode akses bersifat case-sensitive. Pastikan huruf besar/kecil sesuai (contoh: `MHS1`, bukan `mhs1`).

---

## Lisensi

Proyek ini dibuat untuk keperluan penelitian skripsi dan bersifat akademis. Tidak untuk distribusi komersial.

---

_Dikembangkan sebagai bagian dari penelitian evaluasi sistem RAG untuk pencarian dokumen skripsi._

📋 Langkah Selanjutnya untuk Anda
Buat project di supabase.com → catat URL & anon key
Paste & jalankan isi setup_supabase.sql di Supabase SQL Editor
Edit file .env — isi SUPABASE_URL dan SUPABASE_KEY dengan kredensial Anda
Jalankan migrasi:
bash
evaluasi_env\Scripts\activate
python migrate.py
Jalankan aplikasi:
bash
streamlit run app.py
# evaluasi_app
