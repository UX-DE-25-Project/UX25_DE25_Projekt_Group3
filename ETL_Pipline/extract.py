import pandas as pd 
import json 

def extract(filepath: str) -> pd.DataFrame:
    """
    Extracts data from a JSON file and returns it as a pandas DataFrame.

    Parameters:
    filepath (str): The path to the JSON file.

    Returns:
    pd.DataFrame: A DataFrame containing the extracted data.
    """
    with open(filepath, 'r', encoding = "utf-8") as file:
        data = json.load(file)
    
    df = pd.json_normalize(data) # Om JSON-strukturen är komplex, kan json_normalize hjälpa till att platta ut den till en tabellform.
    print(f"extraherade {len(df)} bostäder")
    return df 

if __name__ == "__main__":
    df = extract("../src/data/bostader.json")
    print(df.head()) 