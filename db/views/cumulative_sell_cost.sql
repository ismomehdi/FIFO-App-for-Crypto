-- VIEW: cumulative_sell_cost
-- Description: View to calculate the cumulative cost of the sell amount for each transaction.
--
-- id: 
--      This column is selected from the sell_amounts table without any modification.
--
-- datetime: 
--      This column is selected from the sell_amounts table without any modification.
--
-- ticker:
--      This column is selected from the sell_amounts table without any modification.
--
-- total_price:
--      This column is selected from the sell_amounts table without any modification.
--
-- cumulative_sell_cost:
--      This expression calculates the cumulative cost of the sell amount for each transaction.
--      This is used later on by the sell_stats view for calculating the realized gain/loss.
--
-- The LEFT JOIN ON clause specifies the conditions that the rows must satisfy.


CREATE VIEW cumulative_sell_cost AS
SELECT
    DISTINCT ON (id) id,
    datetime,
    sell_amounts.ticker,
    total_price,
    ROUND(previous_cumulative_cost + ((sell_amounts.cumulative_amount - buy_amounts.previous_cumulative_amount) 
        / (buy_amounts.cumulative_amount - buy_amounts.previous_cumulative_amount)) 
        * (cumulative_cost - previous_cumulative_cost), 2) AS cumulative_sell_cost
FROM
    sell_amounts
    LEFT JOIN buy_amounts 
    ON sell_amounts.cumulative_amount > buy_amounts.previous_cumulative_amount
    AND sell_amounts.cumulative_amount <= buy_amounts.cumulative_amount
    AND sell_amounts.ticker = buy_amounts.ticker
ORDER BY
    id, datetime
;