# 📐 Spesifikasi Desain Sistem Anotasi Relevansi RAG

Dokumen ini mendefinisikan arsitektur sistem, antarmuka pengguna, dan alur data untuk Sistem Evaluasi Relevansi Dokumen. Sistem ini dirancang untuk memfasilitasi penilaian metrik _Retrieval-Augmented Generation_ (RAG) secara terdistribusi dan _real-time_.

---

## 1. Arsitektur Sistem

Sistem beroperasi menggunakan arsitektur _client-server_ sederhana dengan fokus pada konkurensi data tingkat tinggi.

- **Frontend / Client:** Streamlit (Python)
  - Menangani perutean peran (_role-based routing_), pengelolaan status (_session state_), dan rendering form dinamis.
- **Database / Backend:** Supabase (PostgreSQL)
  - Menyediakan persistensi data tersentralisasi, menghilangkan risiko _race conditions_, dan mendukung struktur data dinamis menggunakan tipe `JSONB`.

---

## 2. Struktur Antarmuka Pengguna (UI)

Hierarki visual dibagi berdasarkan peran otentikasi. Tidak ada navigasi kompleks; pendekatan difokuskan pada penyelesaian tugas (_task-driven_).

### 2.1. Halaman Login (Global)

- **Komponen:** Header teks, Input _Password_ (disamarkan), Tombol Submit.
- **Logika:** Pengecekan _hardcoded credentials_ (MHS1, MHS2, DSN3, ADMIN) yang menginisialisasi parameter sesi `role` dan `score_key`.

### 2.2. Dasbor Admin

Fokus pada kuantifikasi data _real-time_ tanpa kemampuan mengubah nilai evaluasi.

| Elemen UI        | Jenis Komponen | Fungsi Utama                                                         |
| :--------------- | :------------- | :------------------------------------------------------------------- |
| **Metrik Utama** | `st.metric`    | Menampilkan rasio penyelesaian tiap evaluator (misal: 45 / 100).     |
| **Tabel Data**   | `st.dataframe` | Visualisasi tabular dari seluruh data JSONB yang telah di-_flatten_. |
| **Kontrol**      | `st.button`    | Fungsi keluar (Logout) dan pembersihan _session state_.              |

### 2.3. Halaman Evaluator

Antarmuka dibagi menjadi panel navigasi lateral dan area kerja utama.

- **Sidebar (Panel Kendali):**
  - Identitas _Role_ yang sedang aktif.
  - `st.selectbox`: Pemilihan fokus evaluasi berdasarkan `Query_ID`.
  - `st.progress`: Indikator penyelesaian spesifik pada query yang dipilih.
- **Main Container (Area Evaluasi):**
  - Pemaparan kueri target.
  - `st.form`: Membungkus seluruh dokumen terkait agar pengiriman data ke server (_submit_) dilakukan secara kolektif per kueri (mengurangi beban API _call_).
  - `st.radio`: Input biner mutlak (`Relevan` = 1, `Tidak Relevan` = 0, `Belum Dinilai` = Null).

---

## 3. Skema Basis Data dan Alur Transaksi

Pemilihan `JSONB` krusial untuk mencegah duplikasi baris dan menyederhanakan _query_ rekapitulasi.

### Entitas: `evaluasi_query`

| Nama Kolom       | Tipe Data PostgreSQL | Keterangan Atribut                             |
| :--------------- | :------------------- | :--------------------------------------------- |
| `id`             | `BIGINT`             | Primary Key, Auto-increment.                   |
| `query_id`       | `TEXT`               | ID kluster (Indexed).                          |
| `query_text`     | `TEXT`               | Teks kueri asli untuk pengujian RAG.           |
| `rank`           | `INT4`               | Urutan pemunculan dokumen.                     |
| `metode`         | `TEXT`               | Algoritma yang digunakan (Standar / HyDE).     |
| `judul_skripsi`  | `TEXT`               | Judul dokumen.                                 |
| `abstrak_murni`  | `TEXT`               | Isi dokumen yang dievaluasi.                   |
| `skor_relevansi` | `JSONB`              | Objek bersarang penyimpan keputusan evaluator. |

### 3.1. Struktur Payload JSONB

Desain data _payload_ distandarisasi untuk mendukung fleksibilitas tanpa mengubah skema utama jika ada penambahan evaluator di kemudian hari.

```json
{
  "mhs1": 1,
  "mhs2": 0,
  "dsn3": null
}
```
