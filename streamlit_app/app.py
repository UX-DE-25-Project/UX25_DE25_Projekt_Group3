# ── app.py ────────────────────────────────────────────────────────────────────
import streamlit as st
from utils.constants import APP_TITLE, APP_ICON, LOGO_PATH
 
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)
 
if "sida" not in st.session_state:
    st.session_state["sida"] = "home"
 
from vyer.home       import show as show_home
from vyer.karta_vy   import show as show_karta
from vyer.statistik  import show as show_statistik
 
# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
* { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0rem 2rem 1rem 2rem !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
 
/* Topbar vit bakgrund för logo */
.logo-bar {
    background: white;
    padding: 1rem;
    border-bottom: 1px solid #E8D5BB;
    text-align: center;
}
 
/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #F5EDE0 !important;
    border-right: 1px solid #E8D5BB !important;
}
section[data-testid="stSidebar"] .stButton button {
    background: white !important;
    border: 1px solid #E8D5BB !important;
    border-radius: 10px !important;
    color: #6B4C3B !important;
    font-weight: 500 !important;
    margin-bottom: 0.3rem !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: #C97B5A !important;
    color: white !important;
    border-color: #C97B5A !important;
}

section[data-testid="stSidebar"] img {
    display: block;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)
 
# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo med vit bakgrund
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=200)
    else:
        st.title("RightHome")
 
    st.markdown("---")
 
    if st.button("Home", use_container_width=True):
        st.session_state["sida"] = "home"
        st.rerun()
 
    if st.button("Karta", use_container_width=True):
        st.session_state["sida"] = "karta"
        st.rerun()
 
    if st.button("Statistik", use_container_width=True):
        st.session_state["sida"] = "statistik"
        st.rerun()
 
# ── Visa rätt sida ────────────────────────────────────────────────────────────
if st.session_state["sida"] == "home":
    show_home()
elif st.session_state["sida"] == "karta":
    show_karta()
elif st.session_state["sida"] == "statistik":
    show_statistik()

