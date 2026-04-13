"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, UserProfile


def main() -> None:
    songs = load_songs("data/songs.csv") 
    # "derek_taste" is a valid categorization for testing the music recommender system.
    # - favorite_genre="pop" exists in songs.csv (e.g., "Sunrise City", "bad guy", "Gym Hero")
    # - favorite_mood="happy" also appears in the dataset
    # - target_energy=0.8 is within the 0-1 range covered by song energy values
    # - likes_acoustic=True tests the boolean logic for acoustic preferences; several pop songs have varied acousticness
    # This profile covers core attributes and ensures the recommend_songs function can evaluate different aspects
    derek_taste = UserProfile(
        favorite_genre="hip hop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=True,
    )
    recommendations = recommend_songs(derek_taste, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
