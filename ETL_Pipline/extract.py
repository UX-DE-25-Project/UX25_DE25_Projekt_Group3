import pandas as pd

def extract(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, encoding="utf-8")
    print(f"Extraherade {len(df)} rader")
    return df 