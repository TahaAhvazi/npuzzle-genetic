import time
from genetic_algorithm import genetic_algorithm, print_solution

# Main program
population_size = 100
mutation_rate = 0.1
max_generations = 1000

solution = genetic_algorithm(population_size, mutation_rate, max_generations)
if solution:
    print("✅ Solution found:")
    print_solution(solution)
else:
    print("🛑 The solution not found!")
