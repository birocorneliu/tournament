Tournament Results
==================

Swiss-system tournament generator and calculator.

Winners are ranked according to OMW.

This works with any amount of players even or odd
and supports draw/tied games.

## Available make targets:
  * `make test` runs tests

tournament.py interface
=======================

```
registerPlayer(name)
```
Adds a player to the tournament by putting an entry in the database. The database should assign an ID number to the player. Different players may have the same names but will receive different ID numbers.

```
countPlayers()
```
Returns the number of currently registered players. This function should not use the Python len() function; it should have the database count the players.

```
deletePlayers()
```
Clear out all the player records from the database.

```
reportMatch(winner, loser, draw=False)
```
Stores the outcome of a single match between two players in the database.

```
deleteMatches()
```
Clear out all the match records from the database.

```
playerStandings()
```
Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has.

```
verifyPlayers(player1, player2)
```
Verifies if players have played or not before

```
swissPairings()
```
Given the existing set of registered players and the matches they have played, generates and returns a list of pairings according to the Swiss system. Each pairing is a tuple (id1, name1, id2, name2), giving the ID and name of the paired players. For instance, if there are eight registered players, this function should return four pairings. This function should use playerStandings to find the ranking of players.
