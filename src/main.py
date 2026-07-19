"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

from .recommender import load_songs, recommend_songs

# Column headers and widths for the results table.
TABLE_HEADERS = ["Rank", "Song", "Artist", "Genre / Mood", "Score", "Why"]
TABLE_WIDTHS = [4, 18, 12, 14, 5, 38]


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


def format_row(cells: list, widths: list) -> str:
    """Render one table row, wrapping any cell that is too long onto extra lines."""
    wrapped = [textwrap.wrap(str(cell), width) or [""] for cell, width in zip(cells, widths)]
    height = max(len(lines) for lines in wrapped)
    out = []
    for line_index in range(height):
        parts = []
        for lines, width in zip(wrapped, widths):
            text = lines[line_index] if line_index < len(lines) else ""
            parts.append(" " + text.ljust(width) + " ")
        out.append("|" + "|".join(parts) + "|")
    return "\n".join(out)


def render_table(headers: list, rows: list, widths: list) -> str:
    """Render a bordered ASCII table with wrapped cells."""
    separator = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
    lines = [separator, format_row(headers, widths), separator]
    for row in rows:
        lines.append(format_row(row, widths))
        lines.append(separator)
    return "\n".join(lines)


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for one named profile as a formatted table."""
    print(f"\n=== {name} ===")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append([
            rank,
            song["title"],
            song["artist"],
            f"{song['genre']} / {song['mood']}",
            f"{score:.2f}",
            explanation,
        ])
    print(render_table(TABLE_HEADERS, rows, TABLE_WIDTHS))
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs, k=5)


if __name__ == "__main__":
    main()
