CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);
ALTER TABLE users ADD CONSTRAINT unique_name UNIQUE (username);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    task TEXT,
    done BOOLEAN DEFAULT FALSE
);