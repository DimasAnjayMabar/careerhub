import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import service

TREN_BADGE = {"naik": "🟢 Naik", "turun": "🔴 Turun", "stagnan": "🟡 Stagnan"}

def render():
    st.title("3️⃣ Profil Perkembangan Individu Mahasiswa")
    st.caption("Layer 3 — jantung dashboard untuk dosen PA (Student 360°).")

    # pilih NIM (default dari Page 2)
    mhs_all = service.list_mahasiswa(prodi_id=st.session_state.selected_prodi_id)
    if not mhs_all:
        st.warning("Belum ada prodi terpilih. Silakan mulai dari Page 1.")
        return
    nims = [m["nim"] for m in mhs_all]
    default_nim = st.session_state.selected_nim if st.session_state.selected_nim in nims else nims[0]
    nim = st.selectbox("Pilih Mahasiswa (NIM)", nims, index=nims.index(default_nim),
                       format_func=lambda x: f"{x} — {service.get_mahasiswa(x)['nama']}")
    st.session_state.selected_nim = nim

    profil = service.get_profil_individu(nim)
    if not profil:
        st.error("Data tidak ditemukan."); return

    m = profil["mahasiswa"]
    ips = profil["ips"]

    # ---- header ringkas ----
    c1,c2,c3,c4 = st.columns([3,1,1,1])
    with c1:
        st.markdown(f"### {m['nama']}")
        st.caption(f"NIM {m['nim']} • {service.get_prodi(m['prodi_id'])['nama_prodi']} • Angkatan {m['angkatan']}")
    with c2:
        st.metric("IPK Terakhir", ips[-1]["ipk_kumulatif"] if ips else "-")
    with c3:
        st.metric("SKS Kumulatif", ips[-1]["sks_kumulatif"] if ips else "-")
    with c4:
        st.metric("Tren", TREN_BADGE.get(profil["tren"], "-"))

    st.divider()

    # ---- line chart IPS + IPK ----
    col1, col2 = st.columns([3,2])
    with col1:
        st.subheader("Tren IPS per Semester & IPK Kumulatif")
        if ips:
            df = pd.DataFrame(ips)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df["semester"], y=df["ip_semester"],
                                     mode="lines+markers", name="IPS",
                                     line=dict(color="#3498db", width=3)))
            fig.add_trace(go.Scatter(x=df["semester"], y=df["ipk_kumulatif"],
                                     mode="lines+markers", name="IPK Kumulatif",
                                     line=dict(color="#2ecc71", width=3, dash="dash")))
            fig.update_layout(xaxis_title="Semester", yaxis_title="Nilai",
                              yaxis_range=[0,4], height=380)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Radar Kompetensi")
        if profil["radar"]:
            df = pd.DataFrame(profil["radar"])
            fig = go.Figure(go.Scatterpolar(
                r=df["nilai"].tolist() + [df["nilai"].tolist()[0]],
                theta=df["kompetensi"].tolist() + [df["kompetensi"].tolist()[0]],
                fill="toself", line=dict(color="#9b59b6")
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,4])),
                              showlegend=False, height=380)
            st.plotly_chart(fig, use_container_width=True)

    # ---- heatmap matkul inti x semester ----
    st.subheader("Heatmap Nilai Mata Kuliah Inti × Semester")
    if profil["heatmap"]:
        df = pd.DataFrame(profil["heatmap"])
        pivot = df.pivot_table(index="matkul", columns="semester",
                               values="nilai", aggfunc="mean")
        fig = px.imshow(pivot, aspect="auto", color_continuous_scale="RdYlGn",
                        zmin=0, zmax=4, text_auto=".2f")
        fig.update_layout(height=max(280, 40*len(pivot)))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("Belum ada nilai matkul inti.")

    # ---- timeline aktivitas ----
    st.subheader("Timeline Aktivitas Non-Akademik per Semester")
    if profil["aktivitas"]:
        df = pd.DataFrame(profil["aktivitas"])
        fig = px.scatter(df, x="semester", y="jenis", color="jenis",
                         symbol="tingkat", hover_data=["nama_aktivitas","tingkat"],
                         size_max=18)
        fig.update_traces(marker=dict(size=16, line=dict(width=1, color="white")))
        fig.update_layout(xaxis_title="Semester", yaxis_title="",
                          height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("Belum ada aktivitas tercatat.")

    # ---- insight box ----
    st.success(f"💡 **Insight otomatis:** {profil['insight']}")

    st.divider()
    if st.button("➡️ Lanjut ke Rekomendasi Karier (Page 4)", type="primary"):
        st.session_state.page = 4
        st.rerun()