from data_loader import get_similar_songs

def hybrid_recommend(input_track_id: str, top_n=10):
    artist, track = input_track_id.split("||")
    results = get_similar_songs(artist, track, limit=top_n)
    return results