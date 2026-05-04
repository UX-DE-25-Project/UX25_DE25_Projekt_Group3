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
