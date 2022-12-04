CREATE VIEW cumul_sold_cost_view AS
SELECT DISTINCT
    id,
    datetime,
    sold_amounts_view.ticker,
    amount_sold,
    price,
    ROUND(prev_cumul_cost + ((sold_amounts_view.cumul_sold - bought_amounts_view.prev_cumul_bought) 
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