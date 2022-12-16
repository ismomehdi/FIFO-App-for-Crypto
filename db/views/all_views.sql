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

CREATE VIEW cumul_sold_cost_view AS
SELECT DISTINCT
    id,
    datetime,
    sold_amounts_view.ticker,
    amount_sold,
    price,
    TRUNC(prev_cumul_cost + ((sold_amounts_view.cumul_sold - bought_amounts_view.prev_cumul_bought) 
    / (bought_amounts_view.cumul_bought - bought_amounts_view.prev_cumul_bought)) * (cumul_cost - prev_cumul_cost), 2) AS cumul_sold_cost
FROM
    sold_amounts_view
    LEFT JOIN bought_amounts_view 
    ON sold_amounts_view.cumul_sold > bought_amounts_view.prev_cumul_bought
    AND sold_amounts_view.cumul_sold <= bought_amounts_view.cumul_bought
    AND sold_amounts_view.ticker = bought_amounts_view.ticker
ORDER BY
    datetime, id    
;

CREATE VIEW sell_stats_view AS
SELECT
    id,
    datetime,
    ticker,
    amount_sold,
    price,
    -- Compute the total profit and loss by subtracting the fifo cost from the price and then multiplying it with the amount
    (price - TRUNC((cumul_sold_cost - COALESCE(LAG(cumul_sold_cost) OVER w, 0)) / NULLIF(amount_sold, 0), 2)) * amount_sold AS total_pnl
FROM
    cumul_sold_cost_view 
WINDOW w AS (
    PARTITION BY ticker
    ORDER BY datetime
    );

CREATE VIEW tx_view AS
SELECT
    id,
    portfolio_id,
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