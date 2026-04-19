import json
import time
import pandas as pd
from services.osm_service import get_nearby_places

def generate_osm_data():
    # Ladda bostadsdata för att få koordinater
    with open("src/data/bostader.json", "r", encoding="utf-8") as f:
        bostader = json.load(f)

    osm_results = {}
    total = len(bostader)

    print(f"Startar OSM-data-generering för {total} bostäder...")

    for i, b in enumerate(bostader):
        b_id = str(b["id"])
        lat = b["latitude"]
        lon = b["longitude"]

        # Ändrat om servern är långsam eller upptagen
        success = False
        retries = 0
        max_retries = 3 # Försök upp till 3 gånger om det misslyckas
        while not success and retries < max_retries:
            try:
                places = get_nearby_places(lat, lon)
                osm_results[b_id] = places
                success = True
                time.sleep(2) # Extra paus efter varje lyckad förfrågan
            except Exception as e:
                retries += 1
                wait_time = retries * 10 # Öka väntetiden mellan försök
                print(f" Fel för {b_id} (försök {retries}. Vänta {wait_time}s... Error: {e}")
                time.sleep(wait_time)

        if not success:
            print(f" Gav upp på bostad {b_id} efter {max_retries} försök.")
            osm_results[b_id] = []

        if (i + 1) % 10 == 0:
            print(f" Status: {i + 1}/{len(bostader)} bearbetade...")

    # Spara ner allt i en JSON-fil
    with open("src/data/osm_data.json", "w", encoding="utf-8") as f:
        json.dump(osm_results, f, ensure_ascii=False, indent=4)

    print("\n Klar! OSM-data genererad och sparad i src/data/osm_data.json")

if __name__ == "__main__":
    generate_osm_data()