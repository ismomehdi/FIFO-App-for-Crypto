--Creates a user, then creates a portfolio for that user, 
--and then creates a settings row for that user with the
--newly created portfolio set as the default portfolio.

WITH user_row AS (
    INSERT INTO
        users (username, password)
    VALUES
        (:username, :password) RETURNING id
),
portfolio_row AS (
    INSERT INTO
        portfolio (user_id, name)
    SELECT
        id,
        'My Portfolio'
    FROM
        user_row RETURNING user_id,
        id
) 
INSERT INTO
    settings (user_id, default_portfolio_id)
SELECT
    user_id,
    id
FROM
    portfolio_row;

