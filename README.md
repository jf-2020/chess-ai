# chess-ai

A small research sandbox for building AI chess agents. Right now it provides a basic command line interface, human vs random AI play, game saving and replay. Neural net & search agents will come next.


## Running the Game

First activate your virtual environment. Then, to play **human** vs **random**, run:

`python -m chess_ai play`

You'll see an ASCII chessboard updated each time it is your turn. Example output is below:

|   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|
| r | n | b | q | k | b | n | r |
| p | p | p | p | p | p | p | p |
| . | . | . | . | . | . | . | . |
| . | . | . | . | . | . | . | . |
| . | . | . | . | P | . | . | . |
| . | . | . | . | . | . | . | . |
| P | P | P | P | P | P | P | P |
| R | N | B | Q | K | B | N | R |

**Legend**: White = uppercase, Black = lowercase.

Enter your moves in **UCI format**, such as:

1.`e2e4`
2.`g1f3`
3.`a7a5`

Note that while **UCI** is universally recognized, if it doesn't appear normal to you, it's *OK* to think of it in the usual algebraic notation.

And to resign, enter `q`.


## Saving the Game

Every completed game is saved automatically in:

`games/`

With file naming following the convention:

`YYYYMMDD_HHMMSS_game.pgn`

These are standard PGN files compatible with any (universal) chess software.


## Replaying a Game

To replay a saved PGN:

`python -m chess_ai replay path/to/game.pgn`

Press **Enter** to advance one move at a time.  
Press **q** during replay to exit early.

You'll see the board update after each move.


# DEV UPDATE LOG

### 0. Base engine and project structure
Created initial package layout, `ChessGame`, `GameSession`, and core architecture.

### 1. CLI play loop
Added `HumanPlayer`, input parsing, ASCII board rendering, and a minimal random agent.

### 2. PGN save + replay
Implemented automatic PGN saving and step-by-step PGN replay.

### 3. CLI entrypoint + cleanup
Added `__main__.py` for simple commands (`python -m chess_ai`), simplified dispatch, and tightened tests.