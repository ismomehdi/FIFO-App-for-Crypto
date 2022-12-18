SELECT
    tx.id,
    tx.datetime,
    tx.ticker,
    @amount AS amount,
    tx.total_price,
    tx.fee,
    tx.note,
    COALESCE(profit_and_loss.type, 'Buy') AS type,
    profit_and_loss.total_pnl
FROM
    tx
LEFT JOIN 
    profit_and_loss
ON 
    tx.id = profit_and_loss.id
WHERE
    portfolio_id = 2
ORDER BY 
    datetime DESC, id DESC;
