# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  
FamJammer- A music recommender that gives users songs based on their enegry and mood preferences

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**VibeFinder 1.0** — a simple music recommender that matches songs to a listener's mood and sound preferences.


---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This recommender takes a listener's stated preferences — like a favorite genre, a mood, and how much energy they want — and returns a short ranked list of songs that best fit. It assumes the user can describe their taste using the same words the catalog uses, and that a good match is one that lines up with those preferences. This is built for classroom exploration, not real users, so the goal is to understand how scoring choices shape recommendations rather than to ship a production app.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Each song is described by its genre, its mood, and a few sound qualities scored from 0 to 1: energy, how positive it feels, how danceable it is, and how acoustic it sounds. The user gives their own version of those same preferences, and the model compares each song to what they asked for. Genre and mood earn points only on an exact match, while the sound qualities earn partial points based on how close the song is to the target, and everything is added up into one score so the highest-scoring songs rise to the top. From the starter logic I ran an experiment that made energy count twice as much and genre count half as much, so I could see how sensitive the rankings are to which preference we treat as most important.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 18 songs spread across 15 genres — from pop, lofi, and hip hop to classical, metal, and funk — and 14 moods such as happy, chill, intense, and melancholy. I did not add or remove any songs; I used the starter dataset as-is. Because most genres and moods appear only once, whole styles of music are barely represented, and common listener words like "sad" or "electronic" don't exist as labels at all, so a lot of real musical taste is missing from the data.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works well for listeners who use the exact genre and mood words in the catalog and who want high-energy music, since that is where most of the songs sit. It correctly captures the idea of "closeness" for sound qualities, so a request for high energy reliably surfaces energetic tracks and a request for acoustic leans toward quieter, softer songs. When I tested a clear pop-and-upbeat profile, the top picks matched my intuition, which told me the basic scoring idea is sound even if the edge cases need work.

---
#stop here 
## 6. Limitations and Bias 
Where the system struggles or behaves unfairly. 
Prompts:  
- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  
##limitions 
Some limitations and bias that the system struggles or behaves unfairly with is requesting songs that aren't in the catalog mood label. For example if a listener who asks for a "sad" song gets zero credit on that request since "sad" isn't one of the catalog's mood labels — the system silently ignores their strongest intent and ranks on energy instead. In our experiment, a "sad but high-energy" profile returned intense rock and EDM tracks, the opposite of what was asked. This means anyone whose words don't exactly match our fixed vocabulary is effectively invisible to the mood and genre parts of the system.
---

## 7. Evaluation  
How you checked whether the recommender behaved as expected. 
Prompts:  
- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

 What I tested and what surprised me: 
I design five edge-case profiles: a conflicting "sad + high energy" user, an out-of-range energy target, a genre-only user, an empty profile, and an all-zeros user and looked at whether the top picks actually matched the request. The surprise was how easily the ranking was hijacked by a single feature: the "sad" request returned intense rock because "sad" isn't a known mood, so energy alone decided everything.

Profile comparisons:
- Conflict (sad+energy) vs. genre-only (pop): The pop user got clean genre matches, while the sad user got loud intense songs because mood is exact-match and "sad" matched nothing, so only energy scored.
- Empty profile vs. all-zeros: the empty user got songs in file order at 0.00, while the all zeros user got the calmest, quietest tracks because zero targets still reward low-energy songs, whereas no targets reward nothing.
- Genre-only (pop) vs. out-of-range (metal, energy=2.0): Pop returned a clean tie at the genre score, while the out-of-range user pushed most songs into negative scores because an energy target above 1.0 breaks the closeness math and penalizes every non-matching song.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes 

Some ideas I would like to include for the next model is having a larger data base to include more diversity in the recommendation. Another thing I would also like to implement is a DJ similar to Spotify's DJ. 
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps

Some new thing I was able to learn from this project was knowing the difference betweem .sort() and sorted(), which helped build my recommender system. However, this does make me wonder how big brands like Spotify's Dj or randomizer select songs for their users.  