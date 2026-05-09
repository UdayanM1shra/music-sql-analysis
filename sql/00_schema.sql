-- schema for the music streaming dataset in sqllite


DROP TABLE IF EXISTS plays;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS artists;
DROP TABLE IF EXISTS users;

CREATE TABLE artists (
    artist_id INTEGER PRIMARY KEY,
    artist_name TEXT NOT NULL,
    genre TEXT,
    monthly_listeners_millions REAL
);

CREATE TABLE songs (
    song_id INTEGER PRIMARY KEY,
    artist_id INTEGER NOT NULL,
    song_title TEXT NOT NULL,
    duration_seconds INTEGER,
    release_date DATE,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    country TEXT,
    plan_type  TEXT,        -- Free, Premium, or Family
    signup_date DATE,
    age INTEGER
);

CREATE TABLE plays (
    play_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    song_id INTEGER NOT NULL,
    played_at TIMESTAMP NOT NULL,
    ms_played INTEGER, -- how long they listened in ms
    skipped INTEGER,    -- 1 if skipped early, 0 if listened fully
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id)
);

CREATE INDEX idx_songs_artist ON songs(artist_id);
CREATE INDEX idx_plays_user   ON plays(user_id);
CREATE INDEX idx_plays_song   ON plays(song_id);
CREATE INDEX idx_plays_date   ON plays(played_at);
