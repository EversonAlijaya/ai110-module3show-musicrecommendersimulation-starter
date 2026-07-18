# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias

The clearest weakness I found is that the recommender has no sense of variety, so it
tends to build a filter bubble. Because every point rewards closeness to what the user
already asked for, the top of each list is just more of the same, and it can even
repeat the same artist: the Chill Lofi Listener's top three included two different
songs by LoRoom. The small 20-song catalog makes this worse, since niche genres like
jazz, classical, and country have only one matching track each, so listeners with those
tastes get thin, lower-scoring results while lofi (three songs) is comparatively well
served. A few generically high-energy songs, such as Bass Cathedral, also resurface
across very different profiles, which is a mild popularity-style bias. The system never
offers a surprising or diverse pick, so a user could not discover anything new outside
their stated preferences.

---

## 7. Evaluation

I tested four profiles: a High-Energy Pop Lover, a Chill Lofi Listener, a Deep Intense
Rock Fan, and a deliberately conflicting edge case that wanted high energy but a sad
mood. For each one I looked at the top five songs and asked whether a real person with
that taste would actually want them, and whether each list was clearly different from
the others.

What surprised me most was the conflicting profile. Because it asked for two things that
do not go together in this catalog, its list split down the middle: an energetic EDM
song took first place to satisfy the "high energy" wish, while a quiet, sad folk song
came second to satisfy the "sad" wish, and no single song could do both. The three
normal profiles behaved as expected, each getting a number one that matched both its
genre and its mood.

Comparing the profiles:

- **Pop Lover vs Lofi Listener:** these are near opposites, so they share no songs. The
  pop fan gets loud, upbeat, danceable tracks and the lofi fan gets quiet, calm,
  acoustic ones. This is the system working as intended.
- **Pop Lover vs Rock Fan:** both want high energy but split on mood, and this is the
  one worth explaining simply. The workout song "Gym Hero" shows up high for the happy
  pop fan, which feels odd because it is an intense gym track, not a cheerful one. It
  ranks high only because it shares the "pop" label and has the right energy, so the
  matching genre pulls it up even though its mood is wrong. The rock fan also gets Gym
  Hero, but for the opposite and correct reason: that fan actually wants the intense
  mood.
- **Lofi Listener vs Rock Fan:** the most extreme opposites, calm and acoustic versus
  loud and aggressive, and their lists have essentially nothing in common, which
  confirms the scoring separates very different tastes cleanly.
- **Edge case vs the normal profiles:** unlike the three coherent profiles, the
  conflicting profile never gets a satisfying number one, which shows the limit of
  asking the system for two contradictory things at once.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
