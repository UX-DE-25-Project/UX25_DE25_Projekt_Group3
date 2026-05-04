# ── components/karta.py ───────────────────────────────────────────────────────
import json


def build_map_html(df, api_key: str, poi_type: str = "") -> str:
    """Bygger Google Maps som HTML-sträng med filtrerad data från Python."""

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

    bostader_js = json.dumps(bostader, ensure_ascii=False)
    poi_js = f'"{poi_type}"' if poi_type else '""'

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ width: 100%; height: 100%; font-family: 'DM Sans', sans-serif; }}
    #map {{ width: 100%; height: 100vh; }}
    #infoPanel {{
        position: fixed; bottom: 20px; left: 20px;
        background: rgba(255,255,255,0.92); backdrop-filter: blur(10px);
        padding: 6px 14px; border-radius: 999px;
        font-size: 12px; color: #555;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 1000; pointer-events: none;
    }}
    #clearRoute {{
        position: fixed; bottom: 20px; left: 50%;
        transform: translateX(-50%);
        background: #E8735A; color: white;
        border: none; padding: 8px 20px;
        border-radius: 999px; font-size: 12px;
        font-weight: 600; cursor: pointer;
        z-index: 1000; display: none;
    }}
    #clearRoute:hover {{ background: #d4634a; }}
    #legend {{
        position: fixed; right: 16px; top: 50%;
        transform: translateY(-50%);
        background: rgba(255,255,255,0.96); backdrop-filter: blur(14px);
        border-radius: 20px; padding: 14px 16px;
        box-shadow: 0 6px 28px rgba(0,0,0,0.13);
        z-index: 1000; display: none;
        flex-direction: column; gap: 4px; min-width: 160px;
    }}
    #legend.visible {{ display: flex; }}
    .legend-title {{ font-size: 13px; font-weight: 600; color: #1a1a1a; margin-bottom: 6px; padding-bottom: 8px; border-bottom: 1px solid #efefef; }}
    .legend-row {{ display: flex; align-items: center; gap: 10px; padding: 4px; }}
    .legend-dot {{ width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }}
    .legend-label {{ font-size: 12px; color: #333; }}
</style>
</head>
<body>
<div id="map"></div>
<div id="infoPanel">Laddar bostäder...</div>
<button id="clearRoute" onclick="rensaRutt()">✕ Rensa rutt</button>
<div id="legend">
    <div class="legend-title">Förklaring</div>
    <div class="legend-row">
        <div class="legend-dot" style="background:#E8735A"></div>
        <span class="legend-label">Bostad</span>
    </div>
    <div id="legend-poi"></div>
</div>
<script>
const BOSTADER = {bostader_js};
const POI_TYPE = {poi_js};
let map, infoWindow, placesService, directionsRenderer;
let bostadMarkers = [], placeMarkers = [], dashLine = null;

const POI_CONFIG = {{
    "library":         {{ name: "Bibliotek",       color: "#4A90D9" }},
    "transit_station": {{ name: "Kollektivtrafik", color: "#27AE60" }},
    "restaurant":      {{ name: "Restaurang",      color: "#E67E22" }},
    "gym":             {{ name: "Gym",             color: "#8E44AD" }},
    "supermarket":     {{ name: "Matbutik",        color: "#16A085" }},
    "school":          {{ name: "Skola",           color: "#2980B9" }},
}};

function initMap() {{
    map = new google.maps.Map(document.getElementById("map"), {{
        center: {{ lat: 59.3293, lng: 18.0686 }}, zoom: 12,
        streetViewControl: false, mapTypeControl: false, fullscreenControl: false,
        styles: [{{ featureType: "poi", elementType: "labels", stylers: [{{ visibility: "off" }}] }}]
    }});
    infoWindow = new google.maps.InfoWindow({{ maxWidth: 270 }});
    placesService = new google.maps.places.PlacesService(map);
    directionsRenderer = new google.maps.DirectionsRenderer({{ suppressMarkers: true }});
    directionsRenderer.setMap(map);
    addBostadMarkers();
    if (BOSTADER.length > 0) {{
    const bounds = new google.maps.LatLngBounds();
    BOSTADER.forEach(b => bounds.extend({{ lat: b.lat, lng: b.lng }}));
    map.fitBounds(bounds);
}}
    
}}

function addBostadMarkers() {{
    bostadMarkers.forEach(m => m.setMap(null)); bostadMarkers = [];
    BOSTADER.forEach(b => {{
        const marker = new google.maps.Marker({{
            position: {{ lat: b.lat, lng: b.lng }}, map,
            icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: 8, fillColor: "#E8735A", fillOpacity: 0.92, strokeColor: "#fff", strokeWeight: 2 }}
        }});
        marker.addListener("click", () => {{
            rensaRutt();
            infoWindow.setContent(buildPopup(b));
            infoWindow.open(map, marker);
            if (placeMarkers.length > 0) ritaDashedLinje({{ lat: b.lat, lng: b.lng }}, placeMarkers[0].getPosition());
        }});
        bostadMarkers.push(marker);
    }});
    document.getElementById("infoPanel").textContent = BOSTADER.length + " bostäder visas";
}}

function formatPris(p) {{
    return p.toLocaleString('sv-SE') + " kr";
}}

function buildPopup(b) {{
    return `<div style="font-family:'DM Sans',sans-serif;width:240px;padding:12px 14px">
        <div style="font-size:15px;font-weight:700;color:#1a1a1a">${{b.adress}}</div>
        <div style="font-size:11px;color:#999;margin-bottom:8px">${{b.område}}</div>
        <div style="font-size:18px;font-weight:700;color:#E8735A">${{formatPris(b.pris)}}</div>
        ${{b.avgift ? `<div style="font-size:11px;color:#bbb">Avgift: ${{formatPris(b.avgift)}}/mån</div>` : ""}}
        <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
            <span style="background:#f0ece8;padding:3px 10px;border-radius:20px;font-size:12px">${{b.rum}} rum</span>
            <span style="background:#f0ece8;padding:3px 10px;border-radius:20px;font-size:12px">${{b.boyta}} kvm</span>
            <span style="background:#f0ece8;padding:3px 10px;border-radius:20px;font-size:12px">${{b.typ}}</span>
        </div>
    </div>`;
}}

function ritaDashedLinje(fran, till) {{
    if (dashLine) dashLine.setMap(null);
    dashLine = new google.maps.Polyline({{
        path: [fran, till], geodesic: true,
        strokeColor: "#1565C0", strokeOpacity: 0,
        icons: [{{ icon: {{ path: "M 0,-1 0,1", strokeOpacity: 1, strokeColor: "#1565C0", strokeWeight: 3, scale: 4 }}, offset: "0", repeat: "16px" }}],
        map
    }});
    document.getElementById("clearRoute").style.display = "block";
}}

function rensaRutt() {{
    if (dashLine) {{ dashLine.setMap(null); dashLine = null; }}
    document.getElementById("clearRoute").style.display = "none";
}}

function visaPOI(type) {{
    placeMarkers.forEach(m => m.setMap(null)); placeMarkers = [];
    const cfg = POI_CONFIG[type]; if (!cfg) return;
    const center = map.getCenter();
    placesService.nearbySearch({{location: center, radius: 5000, type }}, (results, status) => {{
        if (status !== "OK" || !results.length) return;
        results.forEach(place => {{
            if (!place.geometry) return;
            const m = new google.maps.Marker({{
                position: place.geometry.location, map,
                icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: 7, fillColor: cfg.color, fillOpacity: 0.9, strokeColor: "#fff", strokeWeight: 2 }},
                title: place.name
            }});
            m.addListener("click", () => {{
                infoWindow.setContent(`<div style="font-family:'DM Sans',sans-serif;padding:10px">
                    <strong>${{place.name}}</strong><br>
                    <span style="color:#888;font-size:12px">${{place.vicinity || ""}}</span><br>
                    <span style="color:${{cfg.color}};font-size:12px;font-weight:600">${{cfg.name}}</span>
                </div>`);
                infoWindow.open(map, m);
            }});
            placeMarkers.push(m);
        }});
        document.getElementById("legend-poi").innerHTML = `
            <div class="legend-row">
                <div class="legend-dot" style="background:${{cfg.color}}"></div>
                <span class="legend-label">${{cfg.name}}</span>
            </div>`;
        document.getElementById("legend").classList.add("visible");
    }});
}}

window.initMap = initMap;
window.rensaRutt = rensaRutt;
</script>
<script src="https://maps.googleapis.com/maps/api/js?key={api_key}&libraries=places&callback=initMap" async defer></script>
</body>
</html>"""
    return html