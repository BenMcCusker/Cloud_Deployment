CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

TRUNCATE TABLE books RESTART IDENTITY;

INSERT INTO books (title, author) VALUES ('The Gruffalo', 'Julia Donaldson');
INSERT INTO books (title, author) VALUES ('Ada Twist, Scientist', 'Andrea Beaty');
INSERT INTO books (title, author) VALUES ('The Girl Who Drank the Moon', 'Kelly Barnhill');
INSERT INTO books (title, author) VALUES ('Dragons in a Bag', 'Zetta Elliott');

INSERT INTO users (username, password) VALUES ('testuser', '1234');