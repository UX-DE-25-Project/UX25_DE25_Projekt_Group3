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


def render_visningar() -> None:
    """Visar kommande visningar från visningar.csv."""
    vis = load_visningar()

    st.markdown("### Kommande visningar")

    if vis.empty:
        st.caption("Inga visningar inbokade.")
        return

    for _, v in vis.iterrows():
        with st.container(border=True):
            col_datum, col_info = st.columns([1, 3])

            with col_datum:
                datum_str = str(v["visningsdatum"])       # "2026-04-24"
                dag       = datum_str.split("-")[2]       # "24"
                mnad_num  = int(datum_str.split("-")[1])  # 4
                st.markdown(f"**{dag}**  \n{_MANAD[mnad_num]}")

            with col_info:
                st.markdown(f"**{v['adress']}**")
                st.caption(f"Kl {v['starttid']} – {v['sluttid']}")


def render_rekommenderade(df: pd.DataFrame) -> None:
    """
    Visar upp till 5 rekommenderade bostäder från det filtrerade DataFrame.

    Sorterar, lägst pris per kvm, för "bäst värde".

    Args:
        df: Filtrerat merged DataFrame från load_all()
    """
    st.markdown("### Rekommenderade för dig")

    if df.empty:
        st.info("Inga bostäder matchar ditt filter.")
        return

    top = df.sort_values("pris_per_kvm").head(5)

    for _, rad in top.iterrows():
        with st.container(border=True):
            col_info, col_pris = st.columns([3, 1])

            with col_info:
                st.markdown(f"**{rad['adress']}, {rad['område']}**")
                c1, c2, c3 = st.columns(3)
                c1.caption(f"Rum {int(rad['rum'])} rum")
                c2.caption(f"Boyta {int(rad['boyta'])} m²")
                c3.caption(str(rad["typ"]).capitalize())

            with col_pris:
                st.markdown(f"**{format_sek(rad['pris'])}**")
                if rad.get("avgift") and rad["avgift"] > 0:
                    st.caption(f"{int(rad['avgift']):,} kr/mån".replace(",", " "))