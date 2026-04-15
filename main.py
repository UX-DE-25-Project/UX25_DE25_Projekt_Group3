# main.py
import json
import pandas as pd
from ETL_Pipline.extract import extract 
from ETL_Pipline.transform import transform


def main():
    print("Startar RightHome ETL-pipeline...\n")
    
    # STEG 1: EXTRACT
    df_raw = extract("src/data/bostader.json")
    print(f"   Antal rader inlästa: {len(df_raw)}")
    print(f"   Kolumner: {list(df_raw.columns)}\n")
    
    #  STEG 2: TRANSFORM (+ SCB-data)
    df_enriched = transform(df_raw, stats)
    
    #  STEG 3: LOAD till Supabase (efter Supabase är uppsatt)
    # load(df_clean)
    
    print("Extract + transform klar! Nästa steg: Load")

if __name__ == "__main__":
    main()


