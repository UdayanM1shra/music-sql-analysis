# generates a fake music streaming dataset.
# seeded so it's reproducible.

import random
import csv
from datetime import date, datetime, timedelta

random.seed(42)

# ---- Artists with rough popularity weights ----
ARTISTS = [
    ("Taylor Swift",      "Pop",       100),
    ("Drake",             "Hip-Hop",   95),
    ("The Weeknd",        "Pop",       85),
    ("Bad Bunny",         "Reggaeton", 90),
    ("Billie Eilish",     "Pop",       70),
    ("Kendrick Lamar",    "Hip-Hop",   75),
    ("Olivia Rodrigo",    "Pop",       65),
    ("Travis Scott",      "Hip-Hop",   72),
    ("Harry Styles",      "Pop",       68),
    ("SZA",               "R&B",       60),
    ("Dua Lipa",          "Pop",       55),
    ("Post Malone",       "Hip-Hop",   58),
    ("Doja Cat",          "Pop",       62),
    ("Frank Ocean",       "R&B",       40),
    ("Tame Impala",       "Indie",     35),
    ("Arctic Monkeys",    "Indie",     45),
    ("Mac Miller",        "Hip-Hop",   38),
    ("Lana Del Rey",      "Indie",     42),
    ("J Cole",            "Hip-Hop",   50),
    ("Mitski",            "Indie",     25),
    ("Phoebe Bridgers",   "Indie",     22),
    ("Steve Lacy",        "R&B",       30),
    ("Tyler, The Creator","Hip-Hop",   55),
    ("Lorde",             "Pop",       33),
    ("Bon Iver",          "Indie",     20),
]

# ---- Build artists table ----
artists = []
for i, (name, genre, weight) in enumerate(ARTISTS, start=1):
    artists.append({
        "artist_id": i,
        "artist_name": name,
        "genre": genre,
        # number of monthly listeners in millions, roughly tied to popularity
        "monthly_listeners_millions": round(weight * random.uniform(0.4, 0.7), 1),
    })

# ---- Songs (each artist has 4-12 songs) ----
song_themes = [
    "Midnight", "Summer", "Lonely", "Forever", "Lost", "Dreaming", "Heartbreak",
    "Sunshine", "Falling", "Crazy", "Together", "Goodbye", "Paradise", "Drive",
    "Memory", "Stay", "Run", "Fire", "Cold", "Wonder", "Maybe", "Echo",
    "Rain", "Holding On", "Yellow Light", "Vibes", "After Hours", "Closer",
    "Late Night", "Nothing Else", "Coming Home", "Wasted", "Slow Down",
]

songs = []
song_id = 1
for artist in artists:
    num_songs = random.randint(4, 12)
    artist_themes = random.sample(song_themes, num_songs)
    for theme in artist_themes:
        songs.append({
            "song_id": song_id,
            "artist_id": artist["artist_id"],
            "song_title": theme,
            "duration_seconds": random.randint(140, 320),
            "release_date": (date(2020, 1, 1) +
                             timedelta(days=random.randint(0, 1700))).isoformat(),
        })
        song_id += 1

# ---- Users ----
COUNTRIES = [
    ("United States", 30), ("United Kingdom", 12), ("Australia", 8),
    ("Canada", 7), ("Germany", 8), ("Brazil", 9), ("Mexico", 6),
    ("Japan", 5), ("India", 8), ("France", 4), ("Sweden", 3),
]

PLANS = [("Free", 60), ("Premium", 35), ("Family", 5)]

def weighted_choice(pairs):
    items, weights = zip(*pairs)
    return random.choices(items, weights=weights, k=1)[0]

users = []
for uid in range(1, 1501):  # 1500 users
    users.append({
        "user_id": uid,
        "country": weighted_choice(COUNTRIES),
        "plan_type": weighted_choice(PLANS),
        "signup_date": (date(2022, 1, 1) +
                        timedelta(days=random.randint(0, 1000))).isoformat(),
        "age": random.choices(
            [random.randint(13, 17), random.randint(18, 24),
             random.randint(25, 34), random.randint(35, 49),
             random.randint(50, 70)],
            weights=[10, 30, 30, 20, 10]
        )[0],
    })

# ---- Plays (the big fact table) ----
# Some users are heavy listeners, some are light.
# Listeners have favourite genres they play more.
artist_weights = [a["monthly_listeners_millions"] for a in artists]

plays = []
play_id = 1
play_start = datetime(2024, 1, 1, 0, 0)
play_end = datetime(2025, 6, 30, 23, 59)
total_seconds = int((play_end - play_start).total_seconds())

# Each user has a "listening intensity"
user_intensity = {u["user_id"]: random.choices(
    [random.randint(5, 30), random.randint(30, 100),
     random.randint(100, 400), random.randint(400, 1200)],
    weights=[20, 40, 30, 10]
)[0] for u in users}

# Each user has a slight genre preference
user_genre_pref = {u["user_id"]: random.choice(
    ["Pop", "Hip-Hop", "Indie", "R&B", "Reggaeton", None]
) for u in users}

genre_to_artists = {}
for a in artists:
    genre_to_artists.setdefault(a["genre"], []).append(a["artist_id"])
artist_to_songs = {}
for s in songs:
    artist_to_songs.setdefault(s["artist_id"], []).append(s["song_id"])

for user in users:
    uid = user["user_id"]
    n_plays = user_intensity[uid]
    pref = user_genre_pref[uid]

    for _ in range(n_plays):
        # bias 60% of plays toward preferred genre if they have one
        if pref and random.random() < 0.6:
            artist_id = random.choice(genre_to_artists[pref])
        else:
            artist_id = random.choices(
                [a["artist_id"] for a in artists],
                weights=artist_weights
            )[0]

        song_id_chosen = random.choice(artist_to_songs[artist_id])
        # find duration to compute realistic listen time
        song_duration = next(s["duration_seconds"] for s in songs
                             if s["song_id"] == song_id_chosen)

        played_at = play_start + timedelta(
            seconds=random.randint(0, total_seconds)
        )

        # ms_played: most plays are full, some are skips
        r = random.random()
        if r < 0.15:  # quick skip
            ms_played = random.randint(2000, 25000)
            skipped = 1
        elif r < 0.30:  # mid skip
            ms_played = random.randint(25000, song_duration * 1000 // 2)
            skipped = 1
        else:  # full or near-full play
            ms_played = int(song_duration * 1000 * random.uniform(0.85, 1.0))
            skipped = 0

        plays.append({
            "play_id": play_id,
            "user_id": uid,
            "song_id": song_id_chosen,
            "played_at": played_at.isoformat(timespec="seconds"),
            "ms_played": ms_played,
            "skipped": skipped,
        })
        play_id += 1

# ---- Write CSVs ----
def write_csv(rows, fname):
    with open(fname, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

OUT = "/home/claude/music-sql-analysis/data"
write_csv(artists, f"{OUT}/artists.csv")
write_csv(songs, f"{OUT}/songs.csv")
write_csv(users, f"{OUT}/users.csv")
write_csv(plays, f"{OUT}/plays.csv")

print(f"artists: {len(artists)}")
print(f"songs: {len(songs)}")
print(f"users: {len(users)}")
print(f"plays: {len(plays)}")
