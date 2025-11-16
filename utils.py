import random

def generate_board():
    # 6 pares → 12 cartas
    base_cards = ["A", "B", "C", "D", "E", "F"]
    board = base_cards * 2
    random.shuffle(board)
    return board