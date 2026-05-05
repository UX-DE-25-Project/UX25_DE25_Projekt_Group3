# ── vyer/karta_vy.py ─────────────────────────────────────────────────────────

import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path
from components.filter_bar import render_filter_bar
from components.karta import build_map_html
from utils.constants import GOOGLE_MAPS_KEY

ICONS_PATH = Path("assets/icons")

POI_OPTIONS = [
    ("BibliotekIcon.png",         "Bibliotek",       "library"),
    ("KollektivtrafikIcon.png",  "Kollektivtrafik", "transit_station"),
    ("ResturangIcon.png",        "Restaurang",      "restaurant"),
    ("GymIcon.png",              "Gym",             "gym"),
    ("MatbutikIcon.png",         "Matbutik",        "supermarket"),
    ("SkolaIcon.png",            "Skola",           "school"),
]


def get_icon_b64(filename: str) -> str:
    filepath = ICONS_PATH / filename
    if filepath.exists():
        return base64.b64encode(filepath.read_bytes()).decode()
    return ""


def show():
    if "aktiv_poi" not in st.session_state:
        st.session_state["aktiv_poi"] = ""

    df_filtrerad, valt_omrade = render_filter_bar()
    st.markdown("---")

    col_karta, col_poi = st.columns([4, 1])

    with col_poi:
        st.markdown(
            "<p style='font-size:13px;font-weight:600;color:#6B4C3B;margin-bottom:8px;'>Visa närhet till</p>",
            unsafe_allow_html=True,
        )

        for i in range(0, len(POI_OPTIONS), 2):
            c1, c2 = st.columns(2, gap="small")
            pairs = POI_OPTIONS[i:i+2]
            for col, (ikon_fil, namn, typ) in zip([c1, c2], pairs):
                with col:
                    is_active = st.session_state["aktiv_poi"] == typ
                    ikon_b64 = get_icon_b64(ikon_fil)
                    border_color = "#C97B5A" if is_active else "#E8D5BB"
                    bg_color = "#FDF0E6" if is_active else "white"
                    shadow = "box-shadow: 0 0 0 2px #C97B5A;" if is_active else ""

                    # Klickbar ikon-knapp som HTML
                    html = f"""
                    <div title="{namn}" style="
                        background:{bg_color};
                        border:2px solid {border_color};
                        border-radius:14px;
                        padding:10px;
                        text-align:center;
                        cursor:pointer;
                        margin-bottom:8px;
                        {shadow}
                        transition: all 0.15s;
                    ">
                        <img src="data:image/png;base64,{ikon_b64}"
                             style="width:100%;max-width:44px;height:auto;display:block;margin:0 auto;">
                    </div>
                    """
                    st.markdown(html, unsafe_allow_html=True)

                    # Osynlig knapp för Streamlit-klick (dold under HTML)
                    st.markdown(
                        f"""<style>
                        div[data-testid="stButton"] > button[kind="secondary"]#poi_{typ} {{
                            opacity: 0; position: absolute; top: -60px; left: 0;
                            width: 100%; height: 60px; cursor: pointer;
                        }}
                        </style>""",
                        unsafe_allow_html=True,
                    )
                    if st.button(" ", key=f"poi_{typ}", use_container_width=True):
                        st.session_state["aktiv_poi"] = "" if is_active else typ
                        st.rerun()

        st.markdown("---")
        st.markdown(
            f"<div style='font-size:11px;color:#6B4C3B;text-align:center;'>🏠 <b>{len(df_filtrerad)}</b> bostäder<br><span style='color:#999'>{valt_omrade}</span></div>",
            unsafe_allow_html=True,
        )

    with col_karta:
        if not GOOGLE_MAPS_KEY:
            st.warning("Lägg till GOOGLE_MAPS_API_KEY i din .env-fil!")
            return

        map_html = build_map_html(
            df_filtrerad,
            GOOGLE_MAPS_KEY,
            st.session_state["aktiv_poi"]
        )
        components.html(map_html, height=650, scrolling=False)