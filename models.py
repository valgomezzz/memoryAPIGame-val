import random
import time

class MemoryGame:
    def __init__(self):
        # Tiempo de inicio
        self.start_time = time.time()

        # Movimientos del jugador
        self.moves = 0

        # 🔥 10 cartas disponibles (0–9)
        available_cards = list(range(10))

        # 🔥 Seleccionar aleatoriamente 8 cartas únicas
        selected = random.sample(available_cards, 8)

        # 🔥 Duplicar (crear pares)
        deck = selected * 2

        # 🔥 Mezclar
        random.shuffle(deck)

        # 🔥 Crear tablero
        self.board = [
            {"id": i, "value": deck[i], "revealed": False, "solved": False}
            for i in range(16)
        ]

        # Cartas seleccionadas
        self.first_card = None
        self.solved_pairs = 0


    def flip_card(self, card_id: int):
        """Voltear carta correctamente"""
        card = self.board[card_id]

        # No permitir voltear carta resuelta o ya visible
        if card["revealed"] or card["solved"]:
            return self.get_state()

        # Voltearla
        card["revealed"] = True

        # Si no hay carta previa → es la primera del turno
        if not self.first_card:
            self.first_card = card

        else:
            # Segunda carta → contar movimiento
            self.moves += 1

            # Si coinciden → marcar como resueltas
            if self.first_card["value"] == card["value"]:
                self.first_card["solved"] = True
                card["solved"] = True
                self.solved_pairs += 1
            else:
                # Si falló → SOLO el frontend la ocultará
                pass

            # Reiniciar selección
            self.first_card = None

        return self.get_state()


    def get_state(self):
        """Retorna estado completo para frontend"""
        elapsed = round(time.time() - self.start_time, 1)

        return {
            "board": self.board,
            "moves": self.moves,
            "pairs_found": self.solved_pairs,
            "game_over": self.solved_pairs == 8,
            "elapsed_time": elapsed
        }