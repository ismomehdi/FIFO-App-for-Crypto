-- VIEW: type
-- Description: Calculates the type of each transaction.
--
-- id: 
--      This column is selected from the tx table without any modification.
--
-- type: 
--      Creates a new column called type that is either 'Buy' or 'Sell' depending 
--      on whether the amount is positive or negative.

CREATE VIEW type AS
SELECT
    id,
    (CASE
    WHEN amount > 0 THEN 'Buy'
    ELSE 'Sell'
    END) AS type
FROM
    tx;
    