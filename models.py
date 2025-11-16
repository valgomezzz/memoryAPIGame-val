from typing import List

class GameState:
    def __init__(self):
        self.board: List[str] = []
        self.revealed: List[int] = []
        self.moves: int = 0