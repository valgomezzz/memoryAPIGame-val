from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import uuid

app = FastAPI()

# Memoria temporal de juegos (en producción usarías una DB)
games = {}

class Move(BaseModel):
    pos1: int
    pos2: int

@app.get("/")
def root():
    return {"message": "🟪 Memory Game API funcionando correctamente"}

def generate_board():
    cards = list(range(1, 9)) * 2  # 8 parejas -> 16 cartas
    random.shuffle(cards)
    return cards

@app.post("/game/create")
def create_game():
    game_id = str(uuid.uuid4())

    board = generate_board()
    state = ["?" for _ in range(16)]  # Todas cubiertas

    games[game_id] = {
        "board": board,
        "state": state,
        "moves": 0,
        "matches": 0,
        "won": False
    }

    return {
        "game_id": game_id,
        "state": state
    }

@app.get("/game/{game_id}")
def get_game(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    return games[game_id]

@app.post("/game/{game_id}/move")
def make_move(game_id: str, move: Move):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    pos1 = move.pos1
    pos2 = move.pos2

    # Validaciones
    if pos1 == pos2:
        raise HTTPException(status_code=400, detail="Choose two different positions")

    if not (0 <= pos1 < 16 and 0 <= pos2 < 16):
        raise HTTPException(status_code=400, detail="Positions must be between 0 and 15")

    if game["state"][pos1] != "?" or game["state"][pos2] != "?":
        raise HTTPException(status_code=400, detail="One or both cards are already revealed")

    game["moves"] += 1

    card1 = game["board"][pos1]
    card2 = game["board"][pos2]

    if card1 == card2:
        game["state"][pos1] = card1
        game["state"][pos2] = card2
        game["matches"] += 1

        if game["matches"] == 8:
            game["won"] = True

        return {
            "match": True,
            "card": card1,
            "state": game["state"],
            "won": game["won"]
        }
    else:
        return {
            "match": False,
            "card1": card1,
            "card2": card2,
            "state": game["state"]
        }

@app.post("/game/{game_id}/reset")
def reset_game(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    board = generate_board()

    games[game_id] = {
        "board": board,
        "state": ["?" for _ in range(16)],
        "moves": 0,
        "matches": 0,
        "won": False
    }

    return {"message": "Game reset", "state": games[game_id]["state"]}