# ── components/kpi_cards.py ───────────────────────────────────────────────────
# KPI-kort som kommer att visas överst på statistiksidan.

import streamlit as st
import duckdb
import pandas as pd
from utils.helpers import format_sek, format_antal


def render_kpis(df: pd.DataFrame) -> None:
    """
    Renderar fyra KPI-kort för ett givet DataFrame.

    Args:
        df: Merged DataFrame från load_all()
    """
    if df.empty:
        st.info("Inga bostäder att visa KPI:er för.")
        return

    # ── DuckDB beräkningar ────────────────────────────────────────────────
    antal        = len(df)
    snittpris    = duckdb.sql("SELECT ROUND(AVG(pris), -3)::BIGINT FROM df").fetchone()[0]
    snitt_kvm    = duckdb.sql("SELECT ROUND(AVG(boyta), 0)::INT FROM df").fetchone()[0]
    tillgangliga = duckdb.sql("SELECT COUNT(*) FROM df WHERE tillgänglig = true").fetchone()[0]

    # ── Renderar kolumner ──────────────────────────────────────────────────────
    cols = st.columns(4)
    metrics = [
        ("Antal bostäder",  f"{antal:,}".replace(",", " "),       None),
        ("Snittpris",       format_sek(snittpris),                 None),
        ("Snitt boyta",     f"{snitt_kvm} m²",                    None),
        ("Tillgängliga",    f"{tillgangliga:,}".replace(",", " "), None),
    ]

    for col, (label, value, delta) in zip(cols, metrics):
        with col:
            st.metric(label=label, value=value, delta=delta)