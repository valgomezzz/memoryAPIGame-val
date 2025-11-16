import random
import time

class MemoryGame:
    def __init__(self):
        self.start_time = time.time()
        self.moves = 0

        available = list(range(10))
        selected = random.sample(available, 8)
        deck = selected * 2
        random.shuffle(deck)

        self.board = [
            {"id": i, "value": deck[i], "revealed": False, "solved": False}
            for i in range(16)
        ]

        self.first_card = None
        self.solved_pairs = 0


    def flip_card(self, card_id):
        """Voltear carta y manejar la lógica de parejas correctamente"""
        card = self.board[card_id]

        # No permitir voltear cartas ya resueltas
        if card["solved"]:
            return self.get_state()

        # No permitir tocar más de 2 al tiempo
        opened = [c for c in self.board if c["revealed"] and not c["solved"]]
        if len(opened) >= 2:
            return self.get_state()

        # Si ya estaba revelada, ignorar
        if card["revealed"]:
            return self.get_state()

        # Voltear esta carta
        card["revealed"] = True

        # PRIMERA CARTA DEL TURNO
        if self.first_card is None:
            self.first_card = card
            return self.get_state()

        # SEGUNDA CARTA DEL TURNO
        self.moves += 1

        # SI HACEN MATCH
        if self.first_card["value"] == card["value"]:
            self.first_card["solved"] = True
            card["solved"] = True
            self.solved_pairs += 1
            self.first_card = None
            return self.get_state()

        # SI NO HACEN MATCH → esperar medio segundo ANTES de ocultar
        first = self.first_card
        second = card

        time.sleep(0.5)  # ⭐️ IMPORTANTE: permite que el frontend vea la carta

        first["revealed"] = False
        second["revealed"] = False
        self.first_card = None

        return self.get_state()


    def get_state(self):
        elapsed = round(time.time() - self.start_time, 1)

        return {
            "board": self.board,
            "moves": self.moves,
            "pairs_found": self.solved_pairs,
            "game_over": self.solved_pairs == 8,
            "elapsed_time": elapsed
        }