# ── app.py ────────────────────────────────────────────────────────────────────
# Entry point för RightHome Streamlit-appen.
# Hanterar bara navigation mellan sidorna — inget annat!
 
import streamlit as st
from utils.constants import APP_TITLE, APP_ICON, LOGO_PATH
 
# ── Sidkonfiguration ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# ── Navigation ────────────────────────────────────────────────────────────────
from pages.entre     import show as show_entre
from pages.karta_vy  import show as show_karta
from pages.statistik import show as show_statistik
 
# Spara aktiv sida i session state
if "sida" not in st.session_state:
    st.session_state["sida"] = "entre"
 
# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
* { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)
 
# ── Navbar ────────────────────────────────────────────────────────────────────
col_logo, col_nav = st.columns([1, 3])
 
with col_logo:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=140)
    else:
        st.markdown("### 🏠 RightHome")
 
with col_nav:
    nav1, nav2, nav3, _ = st.columns([1, 1, 1, 3])
    with nav1:
        if st.button("🏠 Start", use_container_width=True,
                     type="primary" if st.session_state["sida"] == "entre" else "secondary"):
            st.session_state["sida"] = "entre"
            st.rerun()
    with nav2:
        if st.button("🗺️ Karta", use_container_width=True,
                     type="primary" if st.session_state["sida"] == "karta" else "secondary"):
            st.session_state["sida"] = "karta"
            st.rerun()
    with nav3:
        if st.button("📊 Statistik", use_container_width=True,
                     type="primary" if st.session_state["sida"] == "statistik" else "secondary"):
            st.session_state["sida"] = "statistik"
            st.rerun()
 
st.markdown("<hr style='margin:0;border-color:#E8D5BB'>", unsafe_allow_html=True)
 
# ── Visa rätt sida ────────────────────────────────────────────────────────────
if st.session_state["sida"] == "entre":
    show_entre()
elif st.session_state["sida"] == "karta":
    show_karta()
elif st.session_state["sida"] == "statistik":
    show_statistik()
 