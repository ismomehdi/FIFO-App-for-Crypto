SELECT
    tx_view.id,
    tx_view.datetime,
    tx_view.ticker,
    tx_view.amount,
    tx_view.price,
    tx_view.fee,
    tx_view.note,
    tx_view.type,
    sell_stats_view.total_pnl
FROM
    tx_view
LEFT JOIN 
    sell_stats_view
ON 
    tx_view.id = sell_stats_view.id
WHERE
    tx_view.portfolio_id = 1
ORDER BY 
    datetime, tx_view.id;
