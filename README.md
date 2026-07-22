# 🎵 Music Recommender Simulation
#Start here
## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version takes a listener's preferences like a genre, a mood, and how much energy they want and gives each song a score based on how closely it matches, then returns the top picks. I also ran experiments with edge-case profiles and adjusted the scoring weights to see how easily the rankings can be biased toward one preference.
#End here
---

## How The System Works
  ## Bais 
  Some bais that can happend is genre being over-prioritization or some moods being undervalued. Another thing that could lead to some bais is categoires would only reward exact string matches, even if they have the same score. 
  ## Explaing how Streaming platforms predict:
  Some way main streaming platforms like Spotify or YouTube predict what someone will like next is by using two different methods: Collaborative filtering and Content-based filtering. 
  
  Each method uses different type of data. For example, content-based filtering uses song atttributes such as tempo, genre, audio, and lyrics to be able to predict what they will want next. In other words this method ask "What resembles what the user has enjoyed"       
  
  However, for collaborative filtering, the data that is used is plays, likes, and skips to be able to predict what the user will want to do next. In other words this method ask "What did similar users enjoy" 
  
  Explaining my design in plain language:

  The plain design for how the system will work is using a distance measurer. What does this mean? This means that in my design we will use enegry of the song, and subtract them from the value of the enegry wanted. Which ever is closest to 0 is the perfect match to this song and if songs have the same score then there is a ranking that helps sort them order.   
Some prompts to answer:

- What features does each `Song` use in your system
  Some features that my song includes in my system is using energy 
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
  Some information that my UserProfile store is score_song, recommend_song, and explaing the recommendtion. 
- How does your `Recommender` compute a score for each song
  The way my recommdender computes a score for each song is by comparing scores with global and relative songs. Then a value; k is created and the highest k is returned. 
- How do you choose which songs to recommend
  The way I design this for which song to recommend next is by using two different methods score_song and recommend_song which compares each song to one another and returns the top vaule. 
You can include a simple diagram or bullet list if helpful.

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

============================================================
  Top 5 recommendations
  Profile: genre=pop, mood=happy, energy=0.8, valence=0.8, danceability=0.8, acousticness=0.2
============================================================

 1. Sunrise City - Neon Echo
    Score: 5.45
    Reasons:
      - genre match (pop) +2.0
      - mood match (happy) +1.0
      - energy 0.82 vs target 0.80 +0.98
      - valence 0.84 vs target 0.80 +0.48
      - danceability 0.79 vs target 0.80 +0.49
      - acousticness 0.18 vs target 0.20 +0.49

 2. Gym Hero - Max Pulse
    Score: 4.24
    Reasons:
      - genre match (pop) +2.0
      - energy 0.93 vs target 0.80 +0.87
      - valence 0.77 vs target 0.80 +0.48
      - danceability 0.88 vs target 0.80 +0.46
      - acousticness 0.05 vs target 0.20 +0.42

 3. Rooftop Lights - Indigo Parade
    Score: 3.37
    Reasons:
      - mood match (happy) +1.0
      - energy 0.76 vs target 0.80 +0.96
      - valence 0.81 vs target 0.80 +0.49
      - danceability 0.82 vs target 0.80 +0.49
      - acousticness 0.35 vs target 0.20 +0.43

 4. Payday Strut - Groove Cartel
    Score: 2.40
    Reasons:
      - energy 0.80 vs target 0.80 +1.00
      - valence 0.86 vs target 0.80 +0.47
      - danceability 0.90 vs target 0.80 +0.45
      - acousticness 0.15 vs target 0.20 +0.47

 5. Concrete Dreams - Blocktext
    Score: 2.33
    Reasons:
      - energy 0.78 vs target 0.80 +0.98
      - valence 0.62 vs target 0.80 +0.41
      - danceability 0.85 vs target 0.80 +0.48
      - acousticness 0.12 vs target 0.20 +0.46

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried
================================================================
1. CONFLICT: energy=0.9 + mood=sad
  exposes: Mood is dropped silently; scorer just maximizes energy.
  prefs:   {'mood': 'sad', 'energy': 0.9}
----------------------------------------------------------------
    0.99  Storm Runner         genre=rock       mood=intense
    0.97  Gym Hero             genre=pop        mood=intense
    0.95  Neon Pulse           genre=edm        mood=euphoric

================================================================
2. OUT-OF-RANGE: genre=metal + energy=2.0
  exposes: No clamping -> closeness goes negative for non-matches.
  prefs:   {'genre': 'metal', 'energy': 2.0}
----------------------------------------------------------------
    1.98  Iron Verdict         genre=metal      mood=aggressive
   -0.05  Neon Pulse           genre=edm        mood=euphoric
   -0.07  Gym Hero             genre=pop        mood=intense

================================================================
3. GENRE STEAMROLLER: genre=pop only
  exposes: Ties at 2.00 broken by CSV order; genre outweighs audio features.
  prefs:   {'genre': 'pop'}
----------------------------------------------------------------
    2.00  Sunrise City         genre=pop        mood=happy
    2.00  Gym Hero             genre=pop        mood=intense
    0.00  Midnight Coding      genre=lofi       mood=chill

================================================================
4. EMPTY PROFILE: no prefs
  exposes: Everything scores 0.00; file order presented as recommendations.
  prefs:   {}
----------------------------------------------------------------
    0.00  Sunrise City         genre=pop        mood=happy
    0.00  Midnight Coding      genre=lofi       mood=chill
    0.00  Storm Runner         genre=rock       mood=intense

================================================================
5. ALL-ZEROS: anti-recommender
  exposes: No sanity floor; happily returns the most lifeless tracks.
  prefs:   {'energy': 0.0, 'valence': 0.0, 'danceability': 0.0, 'acousticness': 0.0}
----------------------------------------------------------------
    1.52  Winter Nocturne      genre=classical  mood=melancholy
    1.23  Spacewalk Thoughts   genre=ambient    mood=chill
    1.15  Velvet Hours         genre=r&b        mood=romantic

    
Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

The edge-case profiles test whether the recommender still behaves sensibly when a user's request is unusual or contradictory like asking for a "sad" mood that isn't in the catalog, or setting an energy target that's out of range. The weight-shift experiment tests how sensitive the rankings are to which preference we treat as most important, by doubling energy and halving genre to see if the top picks change.
---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

Some limitations and risks that the system struggles with is requesting songs that aren't in the catalog mood label. For example if a listener who asks for a "sad" song gets zero credit on that request since "sad" isn't one of the catalog's mood labels — the system silently ignores their strongest intent and ranks on energy instead. In our experiment, a "sad but high-energy" profile returned intense rock and EDM tracks, the opposite of what was asked. This means anyone whose words don't exactly match our fixed vocabulary is effectively invisible to the mood and genre parts of the system. Additionally, because our data size is small it doesn't allow for users to get an accurate recommendation. 
---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Somethings that I learned from doing this project is finding out how data is used to predicated/recommend users songs. Seeing how they is words into numerical to be able to do this felt weird since I noticed that this leads to many biases or unfairness. For example my data didn't have anything about sad song which made it hard for users to find songs that were sad. However, through trail and error I was able to find ways to remove this bais, but I do believe that there could still be some bais which I haven't found. 


