"""
index.py
Container / router. Jalankan: streamlit run index.py
"""
import streamlit as st
import layer1, layer2, layer3, layer4

st.set_page_config(page_title="Dashboard Mahasiswa 4-Layer", layout="wide")

# ---- session state ----
defaults = {"page": 1, "selected_prodi_id": None, "selected_nim": None}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---- sidebar navigasi ----
with st.sidebar:
    st.title("🎓 Dashboard 4-Layer")
    st.caption("Progressive disclosure: ringkas → detail")

    pages = {
        1: "1️⃣ Ringkasan Prodi",
        2: "2️⃣ Segmentasi Mahasiswa",
        3: "3️⃣ Profil Individu",
        4: "4️⃣ Rekomendasi Karier",
    }
    for num, label in pages.items():
        if st.button(label, use_container_width=True,
                     type="primary" if st.session_state.page == num else "secondary"):
            st.session_state.page = num
            st.rerun()

    st.divider()
    st.markdown("**Konteks aktif**")
    st.write(f"Prodi: `{st.session_state.selected_prodi_id or '-'}`")
    st.write(f"NIM: `{st.session_state.selected_nim or '-'}`")

# ---- routing ----
page = st.session_state.page
if page == 1:
    layer1.render()
elif page == 2:
    layer2.render()
elif page == 3:
    layer3.render()
elif page == 4:
    layer4.render()