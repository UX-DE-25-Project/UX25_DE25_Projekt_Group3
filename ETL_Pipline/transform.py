import pandas as pd

def transform(df: pd.DataFrame) -> pd.DataFrame:

    # Ta bort rader som saknar viktig information
    df_clean = df.dropna(subset=['pris', 'adress', 'stad', 'boyta'])
    
    # Gör pris och boyta till siffror
    df_clean['pris'] = pd.to_numeric(df_clean['pris'], errors='coerce')
    df_clean['boyta'] = pd.to_numeric(df_clean['boyta'], errors='coerce')
    
    # Ta bort rader med ogiltigt pris eller ogiltig boyta
    df_clean = df_clean[(df_clean['pris'] > 0) & (df_clean['boyta'] > 0)]
    
    return df_clean
