import streamlit as st
import pandas as pd
import service

def render():
    st.header("📊 Dashboard Tracer Study")
    st.caption("Gunakan filter di bawah untuk mengeksplorasi segmen data tertentu.")

    # ---------- FILTER GLOBAL (di atas biar langsung kelihatan efeknya) ----------
    with st.container(border=True):
        st.subheader("🔎 Filter Global")
        col1, col2 = st.columns(2)

        with col1:
            angkatan_opsi = ["Semua"] + [str(a) for a in service.get_all_angkatan()]
            angkatan_pilihan = st.selectbox("Angkatan", angkatan_opsi, key="f3_angkatan")

        with col2:
            bidang_opsi = ["Semua"] + [b["nama_bidang"] for b in service.get_all_bidang()]
            bidang_pilihan = st.selectbox("Bidang Pekerjaan", bidang_opsi, key="f3_bidang")

    # Konversi ke parameter query
    angkatan_param = None if angkatan_pilihan == "Semua" else int(angkatan_pilihan)
    bidang_param = None
    if bidang_pilihan != "Semua":
        for b in service.get_all_bidang():
            if b["nama_bidang"] == bidang_pilihan:
                bidang_param = b["bidang_id"]
                break

    # Info filter aktif
    if angkatan_param or bidang_param:
        st.info(
            f"Filter aktif → "
            f"Angkatan: **{angkatan_pilihan}**, "
            f"Bidang: **{bidang_pilihan}**"
        )

    # ---------- KPI (terpengaruh filter) ----------
    kpi = service.kpi_summary(angkatan=angkatan_param, bidang_id=bidang_param)

    if kpi["total_responden"] == 0:
        st.warning("Tidak ada responden yang cocok dengan filter ini.")
        return

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Responden", kpi["total_responden"])
    c2.metric("Rata-rata Waktu Tunggu", f"{kpi['avg_waktu_tunggu_bulan']} bln")
    c3.metric("Sesuai", f"{kpi['persen_sesuai']}%")
    c4.metric("Sebagian Sesuai", f"{kpi['persen_sebagian']}%")
    c5.metric("Tidak Sesuai", f"{kpi['persen_tidak']}%")

    st.divider()

    # ---------- CHART (terpengaruh filter) ----------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Bidang Pekerjaan")
        df = pd.DataFrame(service.distribusi_bidang(angkatan=angkatan_param, bidang_id=bidang_param))
        if not df.empty:
            st.bar_chart(df.set_index("bidang"))
        else:
            st.caption("Tidak ada data.")

    with col2:
        st.subheader("Distribusi Waktu Tunggu Kerja")
        df = pd.DataFrame(service.distribusi_waktu_tunggu(angkatan=angkatan_param, bidang_id=bidang_param))
        if not df.empty:
            st.bar_chart(df.set_index("range"))
        else:
            st.caption("Tidak ada data.")

    st.subheader("Kesesuaian Kerja vs Program Studi")
    df = pd.DataFrame(service.kesesuaian_vs_prodi(angkatan=angkatan_param, bidang_id=bidang_param))
    if not df.empty:
        df = df.set_index("prodi")
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df)
    else:
        st.caption("Tidak ada data.")