import streamlit as st
import pandas as pd
import service

def _render_career_card(nama_bidang: str, match: list, gap: list, skor: float = None):
    st.markdown(f"### 🎯 {nama_bidang}")
    if skor is not None:
        st.progress(min(skor, 1.0), text=f"Skor Kecocokan: {skor*100:.1f}%")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ Skill yang sudah match**")
        for m in match:
            st.markdown(f"- 🟢 {m['nama_skill']} _({m['jenis']})_")
    with col2:
        st.markdown("**📚 Skill gap yang perlu dipelajari**")
        for g in gap:
            st.markdown(f"- 🔴 {g['nama_skill']} _({g['jenis']})_")


def render():
    st.header("🧭 Career Navigation System")

    tab1, tab2 = st.tabs(["Career Explorer", "Ayo Navigasi Karirmu 🚀"])

    # ---------------- TAB 1: CAREER EXPLORER ----------------
    with tab1:
        st.subheader("Browse Karier per Bidang")
        bidang_list = service.get_all_bidang()
        nama_list = [b["nama_bidang"] for b in bidang_list]

        col1, col2 = st.columns(2)
        with col1:
            pilihan1 = st.selectbox("Bidang 1", nama_list, key="f4_exp1")
        with col2:
            pilihan2 = st.selectbox("Bidang 2", ["(tidak ada)"] + nama_list, key="f4_exp2")

        def _get_bidang_by_name(nama):
            for b in bidang_list:
                if b["nama_bidang"] == nama:
                    return b
            return None

        def _card(nama_bidang):
            top_hard = service.top_hard_skills_per_bidang(5).get(nama_bidang, [])
            top_soft = service.top_soft_skills_per_bidang(5).get(nama_bidang, [])
            sert = service.sertifikasi_per_bidang(3).get(nama_bidang, [])
            st.markdown(f"#### 💼 {nama_bidang}")
            st.markdown("**Hard Skills teratas:**")
            st.write(", ".join([h["skill"] for h in top_hard]) or "-")
            st.markdown("**Soft Skills teratas:**")
            st.write(", ".join([s["skill"] for s in top_soft]) or "-")
            st.markdown("**Sertifikasi bermanfaat:**")
            st.write(", ".join([x["sertifikasi"] for x in sert]) or "-")

        if pilihan2 == "(tidak ada)":
            _card(pilihan1)
        else:
            c1, c2 = st.columns(2)
            with c1:
                _card(pilihan1)
            with c2:
                _card(pilihan2)

    # ---------------- TAB 2: CAREER MATCHER ----------------
    with tab2:
        st.subheader("Ayo Navigasi Karirmu!")
        st.caption("Centang skill yang kamu miliki, sistem akan merekomendasikan bidang karier paling cocok "
                   "berdasarkan pola alumni. Anonim — tanpa login.")

        with st.expander("🔎 Mulai Career Matcher", expanded=True):
            hard_skills = service.get_all_skill(jenis="hard")
            soft_skills = service.get_all_skill(jenis="soft")

            st.markdown("**Hard Skills yang kamu miliki:**")
            hard_choice = st.multiselect(
                "Pilih hard skills",
                options=[(s["skill_id"], s["nama_skill"]) for s in hard_skills],
                format_func=lambda x: x[1],
                key="f4_hard_ms",
            )

            st.markdown("**Soft Skills yang kamu miliki:**")
            soft_choice = st.multiselect(
                "Pilih soft skills",
                options=[(s["skill_id"], s["nama_skill"]) for s in soft_skills],
                format_func=lambda x: x[1],
                key="f4_soft_ms",
            )

            submitted = st.button("🚀 Hitung Rekomendasi Karier", type="primary")

        if submitted:
            user_skill_ids = {sid for sid, _ in hard_choice} | {sid for sid, _ in soft_choice}
            if not user_skill_ids:
                st.warning("Pilih minimal 1 skill dulu ya.")
            else:
                hasil = service.recommend_bidang_for_skills(user_skill_ids, top_n=5)
                st.success("Berikut Top 5 bidang paling cocok untukmu:")

                for i, h in enumerate(hasil, start=1):
                    with st.container(border=True):
                        st.markdown(f"#### #{i} — {h['nama_bidang']}")
                        st.progress(min(h["skor"], 1.0), text=f"Skor Kecocokan: {h['skor']*100:.1f}%")

                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("**✅ Sudah match**")
                            for m in h["match"]:
                                st.markdown(f"- 🟢 {m['nama_skill']} _({m['jenis']})_")
                            if not h["match"]:
                                st.caption("Belum ada yang match.")
                        with c2:
                            st.markdown("**📚 Perlu dipelajari**")
                            for g in h["gap"]:
                                st.markdown(f"- 🔴 {g['nama_skill']} _({g['jenis']})_")
                            if not h["gap"]:
                                st.caption("Semua skill sudah match! 🎉")

                # Catat log anonim
                top1 = hasil[0]
                service.catat_log_eksplorasi(top1["bidang_id"], top1["skor"], list(user_skill_ids))

                st.info(
                    "⚠️ **Disclaimer:** Rekomendasi ini adalah agregasi pola alumni, "
                    "bukan prediksi personal atau hasil AI. Gunakan sebagai bahan eksplorasi awal."
                )

                # Insight tambahan (opsional)
                with st.expander("📈 Insight: Skill yang paling sering dicari mahasiswa"):
                    insight = service.insight_skill_paling_dicari()
                    if insight:
                        st.dataframe(pd.DataFrame(insight), use_container_width=True)