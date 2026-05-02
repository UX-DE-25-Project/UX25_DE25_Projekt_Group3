import json
import time
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "services"))
from services.osm_service import get_nearby_places

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOSTADER_PATH = os.path.join(BASE_DIR, "src", "data", "bostader.json")
OSM_OUTPUT_PATH = os.path.join(BASE_DIR, "src", "data", "osm_data.json")

def generate_osm_data():
    with open(BOSTADER_PATH, "r", encoding="utf-8") as f:
        bostader = json.load(f)

    # Återuppta tidigare körning
    if os.path.exists(OSM_OUTPUT_PATH):
        with open(OSM_OUTPUT_PATH, "r", encoding="utf-8") as f:
            osm_results = json.load(f)
        already_done = {k for k, v in osm_results.items() if v}
        print(f"Återupptar — {len(already_done)} bostäder redan klara.")
    else:
        osm_results = {}
        already_done = set()

    total = len(bostader)
    print(f"Startar OSM-data-generering för {total} bostäder...\n")

    for i, b in enumerate(bostader):
        b_id = str(b["id"])
        lat = b["latitude"]
        lon = b["longitude"]

        if b_id in already_done:
            continue

        success = False
        retries = 0
        max_retries = 3

        while not success and retries < max_retries:
            try:
                places = get_nearby_places(lat, lon)
                osm_results[b_id] = places
                success = True
                time.sleep(1.5)
            except Exception as e:
                retries += 1
                wait_time = retries * 10
                print(f"  Fel för bostad {b_id} (försök {retries}). Väntar {wait_time}s... Error: {e}")
                time.sleep(wait_time)

        if not success:
            print(f"  Gav upp på bostad {b_id} efter {max_retries} försök.")
            osm_results[b_id] = []

        # Progressen ska sparas var 10:e bostad
        if (i + 1) % 10 == 0:
            with open(OSM_OUTPUT_PATH, "w", encoding="utf-8") as f:
                json.dump(osm_results, f, ensure_ascii=False, indent=2)
            done_count = sum(1 for v in osm_results.values() if v)
            print(f"  Status: {i + 1}/{total} bearbetade — {done_count} med data")

    # Slutlig sparning
    with open(OSM_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(osm_results, f, ensure_ascii=False, indent=2)

    done_count = sum(1 for v in osm_results.values() if v)
    print(f"\n✅ Klar! {done_count}/{total} bostäder fick OSM-data.")
    print(f"   Sparad i: {OSM_OUTPUT_PATH}")

if __name__ == "__main__":
    generate_osm_data()