# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Music recommendation can be a complex endeavor, especially at scale and for enterprise organizations. Multiple factors influence what a user might enjoy, including what similar users prefer (collaborative filtering) and the characteristics of songs a user has already indicated they like (content-based filtering).

For this demo project, which has a single execution point, we will focus on the latter. This approach analyzes songs and applies a scoring and ranking algorithm based primarily on attributes such as genre, mood, energy, and acousticness.
---

## How The System Works

Each song is scored against the user's taste profile using four weighted signals that sum to a maximum of **1.0**:

| Signal | Weight | How it's measured |
|---|---|---|
| **Genre match** | 0.40 | +0.40 if the song's genre exactly matches the user's preferred genre |
| **Mood match** | 0.30 | +0.30 if the song's mood exactly matches the user's preferred mood |
| **Energy proximity** | 0.20 | `0.20 × (1 − |song_energy − target_energy|)` — full points for a perfect match, less as the gap widens |
| **Acousticness preference** | 0.10 | +0.10 if the user likes acoustic and `acousticness > 0.6`, or dislikes acoustic and `acousticness < 0.4` |

**`UserProfile`** stores four fields that map directly to those signals: `favorite_genre`, `favorite_mood`, `target_energy` (0–1 float), and `likes_acoustic` (boolean).

**Ranking** uses greedy selection over the scored list. Ties are broken by artist diversity — if two songs share the same score, the one from an artist not already in the results is preferred, preventing any single artist from dominating the top-k.

**Potential biases to be aware of:**
- **Genre dominance** — at 0.40, genre alone is nearly half the score. A song that perfectly matches the user's mood, energy, and acousticness but differs in genre (e.g., a Jazz track for a Pop fan) can never outscore a weak genre match, even if it would genuinely resonate.
- **Mood over nuance** — mood is binary (exact match or nothing). Two songs with very similar emotional tones but different mood labels score identically to songs that are complete mismatches.
- **Energy bias toward the midrange** — the proximity formula rewards songs near 0.5 energy more easily than extreme values (0.0 or 1.0), since there are more neighbors in the middle of the scale.
- **Acousticness cliff** — the 0.4 / 0.6 thresholds create hard cutoffs; a song at 0.61 acousticness earns full points while one at 0.59 earns none, even though the difference is negligible.

---

## Concise Model Card (1-sentence answers)

- **Model Name**: VibeMatch (CLI Simulation) v1.0.
- **Intended Use**: A classroom, CLI-first demo that ranks a small CSV catalog into top‑K recommendations from a user’s stated preferences.
- **How it Works**: Each song gets a weighted score from genre + mood matches, energy closeness to a target, and an acousticness bonus, then the list is sorted with an artist-diversity tie-break.
- **Data**: `data/songs.csv` contains 20 songs with genre/mood and numeric attributes, including 10 added real songs to increase variety.
- **Strengths**: Works well when a user has clear genre/mood intent and a rough energy target, and it can explain recommendations transparently.
- **Limitations & Bias**: It ignores many musical factors and user history, so results can be brittle and reflect catalog imbalances (and a few hard thresholds).
- **Evaluation**: Checked multiple user profiles in the CLI and verified the top results and explanations matched the intended scoring logic.
- **Future Work**: Add tempo/valence/danceability (and learnable weights), improve diversity controls, and generate more user-friendly explanations.
- **Personal Reflection**: This project made it clear how simple scoring rules can feel smart while still baking in bias when data and preferences are simplified.

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
![Result screenshot](image.png)

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


---
