from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import json

app = Flask(__name__)
CORS(app)  # Tillåt anrop från din HTML

# Ladda in dina CSV-filer
def load_data():
    try:
        bostader = pd.read_csv('bostader.csv')
        priser = pd.read_csv('priser.csv')
        platser = pd.read_csv('platser.csv')
        cleaned = pd.read_csv('right_home_cleaned.csv')
        return bostader, priser, platser, cleaned
    except Exception as e:
        print(f"Fel vid laddning: {e}")
        return None, None, None, None

bostader, priser, platser, cleaned = load_data()

# API endpoint för att hämta alla bostäder
@app.route('/api/bostader', methods=['GET'])
def get_bostader():
    if bostader is not None:
        return jsonify(bostader.to_dict(orient='records'))
    return jsonify([])

# API endpoint för statistik
@app.route('/api/statistik', methods=['GET'])
def get_statistik():
    if bostader is not None:
        stats = {
            'antal_bostader': len(bostader),
            'snittpris': int(bostader['pris'].mean()) if 'pris' in bostader.columns else 0,
            'tillgangliga': len(bostader[bostader['status'] == 'ledig']) if 'status' in bostader.columns else len(bostader),
            'pris_per_kvm': int(bostader['pris_per_kvm'].mean()) if 'pris_per_kvm' in bostader.columns else 0
        }
        return jsonify(stats)
    return jsonify({})

# API endpoint för filtrering
@app.route('/api/filtrera', methods=['POST'])
def filtrera_bostader():
    data = request.json
    if bostader is None:
        return jsonify([])
    
    filtered = bostader.copy()
    
    # Filtrera på pris
    if 'max_pris' in data and data['max_pris']:
        filtered = filtered[filtered['pris'] <= data['max_pris']]
    
    # Filtrera på boyta
    if 'min_boyta' in data and data['min_boyta']:
        filtered = filtered[filtered['boyta'] >= data['min_boyta']]
    
    # Filtrera på rum
    if 'rum' in data and data['rum']:
        filtered = filtered[filtered['rum'] == data['rum']]
    
    # Filtrera på typ (hyra/köpa)
    if 'typ' in data and data['typ']:
        filtered = filtered[filtered['upplåtelseform'].str.lower() == data['typ'].lower()]
    
    # Filtrera på område
    if 'omrade' in data and data['omrade']:
        filtered = filtered[filtered['område'].str.contains(data['omrade'], case=False, na=False)]
    
    return jsonify(filtered.to_dict(orient='records'))

# API endpoint för prispunkter på kartan
@app.route('/api/prispunkter', methods=['GET'])
def get_prispunkter():
    if priser is not None:
        return jsonify(priser.to_dict(orient='records'))
    return jsonify([])

# API endpoint för platser/aktiviteter
@app.route('/api/platser', methods=['GET'])
def get_platser():
    if platser is not None:
        return jsonify(platser.to_dict(orient='records'))
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=5000)