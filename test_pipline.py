import pandas as pd
from ETL_Pipline.extract import extract
from ETL_Pipline.transform import transform

print("=" * 40)
print("STEG 1 — Testar extract()")
print("=" * 40)
df_raw = extract("ETL_Pipline/right_home_cleaned.csv")
if df_raw is None:
    print("FAIL — kunde inte läsa filen")
else:
    print(f"OK — {len(df_raw)} rader, {len(df_raw.columns)} kolumner")
    print(f"Kolumner: {list(df_raw.columns)}\n")

print("=" * 40)
print("STEG 2 — Testar transform()")
print("=" * 40)
df_bostader, df_priser, df_platser = transform(df_raw)
print(f"OK — bostader: {len(df_bostader)} rader")
print(f"OK — priser:   {len(df_priser)} rader")
print(f"OK — platser:  {len(df_platser)} rader\n")

print("=" * 40)
print("STEG 3 — Sneak peek på datan")
print("=" * 40)
print("Bostader:")
print(df_bostader.head(2))
print("\nPriser:")
print(df_priser.head(2))
print("\nPlatser:")
print(df_platser.head(2))