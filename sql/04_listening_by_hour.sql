-- when do people listen most? by hour of day.
-- uses sqlite's strftime to pull the hour out of the timestamp

SELECT
    CAST(strftime('%H', played_at) AS INTEGER) AS hour_of_day,
    COUNT(*)                                   AS plays,
    ROUND(AVG(ms_played) / 1000.0, 1)          AS avg_seconds_listened
FROM plays
GROUP BY hour_of_day
ORDER BY hour_of_day;
