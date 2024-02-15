import random
import copy

def create_population(graph,num_population):
    population = []
    for _ in range(num_population):
        chromosome = list(graph.keys())[1:]
        random.shuffle(chromosome)
        population.append(chromosome)

    return population


def calculate_fitness(graph, first_node, chromosome):
    fitness = 0
    second_node = chromosome[0]
    if second_node in graph[first_node]:
        fitness += graph[first_node][second_node]
    else:
        return 100000

    for i in range(len(chromosome) - 1):
        current_node = chromosome[i]
        next_node = chromosome[i + 1]

        if next_node in graph[current_node]:
            fitness += graph[current_node][next_node]
        else:
            return 100000

    last_node = chromosome[len(chromosome) - 1]
    if first_node in graph[last_node]:
        fitness += graph[last_node][first_node]
    else:
        return 100000

    return fitness


def selection(graph, selection_type, num_population, first_node, population):
    if selection_type == 'Ranking':
        ranked_population = sorted(population, key=lambda x: calculate_fitness(graph, first_node, x), reverse=True)
        ranked_fitness = [calculate_fitness(graph, first_node, chromosome) for chromosome in ranked_population]
        total_fitness = sum(ranked_fitness)
        selection_probabilities = [fitness / total_fitness for fitness in ranked_fitness]
        selected_indices = random.choices(range(len(ranked_population)), weights=selection_probabilities,
                                          k=num_population)
        selected_population = [ranked_population[index] for index in selected_indices]
        return selected_population
    elif selection_type == 'Tournament':
        selected_population = []
        for _ in range(num_population):
            tournament_size = int(0.1 * num_population)
            tournament = random.sample(population, tournament_size)
            best_chromosome = max(tournament, key=lambda x: calculate_fitness(graph, first_node, x))
            selected_population.append(best_chromosome)
        return selected_population


def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:crossover_point] + [node for node in parent2 if node not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [node for node in parent1 if node not in parent2[:crossover_point]]
    return child1, child2


def mutate(chromosome):
    mutation_point1 = random.randint(0, len(chromosome) - 1)
    mutation_point2 = random.randint(0, len(chromosome) - 1)
    chromosome[mutation_point1], chromosome[mutation_point2] = chromosome[mutation_point2], chromosome[
        mutation_point1]
    return chromosome


def evolve(graph, stopping_criteria, num_generations, num_population, crossover_percentage,mutation_percentage, elitism_percentage, selection_type, first_node):
    best_chromosome = None
    best_fitness = 0
    all_fitness = []
    num_fitness = 0
    population = create_population(graph, num_population)

    if stopping_criteria == 'generation':
        for generation in range(num_generations):
            parents = selection(graph, selection_type, num_population, first_node, population)

            offspring = []
            num_offspring = int(num_population * crossover_percentage)
            for _ in range(num_offspring):
                parent1, parent2 = random.sample(parents, 2)
                child1, child2 = crossover(parent1, parent2)
                offspring.append(child1)
                offspring.append(child2)

            # mutation
            num_mutations = int(num_population * mutation_percentage)
            for _ in range(num_mutations):
                index = random.randint(0, len(population) - 1)
                population[index] = mutate(population[index])

            population = population + offspring
            population = sorted(population, key=lambda x: calculate_fitness(graph, first_node, x))

            # Apply elitism
            num_elites = int(num_population * elitism_percentage)
            population = population[:num_elites]

            best_chromosome = population[0]
            best_fitness = calculate_fitness(graph, first_node, best_chromosome)

            if best_fitness == 100000:
                all_fitness.append(0)
            else:
                all_fitness.append(best_fitness)
        num_fitness = num_generations

    elif stopping_criteria == 'saturation':
        best_fitness = float('inf')
        best_chromosome = None
        no_change = 0

        while True:
            # selection
            parents = selection(graph, selection_type, num_population, first_node, population)

            # crossover
            offspring = []
            num_offspring = int(num_population * crossover_percentage)
            for _ in range(num_offspring):
                parent1, parent2 = random.sample(parents, 2)
                child1, child2 = crossover(parent1, parent2)
                offspring.append(child1)
                offspring.append(child2)

            # mutation
            num_mutations = int(num_population * mutation_percentage)
            for _ in range(num_mutations):
                index = random.randint(0, len(population) - 1)
                population[index] = mutate(population[index])

            population = population + offspring

            population = sorted(population, key=lambda x: calculate_fitness(graph, first_node, x))

            # Apply elitism
            num_elites = int(num_population * elitism_percentage)
            population = population[:num_elites]

            current_best_fitness = calculate_fitness(graph, first_node, population[0])
            if current_best_fitness >= best_fitness:
                no_change += 1
            else:
                best_fitness = current_best_fitness
                best_chromosome = copy.deepcopy(population[0])
                no_change = 0

            if best_fitness == 100000:
                all_fitness.append(0)
            else:
                all_fitness.append(best_fitness)

            num_fitness += 1

            if no_change > 100:
                break

    return best_chromosome, best_fitness, all_fitness, num_fitness

