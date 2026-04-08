import duckdb
import pandas as pd

con = duckdb.connect(database=':memory:')

con.execute("""
    CREATE OR REPLACE VIEW bostader AS
    SELECT * FROM read_json_auto('src/data/bostader.json')
""")

print("EDA - Bostadsmarknaden(Stockholm, Göteborg och Malmö)\n" + "-"*50)

# Analys 1: Priskoll - Genomsnittligt pris per stad
print("\n1. Snittpriser och storlek per stad (endast köp):")
query_stad = """
    SELECT
        stad,
        COUNT(*) AS antal objekt,
        ROUND(AVG(pris)) AS snittpris,
        ROUND(AVG(boyta)) AS snitt_boyta_m2,
        ROUND(AVG(kvadratmeterpris), 0) AS snitt_kr_per_m2
    FROM bostader
    WHERE upplåtelseform = 'köpa'
    GROUP BY stad
    ORDER BY snitt_kr_per_m2 DESC
"""

df_stad = con.execute(query_stad).df()
print(df_stad.to_string(index=False))