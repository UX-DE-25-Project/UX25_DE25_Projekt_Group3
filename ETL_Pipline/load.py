import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

load_dotenv("../.env")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def load(df: pd.DataFrame, tabell: str):
    if tabell == "platser":
        df = df.rename(columns={"område": "kommun", "plats_id": "id"})
    
    if tabell == "bostader":
        df["created_at"] = df["created_at"].astype(str)
        df["tillgänglig"] = df["tillgänglig"].astype(bool)

    print(f"Laddar upp {tabell}...")
    supabase.table(tabell).upsert(df.to_dict(orient="records")).execute()
    print(f"{len(df)} rader uppladdade till '{tabell}'!")