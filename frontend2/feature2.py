import streamlit as st
import pandas as pd
import service

def render():
    st.header("📉 Analisis Skill Gap")
    st.caption("Membandingkan kompetensi yang dibutuhkan industri vs yang dirasa kurang oleh alumni.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Ranking Skill Gap Terbesar",
        "Dibutuhkan vs Dirasa Kurang",
        "Tren Antar Angkatan",
        "Waktu Tunggu vs Gap",
    ])

    with tab1:
        data = service.ranking_skill_gap(top_n=10)
        df = pd.DataFrame(data)
        st.bar_chart(df.set_index("skill"))
        st.dataframe(df, use_container_width=True)

    with tab2:
        data = service.gap_view_dibutuhkan_vs_kurang(top_n=8)
        df = pd.DataFrame(data).set_index("skill")
        st.bar_chart(df)
        st.dataframe(df.reset_index(), use_container_width=True)

    with tab3:
        data = service.tren_gap_antar_angkatan()
        angkatan_list = list(data.keys())
        df_all = pd.DataFrame({
            ang: {item["skill"]: item["jumlah"] for item in items}
            for ang, items in data.items()
        }).fillna(0).astype(int)
        st.dataframe(df_all, use_container_width=True)
        st.line_chart(df_all)

    with tab4:
        data = service.waktu_tunggu_vs_gap()
        df = pd.DataFrame(data)
        st.scatter_chart(df, x="waktu_bulan", y="jumlah_gap", color="angkatan")
        st.dataframe(df, use_container_width=True)
        corr = df["waktu_bulan"].corr(df["jumlah_gap"])
        st.metric("Korelasi Waktu Tunggu vs Jumlah Gap", f"{corr:.2f}")