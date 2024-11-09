class GeneticAlgorithm:
    def __init__(self, init_population, environment, epochs:int, pop_size: int, fitness: callable, crossover: callable, mutation: callable):
        """_summary_

        Args:
            init_population (_type_): am ar
            environment (_type_): _description_
            epochs (int): _description_
            pop_size (int): _description_
            fitness (callable): _description_
            crossover (callable): _description_
            mutation (callable): _description_
        """
        self.init_population = init_population
        self.environment = environment
        self.epochs = epochs
        self.fitness = fitness
        self.crossover = crossover
        self.mutation = mutation
        self.pop_size = pop_size
        self.generations = []
        self.fit_history = []
    
    def run(self):
        population = self.init_population
        # Add the initial population to the generations list
        self.generations.append(population)

        for _ in range(self.epochs):
            # Add the fitness of the population to the fit_history list
            population_fit = [self.fitness(x, self.environment) for x in population]
            # Add the fitness of the population to the fit_history list
            self.fit_history.append(population_fit)

            # Sort the population by fitness
            population.sort(key=lambda x: self.fitness(x, self.environment))
            # Add the fitness of the population to the fit_history list
            population = self.reproduce(population)
            # Add the new population to the generations list
            self.generations.append(population)
           
        return self.generations, self.fit_history


    def reproduce(self, population):
        pop_len = len(population)
        new_generation = []

        for individual_idx in range(len(population)):
            nxt_individual_idx = (individual_idx + 1) % pop_len

            first_individual = population[individual_idx]
            second_individual = population[nxt_individual_idx]
            new_individual = self.crossover(first_individual, second_individual, self.environment)
            new_individual = self.mutation(new_individual, self.environment)

            new_generation.append(new_individual)

        return new_generation
