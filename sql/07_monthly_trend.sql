-- monthly play trend with month over month change
-- uses a window function (LAG) to compare each month to the one before

WITH monthly_plays AS (
    SELECT
        strftime('%Y-%m', played_at) AS month,
        COUNT(*)                     AS plays
    FROM plays
    GROUP BY month
)
SELECT
    month,
    plays,
    LAG(plays) OVER (ORDER BY month) AS prev_month_plays,
    plays - LAG(plays) OVER (ORDER BY month) AS change_vs_prev,
    ROUND(
        100.0 * (plays - LAG(plays) OVER (ORDER BY month))
              / LAG(plays) OVER (ORDER BY month),
        2
    ) AS pct_change
FROM monthly_plays
ORDER BY month;
