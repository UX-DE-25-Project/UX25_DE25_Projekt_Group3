import json
import random
from datetime import datetime, timedelta

områden = [
    "Södermalm", "Östermalm", "Vasastan", "Kungsholmen",
    "Lidingö", "Solna", "Nacka", "Sundbyberg",
    "Hägersten", "Bromma", "Farsta", "Spånga"
]

städer = {
    "Stockholm": [
        "Södermalm", "Östermalm", "Vasastan", "Kungsholmen"
    ],
    "Göteborg": [
        "Centrum", "Hisingen", "Majorna", "Linnéstaden"
    ],
    "Malmö": [
        "Västra Hamnen", "Rosengård", "Limhamn", "Hyllie"
    ]
}

bas_pris_per_kvm = {
    "Stockholm": 9500,
    "Göteborg": 6500,
    "Malmö": 4500
}

gatunamn = [
    "Storgatan", "Parkvägen", "Björkgatan", "Lindvägen",
    "Skolvägen", "Kyrkogatan", "Strandvägen", "Bergsgatan",
    "Drottninggatan", "Kungsgatan", "Hornsgatan", "Sveavägen"
]

koordinater = {
    "Södermalm":   {"lat": 59.3151, "lon": 18.0710},
    "Östermalm":   {"lat": 59.3380, "lon": 18.0800},
    "Vasastan":    {"lat": 59.3430, "lon": 18.0490},
    "Kungsholmen": {"lat": 59.3320, "lon": 18.0290},
    "Lidingö":     {"lat": 59.3670, "lon": 18.1500},
    "Solna":       {"lat": 59.3600, "lon": 18.0010},
    "Nacka":       {"lat": 59.3110, "lon": 18.1630},
    "Sundbyberg":  {"lat": 59.3610, "lon": 17.9710},
    "Hägersten":   {"lat": 59.3020, "lon": 18.0010},
    "Bromma":      {"lat": 59.3370, "lon": 17.9400},
    "Farsta":      {"lat": 59.2430, "lon": 18.0940},
    "Spånga":      {"lat": 59.3830, "lon": 17.9010},
    #lägger den biten - ska dubbel kolla om den är fonktionell 
    "Centrum":     {"lat": 57.7089, "lon": 11.9746},
    "Hisingen":    {"lat": 57.7300, "lon": 11.9000},
    "Majorna":     {"lat": 57.6990, "lon": 11.9330},
    "Linnéstaden": {"lat": 57.6970, "lon": 11.9520},
    "Västra Hamnen": {"lat": 55.6130, "lon": 12.9760},
    "Rosengård":   {"lat": 55.5910, "lon": 13.0320},
    "Limhamn":     {"lat": 55.5860, "lon": 12.9300},
    "Hyllie":      {"lat": 55.5620, "lon": 12.9750},
}

def generera_bostad(id):
    typ = random.choice(["lägenhet", "hus"])
    upplåtelseform = random.choice(["hyra", "köpa"])
    stad = random.choice(list(städer.keys()))
    område = random.choice(städer[stad]) # väljer område baserat på stad
    
    rum = random.randint(1, 6)
    boyta = rum * random.randint(18, 28)
    
    dagar_sen = random.randint(0, 365)
    created_at = (datetime.now() - timedelta(days=dagar_sen)).strftime("%Y-%m-%d")

    if upplåtelseform == "hyra":
        pris = int((boyta * 150) * random.uniform(0.8, 1.2))
        avgift = 0
    else:
        m2_pris = bas_pris_per_kvm[stad] * random.uniform(0.8, 1.4)
        pris = int(boyta * m2_pris)
        avgift = int((boyta * 60) * random.uniform(0.7, 1.3)) if typ == "lägenhet" else random.randint(1500, 3000)

    bas_koords = koordinater[område]
    lat = round(bas_koords["lat"] + random.uniform(-0.01, 0.01), 5)
    lon = round(bas_koords["lon"] + random.uniform(-0.01, 0.01), 5)

    gata = random.choice(gatunamn)
    nummer = random.randint(1, 120)

    return {
        "id": id,
        "typ": typ,
        "upplåtelseform": upplåtelseform,
        "pris": pris,
        "avgift": avgift,
        "rum": rum,
        "boyta": boyta,
        "kvadratmeterpris": int(pris/boyta) if upplåtelseform == "köpa" else 0,
        "område": område,
        "stad": stad,
        "adress": f"{gata} {nummer}",
        "latitude": lat,
        "longitude": lon,
        "tillgänglig": random.choice([True, True, True, False]),
        "created_at": created_at
    }

bostäder = [generera_bostad(i) for i in range(1, 1001)]

with open("src/data/bostader.json", "w", encoding="utf-8") as f:
    json.dump(bostäder, f, ensure_ascii=False, indent=2)

print("1000 bostäder genererade och sparade i src/data/bostader.json")
print(f"Data redo för Supabase, inkluderar 'avgift', 365 dagars historik mm.") 
