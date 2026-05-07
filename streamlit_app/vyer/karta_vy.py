# ── vyer/karta_vy.py ──────────────────────────────────────────────────────────
import streamlit as st
import streamlit.components.v1 as components
import base64
from components.filter_bar import render_filter_bar
from utils.constants import GOOGLE_MAPS_KEY, ICONS_DIR, POI_OPTIONS as POI_CONST

POI_COLORS = {
    "library":         "#E53935",
    "transit_station": "#00897B",
    "restaurant":      "#F57C00",
    "gym":             "#8E24AA",
    "supermarket":     "#1E88E5",
    "school":          "#43A047",
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

    knappar_html = ""
    for ikon_fil, namn, typ in POI_LIST:
        b64   = get_icon_b64(ikon_fil)
        color = POI_COLORS.get(typ, "#C97B5A")
        img_tag = (
            f'<img src="data:image/png;base64,{b64}" '
            f'style="width:58px;height:58px;object-fit:contain;">'
            if b64 else
            f'<div style="width:58px;height:58px;background:#eee;border-radius:8px;"></div>'
        )
        knappar_html += (
            '<div class="poi-btn" data-typ="' + typ + '" data-color="' + color + '"'
            ' onclick="togglePOI(this, \'' + typ + '\')"'
            ' style="background:white;border:2.5px solid #E8D5BB;border-radius:14px;'
            'padding:8px;cursor:pointer;display:flex;align-items:center;'
            'justify-content:center;user-select:none;transition:all 0.15s;aspect-ratio:1;">'
            + img_tag +
            '</div>'
        )

    # Bygg JavaScript separat för att undvika f-string konflikter
    js_code = """
var BOSTADER    = """ + bostader_js + """;
var AKTIVA_INIT = """ + aktiva_js + """;
var POI_CONFIG  = """ + poi_config_js + """;
var valdKategoriTyp = 'library'; // Standardval
var map, infoWindow, placesService, directionsService, directionsRenderer;
var bostadMarkers = [], placeMarkers = {}, valdBostad = null, valdPOI = null;
var aktivaPOI = new Set(AKTIVA_INIT);

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 59.3293, lng: 18.0686 }, zoom: 12,
        streetViewControl: false, mapTypeControl: false, fullscreenControl: false,
        styles: [{ featureType: "poi", elementType: "labels", stylers: [{ visibility: "off" }] }]
    });
    infoWindow        = new google.maps.InfoWindow({ maxWidth: 280 });
    placesService     = new google.maps.places.PlacesService(map);
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        suppressMarkers: true,
        polylineOptions: { strokeWeight: 4, strokeOpacity: 0.8 }
    });
    directionsRenderer.setMap(map);

    addBostadMarkers();

    if (BOSTADER.length > 0) {
        var bounds = new google.maps.LatLngBounds();
        BOSTADER.forEach(function(b) { bounds.extend({ lat: b.lat, lng: b.lng }); });
        map.fitBounds(bounds);
    }

    AKTIVA_INIT.forEach(function(typ) {
        var btn = document.querySelector('.poi-btn[data-typ="' + typ + '"]');
        if (btn) setBtnActive(btn, true);
    });

    if (AKTIVA_INIT.length > 0) {
        google.maps.event.addListenerOnce(map, 'idle', function() {
            AKTIVA_INIT.forEach(function(typ) { visaPOI(typ); });
        });
    }
}

function setBtnActive(btn, on) {
    var color = btn.getAttribute('data-color');
    btn.style.border     = on ? '2.5px solid ' + color : '2.5px solid #E8D5BB';
    btn.style.background = on ? '#F5F9FF' : 'white';
    btn.style.boxShadow  = on ? '0 0 0 3px ' + color + '44' : 'none';
}

function togglePOI(btn, typ) {
    // Spara vilken typ som är aktiv för rutt-sökningen
    valdKategoriTyp = typ; 

    if (aktivaPOI.has(typ)) {
        aktivaPOI.delete(typ);
        setBtnActive(btn, false);
        if (placeMarkers[typ]) {
            placeMarkers[typ].forEach(function(m) { m.setMap(null); });
            delete placeMarkers[typ];
        }
    } else {
        // Rensa andra aktiva om du bara vill se en åt gången (valfritt)
        // aktivaPOI.clear(); 
        
        aktivaPOI.add(typ);
        setBtnActive(btn, true);
        visaPOI(typ);
        
        // Om vi redan har en vald bostad, uppdatera rutt och popup direkt!
        if (valdBostad) {
            // Trigga ett "fejkat" klick på den valda bostaden för att uppdatera info
            triggerBostadUpdate(); 
        }
    }
}

function triggerBostadUpdate() {
    // Hitta markören för den valda bostaden och kör dess klick-logik igen
    bostadMarkers.forEach(function(m) {
        if (m.getPosition().lat() === valdBostad.lat && m.getPosition().lng() === valdBostad.lng) {
            google.maps.event.trigger(m, 'click');
        }
    });
}

function addBostadMarkers() {
    bostadMarkers.forEach(function(m) { m.setMap(null); });
    bostadMarkers = [];

    BOSTADER.forEach(function(b) {
        var marker = new google.maps.Marker({
            position: { lat: b.lat, lng: b.lng },
            map: map,
            icon: { path: google.maps.SymbolPath.CIRCLE, scale: 7,
                    fillColor: "#E8735A", fillOpacity: 0.9,
                    strokeColor: "#fff", strokeWeight: 2 }
        });

        marker.addListener("click", function() {
            valdBostad = { lat: b.lat, lng: b.lng };
            
            var req = {
                location: valdBostad,
                rankBy: google.maps.places.RankBy.DISTANCE,
                type: valdKategoriTyp
            };

            placesService.nearbySearch(req, function(results, status) {
                if (status === "OK" && results.length > 0) {
                    var narmaste = results[0]; // Fixat: Hämta första träffen
                    valdPOI = narmaste.geometry.location;
                    infoWindow.setContent(buildPowerBIPopup(b, narmaste.name));
                    infoWindow.open(map, marker);
                    visaRutt(1); // Starta med gångväg
                } else {
                    infoWindow.setContent(buildPopup(b));
                    infoWindow.open(map, marker);
                }
            });
        });
        bostadMarkers.push(marker);
    });
}


// Fixad för att undvika HTML-syntaxfel
function transportKnappar() {
    return '<div style="margin-top:10px;border-top:1px solid #eee;padding-top:10px;">'
        + '<div style="font-size:11px;color:#999;margin-bottom:6px;">Visa väg:</div>'
        + '<div style="display:flex;gap:6px;">'
        // Vi skickar 1, 2 eller 3 istället för text med citattecken
        + '<button onclick="visaRutt(1)" style="flex:1;padding:6px 4px;border:1px solid #E8D5BB;border-radius:8px;background:white;cursor:pointer;font-size:16px;">🚶</button>'
        + '<button onclick="visaRutt(2)" style="flex:1;padding:6px 4px;border:1px solid #E8D5BB;border-radius:8px;background:white;cursor:pointer;font-size:16px;">🚌</button>'
        + '<button onclick="visaRutt(3)" style="flex:1;padding:6px 4px;border:1px solid #E8D5BB;border-radius:8px;background:white;cursor:pointer;font-size:16px;">🚗</button>'
        + '</div></div>';
}

function buildPopup(b) {
    return '<div style="font-family:sans-serif;width:250px;padding:12px 14px">'
        + '<div style="font-size:15px;font-weight:700;color:#1a1a1a">' + b.adress + '</div>'
        + '<div style="font-size:11px;color:#999;margin-bottom:8px">' + b.område + '</div>'
        + '<div style="font-size:18px;font-weight:700;color:#E8735A">' + b.pris.toLocaleString('sv-SE') + ' kr</div>'
        + (b.avgift ? '<div style="font-size:11px;color:#bbb">Avgift: ' + b.avgift.toLocaleString('sv-SE') + ' kr/mån</div>' : '')
        + '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">'
        + '<span style="background:#f0ece8;padding:3px 10px;border-radius:20px;font-size:12px">' + b.rum + ' rum</span>'
        + '<span style="background:#f0ece8;padding:3px 10px;border-radius:20px;font-size:12px">' + b.boyta + ' kvm</span>'
        + '<span style="background:#f0ece8;padding:3px 10px;border-radius:20px;font-size:12px">' + b.typ + '</span>'
        + '</div>'
        + (valdPOI ? transportKnappar() : '<div style="font-size:11px;color:#bbb;margin-top:8px;">Klicka på en POI-markör för att visa väg.</div>')
        + '</div>';
}

function buildPOIPopup(place, cfg) {
    return '<div style="font-family:sans-serif;padding:10px 12px;min-width:180px">'
        + '<strong style="font-size:14px">' + place.name + '</strong><br>'
        + '<span style="color:#888;font-size:12px">' + (place.vicinity || '') + '</span><br>'
        + '<span style="color:' + cfg.color + ';font-size:12px;font-weight:600">' + cfg.name + '</span>'
        + (valdBostad ? transportKnappar() : '<div style="font-size:11px;color:#bbb;margin-top:8px;">Klicka på en bostad för att visa väg.</div>')
        + '</div>';
}

function buildPowerBIPopup(b, narmasteNamn) {
    var kat = "plats";
    if (POI_CONFIG[valdKategoriTyp]) {
        kat = POI_CONFIG[valdKategoriTyp].name;
    }
    
    var html = '<div style="font-family:sans-serif;width:240px;padding:10px;">';
    html += '<div style="font-weight:700;font-size:16px;">' + b.pris.toLocaleString("sv-SE") + ' kr</div>';
    html += '<div style="color:#666;font-size:12px;margin-bottom:10px;">' + b.adress + '</div>';
    html += '<div style="border-top:1px solid #eee;padding-top:10px;margin-top:10px;">';
    html += '<div style="font-size:10px;color:#E8735A;font-weight:bold;text-transform:uppercase;">Närmaste ' + kat + '</div>';
    html += '<div style="font-size:13px;margin:5px 0;font-weight:600;">' + narmasteNamn + '</div>';
    html += transportKnappar();
    html += '</div></div>';
    return html;
}
function visaRutt(val) {
    if (!valdBostad || !valdPOI) return;
    
    // Fixat: Översätt siffra till Googles TravelMode
    var mode = "WALKING";
    if (val === 2) mode = "TRANSIT";
    if (val === 3) mode = "DRIVING";
    if (typeof val === "string") mode = val; // Om text skickas direkt

    if (directionsRenderer) directionsRenderer.setMap(null);
    directionsRenderer = new google.maps.DirectionsRenderer({
        suppressMarkers: true,
        polylineOptions: { strokeColor: '#E8735A', strokeWeight: 5, strokeOpacity: 0.8 }
    });
    directionsRenderer.setMap(map);

    directionsService.route({
        origin: valdBostad,
        destination: valdPOI,
        travelMode: google.maps.TravelMode[mode]
    }, function(result, status) {
        if (status === 'OK') {
            directionsRenderer.setDirections(result);
        }
    });
}

 function rensaRutt() {
    console.log("Rensar kartan..."); // Se i konsolen om knappen ens svarar

    // 1. Dölj rutt-linjen direkt
    if (directionsRenderer) {
        directionsRenderer.setDirections({routes: []}); // Tömmer rutten internt
        directionsRenderer.setMap(null);
    }
    
    // 2. Skapa en helt ny, tom renderer för framtiden
    directionsRenderer = new google.maps.DirectionsRenderer({
        suppressMarkers: true,
        map: map,
        polylineOptions: { strokeColor: '#E8735A', strokeWeight: 5 }
    });

    // 3. Stäng popup-rutan direkt
    if (infoWindow) {
        infoWindow.close();
    }

    // 4. Ta bort ALLA POI-prickar (som dök upp när du tryckte på knappar)
    if (placeMarkers) {
        Object.keys(placeMarkers).forEach(function(typ) {
            placeMarkers[typ].forEach(function(m) {
                m.setMap(null);
            });
            placeMarkers[typ] = [];
        });
    }

    // 5. Nollställ variablerna
    valdBostad = null;
    valdPOI = null;

    // 6. Dölj knappen
    var btn = document.getElementById("clearRoute");
    if (btn) btn.style.display = "none";
}

function visaPOI(type) {
    var cfg = POI_CONFIG[type];
    if (!cfg) return;

    // 1. Rensa ALLA gamla POI-markörer för just denna typ först
    if (placeMarkers[type]) {
        placeMarkers[type].forEach(function(m) { m.setMap(null); });
    }
    placeMarkers[type] = [];

    // 2. Gör sökningen
    var bounds = map.getBounds();
    var center = bounds ? bounds.getCenter() : map.getCenter();
    
    placesService.nearbySearch({ location: center, radius: 2000, type: type }, function(results, status) {
        if (status === "OK") {
            results.forEach(function(place) {
                var m = new google.maps.Marker({
                    position: place.geometry.location,
                    map: map,
                    icon: { 
                        path: google.maps.SymbolPath.CIRCLE, 
                        scale: 4, // Gör dem mindre så det inte blir stökigt
                        fillColor: cfg.color, 
                        fillOpacity: 0.7,
                        strokeWeight: 1 
                    }
                });
                placeMarkers[type].push(m);
            });
        }
    });
}

window.initMap   = initMap;
window.rensaRutt = rensaRutt;
window.visaRutt  = visaRutt;
"""

    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:100%; height:100%; font-family:'DM Sans',sans-serif; overflow:hidden; }
