import json
import os
import pandas as pd
from ETL_Pipline.extract import extract
from ETL_Pipline.transform import transform

def load_local_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def main():
    print("Startar RightHome ETL-pipeline...\n")
    
    # Extraherar rådata från JSON-fil
    input_file = "src/data/bostader.json"
    print(f"Läser in rådata från: {input_file}")
    
    df_raw = extract(input_file)

    if df_raw is None:
        print("Kunde inte läsa datafilen.")
        return
    
    # Ladda SCB och OSM-data
    # Ladda sparade JSON-filer för att undvika errors och annat
    scb_stats = load_local_json("src/data/scb_stats.json")
    osm_data = load_local_json("src/data/osm_data.json")

    # Transformera data
    print("Transformerar data (inklusive SCB och OSM)...")
    df_bostader, df_priser, df_platser = transform(df_raw, scb_stats=scb_stats, osm_data=osm_data)

    # Sparar filerna i ETL_Pipline mappen
    print("\n Sparar ren data som CSV-filer för Power BI...")
    output_path = "ETL_Pipline/"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    df_bostader.to_csv(f"{output_path}bostader.csv", index=False)
    df_platser.to_csv(f"{output_path}platser.csv", index=False)
    df_priser.to_csv(f"{output_path}priser.csv", index=False)

    print(f"Klart! Filer sparade i {output_path}")
    print(f" - {len(df_bostader)} bostäder bearbetade")
    print(f" - {len(df_platser)} platser bearbetade")
    print(f" - {len(df_priser)} priser bearbetade")

if __name__ == "__main__":
    main()