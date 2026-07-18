# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify and YouTube predict what you'll love next by
combining two strategies. Collaborative filtering looks at behavior: if people who
like the songs you like also enjoy some other track, it recommends that track,
without knowing anything about how it sounds. Content-based filtering ignores other
users and instead compares the attributes of the songs themselves (tempo, energy,
mood, genre), recommending songs similar to ones you already enjoy. At scale these
run as a pipeline that scores a huge pool of candidate songs, ranks them, filters
out what you've already heard, and shows the top few, all tuned on implicit signals
like skips and listen time far more than explicit likes. My simulation is a small,
transparent content-based recommender. It has no other users and no behavioral
history, so it prioritizes matching a user's stated taste to a song's audio features,
rewarding songs whose "vibe" is closest to what the user wants rather than songs that
are simply the loudest or fastest.

### Song features

Each `Song` uses the attributes from `data/songs.csv`:

- `id`, `title`, `artist`: identity and display (not used in scoring)
- `genre`, `mood`: categorical labels (e.g. `lofi`, `chill`)
- `energy`, `valence`, `danceability`, `acousticness`: numeric audio features on a 0 to 1 scale
- `tempo_bpm`: tempo in beats per minute (roughly 60 to 160)

The catalog has 20 songs spanning 17 genres and 13 moods.

### UserProfile

The user profile is a dictionary of target values for the same features, meaning the
taste we score against. Here is the primary example profile, a High-Energy Pop Lover:

```python
user_prefs = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.85,
    "target_valence": 0.80,
    "target_danceability": 0.80,
    "target_tempo_bpm": 125,
    "target_acousticness": 0.15,
}
```

A profile can also carry a list of already-heard song ids to exclude from results.

### Scoring rule (one song)

For each numeric feature the recommender rewards closeness, not high values, using
`similarity = 1 - |song_value - target_value|`, so a song that sits right on the
target earns close to the full weight and a song far away earns almost nothing. Genre
and mood are exact-match bonuses. Every component also produces a short reason string
so each recommendation can explain itself.

| Component | Rule | Max points |
|---|---|---|
| Genre match | `+2.5` if `song.genre == favorite_genre` | 2.5 |
| Mood match | `+2.0` if `song.mood == favorite_mood` | 2.0 |
| Energy similarity | `1.5 * (1 - |song.energy - target_energy|)` | 1.5 |
| Valence similarity | `1.5 * (1 - |song.valence - target_valence|)` | 1.5 |
| Danceability similarity | `1.0 * (1 - |song.danceability - target_danceability|)` | 1.0 |
| Acousticness similarity | `1.0 * (1 - |song.acousticness - target_acousticness|)` | 1.0 |
| Tempo similarity | `1.0 * (1 - |song.tempo_bpm - target_tempo_bpm| / 100)` | 1.0 |

The maximum possible score is 10.5. Tempo is divided by 100 (about the 60 to 160 BPM
spread of the catalog) so a large BPM gap cannot swamp the 0 to 1 features, and the
tempo term is clamped at 0 so it never goes negative.

This weighting is a deliberate, mood-forward design choice. Genre is the largest single
term, but mood (2.0) plus valence (up to 1.5) gives the emotional axis a combined weight
of 3.5, which outweighs a genre match. That mirrors how many listeners actually build
playlists: they pick sad or happy first and genre second.

### Ranking rule (the list)

The recommender scores every song with the rule above, drops any already in the
user's heard list, sorts by score from highest to lowest, and returns the top K.
Scoring judges a single song; ranking runs the whole competition.

```
user_prefs ──┐
             ├─► score each song (genre + mood bonus + numeric closeness)
songs.csv ───┘        │
                      ▼
             sort by score (high to low) -> drop heard -> take top K
```

### Biases I expect

- Because the emotional axis outweighs genre by design, the system may underrate a
  strong genre-match song when its mood label is slightly off, even if the listener
  would still enjoy it.
