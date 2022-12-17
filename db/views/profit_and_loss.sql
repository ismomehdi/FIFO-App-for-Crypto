-- VIEW: profit_and_loss
-- Description: Calculates the total profit and loss for transactions in the cumulative_sell_cost view.
--
-- id:
--     This column is selected from the cumulative_sell_cost table without any modification.
--
-- total_pnl:
--      This expression calculates the total profit and loss for each transaction. The result 
--      is cast to a numeric value with 18 digits and 2 decimal places.

CREATE VIEW profit_and_loss AS
SELECT
    id,
    (total_price - (cumulative_sell_cost - COALESCE(LAG(cumulative_sell_cost) OVER partition_by_ticker, 0)))
        ::numeric(18,2)  AS total_pnl
FROM
    cumulative_sell_cost 
WINDOW partition_by_ticker AS (
    PARTITION BY ticker
    ORDER BY datetime
    );
