import pandas as pd
 
df = pd.read_csv("bostader.csv")
 
# Sparade alternativer för demo-bostäder, matcha UX-design
sparade_ids = [6, 27, 30]
df["sparad"] = 0
df.loc[df["id"].isin(sparade_ids), "sparad"] = 1
 
df.to_csv("bostader.csv", index=False)
 
# Check
print(df[df["sparad"] == 1][["id", "adress", "sparad"]])
print(f"\nKlar — {df['sparad'].sum()} bostäder markerade som sparade")