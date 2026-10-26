-- operational_analytics.sql
-- Strategy queries assessing service failures and user impacts

-- QUERY 1: Pinpoint high-tier premium users caught in the automated refund failure loop
-- Purpose: Targets priority batch workflows to protect higher-tier loyalty segments
WITH RefundFailures AS (
    SELECT 
        t.user_id,
        u.subscription_tier,
        COUNT(t.transaction_id) as failed_refund_count,
        SUM(t.amount) as total_trapped_capital_base
    FROM transactions t
    JOIN users u ON t.user_id = u.user_id
    WHERE t.status = 'failed'
    GROUP BY t.user_id, u.subscription_tier
)
SELECT 
    user_id,
    subscription_tier,
    failed_refund_count,
    total_trapped_capital_base,
    RANK() OVER (PARTITION BY subscription_tier ORDER BY total_trapped_capital_base DESC) as priority_rank
FROM RefundFailures
WHERE subscription_tier IN ('Ultra', 'Metal', 'Premium')
LIMIT 15;


-- QUERY 2: Analyze rolling average handle times (AHT) to observe operational queue degradation
-- Purpose: Quantifies how severely the airline disruption damaged support performance thresholds
SELECT 
    DATE(created_at) as operation_date,
    initial_tag,
    COUNT(ticket_id) as total_escalations,
    AVG(handle_time_minutes) as daily_avg_handle_time,
    AVG(handle_time_minutes) - AVG(AVG(handle_time_minutes)) OVER(PARTITION BY initial_tag ORDER BY DATE(created_at) ROWS BETWEEN 7 PRECEDING AND CURRENT ROW) as deviation_from_baseline
FROM support_tickets
GROUP BY operation_date, initial_tag
ORDER BY operation_date ASC;
