import pandas as pd
import json

def transform(df: pd.DataFrame, scb_stats=None):
    # Byt namn på kolumner
    df = df.rename(columns={
        "latitude": "lat",
        "longitude": "lon"
    })

    # Rätt datatyper
    df["id"]               = df["id"].astype(int)
    df["pris"]             = pd.to_numeric(df["pris"], errors="coerce")
    df["avgift"]           = pd.to_numeric(df["avgift"], errors="coerce")
    df["rum"]              = pd.to_numeric(df["rum"], errors="coerce").astype("Int64")
    df["boyta"]            = pd.to_numeric(df["boyta"], errors="coerce")
    df["kvadratmeterpris"] = pd.to_numeric(df["kvadratmeterpris"], errors="coerce")
    df["tillgänglig"]      = df["tillgänglig"].astype(bool)
    df["created_at"]       = pd.to_datetime(df["created_at"], format="%Y-%m-%d")
    df["valuta"]           = "SEK"
    df["boyta_enhet"]      = "m²"
    df["pris_per_kvm"]     = (df["pris"] / df["boyta"]).round(0)
    df["typ"]              = df["typ"].str.lower().str.strip()
    df["upplåtelseform"]   = df["upplåtelseform"].str.lower().str.strip()
    df["område"]           = df["område"].str.strip()
    df["stad"]             = df["stad"].str.strip()
    df = df.dropna(subset=["pris", "lat", "lon", "område", "stad"])
    df = df.drop_duplicates(subset=["id"])

    # Tar bort saknade värden och dubletter
    df = df.dropna(subset=["pris", "lat", "lon", "område", "stad"])
    df = df.drop_duplicates(subset=["id"])

    # ── Tabell 1: platser ──────────────────────────────
    df_platser = df[["område", "stad"]].drop_duplicates().reset_index(drop=True)
    df_platser["plats_id"] = df_platser.index + 1

    # SCB-data
    if scb_stats:
        print("   Berikar platsdata med SCB-statistik...")
        pop_map = {}
        for stad, info in scb_stats.items():
            val = info["folkmangd"]
            pop_val = val if isinstance(val, list) else val
            pop_map[stad] = int(pop_val) if pop_val != "N/A" else None

        # Befolkningen baserat på stad
        df_platser['kommun_befolkning'] = df_platser['stad'].map(pop_map)
        # Pandas "Int64" för att hantera eventuella tomma värden (NaN) utan att det blir floats
        df_platser['kommun_befolkning'] = df_platser['kommun_befolkning'].astype("Int64")

    # Koppla plats_id tillbaka till huvudtabellen
    df = df.merge(df_platser, on=["område", "stad"], how="left")

    # ── Tabell 2: bostader ─────────────────────────────
    df_bostader = df[[
        "id", "typ", "upplåtelseform", "rum", "boyta",
        "boyta_enhet", "tillgänglig", "created_at",
        "adress", "lat", "lon", "plats_id"
    ]]

    # ── Tabell 3: priser ───────────────────────────────
    df_priser = df[[
        "id", "pris", "avgift",
        "kvadratmeterpris", "pris_per_kvm", "valuta"
    ]].rename(columns={"id": "bostad_id"})

    print(f" Transform klar — {len(df)} rena rader")
    print(f" Städer: {df['stad'].unique()}")
    print(f" Typer: {df['typ'].unique()}")
    print(f" Datum från: {df['created_at'].min().date()} till {df['created_at'].max().date()}")

    return df_bostader, df_priser, df_platser

# Lokal testning av transform.py
if __name__ == "__main__":
    from extract import extract
    
    print("--- Testkör transform.py ---")
    df_raw = extract("../src/data/bostader.json")
    
    # SCB-datan för lokal testning av filen
    try:
        with open("../src/data/scb_stats.json", "r", encoding="utf-8") as f:
            scb_data = json.load(f)
    except FileNotFoundError:
        scb_data = None
        
    df_bostader, df_priser, df_platser = transform(df_raw, scb_data)

    # Lokala filer, snabb inspektion
    df_platser.to_csv("platser.csv", index=False)
    df_bostader.to_csv("bostader.csv", index=False)
    df_priser.to_csv("priser.csv", index=False)

    print("CSV:er sparade i src/data/")