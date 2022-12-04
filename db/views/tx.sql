CREATE VIEW tx_view AS
SELECT
    id,
    user_id,
    datetime,
    ticker,
    @amount AS amount,
    price,
    fee,
    note,
    (CASE
    WHEN amount > 0 THEN 'Buy'
    ELSE 'Sell'
    END) AS type
FROM
    tx;