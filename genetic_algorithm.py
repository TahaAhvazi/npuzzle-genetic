import random
import time
from puzzle import calculate_heuristic, generate_random_state, PUZZLE_SIZE

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
