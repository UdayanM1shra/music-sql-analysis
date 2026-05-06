-- top 10 most played artists
-- basic join + group by + count

SELECT
    a.artist_name,
    a.genre,
    COUNT(*) AS total_plays
FROM plays p
JOIN songs s   ON p.song_id = s.song_id
JOIN artists a ON s.artist_id = a.artist_id
GROUP BY a.artist_id, a.artist_name, a.genre
ORDER BY total_plays DESC
LIMIT 10;
