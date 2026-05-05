# ── pages/statistik.py ────────────────────────────────────────────────────────
# Statistiksidan

import streamlit as st

from components.kpi_cards import render_kpis
from components.charts    import (
    render_snittpris_per_typ,
    render_upplatelseform,
    render_pris_per_kvm,
    render_rumsfordelning,
)
from utils.helpers        import load_all, read_css
from utils.constants      import STYLES_PATH


def show() -> None:
    """Renderar statistiksidan, som sedan kommer att anropas från app.py."""
    read_css(STYLES_PATH / "app.css")