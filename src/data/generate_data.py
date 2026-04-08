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

def slumpa_koordinat(område):
    bas = koordinater[område]
    return {
        "lat": round(bas["lat"] + random.uniform(-0.01, 0.01), 5),
        "lon": round(bas["lon"] + random.uniform(-0.01, 0.01), 5)
    }

def generera_bostad(id):
    typ = random.choice(["lägenhet", "hus"])
    upplåtelseform = random.choice(["hyra", "köpa"])
    stad = random.choice(list(städer.keys()))
    område = random.choice(städer[stad]) # väljer område baserat på stad
    rum = random.randint(1, 6)
    boyta = rum * random.randint(18, 28)
    random_days = random.randint(0, 10)
    created_at = (datetime.now() - timedelta(days=random_days)).strftime("%Y-%m-%d")

    if upplåtelseform == "hyra":
        pris = random.randint(6000, 20000)
    else:
        pris = random.randint(1000000, 5000000)

    gata = random.choice(gatunamn)
    nummer = random.randint(1, 120)

    return {
        "id": id,
        "typ": typ,
        "upplåtelseform": upplåtelseform,
        "pris": pris,
        "rum": rum,
        "boyta": boyta,
        "område": område,
        "stad": stad,
        "adress": f"{gata} {nummer}",
        "koordinater": slumpa_koordinat(område),
        "tillgänglig": random.choice([True, True, True, False]),
        "created_at": created_at
    }

bostäder = [generera_bostad(i) for i in range(1, 1001)]

with open("src/data/bostader.json", "w", encoding="utf-8") as f:
    json.dump(bostäder, f, ensure_ascii=False, indent=2)

print("1000 bostäder genererade och sparade i src/data/bostader.json")
