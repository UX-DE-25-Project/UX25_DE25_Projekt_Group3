import json
import time
import pandas as pd
from services.scb_service import get_nearby_places

def generate_osm_data():
    # Ladda bostadsdata för att få koordinater
    with open("src/data/bostader.json", "r", encoding="utf-8") as f:
        bostader = json.load(f)

    osm_results = {}
    total = len(bostader)

    print(f"Startar OSM-data-generering för {total} bostäder...")

    
    