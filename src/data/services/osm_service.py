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
      node[]