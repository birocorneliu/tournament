-- Table definitions for the tournament project.
-- CREATE DATABASE tournament;

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT
    );

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    winner integer REFERENCES players(id),
    loser integer REFERENCES players(id)
    );

-- Create view that contains player_id, wins, loses and plays
CREATE VIEW wins AS
    select players.id, wins, loses, (wins + loses) as plays
      from players
      join (
        select p.id, count(m.loser) as loses
          from players p left join matches m on p.id=m.loser
          group by p.id) as ls
      on ls.id =players.id
      join (
        select p.id, count(m.winner) as wins
          from players p left join matches m on p.id=m.winner
          group by p.id) as wn
      on wn.id=players.id;

--DROP VIEW wins;
--DROP TABLE matches;
--DROP TABLE players;
