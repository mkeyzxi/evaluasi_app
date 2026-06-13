import streamlit as st
import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

# ─── Konfigurasi ──────────────────────────────────────────────
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Variabel SUPABASE_URL dan SUPABASE_KEY belum diset. Periksa file .env Anda.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ─── Fungsi Data (Supabase) ──────────────────────────────────
def load_data():
    """Mengambil seluruh data dari tabel 'evaluasi' di Supabase."""
    try:
        response = supabase.table("evaluasi").select("*").order("query_id").order("metode").order("rank").execute()
        data = response.data
        # Pastikan setiap baris punya skor_relevansi yang valid
        for item in data:
            if item.get("skor_relevansi") is None:
                item["skor_relevansi"] = {"mhs1": None, "mhs2": None, "dsn3": None}
        return data
    except Exception as e:
        st.error(f"Gagal mengambil data dari Supabase: {e}")
        return []


def update_skor(row_id, score_key, value):
    """
    Update skor relevansi untuk satu baris tertentu di Supabase.
    Menggunakan JSONB patch agar hanya key yang bersangkutan yang diperbarui,
    tanpa menimpa key evaluator lain.

    Args:
        row_id: ID baris di tabel evaluasi
        score_key: key di dalam JSONB (mhs1, mhs2, atau dsn3)
        value: nilai skor (1, 0, atau None)
    """
    try:
        # Ambil skor_relevansi yang ada saat ini
        current = supabase.table("evaluasi").select("skor_relevansi").eq("id", row_id).execute()
        if current.data:
            skor = current.data[0].get("skor_relevansi") or {}
        else:
            skor = {}

        # Update hanya key milik evaluator ini
        skor[score_key] = value

        # Simpan kembali
        supabase.table("evaluasi").update({"skor_relevansi": skor}).eq("id", row_id).execute()
    except Exception as e:
        st.error(f"Gagal menyimpan skor: {e}")


# ─── Halaman Login ────────────────────────────────────────────
def login():
    st.markdown("<h2 style='text-align: center;'>Sistem Evaluasi Relevansi Dokumen</h2>", unsafe_allow_html=True)
    st.write("Masukkan kode akses Anda. Penilaian Anda merepresentasikan integritas riset ini.")

    # 4 Kode Akses: MHS1, MHS2, DSN3, ADMIN
    code = st.text_input("Kode Akses", type="password")

    if st.button("Masuk", use_container_width=True):
        if code == "MHS1":
            st.session_state['role'] = 'Mahasiswa 1'
            st.session_state['score_key'] = 'mhs1'
            st.rerun()
        elif code == "MHS2":
            st.session_state['role'] = 'Mahasiswa 2'
            st.session_state['score_key'] = 'mhs2'
            st.rerun()
        elif code == "DSN3":
            st.session_state['role'] = 'Dosen / Mahasiswa 3'
            st.session_state['score_key'] = 'dsn3'
            st.rerun()
        elif code == "ADMIN":
            st.session_state['role'] = 'Admin'
            st.rerun()
        else:
            st.error("Kode akses salah. Periksa kembali.")


# ─── Halaman Admin ────────────────────────────────────────────
def admin_page(data):
    st.title("Dashboard Admin")
    st.write("Pantau kuantitas evaluasi dari masing-masing penilai secara real-time.")

    if st.button("Keluar (Logout)"):
        st.session_state.clear()
        st.rerun()

    total_docs = len(data)
    mhs1_done = sum(1 for d in data if d.get("skor_relevansi", {}).get("mhs1") is not None)
    mhs2_done = sum(1 for d in data if d.get("skor_relevansi", {}).get("mhs2") is not None)
    dsn3_done = sum(1 for d in data if d.get("skor_relevansi", {}).get("dsn3") is not None)

    st.subheader("Statistik Penilaian")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="MHS 1 Selesai", value=f"{mhs1_done} / {total_docs}")
    col2.metric(label="MHS 2 Selesai", value=f"{mhs2_done} / {total_docs}")
    col3.metric(label="DSN 3 Selesai", value=f"{dsn3_done} / {total_docs}")

    st.subheader("Tabel Keseluruhan Data")

    # Flatten JSONB skor_relevansi menjadi kolom terpisah untuk tampilan
    df = pd.DataFrame(data)
    if not df.empty:
        skor_df = pd.json_normalize(df['skor_relevansi'])
        skor_df.columns = [f"skor_{col}" for col in skor_df.columns]
        df = pd.concat([df.drop(columns=['skor_relevansi']), skor_df], axis=1)
        display_cols = ['query_id', 'query_text', 'rank', 'metode', 'skor_mhs1', 'skor_mhs2', 'skor_dsn3']
        available_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[available_cols], use_container_width=True)
    else:
        st.info("Belum ada data di tabel evaluasi.")


