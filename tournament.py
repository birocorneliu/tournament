#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("delete from matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("delete from players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("select count(*) from players;")
    response = int(cursor.fetchone()[0])
    db.close()
    return response


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("insert into players (name) values (%s);", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = """
        SELECT id, name, wins, plays
          FROM players
          JOIN wins USING (id)
          ORDER BY (wins-loses) DESC, wins DESC;
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute(query)
    response = [entry for entry in cursor.fetchall()]
    db.close()
    return response


def reportMatch(winner, loser, draw=False):
    """Records the outcome of a single match between two players.

    If there is a draw, every player will recive in the same time
    a win and a loss. This will basically give him half a point.

    Args:
      winner: the id number of the player who won
      loser: the id number of the player who lost
      draw: true or false if there is a draw or not
    """
    query = """
        insert into matches (winner, loser)
            values (%s, %s);
    """
    db = connect()
    cursor = db.cursor()
    if not draw:
        cursor.execute(query, (winner, loser))
    else:
        cursor.execute(query, (winner, loser))
        cursor.execute(query, (loser, winner))
    db.commit()
    db.close()

def verifyPlayers(player1, player2):
    """Verifies if players played or not before

    Args:
        player1: a tuple of (id, name, wins, matches)
        player2: a tuple of (id, name, wins, matches)
    Returns:
      A tuple which contains (id1, name1, id2, name2) if players haven't played
      else it returns None
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    id1 = player1[0]
    id2 = player2[0]
    query = """
        select * from matches
            where (winner={0} and loser={1})
               or (winner={1} and loser={0});
    """.format(id1, id2)
    db = connect()
    cursor = db.cursor()
    cursor.execute(query)
    response = cursor.fetchone()
    db.close()
    if not response:
        return (player1[0], player1[1], player2[0], player2[1])


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []

    standings = playerStandings()
    if len(standings) % 2 == 1:
        for standing in reversed(standings):
            pairing = verifyPlayers(standing, standing)
            if pairing:
                pairings.append(pairing)
                standings.remove(standing)
                break
    iterations = len(standings) / 2
    for _ in range(iterations):
        standing1 = standings[0]
        standings.remove(standing1)
        for standing in standings:
            pairing = verifyPlayers(standing1, standing)
            if pairing:
                pairings.append(pairing)
                standings.remove(standing)
                break

    return pairings
