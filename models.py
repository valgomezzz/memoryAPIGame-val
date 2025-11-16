import random
import time

class MemoryGame:
    def __init__(self):
        # Tiempo de inicio
        self.start_time = time.time()

        # Movimientos del jugador
        self.moves = 0

        # 🔥 1. Hay 10 cartas disponibles (0–9)
        available_cards = list(range(10))

        # 🔥 2. Seleccionar aleatoriamente 8 cartas distintas
        selected = random.sample(available_cards, 8)

        # 🔥 3. Duplicar las cartas (un par de cada una)
        deck = selected * 2  # ahora son 16 cartas

        # 🔥 4. Mezclar el mazo
        random.shuffle(deck)

        # 🔥 5. Construir el tablero con estructura original
        self.board = [
            {"id": i, "value": deck[i], "revealed": False, "solved": False}
            for i in range(16)
        ]

        # Variables del juego
        self.first_card = None
        self.solved_pairs = 0


    def flip(self, card_id):
        """Voltear carta y manejar la lógica de parejas"""
        card = self.board[card_id]

        if card["revealed"] or card["solved"]:
            return self.get_state()

        card["revealed"] = True

        if self.first_card is None:
            # Es la primera carta del turno
            self.first_card = card
        else:
            # Segunda carta
            self.moves += 1

            if self.first_card["value"] == card["value"]:
                # Encontró par
                self.first_card["solved"] = True
                card["solved"] = True
                self.solved_pairs += 1
            else:
                # No coincide → ocultarlas luego
                first = self.first_card
                second = card

                # Ocultarlas después de 1 segundo (simulado)
                first["revealed"] = False
                second["revealed"] = False

            # Reiniciar selección
            self.first_card = None

        return self.get_state()


    def get_state(self):
        """Retorna el estado completo del juego"""
        elapsed = round(time.time() - self.start_time, 1)

        return {
            "board": self.board,
            "moves": self.moves,
            "pairs_found": self.solved_pairs,
            "game_over": self.solved_pairs == 8,
            "elapsed_time": elapsed
        }