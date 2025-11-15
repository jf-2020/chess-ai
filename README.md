# Chess AI

A multi-phase AI project to build a chess engine with a command-line interface and eventually a set of neural-network driven AIs of varying type.

While the goal of the project is the chess AI, it's also an attempt to complete a full "end-to-end" AI project (because it's not *just* about the math).

---

### Goal 0: Scaffolding

- Established project structure.
- Separated code into clear domains:
  - `core/` - game logic & abstractions
  - `agents/` - AI implementations
  - `cli/` - command-line interface & human interaction

---

### Goal 1: Core Game Logic & Player Abstractions

- Implemented `ChessGame`, a wrapper around **python-chess**, providing:
  - board state
  - move generation & application
  - game state checks
  - result handling
- Implemented `Player`, a base class for anything that can move.
- Added the first AI, `RandomAgent`.
- Implemented `GameSession`, the game loop that:
  - alternates turns based on board state
  - requests moves from each player
  - applies moves to the shared `ChessGame`
  - handles resignation/quit cases
  - returns a final chess result string (`"1-0"`, `"0-1"`, `"1/2-1/2"`)
- Added first automated test confirming random-vs-random completes successfully.

---

### Goal 2: NEXT STEPS

- Implement CLI interaction:
  - ASCII board rendering
  - `HumanPlayer` input parsing (UCI)
  - a runnable `humand vs random` command
- After that: state enconding & initial neural network model