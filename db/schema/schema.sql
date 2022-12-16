CREATE TABLE users (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL 
);

CREATE TABLE portfolio (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    user_id BIGINT REFERENCES users (id),
    name TEXT NOT NULL
);

CREATE TABLE tx (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    portfolio_id BIGINT REFERENCES portfolio (id),
    datetime TIMESTAMP NOT NULL,
    ticker TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    price NUMERIC NOT NULL,
    fee NUMERIC,
    note TEXT
);

CREATE TABLE settings (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    user_id BIGINT REFERENCES users (id),
    default_portfolio_id BIGINT REFERENCES portfolio (id)
);

CREATE TABLE feedback (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    message TEXT NOT NULL 
);

