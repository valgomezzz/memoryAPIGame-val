import random
import time


class Card:
    def __init__(self, id, value):
        self.id = id
        self.value = value      # Identificador del par (0–7)
        self.revealed = False   # Está boca arriba
        self.solved = False     # Ya se emparejó

    def to_dict(self):
        return {
            "id": self.id,
            "value": self.value if self.revealed or self.solved else None,
            "revealed": self.revealed,
            "solved": self.solved
        }


class MemoryBoard:
    def __init__(self, size=16):
        self.size = size
        self.pairs = size // 2
        self.cards = self._generate_cards()

    def _generate_cards(self):
        values = list(range(self.pairs)) * 2  # Ej: [0,0,1,1,...7,7]
        random.shuffle(values)
        return [Card(i, values[i]) for i in range(self.size)]

    def to_dict(self):
        return [card.to_dict() for card in self.cards]


class MemoryGame:
    def __init__(self):
        self.board = MemoryBoard()
        self.first_pick = None
        self.second_pick = None
        self.moves = 0
        self.solved_pairs = 0
        self.game_over = False

        # 🔥 TEMPORIZADOR
        self.start_time = time.time()
        self.end_time = None

    def _get_elapsed_time(self):
        if self.end_time:
            return round(self.end_time - self.start_time, 2)
        return round(time.time() - self.start_time, 2)

    def flip_card(self, card_id):
        if self.game_over:
            return {"error": "El juego ya terminó"}

        card = self.board.cards[card_id]

        if card.solved or card.revealed:
            return {"error": "Carta ya revelada o resuelta"}

        card.revealed = True

        if self.first_pick is None:
            self.first_pick = card
            return {
                "status": "primera",
                "card": card.to_dict(),
                "elapsed_time": self._get_elapsed_time()
            }

        elif self.second_pick is None:
            self.second_pick = card
            self.moves += 1
            return self._evaluate_turn()

    def _evaluate_turn(self):
        c1 = self.first_pick
        c2 = self.second_pick

        if c1.value == c2.value:
            c1.solved = True
            c2.solved = True
            self.solved_pairs += 1
            result = "match"
        else:
            # Voltear de nuevo
            c1.revealed = False
            c2.revealed = False
            result = "no_match"

        # Reset picks
        self.first_pick = None
        self.second_pick = None

        # Juego terminado
        if self.solved_pairs == self.board.pairs:
            self.game_over = True
            self.end_time = time.time()

        return {
            "result": result,
            "moves": self.moves,
            "solved_pairs": self.solved_pairs,
            "game_over": self.game_over,
            "elapsed_time": self._get_elapsed_time(),
            "board": self.board.to_dict()
        }

    def reset_game(self):
        self.__init__()

    def get_state(self):
        return {
            "board": self.board.to_dict(),
            "moves": self.moves,
            "solved_pairs": self.solved_pairs,
            "game_over": self.game_over,
            "elapsed_time": self._get_elapsed_time()
        }