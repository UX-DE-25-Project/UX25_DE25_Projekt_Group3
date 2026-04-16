import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

# Ladda miljövariabler
load_dotenv("../.env")

def load(df_bostader, df_priser, df_platser):
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if not SUPABASE_KEY:
        print("FEL: Kunde inte hitta SUPABASE_KEY i .env-filen!")
        print(f"Letade i: {os.path.abspath('../.env')}")
        return

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    # 1. Förbered platser (Specifika namnbyten)
    print("Förbereder platser...")
    df_platser_upload = df_platser.rename(columns={
        "område": "kommun",
        "plats_id": "id"
    })

    # 2. Förbered bostäder (Datatyper)
    df_bostader_upload = df_bostader.copy()
    df_bostader_upload["created_at"] = df_bostader_upload["created_at"].astype(str)
    df_bostader_upload["tillgänglig"] = df_bostader_upload["tillgänglig"].astype(bool)

    # - Detta bör laddas upp i rätt ordning -

    try:
        # 1. platser först
        print("Laddar upp platser...")
        supabase.table("platser").upsert(df_platser_upload.to_dict(orient="records")).execute()
        print(f" {len(df_platser_upload)} platser uppladdade!")

        # 2. bostader
        print("Laddar upp bostader...")
        supabase.table("bostader").upsert(df_bostader_upload.to_dict(orient="records")).execute()
        print(f" {len(df_bostader_upload)} bostäder uppladdade!")

        # 3. priser sist
        print("Laddar upp priser...")
        supabase.table("priser").upsert(df_priser.to_dict(orient="records")).execute()
        print(f" {len(df_priser)} priser uppladdade!")

    except Exception as e:
        print(f"Fel vid uppladdning: {e}")

# Så att filen kan fortfarande köras självständigt:
if __name__ == "__main__":
    print("Kör som fristående skript - läser lokala CSV-filer...")
    df_p = pd.read_csv("src/data/platser_clean.csv")
    df_b = pd.read_csv("src/data/bostader_clean.csv")
    df_pr = pd.read_csv("src/data/priser_clean.csv")
    load(df_b, df_pr, df_p)