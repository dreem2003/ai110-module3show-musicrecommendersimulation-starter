# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch (CLI Simulation) v1.0**  

---

## 2. Intended Use  

This is a classroom, CLI-first demo that recommends a top‑K ranked list of songs from a small CSV catalog based on a user’s stated genre/mood preferences and a few numeric targets.  

---

## 3. How the Model Works  

For each song, the system adds points for matching the user’s favorite genre and mood, adds more points the closer the song’s energy is to the target, and adds a small bonus if acousticness matches the user’s acoustic preference, then sorts by score to return the top K (breaking ties to avoid repeating the same artist when possible).  

---

## 4. Data  

The catalog is a small CSV of **20 songs** with attributes like genre, mood, energy, tempo, valence, danceability, and acousticness, and I expanded it by adding 10 real songs to increase variety.  

---

## 5. Strengths  

It works best for users with clear genre/mood goals and a rough energy target, producing recommendations that feel intuitive and easy to explain in plain language.  

---

## 6. Limitations and Bias 

It ignores listening history and many musical signals (e.g., lyrics, instrumentation, popularity, novelty), so it can over‑reward a single stated preference and reflect any genre/mood gaps present in the small catalog.  

---

## 7. Evaluation  

I tested a few different user profiles (e.g., pop/happy/high‑energy vs. chill/lofi vs. acoustic‑leaning tastes) and checked that top results matched the intended preferences and that explanations matched the scoring logic.  

---

## 8. Future Work  

Next I would incorporate more features (tempo/valence/danceability), learn weights from feedback, and add stronger diversity controls (artist/genre/time‑period) with clearer, user-friendly explanations.  

---

## 9. Personal Reflection  

Building this showed me how even a simple, transparent scoring rule can feel “smart,” but also how quickly recommendations become biased or brittle when the dataset is small and the user’s taste is more nuanced than a few fields.  
