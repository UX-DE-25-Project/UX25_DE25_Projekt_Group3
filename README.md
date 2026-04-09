# RightHome 

## Vad vi bygger

En bostadsportal där användare kan:
- Logga in och kolla lägenheter
- Filtrera på boyta, pris, rum
- Ställa sig i kö
- Samla poäng

## Vad vi gjort hittills

### 1. Fake data (1000 bostäder)
- Genererat 1000 st fake bostäder med all nödvändig info:
  - Adress, stad, antal rum, boyta, månadshyra
- Ligger i `data/bostader.json`

### 2. ETL-pipeline (Python) - Klar
- **`extract.py`** - Läser in JSON-filen och returnerar en pandas DataFrame (KLAR)
- **`transform.py`** - Rensar data (Klar)
- **`load.py`** - Laddar till Supabase (Klar)

## Vad är EDA egentligen?

EDA (Exploratory Data Analysis) = att utforska och förstå datan innan vi bygger dashboards eller modeller.

Det handlar inte bara om grafer – utan om att svara på frågor som:
- Hur ser datan ut nu efter transform?
- Finns det fortfarande fel?
- Vad är mönstren?
- Finns det outliers (konstiga värden)?

### 3. Power BI - Visualisering (Pågår)

Vi använder Power BI för att skapa en interaktiv dashboard över våra bostäder.

**Vad vi ska visualisera:**
- Karta – alla bostäder utifrån latitude och longitude
- Prisfördelning – histogram över hyror och priser
- Bostäder per stad – stapeldiagram
- Pris per kvadratmeter – jämförelse mellan städer
- Lägenhet vs Hus – cirkeldiagram

**Datakälla:** Power BI kopplas till vår JSON-fil (bostader.json) eller Supabase-databasen.
