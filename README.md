# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is called MoodMatch 1.0. It is a content-based recommender that runs in the
terminal. It loads a catalog of 20 songs from a CSV file, compares each song against a
user's taste profile (favourite genre and mood, plus target energy, valence,
danceability, acousticness, and tempo), and scores every song by how closely it matches.
It then ranks the songs and prints the top five with a short reason for each pick, so it
is always clear where the points came from. The weighting is deliberately mood-forward,
meaning mood and valence together outweighs a genre match.

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
| Energy similarity | `1.5 * (1 - song.energy - target_energy)` | 1.5 |
| Valence similarity | `1.5 * (1 - song.valence - target_valence)` | 1.5 |
| Danceability similarity | `1.0 * (1 - song.danceability - target_danceability)` | 1.0 |
| Acousticness similarity | `1.0 * (1 - song.acousticness - target_acousticness)` | 1.0 |
| Tempo similarity | `1.0 * (1 - song.tempo_bpm - target_tempo_bpm / 100)` | 1.0 |

The maximum possible score is 10.5. Tempo is divided by 100 (about the 60 to 160 BPM
spread of the catalog) so a large BPM gap cannot swamp the 0 to 1 features, and the
tempo term is clamped at 0 so it never goes negative.

This weighting is a deliberate, mood-forward design choice. Genre is the largest single
term, but mood (2.0) plus valence (up to 1.5) gives the emotional axis a combined weight
of 3.5, which outweighs a genre match. That mirrors how many listeners actually build
playlists: they pick sad or happy first and genre second.

### Ranking rule (the list)

The recommender scores every song with the rule above, drops any already in the user's
heard list, then fills the top K one slot at a time. Each round it picks whichever song
ranks highest once a repeat-artist penalty is applied: every song by an artist already
in the list loses 1.0 point. This stops a single artist taking over the results, and
the deduction is shown in that song's reasons so it stays visible. Scoring judges a
single song; ranking runs the whole competition.

```
user_prefs ──┐
             ├─► score each song (genre + mood bonus + numeric closeness)
songs.csv ───┘        │
                      ▼
      drop heard -> pick top K one at a time, applying repeat-artist penalty
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
   ```

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

=== High-Energy Pop Lover ===
+------+--------------------+--------------+----------------+-------+----------------------------------------+
| Rank | Song               | Artist       | Genre / Mood   | Score | Why                                    |
+------+--------------------+--------------+----------------+-------+----------------------------------------+
| 1    | Sunrise City       | Neon Echo    | pop / happy    | 10.29 | genre match: pop (+2.5), mood match:   |
|      |                    |              |                |       | happy (+2.0), energy +1.46, valence    |
|      |                    |              |                |       | +1.44, danceability +0.99,             |
|      |                    |              |                |       | acousticness +0.97, tempo +0.93        |
+------+--------------------+--------------+----------------+-------+----------------------------------------+
| 2    | Gym Hero           | Max Pulse    | pop / intense  | 8.09  | genre match: pop (+2.5), energy +1.38, |
|      |                    |              |                |       | valence +1.46, danceability +0.92,     |
|      |                    |              |                |       | acousticness +0.90, tempo +0.93        |
+------+--------------------+--------------+----------------+-------+----------------------------------------+
| 3    | Rooftop Lights     | Indigo       | indie pop /    | 7.62  | mood match: happy (+2.0), energy       |
|      |                    | Parade       | happy          |       | +1.36, valence +1.48, danceability     |
|      |                    |              |                |       | +0.98, acousticness +0.80, tempo +0.99 |
+------+--------------------+--------------+----------------+-------+----------------------------------------+
| 4    | Bass Cathedral     | Deep Sector  | house /        | 5.54  | energy +1.46, valence +1.29,           |
|      |                    |              | energetic      |       | danceability +0.88, acousticness       |
|      |                    |              |                |       | +0.93, tempo +0.99                     |
+------+--------------------+--------------+----------------+-------+----------------------------------------+
| 5    | Neon Pulse         | Voltage      | edm /          | 5.48  | energy +1.35, valence +1.38,           |
|      |                    |              | energetic      |       | danceability +0.90, acousticness       |
|      |                    |              |                |       | +0.88, tempo +0.97                     |
+------+--------------------+--------------+----------------+-------+----------------------------------------+
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
3. Spacewalk Thoughts by Orbit Bloom  [ambient / chill]  Score: 7.33
4. Focus Flow by LoRoom  [lofi / focused]          Score: 7.24  (repeat artist penalty: -1.00)
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

### Weight-shift experiment (energy x2, genre /2)

I temporarily set the energy weight to 3.0 and the genre bonus to 1.25, then reverted.
The clearest effect was on the High-Energy Pop Lover: Gym Hero (pop but "intense")
fell out of the top 2 and Rooftop Lights (happy, right energy, but indie pop) rose to
second. Profiles whose top songs already match on every feature, like the Chill Lofi
Listener, barely moved. The shift was mostly just different, with a small accuracy gain
on the pop list, but it weakens the deliberate mood-and-genre weighting, so the
finalized weights are kept.

---

## Limitations and Risks

- The catalog is tiny at 20 songs, and most genres have only one track, so a listener  with a niche taste gets thin results while lofi (three tracks) is comparatively well served.
- It only rewards similarity to what the user already asked for, so it builds a filter bubble and can repeat the same artist. The Chill Lofi profile got two LoRoom songs in its top three.
- It does not understand lyrics, language, artist popularity, release era, or a song's meaning
- Conflicting preferences are handled poorly. Asking for high energy and a sad mood splits the list between songs that satisfy one wish or the other, without flagging that no song satisfies both.
- The weights are my own judgement call rather than an objective truth, so the results reflect what I decided to prioritise.

There is a fuller discussion in the model card

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this made it concrete how a recommender turns data into a prediction. A song is
just a row of labels and numbers, and a taste profile is the same shape, so a prediction
is nothing more than comparing the two field by field, awarding points for how closely
they line up, adding those points into one number, and sorting. The interesting part is
that the weights are a judgement call, not a fact. When I made mood and happiness
outweigh genre, the recommendations changed noticeably, which means the "right" answer
the system produces is really a reflection of what its designer cares about, in my case it was mood rather than genre.

Bias shows up in more places than I expected. The catalog itself decides who gets served
well, and because lofi has three songs while jazz and classical have one each, a lofi
listener gets a rich list and a jazz listener gets a thin one purely because of what I
happened to include. The scoring only ever rewards similarity to what the user already
asked for, so it creates a filter bubble and can repeat the same artist without noticing,
and it never offers anything new. A few middle-of-the-road high-energy songs also kept
resurfacing across very different profiles, which is a small version of the popularity
bias that real platforms have, where songs that already get recommended collect more
data and end up getting recommended even more.



