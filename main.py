# main.py
import json
import pandas as pd
from ETL_Pipline.extract import extract 
from ETL_Pipline.transform import transform
from ETL_Pipline.load_to_supabase import load


def main():
    print("Startar RightHome ETL-pipeline...\n")
    
    # STEG 1: EXTRACT
    print("STEG 1: Extraherar data...")
    df_raw = extract("src/data/bostader.json")
    # Hämta SCB-datan
    with open("src/data/scb_stats.json", "r", encoding="utf-8") as f:
        scb_stats = json.load(f)
    
    print(f"   Antal rader inlästa: {len(df_raw)}")
    print(f"   Kolumner: {list(df_raw.columns)}\n")
    
    #  STEG 2: TRANSFORM (+ SCB-data)
    print("STEG 2: Transformerar data och berikar med SCB-statistik...")
    # Tre nya tabeller som transform returnerar
    df_bostader, df_priser, df_platser = transform(df_raw, scb_stats)
    
    # Spara kopior lokalt
    df_bostader.to_csv("src/data/bostader_rich.csv", index=False)
    df_priser.to_csv("src/data/priser_rich.csv", index=False)
    df_platser.to_csv("src/data/platser_rich.csv", index=False)

    # STEG 3: LOAD
    print("STEG 3: Laddar upp till Supabase...")
    load(df_bostader, df_priser, df_platser)
    
    print("\n Allt klart! Databasen är nu uppdaterad med SCB-berikad data.")

if __name__ == "__main__":
    main()