import duckdb
import pandas as pd

con = duckdb.connect(database=':memory:')

con.execute("""
    CREATE OR REPLACE VIEW bostader AS
    SELECT * FROM read_json_auto('src/data/bostader.json')
""")

print