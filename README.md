# chess-ai!

A small research sandbox for building AI chess agents. Currently features a clean CLI, human-vs-random AI play, game saving and replay. Neural net & search agents coming soon.

---
# User Guide

## Running the Program

If you haven't already, activate a virtual environment in your project root:

```
source .venv/Scripts/activate
pip install -e .
```
Then run:

`python -m chess_ai`

After that, you'll see a simple menu:

`chess-ai menu:`
- `  1) Play human vs random`
- `  2) Replay a PGN file`
- `  q) Quit`

## Playing a Game (Human vs Random)

Choose **(1)** from the menu, or run:

`python -m chess_ai play`

You'll see an ASCII rendered board updated each time it is your turn much like below:

|  | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| 8 | r | n | b | q | k | b | n | r |
| 7 | p | p | p | p | p | p | p | p |
| 6 | . | . | . | . | . | . | . | . |
| 5 | . | . | . | . | . | . | . | . |
| 4 | . | . | . | . | P | . | . | . |
| 3 | . | . | . | . | . | . | . | . |
| 2 | P | P | P | P | . | P | P | P |
| 1 | R | N | B | Q | K | B | N | R |

**White** is in uppercase; **black** is in lower. You'll notice game & board *metadata* like ranks, files, borders, the side-to-move and the last-move-played as well.

The engine operates on **UCI format**, so make sure your move syntax is like:
- `e2e4`
- `g1f3`
- `a7a5`

And to resign, enter `q`.


## Saving the Game

You can choose whether the game to save a game:

`python -m chess_ai play --save`

But you'll also be prompted via the menu:

`Save game when finished? [y/N]:`

Each saved game is stored in a standard PGN file format with the following naming convention:

`YYYYMMDD_HHMMSS_game.pgn`

To be found in this folder:

`games/`


## Replaying a Game

To replay a saved game (via a PGN file), run:

`python -m chess_ai replay path/to/game.pgn`

Press **Enter** to advance one move at a time and **q** to exit. The board will update after each move.


--- 
# Update Log

### 0. Base Engine & Project Structure
Created initial package layout, `ChessGame`, `GameSession`, and core architecture.

### 1. Board Interface & Play Loop
Added `HumanPlayer`, input parsing, ASCII board rendering, and a minimal random agent.

### 2. Save + Replay
Implemented automatic PGN saving and step-by-step PGN replay.

### 3. CLI Entrypoint
Added `__main__.py` for simple commands (`python -m chess_ai`), simplified dispatch, and tightened tests.

### 4. TODO
 * Web Interface
 * AI components