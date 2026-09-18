import streamlit as st
import feature1
import feature2
import feature3
import feature4

st.set_page_config(
    page_title="Tracer Study & Career Navigation",
    page_icon="🎓",
    layout="wide",
)

st.sidebar.title("🎓 Tracer Study App")
st.sidebar.caption("UK Petra — Dummy Demo")

PAGES = {
    "1. Peta Kompetensi Dunia Kerja": feature1.render,
    "2. Analisis Skill Gap": feature2.render,
    "3. Dashboard Tracer Study": feature3.render,
    "4. Career Navigation System": feature4.render,
}

pilihan = st.sidebar.radio("Navigasi Fitur", list(PAGES.keys()))
st.sidebar.divider()
st.sidebar.info("Data dummy untuk keperluan screenshot fitur EIS.")

PAGES[pilihan]()