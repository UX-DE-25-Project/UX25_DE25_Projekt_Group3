# ── pages/entre.py ────────────────────────────────────────────────────────────
import streamlit as st
import base64
from utils.constants import IMAGES_DIR


def get_base64_image(image_path) -> str:
    """Konverterar en bild till base64 för CSS-bakgrund."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def show():
    bg_path = IMAGES_DIR / "entry_vy.png"

    # ── Bakgrundsbild via CSS ─────────────────────────────────────────────────
    if bg_path.exists():
        b64 = get_base64_image(bg_path)
        bg_css = f"url('data:image/png;base64,{b64}')"
    else:
        bg_css = "linear-gradient(135deg, #F5EDE0 0%, #E8D5BB 100%)"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

    .entre-section {{
        min-height: 88vh;
        background-image: {bg_css};
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 3rem;
        position: relative;
    }}

    .entre-section::before {{
        content: '';
        position: absolute;
        inset: 0;
        background: rgba(44, 26, 14, 0.45);
    }}

    .entre-content {{
        position: relative;
        z-index: 2;
        max-width: 700px;
    }}

    .entre-title {{
        font-family: 'DM Serif Display', serif;
        font-size: 4rem;
        color: #FDFAF6;
        line-height: 1.1;
        margin-bottom: 0.8rem;
        text-shadow: 0 2px 20px rgba(0,0,0,0.3);
    }}

    .entre-tagline {{
        font-size: 1.15rem;
        color: #F5EDE0;
        opacity: 0.9;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 2.5rem;
    }}

    .entre-badge {{
        display: inline-block;
        background: rgba(253, 250, 246, 0.15);
        border: 1px solid rgba(253, 250, 246, 0.3);
        border-radius: 30px;
        padding: 0.4rem 1.2rem;
        color: #FDFAF6;
        font-size: 0.85rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(8px);
    }}

    .entre-stats {{
        display: flex;
        gap: 2rem;
        justify-content: center;
        margin-top: 2.5rem;
    }}

    .entre-stat {{
        text-align: center;
        color: #FDFAF6;
    }}

    .entre-stat-num {{
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        line-height: 1;
    }}

    .entre-stat-label {{
        font-size: 0.78rem;
        opacity: 0.75;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.2rem;
    }}
    </style>

    <div class="entre-section">
        <div class="entre-content">
            <div class="entre-badge">🏠 Stockholm & Omgivningar</div>
            <div class="entre-title">Hitta rätt<br>bostad för dig</div>
            <div class="entre-tagline">Utforska bostäder, priser och områden</div>
            <div class="entre-stats">
                <div class="entre-stat">
                    <div class="entre-stat-num">1 000+</div>
                    <div class="entre-stat-label">Bostäder</div>
                </div>
                <div class="entre-stat">
                    <div class="entre-stat-num">20+</div>
                    <div class="entre-stat-label">Områden</div>
                </div>
                <div class="entre-stat">
                    <div class="entre-stat-num">Live</div>
                    <div class="entre-stat-label">Data</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Knapp centrerad under bilden ──────────────────────────────────────────
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        if st.button("🗺️ Utforska bostäder →", use_container_width=True, type="primary"):
            st.session_state["sida"] = "karta"
            st.rerun()