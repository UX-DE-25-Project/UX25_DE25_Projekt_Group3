# ── vyer/karta_vy.py ──────────────────────────────────────────────────────────
import streamlit as st
import streamlit.components.v1 as components
from components.filter_bar import render_filter_bar
from components.karta import build_map_html
from utils.constants import GOOGLE_MAPS_KEY


def show():
    # ── CSS ───────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .block-container { padding: 0.5rem 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── Filterrad från kollegans komponent ────────────────────────────────────
    df_filtrerad, valt_omrade = render_filter_bar()

    st.markdown("---")

    # ── POI-knappar ───────────────────────────────────────────────────────────
    poi_options = {
        "Bibliotek":       "library",
        "Kollektivtrafik": "transit_station",
        "Restaurang":      "restaurant",
        "Gym":             "gym",
        "Matbutik":        "supermarket",
        "Skola":           "school",
    }

    if "aktiv_poi" not in st.session_state:
        st.session_state["aktiv_poi"] = ""

    poi_cols = st.columns(6)
    for i, (namn, typ) in enumerate(poi_options.items()):
        with poi_cols[i]:
            if st.button(namn, use_container_width=True, key=f"poi_{i}"):
                if st.session_state["aktiv_poi"] == typ:
                    st.session_state["aktiv_poi"] = ""
                else:
                    st.session_state["aktiv_poi"] = typ

    st.caption(f"{len(df_filtrerad)} bostäder visas — område: {valt_omrade}")

    # ── Google Maps ───────────────────────────────────────────────────────────
    if not GOOGLE_MAPS_KEY:
        st.warning("Lägg till GOOGLE_MAPS_API_KEY i din .env-fil!")
        return

    map_html = build_map_html(
        df_filtrerad,
        GOOGLE_MAPS_KEY,
        st.session_state["aktiv_poi"]
    )

    components.html(map_html, height=650, scrolling=False)