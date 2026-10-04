import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import service

def render():
    st.title("1️⃣ Ringkasan Program Studi")
    st.caption("Layer 1 — untuk pimpinan. Klik salah satu prodi untuk drill-through ke Page 2.")

    kpi = service.get_kpi_prodi()

    # ---- headline number ----
    total_mhs = sum(k["jumlah_mahasiswa"] for k in kpi)
    avg_ipk = round(sum(k["rata_ipk"]*k["jumlah_mahasiswa"] for k in kpi)/total_mhs, 2)
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        st.metric("Total Mahasiswa (3 Prodi)", total_mhs)
    with c2:
        st.metric("Rata-rata IPK Fakultas", avg_ipk)
    with c3:
        st.metric("Prodi", len(kpi))

    st.divider()

    # ---- KPI cards per prodi ----
    st.subheader("KPI per Prodi")
    cols = st.columns(len(kpi))
    for col, k in zip(cols, kpi):
        with col:
            st.markdown(f"### {k['nama_prodi']}")
            st.metric("Rata-rata IPK", k["rata_ipk"])
            st.metric("Tren Naik", f"{k['pct_naik']}%")
            st.metric("Sertifikasi/Magang", f"{k['pct_sertifikasi_magang']}%")
            if st.button(f"Drill ke {k['prodi_id']}", key=f"drill_{k['prodi_id']}"):
                st.session_state.selected_prodi_id = k["prodi_id"]
                st.session_state.page = 2
                st.rerun()

    st.divider()

    # ---- bar chart perbandingan IPK ----
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Perbandingan IPK antar Prodi")
        fig = px.bar(kpi, x="nama_prodi", y="rata_ipk", color="nama_prodi",
                     text="rata_ipk", range_y=[0,4])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Distribusi Tren Mahasiswa")
        fig = go.Figure()
        for k in kpi:
            fig.add_trace(go.Bar(name=k["nama_prodi"], x=["Naik","Stagnan","Turun"],
                                 y=[k["pct_naik"], k["pct_stagnan"], k["pct_turun"]]))
        fig.update_layout(barmode="group", yaxis_title="%")
        st.plotly_chart(fig, use_container_width=True)

    # ---- donut distribusi karier ----
    st.subheader("Distribusi Rekomendasi Karier per Prodi")
    cols = st.columns(len(kpi))
    for col, k in zip(cols, kpi):
        with col:
            if k["distribusi_karier"]:
                fig = px.pie(names=list(k["distribusi_karier"].keys()),
                             values=list(k["distribusi_karier"].values()),
                             hole=0.5, title=k["nama_prodi"])
                st.plotly_chart(fig, use_container_width=True)

    st.info("💡 Klik tombol **Drill ke <prodi>** di atas untuk masuk ke Page 2 (Segmentasi Mahasiswa).")