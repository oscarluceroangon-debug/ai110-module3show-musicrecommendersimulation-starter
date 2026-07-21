"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile. Numeric keys (energy/valence/danceability/
    # acousticness) are optional targets — include only the ones you care about.
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.8,
        "danceability": 0.8,
        "acousticness": 0.2,
    }

    k = 5
    recommendations = recommend_songs(user_prefs, songs, k=k)

    # Build a compact one-line summary of the profile we searched with.
    profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())

    line = "=" * 60
    print(f"\n{line}")
    print(f"  Top {len(recommendations)} recommendations")
    print(f"  Profile: {profile}")
    print(line)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        # `explanation` is the reasons joined by "; " — split it back out so
        # each reason gets its own bulleted line.
        reasons = explanation.split("; ")

        print(f"\n {rank}. {song['title']} - {song['artist']}")
        print(f"    Score: {score:.2f}")
        print("    Reasons:")
        for reason in reasons:
            print(f"      - {reason}")

    print()


if __name__ == "__main__":
    main()
