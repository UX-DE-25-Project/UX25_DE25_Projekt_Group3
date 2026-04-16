import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

# Ladda miljövariabler
load_dotenv("../.env")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_KEY:
    print("FEL: Kunde inte hitta SUPABASE_KEY i .env-filen!")
    print(f"Letade i: {os.path.abspath('../.env')}")
    exit()
else:
    print(f"Nyckel hittad! Den börjar med: {SUPABASE_KEY[:10]}...")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Ladda CSV:er
df_platser = pd.read_csv("platser.csv")
df_platser = df_platser.rename(columns={
    "område": "kommun",
    "plats_id": "id"
})
df_bostader = pd.read_csv("bostader.csv")
df_priser   = pd.read_csv("priser.csv")

# Konvertera till rätt format
df_bostader["created_at"] = df_bostader["created_at"].astype(str)
df_bostader["tillgänglig"] = df_bostader["tillgänglig"].astype(bool)

# ── Ladda upp i rätt ordning ──────────────────────────
# 1. platser först (eftersom bostader refererar till den)
print(" Laddar upp platser...")
supabase.table("platser").upsert(df_platser.to_dict(orient="records")).execute()
print(f"{len(df_platser)} platser uppladdade!")

# 2. bostader
print(" Laddar upp bostader...")
supabase.table("bostader").upsert(df_bostader.to_dict(orient="records")).execute()
print(f"{len(df_bostader)} bostäder uppladdade!")

# 3. priser sist (refererar till bostader)
print(" Laddar upp priser...")
supabase.table("priser").upsert(df_priser.to_dict(orient="records")).execute()
print(f"{len(df_priser)} priser uppladdade!")

print("\n All data uppladdad till Supabase!")