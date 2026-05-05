# ── vyer/karta_vy.py ──────────────────────────────────────────────────────────
import streamlit as st
import streamlit.components.v1 as components
import base64
from components.filter_bar import render_filter_bar
from components.karta import build_map_html
from utils.constants import GOOGLE_MAPS_KEY, ICONS_DIR, POI_OPTIONS as POI_CONST

# Färger per POI-typ — matchar kartan
POI_COLORS = {
    "library":         "#4A90D9",
    "transit_station": "#27AE60",
    "restaurant":      "#E67E22",
    "gym":             "#8E44AD",
    "supermarket":     "#16A085",
    "school":          "#2980B9",
}

POI_LIST = [
    (info["icon"], namn, info["google_type"])
    for namn, info in POI_CONST.items()
]


def get_icon_b64(filename: str) -> str:
    filepath = ICONS_DIR / filename
    if filepath.exists():
        return base64.b64encode(filepath.read_bytes()).decode()
    return ""


def render_poi_knapp(col, ikon_fil, namn, typ, aktiva):
    with col:
        is_active = typ in aktiva
        b64 = get_icon_b64(ikon_fil)
        poi_color = POI_COLORS.get(typ, "#C97B5A")
        border = poi_color if is_active else "#E8D5BB"
        bg = "#FFF8F3" if is_active else "white"
        shadow = "box-shadow:0 0 0 2px " + poi_color + ";" if is_active else ""

        if b64:
            html_parts = [
                '<div style="',
                "background:", bg, ";",
                "border:2px solid ", border, ";",
                "border-radius:12px;",
                "padding:8px 4px 4px 4px;",
                "text-align:center;",
                "margin-bottom:2px;",
                shadow,
                '">',
                '<img src="data:image/png;base64,', b64, '" ',
                'style="width:34px;height:34px;object-fit:contain;display:block;margin:0 auto;">',
                '</div>'
            ]
            st.markdown("".join(html_parts), unsafe_allow_html=True)

        if st.button(
            namn,
            key="poi_" + typ,
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            aktiva_ny = set(aktiva)
            if is_active:
                aktiva_ny.discard(typ)
            else:
                aktiva_ny.add(typ)
            st.session_state["aktiva_poi"] = list(aktiva_ny)
            st.rerun()


def show():
    # Multival — lista istället för enstaka
    if "aktiva_poi" not in st.session_state:
        st.session_state["aktiva_poi"] = []

    df_filtrerad, valt_omrade = render_filter_bar()
    st.markdown("---")

    col_karta, col_poi = st.columns([4, 1])
    aktiva = st.session_state["aktiva_poi"]

    with col_poi:
        st.markdown(
            "<p style='font-size:13px;font-weight:600;color:#6B4C3B;margin-bottom:6px;'>"
            "Visa närhet till</p>",
            unsafe_allow_html=True,
        )

        for i in range(0, len(POI_LIST), 2):
            pairs = POI_LIST[i:i+2]
            c1, c2 = st.columns(2, gap="small")
            cols = [c1, c2]
            for j, (ikon_fil, namn, typ) in enumerate(pairs):
                render_poi_knapp(cols[j], ikon_fil, namn, typ, aktiva)

        # Legend — visa valda med färgpunkt
        if aktiva:
            st.markdown("<hr style='margin:8px 0;'>", unsafe_allow_html=True)
            for _, namn, typ in POI_LIST:
                if typ in aktiva:
                    color = POI_COLORS.get(typ, "#C97B5A")
                    st.markdown(
                        '<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">'
                        '<div style="width:10px;height:10px;border-radius:50%;background:' + color + ';flex-shrink:0;"></div>'
                        '<span style="font-size:11px;color:#6B4C3B;">' + namn + '</span>'
                        '</div>',
                        unsafe_allow_html=True,
                    )

        st.markdown("<hr style='margin:8px 0;'>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:11px;color:#6B4C3B;text-align:center;">'
            "🏠 <b>" + str(len(df_filtrerad)) + "</b> bostäder<br>"
            '<span style="color:#999;">' + valt_omrade + "</span></div>",
            unsafe_allow_html=True,
        )

    with col_karta:
        if not GOOGLE_MAPS_KEY:
            st.warning("Lägg till GOOGLE_MAPS_API_KEY i din .env-fil!")
            return

        map_html = build_map_html(
            df_filtrerad,
            GOOGLE_MAPS_KEY,
            aktiva,  # skickar lista nu
        )
        components.html(map_html, height=650, scrolling=False)

        