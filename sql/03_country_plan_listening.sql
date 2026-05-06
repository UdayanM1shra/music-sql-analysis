-- average plays per user, broken down by country and plan type
-- two-dimensional grouping

SELECT
    u.country,
    u.plan_type,
    COUNT(DISTINCT u.user_id)                           AS num_users,
    COUNT(p.play_id)                                    AS total_plays,
    ROUND(1.0 * COUNT(p.play_id)
              / COUNT(DISTINCT u.user_id), 1)           AS avg_plays_per_user
FROM users u
LEFT JOIN plays p ON u.user_id = p.user_id
GROUP BY u.country, u.plan_type
HAVING COUNT(DISTINCT u.user_id) >= 5  -- skip tiny groups
ORDER BY u.country, u.plan_type;
