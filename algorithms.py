
import random
import time
from config import set_of_colors
from utils import draw_graph

def individuals(color_of_nodes, num_nodes):
    for i in range(1, num_nodes + 1):
        color_of_nodes[i] = random.randint(0, len(set_of_colors) - 1)
    return color_of_nodes

def crossover(parent1, parent2):
    rindex = random.randrange(1, len(parent1))
    child1 = parent1[:rindex] + parent2[rindex:]
    child2 = parent1[rindex:] + parent2[:rindex]
    return child1, child2

def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, len(set_of_colors) - 1)

def fitness(individual, num_nodes, edges):
    num_of_error = sum(
        individual[node] == individual[int(nei)] for node in range(1, num_nodes + 1) for nei in edges[str(node)]
    )
    num_of_colors = len(set(individual[1:num_nodes + 1]))
    return num_of_error + num_of_colors

def genetics_algo(frame_dell, population_size, generations, mutation_rate, crossover_prob, retain, num_nodes, edges, list1, root):
    start_time = time.perf_counter()
    color_of_nodes = [0] * (num_nodes + 2)
    population = [individuals(color_of_nodes[:], num_nodes) for _ in range(population_size)]

    for _ in range(generations):
        population.sort(key=lambda ind: fitness(ind, num_nodes, edges))
        population = population[:int(retain * population_size)]

        for _ in range(int(population_size - len(population))):
            parent1, parent2 = random.sample(population, 2)
            if random.random() < crossover_prob:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            population.append(child1)
            population.append(child2)

    optimal_ans = min(population, key=lambda ind: fitness(ind, num_nodes, edges))
    color_of_nodes = optimal_ans
    end_time = time.perf_counter()

    time_taken = end_time - start_time
    number_of_colors = len(set(color_of_nodes[1:num_nodes + 1]))
    print("Time taken:", time_taken)
    print("Number of colors:", number_of_colors)
    draw_graph(frame_dell, num_nodes, color_of_nodes, edges, list1, root, time_taken, number_of_colors)

def is_valid(color, src, visited, color_of_nodes, edges):
    for child in edges[str(src)]:
        if visited[int(child)] != 0 and color_of_nodes[int(child)] == color:
            return False
    return True

def dfs(src, visited, color_of_nodes, edges):
    visited[src] = 1
    for child in edges[str(src)]:
        if visited[int(child)] == 0:
            for i in range(len(set_of_colors)):
                if is_valid(i, int(child), visited, color_of_nodes, edges):
                    color_of_nodes[int(child)] = i
                    break
            dfs(int(child), visited, color_of_nodes, edges)

def solve(num_nodes, edges, frame_dell, list1, root):
    visited = [0] * (num_nodes + 2)
    color_of_nodes = [0] * (num_nodes + 2)

    start_time = time.perf_counter()
    for i in range(1, num_nodes + 1):
        if visited[i] == 0:
            color_of_nodes[i] = 0
            dfs(i, visited, color_of_nodes, edges)
    end_time = time.perf_counter()

    time_taken = end_time - start_time
    number_of_colors = len(set(color_of_nodes[1:num_nodes + 1]))
    print("Time taken:", time_taken)
    print("Number of colors:", number_of_colors)
    draw_graph(frame_dell, num_nodes, color_of_nodes, edges, list1, root, time_taken, number_of_colors)
