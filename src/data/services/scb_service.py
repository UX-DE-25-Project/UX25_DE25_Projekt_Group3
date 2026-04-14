import requests
import json

def get_scb_population_v2():
    """
    Hämtar statistik via (SCB) PxWebApi v2.
    Vi fokuserar på tabellen för folkmängd per år.
    """