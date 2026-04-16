from ETL_Pipline.extract import extract
from ETL_Pipline.transform import transform
from ETL_Pipline.load import load

def main():
    print("Startar RightHome ETL-pipeline...\n")

    df_raw = extract("ETL_Pipline/right_home_cleaned.csv")
    if df_raw is None:
        print("Kunde inte läsa datafilen.")
        return

    df_bostader, df_priser, df_platser = transform(df_raw)

    load(df_platser, "platser")
    load(df_bostader, "bostader")
    load(df_priser, "priser")

    print("\nAlla pipelines klara!")

if __name__ == "__main__":
    main()