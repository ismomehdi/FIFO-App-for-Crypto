CREATE VIEW sold_amounts_view AS
SELECT
    id,
    ticker,
    datetime,
    - amount AS amount_sold,
    SUM(- amount) OVER w AS cumul_sold,
    price
FROM
    tx
WHERE
    amount < 0 WINDOW w AS (
        PARTITION BY ticker
        ORDER BY datetime
    );