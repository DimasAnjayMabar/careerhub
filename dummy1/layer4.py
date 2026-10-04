import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import service

def render():
    st.title("4️⃣ Rekomendasi Jalur Karier")
    st.caption("Layer 4 — output analisis: skor kecocokan, gap, dan roadmap.")

    nim = st.session_state.selected_nim
    if not nim:
        st.warning("Belum ada NIM terpilih. Mulai dari Page 2 → pilih mahasiswa.")
        return

    m = service.get_mahasiswa(nim)
    st.markdown(f"**Mahasiswa:** {m['nama']} ({nim}) — {service.get_prodi(m['prodi_id'])['nama_prodi']}")

    rekom = service.get_rekomendasi_karier(nim)
    if not rekom:
        st.error("Tidak ada data skor."); return

    top = rekom[0]

    # ---- headline ----
    c1,c2,c3 = st.columns([2,1,1])
    with c1:
        st.metric("🎯 Rekomendasi Utama", top["nama_career"])
    with c2:
        st.metric("Skor Kecocokan", f"{top['skor']}%")
    with c3:
        st.metric("Alternatif ke-2", f"{rekom[1]['nama_career']} ({rekom[1]['skor']}%)")

    st.divider()

    # ---- gauge/cards skor per career ----
    st.subheader("Skor Kecocokan per Career Path")
    cols = st.columns(3)
    for i, r in enumerate(rekom):
        with cols[i % 3]:
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=r["skor"],
                title={"text": r["nama_career"]},
                gauge={"axis": {"range": [0, 100]},
                       "bar": {"color": "#2ecc71" if r["skor"]>=70 else "#f1c40f" if r["skor"]>=50 else "#e74c3c"},
                       "steps": [
                           {"range":[0,50],"color":"#fadbd8"},
                           {"range":[50,70],"color":"#fdebd0"},
                           {"range":[70,100],"color":"#d5f5e3"},
                       ]}
            ))
            fig.update_layout(height=220, margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---- checklist skill dimiliki vs dibutuhkan ----
    st.subheader(f"Checklist Kompetensi untuk {top['nama_career']}")
    checklist = service.get_skill_checklist(nim, top["career_id"])
    for c in checklist:
        badge = c["status"]
        st.markdown(f"{badge} **{c['kompetensi']}** — nilai saat ini `{c['nilai_saat_ini']}` "
                    f"(bobot kepentingan {int(c['bobot']*100)}%)")

    st.divider()

    # ---- roadmap stepper ----
    st.subheader("Roadmap Pengembangan Multi-Semester")
    steps = []
    for c in checklist:
        if c["nilai_saat_ini"] < 3.0:
            steps.append(f"Tingkatkan **{c['kompetensi']}** (gap {round(3.0-c['nilai_saat_ini'],2)}) — "
                         f"ambil mata kuliah pilihan / sertifikasi terkait.")
    if not steps:
        steps.append("Semua kompetensi inti sudah memadai. Fokus: portofolio & networking.")

    st.markdown("**Kompetensi sekarang → Gap → Langkah disarankan**")
    cols = st.columns(len(checklist) if checklist else 1)
    for col, c in zip(cols, checklist):
        with col:
            st.markdown(f"**{c['kompetensi']}**")
            st.progress(min(1.0, c["nilai_saat_ini"]/4.0))
            st.caption(f"{c['nilai_saat_ini']}/4.0 {c['status']}")

    st.markdown("### Langkah Disarankan")
    for i, s in enumerate(steps, 1):
        st.markdown(f"{i}. {s}")

    st.info(f"💡 **Narasi:** Berdasarkan profil akademik & aktivitas, "
            f"**{m['nama']}** paling cocok ke jalur **{top['nama_career']}** ({top['skor']}%). "
            f"Fokus pengembangan pada kompetensi yang masih bertanda ⚠️/❌.")