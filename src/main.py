"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


# Distinct taste profiles used to stress-test the recommender.
PROFILES = {
    "High-Energy Pop Lover": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_valence": 0.80,
        "target_danceability": 0.80,
        "target_tempo_bpm": 125,
        "target_acousticness": 0.15,
    },
    "Chill Lofi Listener": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_valence": 0.55,
        "target_danceability": 0.55,
        "target_tempo_bpm": 75,
        "target_acousticness": 0.80,
    },
    "Deep Intense Rock Fan": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.45,
        "target_danceability": 0.60,
        "target_tempo_bpm": 150,
        "target_acousticness": 0.10,
    },
    # Edge case: high energy but a sad mood, two wishes that usually conflict.
    "Conflicted High-Energy Sad (edge case)": {
        "favorite_genre": "edm",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "target_valence": 0.20,
        "target_danceability": 0.80,
        "target_tempo_bpm": 128,
        "target_acousticness": 0.10,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for one named profile."""
    print(f"\n=== {name} ===")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  [{song['genre']} / {song['mood']}]")
        print(f"   Score: {score:.2f}")
        print(f"   Reasons: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs, k=5)


if __name__ == "__main__":
    main()