#wrapper { display:flex; height:100vh; }
#map { flex:1; height:100%; }
#poi-panel {
    width:200px; min-width:200px;
    background:#FDFAF6;
    border-left:1px solid #E8D5BB;
    padding:14px 16px;
    overflow-y:auto;
    flex-shrink:0;
}
#poi-title { font-size:13px; font-weight:600; color:#6B4C3B; margin-bottom:10px; }
.poi-grid { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
.poi-btn:hover { opacity:0.8; transform:scale(0.97); }
#infoPanel {
    position:fixed; bottom:16px; left:16px;
    background:rgba(255,255,255,0.92);
    padding:5px 12px; border-radius:999px;
    font-size:12px; color:#555;
    pointer-events:none; z-index:1000;
}
#clearRoute {
    position:fixed; bottom:16px; left:40%;
    transform:translateX(-50%);
    background:#E8735A; color:white;
    border:none; padding:7px 18px;
    border-radius:999px; font-size:12px;
    font-weight:600; cursor:pointer;
    z-index:1000; display:none;
}
</style>
</head>
<body>
<div id="wrapper">
  <div id="map"></div>
  <div id="poi-panel">
    <div id="poi-title">Visa närhet till</div>
    <div class="poi-grid">""" + knappar_html + """</div>
  </div>
</div>
<div id="infoPanel">Laddar...</div>
<button id="clearRoute" onclick="rensaRutt()">&#x2715; Rensa rutt</button>
<script>""" + js_code + """</script>
<script src="https://maps.googleapis.com/maps/api/js?key=""" + api_key + """&libraries=places&callback=initMap" async defer></script>
</body>
</html>"""

    return html


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






