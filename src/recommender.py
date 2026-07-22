import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Point-weighting strategy  (the "Algorithm Recipe")
# ---------------------------------------------------------------------------
# Change these numbers to run experiments (see README "Experiments" section).
#   - genre / mood are CATEGORICAL: all-or-nothing. Full points for an exact
#     match, otherwise 0.
#   - the rest are NUMERIC (0-1 audio features): GRADED by closeness, so a
#     near-miss still earns most of the points.
WEIGHTS = {
    # categorical, exact match
    "genre": 1.0,          # EXPERIMENT: halved 2.0 -> 1.0 (was the dominant signal)
    "mood": 1.0,           # +1.0 for an exact mood match
    # numeric, graded by closeness to the user's target
    "energy": 2.0,         # EXPERIMENT: doubled 1.0 -> 2.0 (now strongest signal)
    "valence": 0.5,        # secondary: overall positivity / happiness
    "danceability": 0.5,   # secondary: how danceable
    "acousticness": 0.5,   # secondary: acoustic vs produced
}

# The numeric features scored by closeness, in the order shown to the user.
NUMERIC_FEATURES = ["energy", "valence", "danceability", "acousticness"]


def _numeric_points(feature: str, target: float, value: float) -> Tuple[float, str]:
    """
    Score one numeric feature by how close the song's value is to the target.

    Both are on a 0-1 scale, so the distance is at most 1.0.
    closeness = 1 - distance  ->  1.0 for a perfect match, 0.0 for the worst miss.
    points = weight * closeness.
    Returns (points, reason).
    """
    closeness = 1.0 - abs(target - value)
    points = WEIGHTS[feature] * closeness
    reason = f"{feature} {value:.2f} vs target {target:.2f} +{points:.2f}"
    return points, reason


def _score(
    pref_genre: str,
    pref_mood: str,
    numeric_targets: Dict[str, Optional[float]],
    song_genre: str,
    song_mood: str,
    song_numeric: Dict[str, float],
) -> Tuple[float, List[str]]:
    """
    Shared scoring core used by both the functional and OOP APIs.

    `numeric_targets` maps a feature name -> the user's target (or None to skip
    that feature). `song_numeric` maps the same names -> the song's values.
    Returns (score, reasons) where `reasons` explains where the points came from.
    """
    score = 0.0
    reasons: List[str] = []

    # Genre: exact match -> full points, otherwise nothing.
    if pref_genre and song_genre == pref_genre:
        score += WEIGHTS["genre"]
        reasons.append(f"genre match ({song_genre}) +{WEIGHTS['genre']:.1f}")

    # Mood: exact match -> full points, otherwise nothing.
    if pref_mood and song_mood == pref_mood:
        score += WEIGHTS["mood"]
        reasons.append(f"mood match ({song_mood}) +{WEIGHTS['mood']:.1f}")

    # Numeric features: each graded by closeness, skipped if no target is given.
    for feature in NUMERIC_FEATURES:
        target = numeric_targets.get(feature)
        if target is None:
            continue
        points, reason = _numeric_points(feature, target, song_numeric.get(feature, 0.0))
        score += points
        reasons.append(reason)

    return score, reasons


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
    # Optional targets for the secondary numeric features. Leave as None to
    # skip scoring that feature.
    target_valence: Optional[float] = None
    target_danceability: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score one Song against a UserProfile via the shared _score core."""
        # likes_acoustic (a bool) becomes an acousticness target: like -> 1.0
        # (aim for acoustic), dislike -> 0.0 (aim for produced).
        numeric_targets = {
            "energy": user.target_energy,
            "valence": user.target_valence,
            "danceability": user.target_danceability,
            "acousticness": 1.0 if user.likes_acoustic else 0.0,
        }
        song_numeric = {
            "energy": song.energy,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }
        return _score(
            pref_genre=user.favorite_genre,
            pref_mood=user.favorite_mood,
            numeric_targets=numeric_targets,
            song_genre=song.genre,
            song_mood=song.mood,
            song_numeric=song_numeric,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(
            self.songs,
            key=lambda song: self._score_song(user, song)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score_song(user, song)
        detail = "; ".join(reasons) if reasons else "no strong matches"
        return f"Score {score:.2f} — {detail}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.

    Numeric columns are converted from text to real numbers so you can do
    math on them later: `id` becomes an int, and the audio-feature columns
    (energy, tempo_bpm, valence, etc.) become floats. Any column not listed
    stays a string.
    Required by src/main.py
    """
    int_cols = {"id"}
    float_cols = {
        "energy", "tempo_bpm", "valence", "danceability",
        "acousticness", "instrumentalness", "speechiness", "liveness",
    }

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in int_cols:
                    song[key] = int(value)
                elif key in float_cols:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song (dict) against user preferences (dict).

    user_prefs uses the keys: "genre", "mood", and any numeric targets you want
    to score: "energy", "valence", "danceability", "acousticness". A numeric
    feature is only scored if its key is present, so a minimal profile like
    {"genre": "pop", "mood": "happy", "energy": 0.8} still works.
    Returns (score, reasons).
    Required by recommend_songs() and src/main.py
    """
    numeric_targets = {feature: user_prefs.get(feature) for feature in NUMERIC_FEATURES}
    song_numeric = {feature: song.get(feature, 0.0) for feature in NUMERIC_FEATURES}
    return _score(
        pref_genre=user_prefs.get("genre", ""),
        pref_mood=user_prefs.get("mood", ""),
        numeric_targets=numeric_targets,
        song_genre=song.get("genre", ""),
        song_mood=song.get("mood", ""),
        song_numeric=song_numeric,
    )

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, sorts by score (highest first), and returns the top k.
    Each item is (song_dict, score, explanation).
    Required by src/main.py
    """
    # Score every song in one list comprehension, packing each result as
    # (song, score, explanation). The one-item tuple in the second `for`
    # unpacks score_song's (score, reasons) return value without calling it
    # twice.
    scored = [
        (song, score, "; ".join(reasons) if reasons else "no strong matches")
        for song in songs
        for score, reasons in (score_song(user_prefs, song),)
    ]

    # Sort by score (item[1]) from highest to lowest, then keep the top k.
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
