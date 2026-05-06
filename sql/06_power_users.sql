-- power users
-- find users in the top 10% by play count and look at what they listen to

WITH user_plays AS (
    SELECT
        user_id,
        COUNT(*) AS total_plays
    FROM plays
    GROUP BY user_id
),
threshold AS (
    -- the play count that puts you in the top 10%
    -- ntile would be cleaner but this works in plain sqlite
    SELECT total_plays AS cutoff
    FROM user_plays
    ORDER BY total_plays DESC
    LIMIT 1 OFFSET (SELECT COUNT(*) / 10 FROM user_plays)
),
power_users AS (
    SELECT user_id, total_plays
    FROM user_plays
    WHERE total_plays >= (SELECT cutoff FROM threshold)
)
SELECT
    u.country,
    u.plan_type,
    COUNT(*)                            AS power_users,
    ROUND(AVG(pu.total_plays), 0)       AS avg_plays
FROM power_users pu
JOIN users u ON pu.user_id = u.user_id
GROUP BY u.country, u.plan_type
ORDER BY power_users DESC;