# ─── Halaman Evaluator ───────────────────────────────────────
def evaluator_page(data):
    role = st.session_state['role']
    score_key = st.session_state['score_key']

    st.sidebar.title(f"Penilai: {role}")
    if st.sidebar.button("Keluar (Logout)"):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")

    # Ekstraksi dan pengurutan Query ID
    queries = list(dict.fromkeys([d['query_id'] for d in data]))
    queries.sort()

    selected_query = st.sidebar.selectbox("Fokus Evaluasi (Pilih Query):", queries)

    docs_to_evaluate = [d for d in data if d['query_id'] == selected_query]
    query_text = docs_to_evaluate[0]['query_text'] if docs_to_evaluate else ""

    # Kalkulasi progress per query
    query_done = sum(
        1 for d in docs_to_evaluate
        if d.get("skor_relevansi", {}).get(score_key) is not None
    )
    st.sidebar.progress(query_done / len(docs_to_evaluate) if docs_to_evaluate else 0)
    st.sidebar.write(f"Progress Query {selected_query}: {query_done} / {len(docs_to_evaluate)} dokumen")

    st.title("Evaluasi Relevansi Dokumen")
    st.info(f"**Query Anda:** {query_text}")
    st.warning("Penilaian dilakukan dokumen per dokumen. Telaah kecocokan Abstrak dengan Query.")

    # Form input
    with st.form(key=f"form_{selected_query}"):
        for i, doc in enumerate(docs_to_evaluate):
            with st.container():
                st.markdown(f"### Peringkat {doc['rank']} | Metode: {doc['metode']}")
                st.markdown(f"**Judul:** {doc['judul_skripsi']}")
                st.markdown(f"**Abstrak:** {doc['abstrak_murni']}")

                # Pemetaan status skor yang ada (dari JSONB)
                current_score = doc.get("skor_relevansi", {}).get(score_key)
                if current_score == 1:
                    index = 1
                elif current_score == 0:
                    index = 2
                else:
                    index = 0

                st.radio(
                    "Apakah dokumen ini menjawab kebutuhan query secara relevan?",
                    ["Belum Dinilai", "Relevan", "Tidak Relevan"],
                    index=index,
                    key=f"radio_{selected_query}_{i}",
                    horizontal=True
                )
                st.markdown("---")

        submit_button = st.form_submit_button(label="Simpan Keputusan Relevansi", use_container_width=True)

    if submit_button:
        saved_count = 0
        for i, doc in enumerate(docs_to_evaluate):
            choice = st.session_state[f"radio_{selected_query}_{i}"]
            if choice == "Relevan":
                value = 1
            elif choice == "Tidak Relevan":
                value = 0
            else:
                value = None

            # Update ke Supabase per baris
            update_skor(doc['id'], score_key, value)
            saved_count += 1

        st.success(f"Penilaian untuk {selected_query} berhasil disimpan ke Supabase ({saved_count} dokumen).")
        st.rerun()


# ─── Main ─────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Sistem Anotasi Relevansi",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    data = load_data()
    if not data:
        st.warning("Tidak ada data di tabel evaluasi. Jalankan `python migrate.py` terlebih dahulu.")
        return

    # Routing berdasarkan login
    if 'role' not in st.session_state:
        login()
    else:
        if st.session_state['role'] == 'Admin':
            admin_page(data)
        else:
            evaluator_page(data)


if __name__ == "__main__":
    main()