# RightHome 

## 🎯 Vad vi bygger

En bostadsportal där användare kan:
- Logga in och kolla lägenheter
- Filtrera på boyta, pris, rum
- Ställa sig i kö
- Samla poäng

## ✅ Vad vi gjort hittills

### 1. Fake data (1000 bostäder)
- Genererat 1000 st fake bostäder med all nödvändig info:
  - Adress, stad, antal rum, boyta, månadshyra
- Ligger i `data/bostader.json`

### 2. ETL-pipeline (Python) - pågående
- **`extract.py`** - Läser in JSON-filen och returnerar en pandas DataFrame (KLAR)
- **`transform.py`** - Rensar data (EJ GJORD ÄN)
- **`load.py`** - Laddar till Supabase (EJ GJORD ÄN)

