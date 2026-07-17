"""Music Recommender Simulation: load songs, score them against a user profile, and rank the top matches."""
import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts, converting numeric fields to numbers."""
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            for key in int_fields:
                song[key] = int(song[key])
            for key in float_fields:
                song[key] = float(song[key])
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against a user profile, returning (score, reasons) using the Algorithm Recipe."""
    score = 0.0
    reasons: List[str] = []

    # Categorical exact-match bonuses.
    if user_prefs.get("favorite_genre") == song["genre"]:
        score += 2.5
        reasons.append(f"genre match: {song['genre']} (+2.5)")
    if user_prefs.get("favorite_mood") == song["mood"]:
        score += 2.0
        reasons.append(f"mood match: {song['mood']} (+2.0)")

    # Numeric closeness on the 0 to 1 features: reward small distance to the target.
    numeric_features = [
        ("target_energy", "energy", 1.5),
        ("target_valence", "valence", 1.5),
        ("target_danceability", "danceability", 1.0),
        ("target_acousticness", "acousticness", 1.0),
    ]
    for pref_key, song_key, weight in numeric_features:
        target = user_prefs.get(pref_key)
        if target is not None:
            similarity = max(0.0, 1 - abs(song[song_key] - target))
            points = weight * similarity
            score += points
            reasons.append(f"{song_key} similarity: +{points:.2f}")

    # Tempo closeness, normalized by 100 BPM so it cannot swamp the other features.
    target_tempo = user_prefs.get("target_tempo_bpm")
    if target_tempo is not None:
        similarity = max(0.0, 1 - abs(song["tempo_bpm"] - target_tempo) / 100)
        points = 1.0 * similarity
        score += points
        reasons.append(f"tempo similarity: +{points:.2f}")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, drop already-heard ones, and return the top k as (song, score, explanation)."""
    heard = set(user_prefs.get("heard_ids", []))
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        if song["id"] in heard:
            continue
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
