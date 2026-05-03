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

    # ── Filter expandering ────────────────────────────────────────────────
    if st.session_state.filter_open:
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)

            with c1:
                valda_typer = st.multiselect(
                    "Bostadstyp",
                    options=sorted(df["typ"].dropna().unique().tolist()),
                    key="filter_typ",
                )
            with c2: # EXEMPEL | KAN ÄNDRAS
                pris_max = st.slider(
                    "Max pris (Mkr)",
                    min_value=0.5,
                    max_value=15.0,
                    value=10.0,
                    step=0.5,
                    key="filter_pris",
                )
            with c3: # EXEMPEL | KAN ÄNDRAS
                rum_min = st.selectbox(
                    "Minst antal rum",
                    options=[1, 2, 3, 4, 5, 6],
                    key="filter_rum",
                )

        if valda_typer: # EXEMPEL | KAN ÄNDRAS
            df = df[df["typ"].isin(valda_typer)]
        df = df[df["pris"] <= pris_max * 1_000_000]
        df = df[df["rum"] >= rum_min]

    # ── Områdesfilter ─────────────────────────────────────────────────────────
    if valt_omrade != "Alla":
        df = df[df["område"] == valt_omrade]

    return df, valt_omrade