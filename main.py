# main.py
from extract import extract 


def main():
    print("Startar RightHome ETL-pipeline...\n")
    
    # STEG 1: EXTRACT
    df_raw = extract("data/bostader.json")
    print(f"   Antal rader inlästa: {len(df_raw)}")
    print(f"   Kolumner: {list(df_raw.columns)}\n")
    
    #  STEG 2: TRANSFORM (kommer snart)
    # df_clean = transform(df_raw)
    
    #  STEG 3: LOAD till Supabase (efter Supabase är uppsatt)
    # load(df_clean)
    
    print("Extract klar! Nästa steg: Transform")

if __name__ == "__main__":
    main()


