# main.py
from extract import extract
from transform import transform
from load import load
from dotenv import load_dotenv

load_dotenv()  # läser in .env-filen

def main():
    print("Startar RightHome ETL-pipeline...\n")

    df_raw   = extract("data/bostader.json")
    df_clean = transform(df_raw)
    load(df_clean)

    print("\nPipeline klar! Datan är live i Supabase.")

if __name__ == "__main__":
    main()