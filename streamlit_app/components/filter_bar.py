# ── components/filter_bar.py ──────────────────────────────────────────────────
# Sökfält + filterknapp.
# Ska returnera ett filtrerat DataFrame och valt område.
# DRY: all filtreringslogik på ett ställe.

import streamlit as st
from utils.helpers import load_all, get_omraden