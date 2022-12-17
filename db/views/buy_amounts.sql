-- VIEW: buy_amounts
-- Description: View to calculate the cumulative amounts and costs of bought transactions
--
-- ticker: 
--      This column is selected from the tx table without any modification.
--
-- SUM(amount) OVER partition_by_ticker AS cumulative_amount: 
--      This expression calculates the cumulative sum of the amount column within 
--      each ticker partition.
--
-- previous_cumulative_amount: 
--      This expression calculates the cumulative sum of the amount column within each ticker 
--      partition, but only for rows that come before the current row in the partition. 
--      The COALESCE function is used to return a default value of 0 if there are no rows before 
--      the current row in the partition.
--
-- cumulative_cost: 
--      This expression calculates the cumulative sum of the total_price within each ticker partition.
--
-- previous_cumulative_cost: 
--      This expression calculates the cumulative sum of the total_price within each ticker
--      partition, but only for rows that come before the current row in the partition. 
--      The COALESCE function is used to return a default value of 0 if there are no rows before 
--      the current row in the partition.

CREATE VIEW buy_amounts AS
SELECT
    ticker,
    SUM(amount) OVER partition_by_ticker AS cumulative_amount,
    COALESCE(SUM(amount) OVER previous_rows, 0) as previous_cumulative_amount,
    SUM(total_price) OVER partition_by_ticker AS cumulative_cost,
    COALESCE(SUM(total_price) OVER previous_rows, 0) AS previous_cumulative_cost
FROM
    tx
WHERE
    amount > 0 WINDOW partition_by_ticker AS (
        PARTITION BY ticker
        ORDER BY datetime
    ),
    previous_rows AS (
        PARTITION BY ticker
        ORDER BY datetime ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
    );