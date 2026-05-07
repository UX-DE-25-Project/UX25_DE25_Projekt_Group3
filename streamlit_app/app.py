import streamlit as st
from utils.constants import APP_TITLE, APP_ICON, LOGO_PATH
from vyer.home import show as show_home
from vyer.karta_vy import show as show_karta
from vyer.statistik import show as show_statistik

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

if "sida" not in st.session_state:
    st.session_state["sida"] = "home"

st.markdown("""
<style>
@import url('https://googleapis.com');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dölj Streamlits topbar och ta bort utrymmet */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
}

/* Ta bort padding som header lämnar */
.appview-container > .main > .block-container {
    padding-top: 1rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    padding-bottom: 1rem !important;
}

  /* Tvinga ljus bakgrund på main area */
.appview-container {
    background-color: #FDFAF6 !important;
}
.main {
    background-color: #FDFAF6 !important;
}          
/* Dölj dark mode på selectbox och knappar */
.stSelectbox > div > div {
    background-color: white !important;
    color: #1a1a1a !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #F5EDE0 !important;
    border-right: 1px solid #E8D5BB !important;
    width: 14rem !important;
    min-width: 14rem !important;
    transform: translateX(0) !important;
    visibility: visible !important;
}

/* Dölj collapse-knappen — sidebar alltid synlig */
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

/* Sidebar knappar */
section[data-testid="stSidebar"] .stButton button {
    background: white !important;
    border: 1px solid #E8D5BB !important;
    border-radius: 10px !important;
    color: #6B4C3B !important;
    font-weight: 500 !important;
    margin-bottom: 0.4rem !important;
    width: 100% !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: #C97B5A !important;
    color: white !important;
    border-color: #C97B5A !important;
}

/* Logo centrering */
section[data-testid="stSidebar"] img {
    display: block !important;
    margin: 0 auto !important;
}
/* Fix multiselect — synliga options */
.stMultiSelect [data-baseweb="tag"] {
    background-color: #C97B5A !important;
    color: white !important;
}

.stMultiSelect [data-baseweb="select"] > div {
    background-color: white !important;
    border: 1px solid #E8D5BB !important;
    color: #1a1a1a !important;
}

/* Fix selectbox i filter */
.stSelectbox [data-baseweb="select"] > div {
    background-color: white !important;
    border: 1px solid #E8D5BB !important;
    color: #1a1a1a !important;
}

/* Dropdown lista */
[data-baseweb="popover"] {
    background-color: white !important;
    color: #1a1a1a !important;
}

[data-baseweb="menu"] {
    background-color: white !important;
}

[data-baseweb="option"] {
    background-color: white !important;
    color: #1a1a1a !important;
}

[data-baseweb="option"]:hover {
    background-color: #F5EDE0 !important;
}

/* --- FIX FÖR POI-KNAPPAR (IKONERNA) --- */
/* --- ULTIMATA FIXEN: OSYNLIGA KNAPPAR --- */


/* 2. Tvinga behållaren som Streamlit skapar att kollapsa helt */
section.main div[data-testid="column"] > div > div > div > div:has(button) {
    display: none !important;
    height: 0px !important;
    min-height: 0px !important;
    margin: 0px !important;
    padding: 0px !important;
}

/* 3. Se till att ikonerna (dina iframes) har kvar sina klick-funktioner */
iframe {
    display: block !important;
    margin-bottom: 10px !important;
    border: none !important;
}


</style>
""", unsafe_allow_html=True)

# SIDEBAR NAVIGATION
with st.sidebar:
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

# ROUTING
if st.session_state["sida"] == "home":
    show_home()
elif st.session_state["sida"] == "karta":
    show_karta()
elif st.session_state["sida"] == "statistik":
    show_statistik()
