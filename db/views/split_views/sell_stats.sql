CREATE VIEW sell_stats_view AS
SELECT
    id,
    datetime,
    ticker,
    amount_sold,
    price,
    -- Compute the total profit and loss by subtracting the fifo cost from the price and then multiplying it with the amount
    --(price - ROUND((cumul_sold_cost - COALESCE(LAG(cumul_sold_cost) OVER w, 0)) / NULLIF(amount_sold, 0), 2)) * amount_sold AS total_pnl
    (

        (price - ((cumul_sold_cost - COALESCE(LAG(cumul_sold_cost) OVER w, 0)) / NULLIF(amount_sold, 0))) * amount_sold::numeric(10,2)
    
    )  AS total_pnl
FROM
    cumul_sold_cost_view 
WINDOW w AS (
    PARTITION BY ticker
    ORDER BY datetime
    );


--


