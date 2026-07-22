"""
Adversarial / edge-case profile runner for the Music Recommender.

Each profile is designed to probe a specific weakness in the additive scoring
logic in recommender.py. Run it to see the surprising results for yourself:

    python -m src.adversarial

or:

    python src/adversarial.py
"""

from src.recommender import load_songs, recommend_songs

# Each entry: (title, note about what it exposes, user_prefs)
ADVERSARIAL_PROFILES = [
    (
        "1. CONFLICT: energy=0.9 + mood=sad",
        "Mood is dropped silently; scorer just maximizes energy.",
        {"mood": "sad", "energy": 0.9},
    ),
    (
        "2. OUT-OF-RANGE: genre=metal + energy=2.0",
        "No clamping -> closeness goes negative for non-matches.",
        {"genre": "metal", "energy": 2.0},
    ),
    (
        "3. GENRE STEAMROLLER: genre=pop only",
        "Ties at 2.00 broken by CSV order; genre outweighs audio features.",
        {"genre": "pop"},
    ),
    (
        "4. EMPTY PROFILE: no prefs",
        "Everything scores 0.00; file order presented as recommendations.",
        {},
    ),
    (
        "5. ALL-ZEROS: anti-recommender",
        "No sanity floor; happily returns the most lifeless tracks.",
        {"energy": 0.0, "valence": 0.0, "danceability": 0.0, "acousticness": 0.0},
    ),
]


def show(title: str, note: str, prefs: dict, songs: list, k: int = 3) -> None:
    print("=" * 64)
    print(title)
    print(f"  exposes: {note}")
    print(f"  prefs:   {prefs}")
    print("-" * 64)
    for song, score, _explanation in recommend_songs(prefs, songs, k=k):
        print(
            f"  {score:6.2f}  {song['title']:<20} "
            f"genre={song['genre']:<10} mood={song['mood']}"
        )
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")
    for title, note, prefs in ADVERSARIAL_PROFILES:
        show(title, note, prefs, songs)


if __name__ == "__main__":
    main()
