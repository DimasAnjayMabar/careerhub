import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import service

SEGMEN_COLOR = {"Unggul": "#2ecc71", "Berkembang": "#3498db",
                "Perlu Perhatian": "#f1c40f", "Berisiko": "#e74c3c"}

def render():
    st.title("2️⃣ Segmentasi Performa Mahasiswa")
    st.caption("Layer 2 — untuk kaprodi/tim akademik. Klik satu mahasiswa untuk drill ke Page 3.")

    prodi_id = st.session_state.selected_prodi_id
    prodi_list = service.list_prodi()
    prodi_ids = [p["prodi_id"] for p in prodi_list]
    idx = prodi_ids.index(prodi_id) if prodi_id in prodi_ids else 0
    prodi_id = st.selectbox("Pilih Prodi", prodi_ids, index=idx,
                            format_func=lambda x: service.get_prodi(x)["nama_prodi"])
    st.session_state.selected_prodi_id = prodi_id

    angkatan = st.radio("Angkatan", [None, 2021, 2022, 2023],
                        format_func=lambda x: "Semua" if x is None else str(x),
                        horizontal=True)

    rows = service.get_segmentasi(prodi_id, angkatan)
    if not rows:
        st.warning("Tidak ada data.")
        return

    # ---- kartu ringkasan per segmen ----
    st.subheader("Jumlah Mahasiswa per Segmen")
    from collections import Counter
    cnt = Counter(r["segmen"] for r in rows)
    cols = st.columns(4)
    for col, seg in zip(cols, ["Unggul","Berkembang","Perlu Perhatian","Berisiko"]):
        with col:
            st.markdown(f"### :{'green' if seg=='Unggul' else 'blue' if seg=='Berkembang' else 'orange' if seg=='Perlu Perhatian' else 'red'}[{seg}]")
            st.metric("Jumlah", cnt.get(seg, 0))

    st.divider()

    # ---- kuadran scatter ----
    col1, col2 = st.columns([3,2])
    with col1:
        st.subheader("Diagram Kuadran: Performa Akademik vs Keaktifan Non-Akademik")
        fig = px.scatter(rows, x="aktivitas", y="ipk", color="segmen",
                         color_discrete_map=SEGMEN_COLOR,
                         hover_data=["nim","nama"], size_max=15)
        fig.update_traces(marker=dict(size=14, line=dict(width=1, color="white")))
        fig.update_layout(xaxis_title="Jumlah Aktivitas Non-Akademik",
                          yaxis_title="IPK",
                          legend_title="Segmen")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Alur Perpindahan Segmen antar Semester")
        alur = service.get_alur_segmen(prodi_id)
        labels = list({t["dari"] for t in alur["transisi"]} | {t["ke"] for t in alur["transisi"]})
        idx_map = {l:i for i,l in enumerate(labels)}
        fig = go.Figure(go.Sankey(
            node=dict(label=labels, pad=15, thickness=20,
                      color=[SEGMEN_COLOR.get(l, "#888") for l in labels]),
            link=dict(
                source=[idx_map[t["dari"]] for t in alur["transisi"]],
                target=[idx_map[t["ke"]] for t in alur["transisi"]],
                value=[t["jumlah"] for t in alur["transisi"]]
            )
        ))
        fig.update_layout(height=420, margin=dict(l=10,r=10,t=30,b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---- tabel + drill ke Page 3 ----
    st.subheader("Daftar Mahasiswa")
    st.caption("Klik NIM untuk membuka Profil Individu (Page 3).")
    for r in sorted(rows, key=lambda x: x["ipk"], reverse=True):
        c1,c2,c3,c4,c5 = st.columns([2,3,1,1,2])
        c1.write(r["nim"]); c2.write(r["nama"])
        c3.write(f"IPK {r['ipk']}"); c4.write(f"Akt {r['aktivitas']}")
        c5.markdown(f"**{r['segmen']}**")
        if c5.button("Lihat Profil →", key=f"p_{r['nim']}"):
            st.session_state.selected_nim = r["nim"]
            st.session_state.page = 3
            st.rerun()

    st.info("💡 Klik **Lihat Profil** pada salah satu mahasiswa untuk drill-through ke Page 3 (Profil Individu).")