SELECT
    tx.id,
    tx.datetime,
    tx.ticker,
    @amount AS amount,
    tx.total_price,
    tx.fee,
    tx.note,
    type.type,
    profit_and_loss.total_pnl
FROM
    tx
LEFT JOIN 
    profit_and_loss
ON 
    tx.id = profit_and_loss.id
LEFT JOIN
    type
ON
    tx.id = type.id
WHERE
    portfolio_id = :portfolio_id
ORDER BY 
    datetime DESC, id DESC;
