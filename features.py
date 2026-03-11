from sklearn.preprocessing import MinMaxScaler

AUDIO_FEATURES = [
    'danceability',
    'energy',
    'key',
    'loudness',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo'
]

def normalize_features(df):
    scaler = MinMaxScaler()
    df = df.copy()
    df[AUDIO_FEATURES] = scaler.fit_transform(df[AUDIO_FEATURES])
    return df, scaler

def get_feature_vector(features_df, track_id):
    row = features_df[features_df['id'] == track_id]
    if row.empty:
        return None
    return row[AUDIO_FEATURES].values[0]