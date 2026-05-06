-- top song for each artist
-- uses a window function to rank songs within each artist
-- and pick the #1 per artist

WITH song_play_counts AS (
    SELECT
        a.artist_name,
        s.song_title,
        COUNT(*) AS plays,
        -- give each song a rank within its artist, by play count
        RANK() OVER (
            PARTITION BY a.artist_id
            ORDER BY COUNT(*) DESC
        ) AS rank_within_artist
    FROM plays p
    JOIN songs s   ON p.song_id = s.song_id
    JOIN artists a ON s.artist_id = a.artist_id
    GROUP BY a.artist_id, a.artist_name, s.song_id, s.song_title
)
SELECT
    artist_name,
    song_title AS top_song,
    plays
FROM song_play_counts
WHERE rank_within_artist = 1
ORDER BY plays DESC;
