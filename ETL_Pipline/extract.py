import pandas as pd

def extract(filepath: str) -> pd.DataFrame:
    """
    Detta ska läsa in data från antingen en CSV-fil eller en JSON-fil och returnera en DataFrame.
    """
    try:
        if filepath.endswith('.json'):
            df = pd.read_json(filepath)
        else:
            df = pd.read_csv(filepath, encoding="utf-8")

        print(f"Extraherade {len(df)} rader från {filepath}")
        return df
    
    except Exception as e:
        print(f"Fel vid extrahering av {filepath}: {e}")
        return None