- Mood and valence measure almost the same thing, so a happy song can be rewarded
  twice for one underlying trait, which can crowd out otherwise good matches.
- With a small 20-song catalog, a few dominant genres or moods can pull most profiles
  toward the same handful of songs.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Running `python -m src.main` with the High-Energy Pop Lover profile
(`favorite_genre=pop`, `favorite_mood=happy`, `target_energy=0.85`) produces:

```
Loaded songs: 20

Top recommendations:

1. Sunrise City by Neon Echo  [pop / happy]
   Score: 10.29
   Reasons: genre match: pop (+2.5), mood match: happy (+2.0), energy similarity: +1.46, valence similarity: +1.44, danceability similarity: +0.99, acousticness similarity: +0.97, tempo similarity: +0.93

2. Gym Hero by Max Pulse  [pop / intense]
   Score: 8.09
   Reasons: genre match: pop (+2.5), energy similarity: +1.38, valence similarity: +1.46, danceability similarity: +0.92, acousticness similarity: +0.90, tempo similarity: +0.93

3. Rooftop Lights by Indigo Parade  [indie pop / happy]
   Score: 7.62
   Reasons: mood match: happy (+2.0), energy similarity: +1.36, valence similarity: +1.48, danceability similarity: +0.98, acousticness similarity: +0.80, tempo similarity: +0.99

4. Bass Cathedral by Deep Sector  [house / energetic]
   Score: 5.54
   Reasons: energy similarity: +1.46, valence similarity: +1.29, danceability similarity: +0.88, acousticness similarity: +0.93, tempo similarity: +0.99

5. Neon Pulse by Voltage  [edm / energetic]
   Score: 5.48
   Reasons: energy similarity: +1.35, valence similarity: +1.38, danceability similarity: +0.90, acousticness similarity: +0.88, tempo similarity: +0.97
```

---

## Experiments You Tried

### Multi-profile stress test

Running `python -m src.main` scores all 20 songs against four distinct profiles: a
High-Energy Pop Lover, a Chill Lofi Listener, a Deep Intense Rock Fan, and a
deliberately conflicting edge case (high energy but a sad mood). The top 5 for each:

```
=== High-Energy Pop Lover ===
1. Sunrise City by Neon Echo  [pop / happy]        Score: 10.29
2. Gym Hero by Max Pulse  [pop / intense]          Score: 8.09
3. Rooftop Lights by Indigo Parade  [indie pop / happy]  Score: 7.62
4. Bass Cathedral by Deep Sector  [house / energetic]    Score: 5.54
5. Neon Pulse by Voltage  [edm / energetic]        Score: 5.48

=== Chill Lofi Listener ===
1. Library Rain by Paper Lanterns  [lofi / chill]  Score: 10.30
2. Midnight Coding by LoRoom  [lofi / chill]       Score: 10.19
3. Focus Flow by LoRoom  [lofi / focused]          Score: 8.24
4. Spacewalk Thoughts by Orbit Bloom  [ambient / chill]  Score: 7.33
5. Autumn Letters by The Hollow Pines  [indie folk / melancholic]  Score: 5.54

=== Deep Intense Rock Fan ===
1. Storm Runner by Voltline  [rock / intense]      Score: 10.36
2. Gym Hero by Max Pulse  [pop / intense]          Score: 6.96
3. Iron Verdict by Ashfall  [metal / angry]        Score: 5.47
4. Night Drive Loop by Neon Echo  [synthwave / moody]    Score: 5.06
5. Bass Cathedral by Deep Sector  [house / energetic]    Score: 5.05

=== Conflicted High-Energy Sad (edge case) ===
1. Neon Pulse by Voltage  [edm / energetic]        Score: 7.47
2. Paper Boats by Ellie Frost  [folk / sad]        Score: 5.28
3. Storm Runner by Voltline  [rock / intense]      Score: 5.18
4. Iron Verdict by Ashfall  [metal / angry]        Score: 5.12
5. Bass Cathedral by Deep Sector  [house / energetic]    Score: 5.10
```

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



