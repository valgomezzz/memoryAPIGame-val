from fastapi import APIRouter
import random

router = APIRouter(prefix="/memory", tags=["Memory Game"])

# Estado simple del juego global
game_state = {
    "board": [],
    "revealed": [],
    "moves": 0,
    "matched": 0,
    "finished": False
}

def generate_board(size=4):
    """
    Genera un tablero simple de memoria con pares.
    Size=4 → tablero 4x4 (16 cartas)
    """
    total_cards = size * size
    values = list(range(total_cards // 2)) * 2  # pares
    random.shuffle(values)
    return values

@router.post("/new-game")
def new_game(size: int = 4):
    game_state["board"] = generate_board(size)
    game_state["revealed"] = [False] * (size * size)
    game_state["moves"] = 0
    game_state["matched"] = 0
    game_state["finished"] = False

    return {
        "message": "Nuevo juego creado",
        "board_size": size,
        "total_cards": size * size
    }

@router.get("/board")
def get_board():
    # El HTML solo debe ver cartas ocultas o reveladas
    return {
        "board": [
            game_state["board"][i] if game_state["revealed"][i] else "X"
            for i in range(len(game_state["board"]))
        ],
        "moves": game_state["moves"],
        "matched": game_state["matched"],
        "finished": game_state["finished"]
    }

@router.post("/move")
def play_move(card1: int, card2: int):
    if game_state["finished"]:
        return {"message": "El juego ya terminó"}

    game_state["moves"] += 1

    # Revelar temporalmente
    v1 = game_state["board"][card1]
    v2 = game_state["board"][card2]

    if v1 == v2:
        game_state["revealed"][card1] = True
        game_state["revealed"][card2] = True
        game_state["matched"] += 1

        if game_state["matched"] == len(game_state["board"]) // 2:
            game_state["finished"] = True

        return {
            "result": "match",
            "value": v1,
            "moves": game_state["moves"],
            "finished": game_state["finished"]
        }

    else:
        return {
            "result": "no-match",
            "v1": v1,
            "v2": v2,
            "moves": game_state["moves"]
        }