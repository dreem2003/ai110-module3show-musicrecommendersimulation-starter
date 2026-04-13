from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import pandas as pd

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
        scored = []
        for song in self.songs:
            song_dict = _song_to_dict(song)
            score, _ = score_song(user, song_dict)
            scored.append((song, score))

        return _greedy_rank(
            scored,
            artist_key=lambda s: s.artist,
            k=k
        )

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(user, _song_to_dict(song))
        return "; ".join(reasons) if reasons else "No strong match found"


# --- Helpers ---

def _song_to_dict(song: Song) -> Dict:
    """Converts a Song dataclass to the dict format used by score_song."""
    return {
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "acousticness": song.acousticness,
        "artist": song.artist,
    }

def _normalize_prefs(user_prefs) -> Tuple[str, str, float, bool]:
    """
    Extracts preference fields from either a UserProfile or a plain dict,
    so score_song works with both the OOP and functional paths.
    """
    if isinstance(user_prefs, UserProfile):
        return (
            user_prefs.favorite_genre,
            user_prefs.favorite_mood,
            user_prefs.target_energy,
            user_prefs.likes_acoustic,
        )
    return (
        user_prefs["genre"],
        user_prefs["mood"],
        user_prefs["energy"],
        user_prefs.get("likes_acoustic", False),
    )

def _greedy_rank(scored: list, artist_key, k: int) -> list:
    """
    Selects the top-k items from a (item, score) list using greedy selection.

    Tie-breaking rule: when two songs share the same score, prefer the one
    whose artist is not already represented in the results so far. This
    prevents the same artist from dominating the top-k on equal scores.
    """
    results = []
    seen_artists = set()
    remaining = list(scored)

    while len(results) < k and remaining:
        best_idx = 0
        for i in range(1, len(remaining)):
            best_score = remaining[best_idx][1]
            cand_score = remaining[i][1]

            if cand_score > best_score:
                best_idx = i
            elif cand_score == best_score:
                # Tie: prefer the candidate whose artist is new to results
                best_artist = artist_key(remaining[best_idx][0])
                cand_artist = artist_key(remaining[i][0])
                if cand_artist not in seen_artists and best_artist in seen_artists:
                    best_idx = i

        chosen_item, _ = remaining.pop(best_idx)
        results.append(chosen_item)
        seen_artists.add(artist_key(chosen_item))

    return results


# --- Functional API ---

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    df = pd.read_csv(csv_path, skipinitialspace=True)
    return df.to_dict(orient="records")


def score_song(user_prefs, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Weights:
      genre      0.40  — strongest categorical signal
      mood       0.30  — captures listening intent
      energy     0.20  — best continuous discriminator (widest spread)
      acousticness 0.10 — cleanest tonal separator (electronic vs. organic)

    Returns (score, reasons) where score is in [0.0, 1.0].
    """
    genre, mood, target_energy, likes_acoustic = _normalize_prefs(user_prefs)

    score = 0.0
    reasons = []

    # Genre match (0.40)
    if song["genre"] == genre:
        score += 0.40
        reasons.append(f"Matches your preferred genre ({song['genre']})")

    # Mood match (0.30)
    if song["mood"] == mood:
        score += 0.30
        reasons.append(f"Matches your preferred mood ({song['mood']})")

    # Energy proximity (0.20) — closer to target = higher contribution
    energy_proximity = 1 - abs(song["energy"] - target_energy)
    score += 0.20 * energy_proximity
    reasons.append(f"Energy is a {energy_proximity:.0%} match to your target")

    # Acousticness preference (0.10)
    if likes_acoustic and song["acousticness"] > 0.6:
        score += 0.10
        reasons.append("Acoustic sound matches your preference")
    elif not likes_acoustic and song["acousticness"] < 0.4:
        score += 0.10
        reasons.append("Produced/electronic sound matches your preference")

    return round(score, 4), reasons


def recommend_songs(user_prefs, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, then returns the top-k using greedy artist-diversity
    tie-breaking: when two songs are tied on score, the one from an artist
    not yet in the results is preferred.

    Returns a list of (song_dict, score, explanation) tuples.
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # Wrap into (item, score) pairs expected by _greedy_rank, carrying reasons along
    pairs = [((song, explanation), score) for song, score, explanation in scored]

    ranked = _greedy_rank(pairs, artist_key=lambda x: x[0]["artist"], k=k)

    return [(song, score_for(song, scored), explanation) for song, explanation in ranked]


def score_for(song: Dict, scored: list) -> float:
    """Looks up the precomputed score for a song by id."""
    for s, score, _ in scored:
        if s["id"] == song["id"]:
            return score
    return 0.0
