import pandas as pd

def transform(df: pd.DataFrame):
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

    # ── Tabell 1: platser ──────────────────────────────
    df_platser = df[["område", "stad"]].drop_duplicates().reset_index(drop=True)
    df_platser["plats_id"] = df_platser.index + 1

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

    print(f"   Transform klar — {len(df)} rena rader")
    print(f"   Städer: {df['stad'].unique()}")
    print(f"   Typer: {df['typ'].unique()}")
    print(f"   Datum från: {df['created_at'].min().date()} till {df['created_at'].max().date()}")

    return df_bostader, df_priser, df_platser


if __name__ == "__main__":
    from extract import extract
    df_raw = extract("../src/data/bostader.json")
    df_bostader, df_priser, df_platser = transform(df_raw)

    df_platser.to_csv("platser.csv", index=False)
    df_bostader.to_csv("bostader.csv", index=False)
    df_priser.to_csv("priser.csv", index=False)

    print("CSV:er sparade: platser.csv, bostader.csv, priser.csv")