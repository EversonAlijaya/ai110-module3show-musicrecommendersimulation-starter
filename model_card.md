# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**MoodMatch 1.0**

---

## 2. Intended Use

MoodMatch 1.0 takes a description of someone's music taste and suggests songs from a
small catalog that fit that taste, with a short reason for every pick. It assumes the
user can describe what they want up front, meaning a favourite genre and mood plus
roughly how energetic, upbeat, danceable, acoustic, and fast they like their music. It
also assumes those stated preferences are honest and stable, since it has no listening
history to learn from.

This is a classroom exploration project, not a product. It runs in a terminal on 20
hand-written songs and is meant to make the mechanics of a recommender visible, so it
should not be used to make real recommendations to real listeners.

---

## 3. How the Model Works

The user describes their taste: a favourite genre and mood, plus their ideal energy,
happiness, danceability, acousticness, and tempo. Every song in the catalog carries
those same details.

The system goes through the songs one at a time and gives each one a score. A song
gets a fixed number of points if its genre is the one the user asked for, and a further
fixed number if its mood matches. For the numeric traits, points are awarded for being
close to what the user wants rather than for being high. A song whose energy sits right
on the user's ideal earns almost all the available energy points, and a song far away
earns almost none. The same applies to happiness, danceability, acousticness, and
tempo. Each song ends up with one total score and a short list of notes saying where
its points came from.

Once every song has a score, the system sorts them from highest to lowest and shows the
top five along with their reasons. Scoring handles one song at a time, and sorting is
what turns those individual scores into an actual recommendation list.

Compared with the starter version, I made two main changes. First, I widened what the
system looks at, since the starter only really considered genre, mood, and energy, and
I added happiness, danceability, acousticness, and tempo so it could tell apart songs
that are equally energetic but feel completely different. Second, I made the scoring
mood-forward on purpose: mood and happiness together outweigh a genre match, because
in real life people tend to build playlists around how they want to feel first and what
genre it is second.

---

## 4. Data

The catalog holds 20 songs written by hand for this project, covering 17 genres and 13
moods. The genres range from pop, rock, and lofi through hip-hop, EDM, house, and metal
to classical, jazz, folk, country, reggae, and R&B, and the moods run from happy, chill,
and energetic to sad, angry, melancholic, and nostalgic. Each song lists a title, an
artist, a genre, a mood, and five numeric traits: energy, happiness, danceability,
acousticness, and tempo.

I started from a 10-song starter file and added 10 more, deliberately choosing genres
and moods that were missing so that very different listeners would each have something
to match. I did not remove anything.

Plenty of real musical taste is missing. There are no lyrics, no language or cultural
context, no release year, no popularity, and no sense of what a song means to someone
personally. Most genres are represented by only one song, so a listener with a niche
taste has very little to be matched against.

---

## 5. Strengths

The system works best for listeners who can state a clear, internally consistent taste.
Each of the three coherent profiles I tested got a sensible number one pick that matched
both its genre and its mood, and the three lists barely overlapped, which is what you
want from a recommender that is genuinely responding to different people.

The scoring captures the idea of a "vibe" better than energy alone would. Energy tells
you how calm or intense a song is, and happiness tells you whether that intensity is
cheerful or dark, so the system can correctly separate an upbeat workout track from an
aggressive rock track even though both are high energy.

It also reaches across genre boundaries in a way that matched my intuition. A happy
indie pop song ranked highly for the pop listener without being pop, and an intense pop
song ranked second for the rock listener, both because the mood lined up. Finally,
every recommendation explains itself, so it is always possible to see exactly why a song
appeared and to spot when a result is driven by something like a genre match alone.

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

The first thing I would fix is the filter bubble. Adding a penalty when the same artist
appears more than once in a list would stop results like the lofi profile getting two
LoRoom tracks in its top three, and deliberately reserving one slot for a song outside
the user's usual taste would give the system a way to surprise people rather than only
confirming what they already asked for.

Second, I would grow the catalog and the details it holds. Twenty songs is too few for
niche tastes, since most genres only have one matching track, and adding fields like
release decade, popularity, and more specific mood tags would let the system reflect
things people genuinely care about, such as preferring older music or avoiding
overplayed hits.

Third, I would handle conflicting tastes more honestly. Right now a request for high
energy and a sad mood quietly splits the list between songs that satisfy one wish or
the other, and it would be better for the system to notice that no song satisfies both
and say so, instead of presenting a confusing mix as if it were a confident answer.

---

## 9. Personal Reflection  

The biggest thing I learned is that a recommender is really two ideas working together.
Scoring answers how well one song fits one person, and ranking is what turns a pile of
scores into an actual list. I assumed recommendations came from something complicated,
but the core trick turned out to be simple: reward a song for being close to what
someone wants instead of for having a high value, because always picking the most
energetic song is not the same as picking the right one.

The most useful moment was deciding the weights myself. The AI suggested making genre
the strongest signal, but that did not match how I actually listen, since I build
playlists around whether I want something sad or happy long before I think about genre.
Changing the weights so mood and happiness together outweigh genre made the results feel
much more like mine, and it taught me that these systems encode somebody's opinion about
what matters rather than an objective truth.

AI tools sped up the parts I already understood, like reading the CSV file and sorting
the results, and they were good for explaining ideas. I still had to check them. I
worked out a few scores by hand and compared them with what the program printed to be
sure the math was right, and at one point running a suggested git command without
checking first would have wiped out work that was already saved online.

What surprised me most was the conflicting profile. Asking for high energy and a sad
mood produced a list that quietly split in half, with an energetic dance track first and
a slow sad song second, and neither one actually satisfied the request. It looked
confident even though it had failed. That changed how I think about music apps: when a
recommendation feels wrong, it is probably not broken, it is just optimising for
something slightly different from what I meant. If I kept going, I would add a rule to
stop the same artist repeating and to slip in one unexpected song, so it could help me
discover things instead of only echoing what I already asked for.
