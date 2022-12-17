-- VIEW: sell_amounts
-- Description: View to calculate the cumulative amounts of sold transactions.
--
-- id: 
--      This column is selected from the tx table without any modification.
--
-- ticker: 
--      This column is selected from the tx table without any modification.
--
-- datetime: 
--      This column is selected from the tx table without any modification.
--
-- amount: 
--      This expression negates the amount column and represents the sell
--      amount of each transaction as a negative number.
--
-- cumulative_amount: 
--      This expression calculates the cumulative sum of the negated amount 
--      within each ticker partition.
--
-- total_price:
--      This column is selected from the tx table without any modification.

CREATE VIEW sell_amounts AS
SELECT
    id,
    ticker,
    datetime,
    - amount AS amount,
    SUM(- amount) OVER partition_by_ticker AS cumulative_amount,
    total_price
FROM
    tx
WHERE
    amount < 0 WINDOW partition_by_ticker AS (
        PARTITION BY ticker
        ORDER BY datetime
    );
    
