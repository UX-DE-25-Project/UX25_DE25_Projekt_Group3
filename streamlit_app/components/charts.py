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