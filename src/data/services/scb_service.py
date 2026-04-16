import requests
import json
import os

def get_scb_population_v2():
    """
    Hämtar statistik via (SCB) PxWebApi v2.
    Vi fokuserar på tabellen för folkmängd per år.
    """

    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101A/BefolkningNy"

    selection = {
        "query": [
            {
                "code": "Region",
                "selection": {
                    "filter": "item",
                    "values": ["0180", "1480", "1280"]  # Detta är SCB-koder för Stockholm, Göteborg och Malmö
                }
            },
            {
                "code": "ContentsCode",
                "selection": {
                    "filter": "item",
                    "values": ["BE0101N1"] # Detta är koden för total befolkning
                }
            }
        ],
        "response": {"format": "json"}
    }

    try:
        # Skicka POST-förfrågan till SCB API
        response = requests.post(
            url, 
            json=selection,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        # Regionkoderna 0180, 1480, 1280 motsvarar Stockholm, Göteborg och Malmö
        region_map = {
            "0180": "Stockholm",
            "1480": "Göteborg",
            "1280": "Malmö"
        }

        results = {}
        
        # Kontrollera strukturen på data
        if 'data' in data:
            for entry in data['data']:
                region_key = entry.get('key', [])
                values = entry.get('values', [])
                
                # Förväntar oss att region_key är en lista med en kod, och values är en lista med ett värde
                if region_key and isinstance(region_key, list):
                    region_kod = region_key[0]
                    namn = region_map.get(region_kod, region_kod)
                    
                    # values är en lista, ta första värdet eller "N/A" om den är tom
                    folkmangd = values if values else "N/A"
                                        
                    results[namn] = {
                        "folkmangd": folkmangd,
                        "uppdaterad": "2026-04-15"
                    }
        
        return results if results else data
    
    except requests.exceptions.RequestException as e:
        print(f"SCB API-fel: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parse-fel: {e}")
        return None
    except Exception as e:
        print(f"Oväntat fel: {e}")
        return None

if __name__ == "__main__":
    print("Hämtar befolkningsdata från SCB...")
    stats = get_scb_population_v2()
    
    if stats:
        # Skriv ut i terminalen
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        
        # SPARAS ny fil
        file_path = "src/data/scb_stats.json"
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
            
        print(f"\n All data har sparats i filen: {file_path}")
    else:
        print("Kunde inte hämta data från SCB.")