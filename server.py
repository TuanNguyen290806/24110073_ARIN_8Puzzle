import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from BFS import BFS
from DFS import DFS
from UCS import UCS
ROOT = Path(__file__).parent
ALGORITHMS = {"bfs": BFS, "dfs": DFS, "ucs": UCS}


class EightPuzzle:
    GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    COSTS = {"Up": 1, "Down": 1, "Left": 2, "Right": 2}

    def __init__(self, initial):
        self.initial_state = tuple(initial)

    def is_goal(self, state):
        return state == self.GOAL

    def actions(self, state):
        row, col = divmod(state.index(0), 3)
        acts = []
        if row > 0: acts.append("Up")
        if row < 2: acts.append("Down")
        if col > 0: acts.append("Left")
        if col < 2: acts.append("Right")
        return acts

    def result(self, state, action):
        i = state.index(0)
        j = i + {"Up": -3, "Down": 3, "Left": -1, "Right": 1}[action]
        s = list(state)
        s[i], s[j] = s[j], s[i]
        return tuple(s)

    def step_cost(self, state, action):
        return self.COSTS[action]

def parse_tiles(text):
    try:
        tiles = [int(x) for x in text.split(",")]
    except ValueError:
        return None
    return tuple(tiles) if sorted(tiles) == list(range(9)) else None


def solve(tiles, search):
    problem = EightPuzzle(tiles)
    started = time.perf_counter()
    moves = search(problem)
    seconds = time.perf_counter() - started
    if moves is None:
        return {"moves": None, "states": None, "seconds": seconds}
    states = [tiles]
    for move in moves:
        states.append(problem.result(states[-1], move))
    return {"moves": moves, "states": states, "seconds": seconds}


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def reply_json(self, status, payload):
        self.reply(status, "application/json", json.dumps(payload).encode())

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/":
            self.reply(200, "text/html; charset=utf-8", (ROOT / "index.html").read_bytes())
        elif url.path == "/solve":
            query = parse_qs(url.query)
            tiles = parse_tiles(query.get("tiles", [""])[0])
            search = ALGORITHMS.get(query.get("algo", ["bfs"])[0])
            if tiles is None:
                self.reply_json(400, {"error": "Use each number from 0 to 8 exactly once."})
            elif search is None:
                self.reply_json(400, {"error": "Unknown algorithm."})
            else:
                self.reply_json(200, solve(tiles, search))
        else:
            self.reply_json(404, {"error": "Not found."})

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("Open http://localhost:%d (Ctrl+C to stop)" % port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
