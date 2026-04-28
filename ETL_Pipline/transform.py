import pandas as pd
import json
 
def transform(df: pd.DataFrame, scb_stats=None, osm_data=None):
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
 
    # Sparad som int
    if "sparad" in df.columns:
        df["sparad"] = pd.to_numeric(df["sparad"], errors="coerce").fillna(0).astype(int)
    else:
        df["sparad"] = 0
 
    df = df.dropna(subset=["pris", "lat", "lon", "område", "stad"])
    df = df.drop_duplicates(subset=["id"])
 
    # ── Tabell 1: platser ──────────────────────────────
    df_platser = df[["område", "stad"]].drop_duplicates().reset_index(drop=True)
    df_platser["plats_id"] = df_platser.index + 1
 
    if scb_stats:
        print("SCB-data integrerad i platser.")
        # DEBUG
        print(f"DEBUG Sthlm: {scb_stats.get('Stockholm')}")
 
        pop_map = {}
        for key, info in scb_stats.items():
            clean_key = str(key).lower().replace("kommun", "").strip()
 
            pop_val = None
 
            # Om JSON-filen bara är {"Stockholm": 995574}
            if isinstance(info, (int, str, float)):
                pop_val = info
 
            # Om JSON-filen är en dictionary {"Stockholm": {"folkmangd": 995574}}
            elif isinstance(info, dict):
                pop_val = info.get("folkmangd") or info.get("folkmängd") or info.get("befolkning") or info.get("Population")
                
            if isinstance(pop_val, list) and len(pop_val) > 0:
                pop_val = pop_val[0] # Första värdet i listan
 
            try:
                if pop_val is not None and str(pop_val).strip() != "N/A":
                    clean_pop = str(pop_val).replace(" ", "").replace("\xa0", "")
                    pop_map[clean_key] = int(clean_pop)
            except (ValueError, TypeError):
                continue
 
        df_platser["kommun_befolkning"] = df_platser["stad"].str.lower().str.replace("kommun", "").str.strip().map(pop_map).astype("Int64")
 
        hits = df_platser["kommun_befolkning"].notna().sum()
        print(f"   SCB-data matchade {hits} av {len(df_platser)} platser.")
 
    # Koppla plats_id tillbaka till huvudtabellen
    df = df.merge(df_platser, on=["område", "stad"], how="left")
 
    # ── Tabell 2: bostader (+ OSM) ─────────────────────────────
    df_bostader = df[[
        "id", "typ", "upplåtelseform", "rum", "boyta",
        "boyta_enhet", "tillgänglig", "created_at",
        "adress", "lat", "lon", "plats_id", "sparad"
    ]].copy()
 
    # OSM-data: Skapa kolumner för Points of Interest
    if osm_data:
        print("OSM-data integrerad i bostäder.")
 
        # Kolumner med 0 som standardvärde
        kategorier = ["Kollektivtrafik", "Utbildning & Kultur", "Mat & Shopping", "Fritid", "Religion & Tro", "Hälsa", "Övrigt"]
        for cat in kategorier:
            # Snygga till kolumnnamn
            col_name = "poi_" + cat.lower().replace(" & ", "_").replace("ä", "a").replace("ö", "o").replace(" ", "_") 
            df_bostader[col_name] = 0
 
        # Data baserat på bostadens ID
        for bostad_id, places in osm_data.items():
            if not places: continue
 
            # Antalet platser per kategori för just denna bostad
            cat_counts = {}
            for p in places:
                c = p.get("category")
                cat_counts[c] = cat_counts.get(c, 0) + 1
                
            # Uppdatera rätt rad i DF
            idx = df_bostader.index[df_bostader['id'] == int(bostad_id)]
            if not idx.empty:
                for cat, count in cat_counts.items():
                    col_name = "poi_" + cat.lower().replace(" & ", "_").replace(" ", "_").replace("ä", "a").replace("ö", "o")
                    if col_name in df_bostader.columns:
                        df_bostader.loc[idx, col_name] = count
                
    # ── Tabell 3: priser ───────────────────────────────
    df_priser = df[[
        "id", "pris", "avgift",
        "kvadratmeterpris", "pris_per_kvm", "valuta"
    ]].rename(columns={"id": "bostad_id"})
 
    # ── Tabell 4: visningar ────────────────────────────
    df_visningar = pd.DataFrame([
        {"bostad_id": 1, "adress": "Storgatan 12", "visningsdatum": "2026-04-24", "starttid": "13:00", "sluttid": "14:00"},
        {"bostad_id": 2, "adress": "Parkvägen 5",  "visningsdatum": "2026-04-27", "starttid": "10:30", "sluttid": "11:30"},
    ])
    df_visningar["visningsdatum"] = pd.to_datetime(df_visningar["visningsdatum"])
 
    print(f"   Transform klar — {len(df)} rena rader")
    print(f"   Städer: {df['stad'].unique()}")
    print(f"   Typer: {df['typ'].unique()}")
    print(f"   Datum från: {df['created_at'].min().date()} till {df['created_at'].max().date()}")
 
    return df_bostader, df_priser, df_platser, df_visningar
 
if __name__ == "__main__":
    from extract import extract
 
    # Lokal test av transform-funktionen
    df_raw = extract("../src/data/bostader.json")
    
    # Ladda SCB
    try:
        with open("../src/data/scb_stats.json", "r", encoding="utf-8") as f:
            scb_data = json.load(f)
    except FileNotFoundError:
        scb_data = None
 
    # Ladda OSM
    try:
        with open("../src/data/osm_data.json", "r", encoding="utf-8") as f:
            osm_data = json.load(f)
    except FileNotFoundError:
        osm_data = None
 
    # Ladda OSM (Ex: hur mock-data kan se ut under utveckling...)
    # Laddas in från en fil genererat via api:et
    mock_osm_data = {
        # Exempeldata: bostad med id 123 har 3 närliggande platser, varav 2 är kollektivtrafik och 1 är mat & shopping
        "123": [{"category": "Kollektivtrafik"}, {"category": "Kollektivtrafik"}, {"category": "Mat & Shopping"}]
    }
    
    df_bostader, df_priser, df_platser, df_visningar = transform(df_raw, scb_stats=scb_data, osm_data=mock_osm_data)
 
    df_platser.to_csv("platser.csv", index=False)
    df_bostader.to_csv("bostader.csv", index=False)
    df_priser.to_csv("priser.csv", index=False)
    df_visningar.to_csv("visningar.csv", index=False)
 
    print("CSV:er sparade lokalt: platser.csv, bostader.csv, priser.csv, visningar.csv")
