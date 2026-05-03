# Alla konstanter för RightHome-appen samlade på ett ställe.
# Ändra här → ändras överallt i appen. DRY! 
 
from pathlib import Path
import os
from dotenv import load_dotenv
 
load_dotenv()
 
# ── Sökvägar ──────────────────────────────────────────────────────────────────
ROOT_DIR        = Path(__file__).parent.parent.parent  # repo-roten
ETL_DIR         = ROOT_DIR / "ETL_Pipline"
ASSETS_DIR      = Path(__file__).parent.parent / "assets"
ICONS_DIR       = ASSETS_DIR / "icons"
IMAGES_DIR      = ASSETS_DIR / "images"
SRC_DATA_DIR    = ROOT_DIR / "src" / "data"
 
# ── CSV-filer ─────────────────────────────────────────────────────────────────
CSV_BOSTADER    = ETL_DIR / "bostader.csv"
CSV_PRISER      = ETL_DIR / "priser.csv"
CSV_PLATSER     = ETL_DIR / "platser.csv"
CSV_VISNINGAR   = ETL_DIR / "visningar.csv"
 
# ── JSON-filer (SCB + OSM) ────────────────────────────────────────────────────
JSON_BOSTADER   = SRC_DATA_DIR / "bostader.json"
JSON_OSM        = SRC_DATA_DIR / "osm_data.json"
JSON_SCB        = SRC_DATA_DIR / "scb_stats.json"
 
# ── API-nycklar ───────────────────────────────────────────────────────────────
GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
 
# ── Kolumnnamn — bostader.csv ─────────────────────────────────────────────────
COL_ID              = "id"
COL_TYP             = "typ"
COL_UPPLATELSE      = "upplåtelseform"
COL_RUM             = "rum"
COL_KVM             = "boyta"          # boyta = kvm
COL_KVM_ENHET       = "boyta_enhet"
COL_TILLGANGLIG     = "tillgänglig"
COL_CREATED_AT      = "created_at"
COL_ADRESS          = "adress"
COL_LAT             = "lat"
COL_LNG             = "lon"            # lon (inte lng!)
COL_PLATS_ID        = "plats_id"
COL_SPARAD          = "sparad"
 
# ── POI-kolumner (från bostader.csv) ─────────────────────────────────────────
COL_POI_KOLLEKTIV   = "poi_kollektivtrafik"
COL_POI_UTBILDNING  = "poi_utbildning_kultur"
COL_POI_MAT         = "poi_mat_shopping"
COL_POI_FRITID      = "poi_fritid"
COL_POI_RELIGION    = "poi_religion_tro"
COL_POI_HALSA       = "poi_halsa"
COL_POI_OVRIGT      = "poi_ovrigt"
 
# ── Kolumnnamn — visningar.csv ────────────────────────────────────────────────
COL_VIS_DATUM       = "datum"
COL_VIS_TID         = "tid"
COL_VIS_ADRESS      = "adress"
COL_VIS_DAG         = "dag"
 
# ── Färger (matchar PowerBI-designen) ────────────────────────────────────────
COLOR_CREAM         = "#F5EDE0"
COLOR_SAND          = "#E8D5BB"
COLOR_CORAL         = "#C97B5A"
COLOR_CORAL_LIGHT   = "#E8A882"
COLOR_BROWN         = "#6B4C3B"
COLOR_DARK          = "#2C1A0E"
COLOR_WHITE         = "#FDFAF6"
COLOR_MUTED         = "#9B8070"
 
# ── Karta ─────────────────────────────────────────────────────────────────────
MAP_CENTER_LAT      = 59.3293   # Stockholm
MAP_CENTER_LNG      = 18.0686
MAP_DEFAULT_ZOOM    = 10
 
# ── POI-typer (Google Maps + ikoner) ─────────────────────────────────────────
POI_OPTIONS = {
    "Bibliotek":        {"google_type": "library",          "icon": "BibliotekIcon.png",        "col": COL_POI_UTBILDNING},
    "Kollektivtrafik":  {"google_type": "transit_station",  "icon": "KollektivtrafikIcon.png",  "col": COL_POI_KOLLEKTIV},
    "Restaurang":       {"google_type": "restaurant",       "icon": "ResturangIcon.png",        "col": COL_POI_MAT},
    "Gym":              {"google_type": "gym",              "icon": "GymIcon.png",              "col": COL_POI_FRITID},
    "Matbutik":         {"google_type": "supermarket",      "icon": "MatbutikIcon.png",         "col": COL_POI_MAT},
    "Skola":            {"google_type": "school",           "icon": "SkolaIcon.png",            "col": COL_POI_UTBILDNING},
}
 
# ── Sidinformation ────────────────────────────────────────────────────────────
APP_TITLE           = "RightHome"
APP_TAGLINE         = "Hitta rätt bostad, område"
APP_ICON            = "🏠"
LOGO_PATH           = IMAGES_DIR / "logo.png"
 
 # ── Kolumnnamn — priser.csv ───────────────────────────────────────────────────
COL_BOSTAD_ID           = "bostad_id"
COL_PRIS                = "pris"
COL_AVGIFT              = "avgift"
COL_KVADRATMETERPRIS    = "kvadratmeterpris"
COL_PRIS_PER_KVM        = "pris_per_kvm"
COL_VALUTA              = "valuta"
COL_MANADSKOSTNAD       = "manadskostnad"
 
# ── Kolumnnamn — platser.csv ──────────────────────────────────────────────────
COL_OMRADE              = "område"
COL_STAD                = "stad"
COL_KOMMUN_BEFOLKNING   = "kommun_befolkning"
 
# ── Kolumnnamn — visningar.csv ────────────────────────────────────────────────
COL_VIS_BOSTAD_ID       = "bostad_id"
COL_VIS_ADRESS          = "adress"
COL_VIS_DATUM           = "visningsdatum"
COL_VIS_START           = "starttid"
COL_VIS_SLUT            = "sluttid"
 