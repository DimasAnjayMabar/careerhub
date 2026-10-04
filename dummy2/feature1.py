import streamlit as st
import pandas as pd
import service

def render():
    st.header("🗺️ Peta Kompetensi Dunia Kerja")
    st.caption("Agregasi kompetensi yang benar-benar dibutuhkan alumni di bidang pekerjaannya.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Hard Skills per Bidang",
        "Soft Skills per Bidang",
        "Sertifikasi Paling Bermanfaat",
        "Matriks Prodi × Bidang",
    ])

    with tab1:
        data = service.top_hard_skills_per_bidang(top_n=5)
        bidang_pilihan = st.selectbox("Pilih Bidang Pekerjaan", list(data.keys()), key="f1_hard")
        df = pd.DataFrame(data[bidang_pilihan])
        if not df.empty:
            st.bar_chart(df.set_index("skill"))
            st.dataframe(df, use_container_width=True)

    with tab2:
        data = service.top_soft_skills_per_bidang(top_n=5)
        bidang_pilihan = st.selectbox("Pilih Bidang Pekerjaan", list(data.keys()), key="f1_soft")
        df = pd.DataFrame(data[bidang_pilihan])
        if not df.empty:
            st.bar_chart(df.set_index("skill"))
            st.dataframe(df, use_container_width=True)

    with tab3:
        data = service.sertifikasi_per_bidang(top_n=3)
        bidang_pilihan = st.selectbox("Pilih Bidang Pekerjaan", list(data.keys()), key="f1_sert")
        df = pd.DataFrame(data[bidang_pilihan])
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Belum ada data sertifikasi untuk bidang ini.")

    with tab4:
        matrix = service.matriks_prodi_bidang()
        df = pd.DataFrame(matrix).fillna(0).astype(int)
        st.dataframe(df, use_container_width=True)
        st.caption("Angka = jumlah alumni dari Prodi (baris) yang bekerja di Bidang (kolom).")