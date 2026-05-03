# ── components/filter_bar.py ──────────────────────────────────────────────────
# Sökfält + filterknapp.
# Ska returnera ett filtrerat DataFrame och valt område.
# DRY: all filtreringslogik på ett ställe.

import streamlit as st
from utils.helpers import load_all, get_omraden


def render_filter_bar() -> tuple:
    """
    Renderar sökfält och filteralternativ.

    Returns:
        tuple: (filtrerat DataFrame, valt område som sträng)
    """
    df = load_all()
    omraden = get_omraden(df)

        # ── Filter-toggle i session state ────────────────────────────────
    if "filter_open" not in st.session_state:
        st.session_state.filter_open = False

    # ── Sök-rad ────────────────────────────────────────────────────────────────
    col_sok, col_knapp, col_filter = st.columns([4, 0.8, 1.1])

    with col_sok:
        valt_omrade = st.selectbox(
            label="Sök område",
            options=["Alla"] + omraden,
            label_visibility="collapsed",
            key="filter_omrade",
        )

    with col_knapp:
        st.button("Sök", use_container_width=True, type="primary", key="btn_sok")

    with col_filter:
        if st.button("Filter ≡", use_container_width=True, key="btn_filter"):
            st.session_state.filter_open = not st.session_state.filter_open
