# ── helpers.py ────────────────────────────────────────────────────────────────
# Hjälpfunktioner som används i hela appen.
# Importeras från components och pages via: from utils.helpers import ...

import pandas as pd
import streamlit as st
from pathlib import Path
from utils.constants import (
    CSV_BOSTADER, CSV_PRISER, CSV_PLATSER, CSV_VISNINGAR,
    COL_ID, COL_BOSTAD_ID, COL_PLATS_ID,
    COL_PRIS, COL_KVM, COL_PRIS_PER_KVM,
    COL_OMRADE, COL_KOMMUN_BEFOLKNING,
)

# ── Fil-läsning ───────────────────────────────────────────────────────────────
def read_textfile(path: Path) -> str:
    """Läser textfil och returnerar innehåll som sträng."""
    with open(path, encoding="utf-8") as f:
        return f.read()

def read_css(path: Path) -> None:
    """Laddar en CSS-fil och injicerar den i Streamlit via st.markdown."""
    css = read_textfile(path)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ── Data-laddning ─────────────────────────────────────────────────────────────

@st.cache_data
def load_bostader() -> pd.DataFrame:
    """Laddar bostader.csv."""
    return pd.read_csv(CSV_BOSTADER)


@st.cache_data
def load_priser() -> pd.DataFrame:
    """Laddar priser.csv."""
    return pd.read_csv(CSV_PRISER)


@st.cache_data
def load_platser() -> pd.DataFrame:
    """Laddar platser.csv."""
    return pd.read_csv(CSV_PLATSER)


@st.cache_data
def load_visningar() -> pd.DataFrame:
    """Laddar visningar.csv."""
    return pd.read_csv(CSV_VISNINGAR)


@st.cache_data
def load_all() -> pd.DataFrame:
    """
    Laddar och mergar alla CSV-filer till ett DataFrame.
    bostader ← priser (på bostad_id)
    bostader ← platser (på plats_id)
    """
    bostader  = load_bostader()
    priser    = load_priser()
    platser   = load_platser()

    # Merge bostader + priser
    df = bostader.merge(
        priser,
        left_on=COL_ID,
        right_on=COL_BOSTAD_ID,
        how="left",
        suffixes=("", "_pris")
    )

    # Merge med platser
    df = df.merge(
        platser,
        on=COL_PLATS_ID,
        how="left",
        suffixes=("", "_plats")
    )

    return df


# ── Formatering ───────────────────────────────────────────────────────────────

def format_sek(val) -> str:
    """Formaterar ett tal som SEK. Ex: 4372299 → '4,4M kr'"""
    try:
        v = int(val)
        if v >= 1_000_000:
            return f"{v/1_000_000:.1f}M kr"
        elif v >= 1_000:
            return f"{v/1_000:.0f}k kr"
        return f"{v:,} kr"
    except:
        return "—"


def format_antal(val) -> str:
    """Formaterar ett stort tal med tusentalsavgränsare. Ex: 995574 → '995 574'"""
    try:
        return f"{int(val):,}".replace(",", " ")
    except:
        return "—"


# ── Statistik ─────────────────────────────────────────────────────────────────

def get_snittpris(df: pd.DataFrame) -> int:
    """Returnerar snittpris för ett filtrerat DataFrame."""
    try:
        return int(df[COL_PRIS].mean())
    except:
        return 0


def get_snittpris_per_kvm(df: pd.DataFrame) -> int:
    """Returnerar snittpris per kvm."""
    try:
        return int(df[COL_PRIS_PER_KVM].mean())
    except:
        return 0


def get_befolkning(df: pd.DataFrame) -> int:
    """Returnerar total befolkning för filtrerade områden."""
    try:
        return int(df[COL_KOMMUN_BEFOLKNING].sum())
    except:
        return 0


def get_omraden(df: pd.DataFrame) -> list:
    """Returnerar sorterad lista med unika områden."""
    try:
        return sorted(df[COL_OMRADE].dropna().unique().tolist())
    except:
        return []


def get_snittpris_per_omrade(df: pd.DataFrame) -> pd.DataFrame:
    """Returnerar snittpris grupperat per område, sorterat fallande."""
    try:
        return (
            df.groupby(COL_OMRADE)[COL_PRIS]
            .mean()
            .sort_values(ascending=False)
            .head(20)
            .reset_index()
            .rename(columns={COL_OMRADE: "Område", COL_PRIS: "Snittpris"})
        )
    except:
        return pd.DataFrame()