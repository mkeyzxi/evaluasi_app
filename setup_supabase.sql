-- ============================================================
-- SQL untuk membuat tabel 'evaluasi' di Supabase SQL Editor
-- Jalankan query ini di: Supabase Dashboard > SQL Editor
-- ============================================================

-- 1. Buat tabel evaluasi
CREATE TABLE IF NOT EXISTS evaluasi (
    id              BIGSERIAL PRIMARY KEY,
    query_id        TEXT NOT NULL,
    query_text      TEXT,
    metode          TEXT,
    rank            INTEGER,
    file_source     TEXT,
    judul_skripsi   TEXT,
    abstrak_murni   TEXT,
    skor_relevansi  JSONB DEFAULT '{"mhs1": null, "mhs2": null, "dsn3": null}'::jsonb
);

-- 2. Buat indeks untuk mempercepat query berdasarkan query_id
CREATE INDEX IF NOT EXISTS idx_evaluasi_query_id ON evaluasi (query_id);

-- 3. (Opsional) Nonaktifkan Row Level Security agar semua client bisa CRUD
--    Jika Anda ingin RLS, silakan konfigurasi policy sendiri.
ALTER TABLE evaluasi DISABLE ROW LEVEL SECURITY;
