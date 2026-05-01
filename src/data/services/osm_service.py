import requests


def get_nearby_places(lat, lon, radius=1500):
    """
    Hämtar närliggande platser från OpenStreetMap via Overpass API.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Områden av intresse: skolor, bibliotek, parker, kollektivtrafik osv.

    query = f"""
    [out:json];
    (
      node["amenity"~"school|restaurant|bar|cafe|pharmacy|library|place_of_worship|hospital"](around:{radius},{lat},{lon});
      node["leisure"~"park|fitness_centre|playground"](around:{radius},{lat},{lon});
      node["shop"~"supermarket|mall"](around:{radius},{lat},{lon});
      node["highway"="bus_stop"](around:{radius},{lat},{lon});
      node["railway"~"station|subway_entrance"](around:{radius},{lat},{lon});
    );
    out body;
    """

    try:
        response = requests.get(overpass_url, params={'data': query}, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        places = []
        for element in data.get('elements', []):
            tags = element.get('tags', {})

            # Logik för frontend: kategorisering av platser och områden
            category = "Övrigt"
            raw_type = tags.get('amenity') or tags.get('leisure') or tags.get('shop') or tags.get('highway') or tags.get('railway')

            if raw_type in ['bus_stop', 'station', 'subway_entrance']:
                category = "Kollektivtrafik"
            elif raw_type in ['school', 'library']:
                category = "Utbildning & Kultur"
            elif raw_type in ['restaurant', 'bar', 'cafe', 'supermarket', 'mall']:
                category = "Mat & Shopping"
            elif raw_type in ['park', 'fitness_centre', 'playground']:
                category = "Fritid"
            elif raw_type == 'place_of_worship':
                category = "Religion & Tro"
            elif raw_type in ['pharmacy', 'hospital']:
                category = "Hälsa"

            places.append({
                "name": tags.get('name', 'Namnlös plats'),
                "type": raw_type,
                "category": category,
                "lat": element.get('lat'),
                "lon": element.get('lon')
            })
            
        return places

    except Exception as e:
        print(f" API-fel: {e}")
        return []
    
# Snabbtest för att se att allt faktiskt kom med
if __name__ == "__main__":
    # Testar centrala Stockholm 
    # Bör funka nu, AI korrigering
    # Reminder: Överbelasta inte API:et, uppdatering lär komma...
    results = get_nearby_places(59.3293, 18.0686)
    print(f"Analys klar! Hittade {len(results)} intressanta platser.")
    
    categories = [p['category'] for p in results]
    for cat in set(categories):
        print(f"- {cat}: {categories.count(cat)} st")