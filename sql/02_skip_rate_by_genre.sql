-- skip rate by genre
-- which genres do people skip the most?

SELECT
    a.genre,
    COUNT(*)                                              AS total_plays,
    SUM(p.skipped)                                        AS total_skips,
    ROUND(100.0 * SUM(p.skipped) / COUNT(*), 2)           AS skip_rate_pct
FROM plays p
JOIN songs s   ON p.song_id = s.song_id
JOIN artists a ON s.artist_id = a.artist_id
GROUP BY a.genre
ORDER BY skip_rate_pct DESC;
