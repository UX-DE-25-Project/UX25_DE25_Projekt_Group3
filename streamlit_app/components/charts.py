# ── components/charts.py ──────────────────────────────────────────────────────
# Diagrammen för RightHome-appen bör samlas här.
# Importera från pages.

import streamlit as st
import plotly.express as px
import duckdb
import pandas as pd
from utils.constants import COLOR_CORAL, COLOR_SAND, COLOR_BROWN, COLOR_MUTED


# ── Karta-vy diagram ──────────────────────────────────────────────────────────

def render_prisdiagram(df: pd.DataFrame) -> None:
    """Bar chart: snittpris per område. Visas på karta-sidan."""
    st.markdown("#### Snittpris per område")

    pris_df = duckdb.sql("""
        SELECT
            område AS Område,
            ROUND(AVG(pris), -3)::BIGINT AS Snittpris
        FROM df
        WHERE pris IS NOT NULL
        GROUP BY område
        ORDER BY Snittpris DESC
        LIMIT 15
    """).df()

    if pris_df.empty:
        st.info("Ingen prisdata att visa.")
        return

    fig = px.bar(
        pris_df,
        x="Snittpris",
        y="Område",
        orientation="h",
        color_discrete_sequence=[COLOR_CORAL],
        text_auto=".2s",
        labels={"Snittpris": "Snittpris (kr)", "Område": ""},
    )
    fig.update_layout(
        height=380,
        margin=dict(l=0, r=10, t=0, b=0),
        yaxis=dict(autorange="reversed"),
        showlegend=False,
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


# ── Statistik-diagram ─────────────────────────────────────────────────────────

def render_snittpris_per_typ(df: pd.DataFrame) -> None:
    """Bar chart: snittpris per bostadstyp."""
    st.markdown("#### Snittpris per bostadstyp")

    typ_df = duckdb.sql("""
        SELECT
            typ,
            ROUND(AVG(pris), -3)::BIGINT AS snittpris
        FROM df
        GROUP BY typ
        ORDER BY snittpris DESC
    """).df()

    fig = px.bar(
        typ_df,
        x="typ",
        y="snittpris",
        text_auto=".2s",
        color="typ",
        color_discrete_sequence=[COLOR_CORAL, COLOR_BROWN, COLOR_SAND, COLOR_MUTED],
        labels={"typ": "Bostadstyp", "snittpris": "Snittpris (kr)"},
    )
    fig.update_layout(showlegend=False, margin=dict(t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)


def render_upplatelseform(df: pd.DataFrame) -> None:
    """Pie chart: fördelning upplåtelseform."""
    st.markdown("#### Fördelning upplåtelseform")

    uppl_df = duckdb.sql("""
        SELECT upplåtelseform, COUNT(*) AS antal
        FROM df
        GROUP BY upplåtelseform
    """).df()

    fig = px.pie(
        uppl_df,
        names="upplåtelseform",
        values="antal",
        color_discrete_sequence=[COLOR_CORAL, COLOR_SAND, COLOR_BROWN, COLOR_MUTED],
        hole=0.4,
    )
    fig.update_layout(margin=dict(t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)


def render_pris_per_kvm(df: pd.DataFrame) -> None:
    """Linjediagram: snittpris per kvm för topp 15 områden."""
    st.markdown("#### Snittpris per kvm - topp 15 områden")

    kvm_df = duckdb.sql("""
        SELECT
            område,
            ROUND(AVG(pris_per_kvm), 0)::INT AS snitt_kvm_pris
        FROM df
        WHERE pris_per_kvm IS NOT NULL
        GROUP BY område
        ORDER BY snitt_kvm_pris DESC
        LIMIT 15
    """).df()

    fig = px.line(
        kvm_df,
        x="område",
        y="snitt_kvm_pris",
        markers=True,
        color_discrete_sequence=[COLOR_BROWN],
        labels={"område": "Område", "snitt_kvm_pris": "Pris/kvm (kr)"},
    )
    fig.update_layout(
        xaxis_tickangle=-40,
        height=350,
        margin=dict(t=0, b=0),
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=8))
    st.plotly_chart(fig, use_container_width=True)