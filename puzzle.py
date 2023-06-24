import random

PUZZLE_SIZE = 3
GOAL_STATE = tuple(range(1, PUZZLE_SIZE**2)) + (0,)


def generate_random_state():
    puzzle = list(GOAL_STATE)
    random.shuffle(puzzle)
    return tuple(puzzle)


def get_possible_moves(state):
    moves = []
    empty_index = state.index(0)
    row = empty_index // PUZZLE_SIZE
    col = empty_index % PUZZLE_SIZE

    if row > 0:
        moves.append(empty_index - PUZZLE_SIZE)  #  up
    if row < PUZZLE_SIZE - 1:
        moves.append(empty_index + PUZZLE_SIZE)  #  down
    if col > 0:
        moves.append(empty_index - 1)  #  left
    if col < PUZZLE_SIZE - 1:
        moves.append(empty_index + 1)  #  right

    return moves


def perform_move(state, move):
    puzzle = list(state)
    empty_index = puzzle.index(0)
    puzzle[empty_index], puzzle[move] = puzzle[move], puzzle[empty_index]
    return tuple(puzzle)


def calculate_heuristic(state):
    distance = 0
    for i in range(PUZZLE_SIZE**2):
        if state[i] == 0:
            continue
        goal_row = (state[i] - 1) // PUZZLE_SIZE
        goal_col = (state[i] - 1) % PUZZLE_SIZE
        curr_row = i // PUZZLE_SIZE
        curr_col = i % PUZZLE_SIZE
        distance += abs(goal_row - curr_row) + abs(goal_col - curr_col)
    return distance
