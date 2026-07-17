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
- `tempo_bpm`: tempo in beats per minute (roughly 60 to 152)

### UserProfile

The `UserProfile` stores the user's preferred values for the same features, meaning
the taste we score against:

- Preferred `genre` and `mood`
- Preferred `energy`, `valence`, `danceability`, `acousticness` (0 to 1) and `tempo_bpm`
- A list of already-heard song ids to exclude from results
- (Optional) per-feature weights controlling how much each feature matters

### Scoring rule (one song)

For each numeric feature the recommender rewards closeness, not high values, using
`similarity = 1 - |song_value - user_preference|` (tempo is normalized by its range
first so it can't dominate). It then adds a bonus when `genre` matches and a smaller
bonus when `mood` matches. Genre is weighted higher because it carries information the
numeric features don't, whereas mood is largely a summary of energy plus valence. All
parts combine into one weighted-sum score per song.

### Ranking rule (the list)

The `Recommender` scores every song, drops any already in the user's heard list, sorts
by score (highest first), and returns the top N. Scoring judges a single song; ranking
turns those scores into an actual ordered recommendation list.

```
UserProfile ──┐
              ├─► score each Song (1 - distance, + genre/mood bonus)
Song catalog ─┘        │
                       ▼
              rank by score -> drop heard -> take top N -> recommendations
```

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



