# main.py
import json
import pandas as pd
from ETL_Pipline.extract import extract 
from ETL_Pipline.transform import transform


def main():
    print("Startar RightHome ETL-pipeline...\n")
    
    # STEG 1: EXTRACT
    df_raw = extract("src/data/bostader.json")
    # Hämta SCB-datan
    with open("src/data/scb_stats.json", "r", encoding="utf-8") as f:
        scb_stats = json.load(f)
    
    print(f"   Antal rader inlästa: {len(df_raw)}")
    print(f"   Kolumner: {list(df_raw.columns)}\n")
    
    #  STEG 2: TRANSFORM (+ SCB-data)
    df_enriched = transform(df_raw, scb_stats)
    # Spara den nya datan lokalt innan Load till Supabase
    df_enriched.to_json("src/data/bostader_rich.json", orient="records", force_ascii=False, indent=4)
    
    print("Extract + transform klar! Filen 'bostader_rich.json' skapad.")
    print("Nästa steg: Load till Supabase (när det är uppsatt).")

if __name__ == "__main__":
    main()

        #  STEG 3: LOAD till Supabase (efter Supabase är uppsatt)
    # load(df_clean)



