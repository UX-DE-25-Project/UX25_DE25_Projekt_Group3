import pandas as pd

def transform(df: pd.DataFrame) -> pd.DataFrame:

    # Rätt kolumnnamn (er JSON har latitude/longitude, inte koordinater.lat/lon)
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

    # Fixa created_at — från string "2025-08-19" till riktig datum
    df["created_at"] = pd.to_datetime(df["created_at"], format="%Y-%m-%d")

    # Lägg till valuta-kolumn
    df["valuta"] = "SEK"

    # Lägg till enhet för boyta
    df["boyta_enhet"] = "m²"

    # Beräkna pris per kvm (kontroll mot befintlig kvadratmeterpris)
    df["pris_per_kvm"] = (df["pris"] / df["boyta"]).round(0)

    # Normalisera textvärden
    df["typ"]            = df["typ"].str.lower().str.strip()
    df["upplåtelseform"] = df["upplåtelseform"].str.lower().str.strip()
    df["område"]         = df["område"].str.strip()
    df["stad"]           = df["stad"].str.strip()

    # Rensa bort rader med kritiska nullvärden
    df = df.dropna(subset=["pris", "lat", "lon", "område", "stad"])

    # Ta bort dubletter
    df = df.drop_duplicates(subset=["id"])

    print(f"   Transform klar — {len(df)} rena rader")
    print(f"   Städer: {df['stad'].unique()}")
    print(f"   Typer: {df['typ'].unique()}")
    print(f"   Datum från: {df['created_at'].min().date()} till {df['created_at'].max().date()}")

    return df