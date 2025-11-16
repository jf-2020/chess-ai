# chess-ai

A small research sandbox for building AI chess agents. Currently features a clean CLI, human-vs-random AI play, game saving and replay. Neural net & search agents coming soon.

---

# User Guide

## Running the Program

If you haven't already, activate a virtual environment in your project root:

`source .venv/Scripts/activate`
`pip install -e .`

And run:

`python -m chess_ai`

You'll see a simple menu:
`chess-ai menu:`
`  1) Play human vs random`
`  2) Replay a PGN file`
`  q) Quit`

## Playing a Game (Human vs Random)

Choose 1 from the menu, or run directly:

`python -m chess_ai play`

You'll see an ASCII rendered board, updated each time it is your turn, like below:

+------------------------+
  8 | r n b q k b n r |
  7 | p p p p p p p p |
  6 | . . . . . . . . |
  5 | . . . . . . . . |
  4 | . . . . P . . . |
  3 | . . . . . . . . |
  2 | P P P P . P P P |
  1 | R N B Q K B N R |
  +------------------------+
    a b c d e f g h

The board is displayed with ranks, files, borders, the side-to-move and the last-move-played. **Legend**: White = uppercase, Black = lowercase.

Enter your moves in **UCI format**, such as:

1.`e2e4`
2.`g1f3`
3.`a7a5`

Note that while **UCI** is universally recognized, if it doesn't appear normal to you, it's *OK* to think of it in the usual algebraic notation.

And to resign, enter `q`.


## Saving the Game

You may choose whether the game is saved:

`python -m chess_ai play --save`

Or from the menu, you'll be prompted:

`Save game when finished? [y/N]:`

And saved games go into:

`games/`

Each file is a standard PGN, with naming convention following:

`YYYYMMDD_HHMMSS_game.pgn`


## Replaying a Game

To replay a saved PGN:

`python -m chess_ai replay path/to/game.pgn`

Press **Enter** to advance one move at a time and press **q** to exit early. The board will update after each move.

--- 

# DEV UPDATE LOG

### 0. Base engine and project structure
Created initial package layout, `ChessGame`, `GameSession`, and core architecture.

### 1. CLI play loop
Added `HumanPlayer`, input parsing, ASCII board rendering, and a minimal random agent.

### 2. PGN save + replay
Implemented automatic PGN saving and step-by-step PGN replay.

### 3. CLI entrypoint + cleanup
Added `__main__.py` for simple commands (`python -m chess_ai`), simplified dispatch, and tightened tests.

### 4. TODO
 * Web Interface
 * AI components