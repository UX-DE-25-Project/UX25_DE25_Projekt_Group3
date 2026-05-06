# ── vyer/karta_vy.py ──────────────────────────────────────────────────────────
import streamlit as st
import streamlit.components.v1 as components
import base64
from components.filter_bar import render_filter_bar
from utils.constants import GOOGLE_MAPS_KEY, ICONS_DIR, POI_OPTIONS as POI_CONST

# Tydligt unika färger — ingen liknar en annan
POI_COLORS = {
    "library":         "#E53935",  # röd
    "transit_station": "#B03704",  # mörkorange  
    "restaurant":      "#43060c",  # mörkröd 
    "gym":             "#8E24AA",  # lila
    "supermarket":     "#1E88E5",  # blå
    "school":          "#43A047",  # grön
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

def build_map_with_poi_html(df, api_key: str, aktiva: list) -> str:
    import json

    bostader = []
    for _, row in df.iterrows():
        try:
            lat = float(row.get("lat", 0))
            lng = float(row.get("lon", 0))
            if lat == 0 or lng == 0:
                continue
            bostader.append({
                "lat":    lat,
                "lng":    lng,
                "adress": str(row.get("adress", "—")),
                "pris":   int(row.get("pris", 0)),
                "avgift": int(row.get("avgift", 0)),
                "rum":    int(row.get("rum", 0)),
                "boyta":  int(row.get("boyta", 0)),
                "typ":    str(row.get("typ", "—")),
                "område": str(row.get("område", "—")),
            })
        except:
            continue

    bostader_js   = json.dumps(bostader, ensure_ascii=False)
    aktiva_js     = json.dumps(aktiva)
    poi_config_js = json.dumps({
        typ: {"name": namn, "color": POI_COLORS.get(typ, "#C97B5A")}
        for _, namn, typ in POI_LIST
    })

    # Bara ikon — ingen text under (PNG har redan text inbakad)
    knappar_html = ""
    for ikon_fil, namn, typ in POI_LIST:
        b64   = get_icon_b64(ikon_fil)
        color = POI_COLORS.get(typ, "#C97B5A")
        img_tag = (
            f'<img src="data:image/png;base64,{b64}" '
            f'style="width:58px;height:58px;object-fit:contain;">'
            if b64 else f'<div style="width:70px;height:70px;background:#eee;border-radius:8px;"></div>'
        )
        knappar_html += f"""
        <div class="poi-btn" data-typ="{typ}" data-color="{color}"
             onclick="togglePOI(this, '{typ}')"
             style="background:white;border:2.5px solid #E8D5BB;border-radius:14px;
                    padding:8px;cursor:pointer;display:flex;
                    align-items:center;justify-content:center;
                    user-select:none;transition:all 0.15s;aspect-ratio:1;">
            {img_tag}
        </div>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:100%; height:100%; font-family:'DM Sans',sans-serif; overflow:hidden; }}
#wrapper {{ display:flex; height:100vh; }}
#map {{ flex:1; height:100%; }}
#poi-panel {{
    width:200px;
    min-width:200px;
    background:#FDFAF6;
    border-left:1px solid #E8D5BB;
    padding:14px 16px;
    overflow-y:auto;
    flex-shrink:0;
}}
#poi-title {{
    font-size:13px; font-weight:600; color:#6B4C3B;
    margin-bottom:10px; font-family:'DM Sans',sans-serif;
}}
.poi-grid {{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:8px;
}}
.poi-btn:hover {{ opacity:0.8; transform:scale(0.97); }}
#infoPanel {{
    position:fixed; bottom:16px; left:16px;
    background:rgba(255,255,255,0.92);
    padding:5px 12px; border-radius:999px;
    font-size:12px; color:#555;
    pointer-events:none; z-index:1000;
}}
#clearRoute {{
    position:fixed; bottom:16px; left:40%;
    transform:translateX(-50%);
    background:#E8735A; color:white;
    border:none; padding:7px 18px;
    border-radius:999px; font-size:12px;
    font-weight:600; cursor:pointer;
    z-index:1000; display:none;
}}
</style>
</head>
<body>
<div id="wrapper">
  <div id="map"></div>
  <div id="poi-panel">
    <div id="poi-title">Visa närhet till</div>
    <div class="poi-grid">{knappar_html}</div>
  </div>
</div>
<div id="infoPanel">Laddar...</div>
<button id="clearRoute" onclick="rensaRutt()">✕ Rensa rutt</button>

<script>
const BOSTADER    = {bostader_js};
const AKTIVA_INIT = {aktiva_js};
const POI_CONFIG  = {poi_config_js};

let map, infoWindow, placesService;
let bostadMarkers = [], placeMarkers = {{}}, dashLine = null;
let valdBostad = null;
let aktivaPOI = new Set(AKTIVA_INIT);

function initMap() {{
    map = new google.maps.Map(document.getElementById("map"), {{
        center: {{ lat: 59.3293, lng: 18.0686 }}, zoom: 12,
        streetViewControl: false, mapTypeControl: false, fullscreenControl: false,
        styles: [{{ featureType:"poi", elementType:"labels", stylers:[{{visibility:"off"}}] }}]
    }});
    infoWindow    = new google.maps.InfoWindow({{ maxWidth: 270 }});
    placesService = new google.maps.places.PlacesService(map);

    addBostadMarkers();

    if (BOSTADER.length > 0) {{
        const bounds = new google.maps.LatLngBounds();
        BOSTADER.forEach(b => bounds.extend({{ lat: b.lat, lng: b.lng }}));
        map.fitBounds(bounds);
    }}

    AKTIVA_INIT.forEach(typ => {{
        const btn = document.querySelector('.poi-btn[data-typ="' + typ + '"]');
        if (btn) setBtnActive(btn, true);
    }});

    if (AKTIVA_INIT.length > 0) {{
        google.maps.event.addListenerOnce(map, 'idle', () => {{
            AKTIVA_INIT.forEach(typ => visaPOI(typ));
        }});
    }}
}}

function setBtnActive(btn, on) {{
    const color = btn.getAttribute('data-color');
    btn.style.border     = on ? '2.5px solid ' + color : '2.5px solid #E8D5BB';
    btn.style.background = on ? '#F5F9FF' : 'white';
    btn.style.boxShadow  = on ? '0 0 0 3px ' + color + '44' : 'none';
}}

function togglePOI(btn, typ) {{
    if (aktivaPOI.has(typ)) {{
        aktivaPOI.delete(typ);
        setBtnActive(btn, false);
        if (placeMarkers[typ]) {{
            placeMarkers[typ].forEach(m => m.setMap(null));
            delete placeMarkers[typ];
        }}
    }} else {{
        aktivaPOI.add(typ);
        setBtnActive(btn, true);
        visaPOI(typ);
    }}
}}

function addBostadMarkers() {{
    bostadMarkers.forEach(m => m.setMap(null));
    bostadMarkers = [];
    BOSTADER.forEach(b => {{
        const marker = new google.maps.Marker({{
            position: {{ lat: b.lat, lng: b.lng }}, map,
            icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: 8,
                     fillColor:"#E8735A", fillOpacity:0.92,
                     strokeColor:"#fff", strokeWeight:2 }}
        }});
        marker.addListener("click", () => {{
            valdBostad = {{ lat: b.lat, lng: b.lng }};
            rensaRutt();
            infoWindow.setContent(buildPopup(b));
            infoWindow.open(map, marker);
        }});
        bostadMarkers.push(marker);
    }});
    document.getElementById("infoPanel").textContent = BOSTADER.length + " bostäder visas";
}}

function buildPopup(b) {{
    return '<div style="font-family:sans-serif;width:240px;padding:12px 14px">'
        + '<div style="font-size:15px;font-weight:700;color:#1a1a1a">' + b.adress + '</div>'
        + '<div style="font-size:11px;color:#999;margin-bottom:8px">' + b.område + '</div>'
        + '<div style="font-size:18px;font-weight:700;color:#E8735A">' + b.pris.toLocaleString('sv-SE') + ' kr</div>'
        + (b.avgift ? '<div style="font-size:11px;color:#bbb">Avgift: ' + b.avgift.toLocaleString('sv-SE') + ' kr/mån</div>' : '')
        + '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">'
        + '<span style="background:#f0ece8;padding:3px 10px;border-radius:20px;font-size:12px">' + b.rum + ' rum</span>'
        + '<span style="background:#f0ece8;padding:3px 10px;border-radius:20px;font-size:12px">' + b.boyta + ' kvm</span>'
        + '<span style="background:#f0ece8;padding:3px 10px;border-radius:20px;font-size:12px">' + b.typ + '</span>'
        + '</div></div>';
}}

function visaPOI(type) {{
    const cfg = POI_CONFIG[type];
    if (!cfg) return;
    if (!placeMarkers[type]) placeMarkers[type] = [];

    const bounds = map.getBounds();
    const center = bounds ? bounds.getCenter() : map.getCenter();
    let radius = 5000;
    if (bounds) {{
        const ne = bounds.getNorthEast(), sw = bounds.getSouthWest();
        radius = Math.min(Math.max(Math.abs(ne.lat()-sw.lat()), Math.abs(ne.lng()-sw.lng())) * 55000, 25000);
    }}

    placesService.nearbySearch({{ location: center, radius, type }}, (results, status) => {{
        if (status !== "OK" || !results.length) return;
        results.forEach(place => {{
            if (!place.geometry) return;
            const m = new google.maps.Marker({{
                position: place.geometry.location, map,
                icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: 7,
                         fillColor: cfg.color, fillOpacity:0.9,
                         strokeColor:"#fff", strokeWeight:2 }},
                title: place.name
            }});
            m.addListener("click", () => {{
                if (valdBostad) ritaDashedLinje(valdBostad, place.geometry.location);
                infoWindow.setContent(
                    '<div style="font-family:sans-serif;padding:10px">'
                    + '<strong>' + place.name + '</strong><br>'
                    + '<span style="color:#888;font-size:12px">' + (place.vicinity||'') + '</span><br>'
                    + '<span style="color:' + cfg.color + ';font-size:12px;font-weight:600">' + cfg.name + '</span>'
                    + '</div>'
                );
                infoWindow.open(map, m);
            }});
            placeMarkers[type].push(m);
        }});
    }});
}}

function ritaDashedLinje(fran, till) {{
    if (dashLine) dashLine.setMap(null);
    dashLine = new google.maps.Polyline({{
        path: [fran, till], geodesic: true,
        strokeColor: "#1565C0", strokeOpacity: 0,
        icons: [{{ icon: {{ path:"M 0,-1 0,1", strokeOpacity:1,
                            strokeColor:"#1565C0", strokeWeight:3, scale:4 }},
                  offset:"0", repeat:"16px" }}],
        map
    }});
    document.getElementById("clearRoute").style.display = "block";
}}

function rensaRutt() {{
    if (dashLine) {{ dashLine.setMap(null); dashLine = null; }}
    document.getElementById("clearRoute").style.display = "none";
}}

window.initMap   = initMap;
window.rensaRutt = rensaRutt;
</script>
<script src="https://maps.googleapis.com/maps/api/js?key={api_key}&libraries=places&callback=initMap" async defer></script>
</body>
</html>"""

def show():
    if "aktiva_poi" not in st.session_state:
        st.session_state["aktiva_poi"] = []

    df_filtrerad, valt_omrade = render_filter_bar()
    st.markdown("---")

    aktiva = st.session_state["aktiva_poi"]

    if not GOOGLE_MAPS_KEY:
        st.warning("Lägg till GOOGLE_MAPS_API_KEY i din .env-fil!")
        return

    html = build_map_with_poi_html(df_filtrerad, GOOGLE_MAPS_KEY, aktiva)
    components.html(html, height=650, scrolling=False)
