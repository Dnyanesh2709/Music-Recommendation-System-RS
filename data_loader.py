import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def search_song(query: str):
    params = {"method": "track.search", "track": query,
              "api_key": API_KEY, "format": "json", "limit": 5}
    r = requests.get(BASE_URL, params=params).json()
    tracks = r['results']['trackmatches']['track']
    return [{"name": t['name'], "artist": t['artist'],
             "id": f"{t['artist']}||{t['name']}",
             "album": "",
             "image": t['image'][-1]['#text'] if t['image'] else None
            } for t in tracks]

def get_similar_songs(artist: str, track: str, limit=20):
    params = {"method": "track.getSimilar", "artist": artist,
              "track": track, "api_key": API_KEY,
              "format": "json", "limit": limit}
    r = requests.get(BASE_URL, params=params).json()
    tracks = r.get('similartracks', {}).get('track', [])
    return [{"name": t['name'],
             "artist": t['artist']['name'],
             "id": f"{t['artist']['name']}||{t['name']}",
             "image": t['image'][-1]['#text'] if t['image'] else None,
             "similarity": round(float(t['match']) * 100, 1)
            } for t in tracks]