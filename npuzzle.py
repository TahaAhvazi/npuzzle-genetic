import random
import time

PUZZLE_SIZE = 4

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


def create_initial_population(population_size):
    population = []
    for _ in range(population_size):
        population.append(generate_random_state())
    return population


def select_parents(population):
    tournament_size = 3
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda state: calculate_heuristic(state))
    return tournament[:2]


def crossover(parent1, parent2):
    crossover_point = random.randint(1, PUZZLE_SIZE**2 - 1)
    offspring = list(parent1[:crossover_point])
    for gene in parent2:
        if gene not in offspring:
            offspring.append(gene)
    return tuple(offspring)


def mutate(state, mutation_rate):
    if random.random() < mutation_rate:
        puzzle = list(state)
        index1, index2 = random.sample(range(PUZZLE_SIZE**2), 2)
        puzzle[index1], puzzle[index2] = puzzle[index2], puzzle[index1]
        return tuple(puzzle)
    return state


def genetic_algorithm(population_size, mutation_rate, max_generations):
    population = create_initial_population(population_size)
    best_solution = None
    generation = 0

    while generation < max_generations:
        population.sort(key=lambda state: calculate_heuristic(state))

        if calculate_heuristic(population[0]) == 0:
            best_solution = population[0]
            break

        new_population = [population[0]]  
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population)
            offspring = crossover(parent1, parent2)
            mutated_offspring = mutate(offspring, mutation_rate)
            new_population.append(mutated_offspring)

        population = new_population
        generation += 1

        print(f"Generation {generation}")
        print_solution(population[0])
        print()
        time.sleep(1)  

    return best_solution


def print_solution(solution):
    for i in range(0, PUZZLE_SIZE**2, PUZZLE_SIZE):
        row = solution[i:i + PUZZLE_SIZE]
        row_str = " ".join(str(num) for num in row)
        print(row_str)
    print()


# Main program
population_size = 100
mutation_rate = 0.1
max_generations = 1000

solution = genetic_algorithm(population_size, mutation_rate, max_generations)
if solution:
    print("Solution found:")
    print_solution(solution)
else:
    print("Solution not found within the given number of generations.")