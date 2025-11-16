from fastapi import APIRouter
from models import MemoryGame

router = APIRouter()

# 🔥 Instancia global del juego (persistente mientras Render no duerme)
game = MemoryGame()


@router.get("/create-game")
def create_game():
    global game
    game = MemoryGame()
    return {
        "message": "Juego creado correctamente",
        "state": game.get_state()
    }


@router.get("/state")
def get_state():
    return game.get_state()


@router.get("/flip/{card_id}")
def flip(card_id: int):
    return game.flip_card(card_id)


@router.get("/reset")
def reset():
    global game
    game = MemoryGame()
    return {
        "message": "Juego reiniciado",
        "state": game.get_state()
    }