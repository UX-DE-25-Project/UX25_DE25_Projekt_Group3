# ── vyer/home.py ──────────────────────────────────────────────────────────────
import streamlit as st
import base64
from utils.constants import IMAGES_DIR


def get_base64_image(image_path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

    

def show():
    bg_path = IMAGES_DIR / "entry_vy.png"

    if bg_path.exists():
        b64 = get_base64_image(bg_path)
    else:
        b64 = ""

    # ── CSS — bara bakgrundsbild, inget annat HTML ────────────────────────────
    st.markdown(f"""
<style>
[data-testid="stMain"] {{
    background-image: url('data:image/png;base64,{b64}');
    background-size: cover;
    background-position: center;
}}
[data-testid="stMain"] .stButton button {{
    background-color: #C97B5A !important;
    border: none !important;
    color: white !important;
    border-radius: 10px !important;
}}
</style>
""", unsafe_allow_html=True)

    # ── Streamlit-innehåll ────────────────────────────────────────────────────
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Hitta rätt bostad. Enklare.")
        st.write("UTFORSKA BOSTÄDER, PRISER OCH OMRÅDEN")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Utforska bostäder →", use_container_width=True, type="primary"):
            st.session_state["sida"] = "karta"
            st.rerun()
            