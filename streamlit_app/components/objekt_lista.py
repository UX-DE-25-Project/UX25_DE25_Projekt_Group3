# ── components/objekt_lista.py ────────────────────────────────────────────────
# Tre delfunktioner som kommer att matcha UX:arnas sidopanel och rekommenderade lista design

import streamlit as st
import pandas as pd
from utils.helpers import load_all, load_visningar, format_sek
from utils.constants import COL_SPARAD

# ── Förkortningar ───────────────────────────────────────────────────────
_MANAD = ["", "JAN", "FEB", "MAR", "APR", "MAJ", "JUN",
          "JUL", "AUG", "SEP", "OKT", "NOV", "DEC"]


def render_sparade() -> None:
    """Detta visar bostäder där sparad == 1 i sidopanelens - Mina sparade-sektion."""
    df = load_all()
    sparade = df[df[COL_SPARAD] == 1].head(3)

    st.markdown("### Mina sparade")

    if sparade.empty:
        st.caption("Du har inte sparat några bostäder ännu.")
        return

    for _, rad in sparade.iterrows():
        with st.container(border=True):
            st.markdown(f"**{format_sek(rad['pris'])}**")
            st.caption(f"Område {rad['adress']}, {rad['område']}")
            c1, c2, c3 = st.columns(3)
            c1.caption(f"Rum {int(rad['rum'])} rum")
            c2.caption(f"Boyta {int(rad['boyta'])} m²")
            c3.caption(str(rad["typ"]).capitalize())
