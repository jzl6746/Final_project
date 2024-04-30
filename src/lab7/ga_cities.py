"""
Lab 7: Realistic Cities 

In this lab you will try to generate realistic cities using a genetic algorithm.
Your cities should not be under water, and should have a realistic distribution across the landscape.
Your cities may also not be on top of mountains or on top of each other.
Create the fitness function for your genetic algorithm, so that it fulfills these criterion
and then use it to generate a population of cities.

Please comment your code in the fitness function to explain how are you making sure each criterion is 
fulfilled. Clearly explain in comments which line of code and variables are used to fulfill each criterion.
"""
import matplotlib.pyplot as plt
import pygad
import numpy as np

import sys
from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / ".." / "..").resolve().absolute()))

from src.lab5.landscape import elevation_to_rgba
from src.lab5.landscape import get_elevation

def game_fitness(ga_instance, cities, idx):
    fitness = 0.0001  # Do not return a fitness of 0, it will mess up the algorithm
    
    """
    Create your fitness function here to fulfill the following criteria:
    1. The cities should not be under water
    2. The cities should have a realistic distribution across the landscape
    3. The cities may also not be on top of mountains or on top of each other
    """
   #0.20 to 0.60 desired region

  
    
    if elevation[cities[idx%10] % 100][cities[idx%10] //100] > 0.30:
        fitness += elevation[cities[idx%10] % 100][cities[idx%10] //100]+1
   
    if elevation[cities[idx%10] % 100][cities[idx%10] //100] < 0.60:
        fitness+=elevation[cities[idx%10] % 100][cities[idx%10] //100]+1

    if elevation[cities[idx%10] % 100][cities[idx%10] //100] < 0.30:
        fitness += elevation[cities[idx%10] % 100][cities[idx%10] //100]-100
    
    if elevation[cities[idx%10] % 100][cities[idx%10] //100] > 0.60:
        fitness += elevation[cities[idx%10] % 100][cities[idx%10] //100]-100

    if (np.absolute(0.5-elevation[cities[idx%10] % 100][cities[idx%10] //100])) > 0.1:
        fitness +=1

    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            distance = np.linalg.norm(np.array(cities[i]) - np.array(cities[j]))
            if distance < 10:
                fitness -= 10 
    
    
    return fitness


def setup_GA(fitness_fn, n_cities, size):
    """
    It sets up the genetic algorithm with the given fitness function,
    number of cities, and size of the map

    :param fitness_fn: The fitness function to be used
    :param n_cities: The number of cities in the problem
    :param size: The size of the grid
    :return: The fitness function and the GA instance.
    """
    num_generations = 300
    num_parents_mating = 10

    solutions_per_population = 300
    num_genes = n_cities

    init_range_low = 0
    init_range_high = size[0] * size[1]

    parent_selection_type = "sss"
    keep_parents = 10

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 100

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=fitness_fn,
        sol_per_pop=solutions_per_population,
        num_genes=num_genes,
        gene_type=int,
        init_range_low=init_range_low,
        init_range_high=init_range_high,
        parent_selection_type=parent_selection_type,
        keep_parents=keep_parents,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        mutation_percent_genes=mutation_percent_genes,
    )

    return fitness_fn, ga_instance


def solution_to_cities(solution, size):
    """
    It takes a GA solution and size of the map, and returns the city coordinates
    in the solution.

    :param solution: a solution to GA
    :param size: the size of the grid/map
    :return: The cities are being returned as a list of lists.
    """
    cities = np.array(
        list(map(lambda x: [int(x / size[0]), int(x % size[1])], solution))
    )
    return cities


def show_cities(cities, landscape_pic, cmap="gist_earth"):
    """
    It takes a list of cities and a landscape picture, and plots the cities on top of the landscape

    :param cities: a list of (x, y) tuples
    :param landscape_pic: a 2D array of the landscape
    :param cmap: the color map to use for the landscape picture, defaults to gist_earth (optional)
    """
    cities = np.array(cities)
    plt.imshow(landscape_pic, cmap=cmap)
    plt.plot(cities[:, 1], cities[:, 0], "r.")
    plt.show()


if __name__ == "__main__":
    print("Initial Population")

    size = 100, 100
    n_cities = 10
    elevation = []
    elevation = get_elevation(size) # initialize elevation here from your previous code
    # normalize landscape
    elevation = np.array(elevation)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())
    landscape_pic = elevation_to_rgba(elevation)

    # setup fitness function and GA
    fitness = lambda ga_instance, solution, idx: game_fitness(ga_instance, solution, idx)
    fitness_function, ga_instance = setup_GA(fitness, n_cities, size)

    # Show one of the initial solutions.
    random_solution = ga_instance.initial_population[0]
    cities = solution_to_cities(random_solution, size)
    show_cities(cities, landscape_pic)

    # Run the GA to optimize the parameters of the function.
    ga_instance.run()
    ga_instance.plot_fitness()
    print("Final Population")

    # Show the best solution after the GA finishes running.
    cities = ga_instance.best_solution()[0]
    cities_t = solution_to_cities(cities, size)
    plt.imshow(landscape_pic, cmap="terrain_r")
    plt.plot(cities_t[:, 1], cities_t[:, 0], "r.")
    plt.show()
    print(fitness_function(ga_instance,cities, 0))
