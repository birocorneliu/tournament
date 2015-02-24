-- Table definitions for the tournament project.
-- CREATE DATABASE tournament;

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT
    );


CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    player_a integer REFERENCES players(id),
    player_b integer REFERENCES players(id),
    winner integer REFERENCES players(id),
    CHECK (winner in (player_a, player_b))
    );

CREATE VIEW wins AS
    select p.id, count(m.winner) as wins
    from players p join matches m on p.id=m.winner
    group by p.id;

CREATE VIEW plays AS
    select p.id, count(m.winner) as matches
    from players p join matches m on (p.id=m.player_a or p.id=m.player_b)
    group by p.id;
