# 🧠♟️ chess-ai!

A research sandbox for building chess-playing AI agents — featuring both a command-line interface and an 80s arcade-style web interface you can play in any browser.

Built with Python, Flask, and python-chess, packaged with  Docker, and deployed via Render.

---

### 🌐 Play Online (Web Interface)

If you want to play online, go here:

👉 https://chess-ai.onrender.com

There's an access gate, use this key to unlock it:

`ACCESS_KEY: letmein123`

Once inside, you can play against an automated agent (currently a RandomAgent, but several proper AIs are in the making).

---

### 💻 1. Command Line Game (CLI Mode)

To run the classic terminal-style game locally:

`python -m chess_ai`

It launches an interactive CLI session with board output and move prompts.

---

### 🌐 2. Web-Based Game (Local Dev Server)

Run the Flask web server locally:

`python -m chess_ai.web.app`

Then visit:

👉 http://localhost:5000

Again, you'll have to pass in the access code as above.

(Note that you can override this -- see environment variables!)

---

### 🧪 3. Dev Logs / Tests

Tests are driven by pytest. To run the full suite, use:

`pytest`

Test coverage includes:

* Access-gate
* Web routes
* Core engine
* Session handling
* CLI
* Game logic

Dev logs print automatically from the Flask server when `debug=True` (currently the default).

---

### 🐳 Docker Usage

`Build
docker build -t chess-ai .`

`Run
docker run -p 5000:5000 chess-ai`

Visit the same local URL as above.

---

### ☁️ Render Deployment Notes

The web app is hosted on Render using the project’s Dockerfile, and it proceeds as follows:

1. Clones the GitHub repo
2. Finds the Dockerfile
3. Builds the container
4. Runs it using the CMD inside the Dockerfile
5. Exposes your app publicly at the above Render URL

---

### 🔒 Environment Variables

|Name|Description|Required?|Use|
|---|---|---|---|
|FLASK_SECRET_KEY|Flask session signing|Yes|JFa9_20asdfa82_f12ff|
|ACCESS_KEY|Password for accessing the web UI|Optional|letmein123|

Locally, the app defaults to port 5000.

To run locally with a custom key:

`export ACCESS_KEY=abc123`
`python -m chess_ai.web.app`

---

### 🛠️ Local Development Workflow

Clone:

`git clone https://github.com/jf-2020/chess-ai`
`cd chess-ai`

Create a virtual environment:

`python -m venv .venv`
`source .venv/bin/activate   # or .venv\Scripts\activate (Windows)`

Install dependencies:

`pip install -r requirements.txt`

Run the CLI:

`python -m chess_ai`

Run the web server:

`python -m chess_ai.web.app`

Run tests:

`pytest`

---

### 🏁 Future Roadmap

* Build stronger AI agents (minimax, NN-based, MCTS, expert-based, etc.)
* Move highlighting
* Add PGN web export
* Update UI
* Provide user accounts or saved games