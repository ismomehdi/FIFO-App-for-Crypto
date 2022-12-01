fifo_sql = """
SELECT
    tx1.id,
    tx1.datetime,
    tx1.ticker,
    tx1.amount,
    tx1.price,
    tx1.fee,
    tx1.note,
    tx1.type,
    fifo.total_pnl,
    fifo.pnl_percentage || '%' AS pnl_percentage
FROM
    (
        SELECT
            id,
            datetime,
            ticker,
            @amount AS amount,
            price,
            fee,
            note,
            (
                CASE
                    WHEN amount > 0 THEN 'Buy'
                    ELSE 'Sell'
                END
            ) AS type
        FROM
            tx
        WHERE
            user_id = 1
    ) AS tx1
    LEFT JOIN (
        SELECT
            id,
            datetime,
            ticker,
            amount_sold,
            price,
            -- The next line computes the total profit and loss by subtracting the fifo cost from the price and then multiplying it with the amount
            (
                price - ROUND(
                    (
                        cumul_sold_cost - COALESCE(LAG(cumul_sold_cost) OVER w, 0)
                    ) / amount_sold,
                    2
                )
            ) * amount_sold AS total_pnl,
            -- The next command calculates the pnl percentage with the following formula: (price - fifo cost) / cost * 100.
            ROUND(
                (
                    price - ROUND(
                        (
                            cumul_sold_cost - COALESCE(LAG(cumul_sold_cost) OVER w, 0)
                        ) / amount_sold,
                        2
                    )
                ) / ROUND(
                    (
                        cumul_sold_cost - COALESCE(LAG(cumul_sold_cost) OVER w, 0)
                    ) / amount_sold,
                    2
                ) * 100
            ) AS pnl_percentage
        FROM
            (
                SELECT
                    id,
                    datetime,
                    sold_amounts.ticker,
                    amount_sold,
                    price,
                    ROUND(
                        prev_cumul_cost + (
                            (
                                sold_amounts.cumul_sold - bought_amounts.prev_cumul_bought
                            ) / (
                                bought_amounts.cumul_bought - bought_amounts.prev_cumul_bought
                            )
                        ) * (cumul_cost - prev_cumul_cost),
                        2
                    ) AS cumul_sold_cost
                FROM
                    -- This selects the sold amounts
                    (
                        SELECT
                            id,
                            ticker,
                            datetime,
                            - amount AS amount_sold,
                            SUM(- amount) OVER w AS cumul_sold,
                            price
                        FROM
                            tx
                        WHERE
                            amount < 0 WINDOW w AS (
                                PARTITION BY ticker
                                ORDER BY
                                    datetime
                            )
                    ) AS sold_amounts
                    LEFT JOIN -- This selects the bought amounts
                    (
                        SELECT
                            ticker,
                            SUM(amount) OVER w AS cumul_bought,
                            COALESCE(SUM(amount) OVER prev_w, 0) as prev_cumul_bought,
                            amount * price AS cost,
                            SUM(amount * price) OVER w AS cumul_cost,
                            COALESCE(SUM(amount * price) OVER prev_w, 0) AS prev_cumul_cost
                        FROM
                            tx
                        WHERE
                            amount > 0 WINDOW w AS (
                                PARTITION BY ticker
                                ORDER BY
                                    datetime
                            ),
                            prev_w AS (
                                PARTITION BY ticker
                                ORDER BY
                                    datetime ROWS BETWEEN unbounded preceding
                                    AND 1 preceding
                            )
                    ) AS bought_amounts ON sold_amounts.cumul_sold > bought_amounts.prev_cumul_bought
                    AND sold_amounts.cumul_sold <= bought_amounts.cumul_bought
                    AND sold_amounts.ticker = bought_amounts.ticker
            ) t WINDOW w AS (
                PARTITION BY ticker
                ORDER BY
                    datetime
            )
    ) AS fifo ON tx1.id = fifo.id
ORDER BY
    datetime, tx1.id;
"""