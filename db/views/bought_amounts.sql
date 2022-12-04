CREATE VIEW bought_amounts_view AS
SELECT
    ticker,
    SUM(amount) OVER w AS cumul_bought,
    COALESCE(SUM(amount) OVER prev_w, 0) as prev_cumul_bought,
    amount * price AS cost,
    SUM(amount * price) OVER w AS cumul_cost,
    COALESCE(SUM(amount * price) OVER prev_w, 0) AS prev_cumul_cost
FROM
    tx
WHERE
    amount > 0 WINDOW w AS (
        PARTITION BY ticker
        ORDER BY datetime
    ),
    prev_w AS (
        PARTITION BY ticker
        ORDER BY datetime ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
    );