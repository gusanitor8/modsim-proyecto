class GeneticAlgorithm:
    def __init__(self, init_population, environment, mutation_rate: int, epochs:int, pop_size: int, fitness: callable, crossover: callable, mutation: callable):
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
        self.mutation_rate = mutation_rate
        self.generations = []
        self.fit_history = []
    
    def run(self, stop_at_zero=True):
        population = self.init_population
        solution_found = False
        final_epoch = self.epochs - 1

        # Add the initial population to the generations list
        self.generations.append(population)

        for epoch_no in range(self.epochs):
            # Calculate the fitness for each individual once and store it
            population_fit = [(x, self.fitness(x, self.environment)) for x in population]
            
            # Extract the fitness values and add them to fit_history
            self.fit_history.append([fit for _, fit in population_fit])
            
            # Sort the population based on fitness (using the precomputed fitness values)
            population_fit.sort(key=lambda x: x[1])
            population = [x for x, _ in population_fit[:self.pop_size]]
            
            # Reproduce the population and add the new generation to generations list
            population = self.reproduce(population)
            self.generations.append(population)

            if stop_at_zero:
                # If any individual has a fitness of 0, we stop
                if any(fit == 0 for _, fit in population_fit) and not solution_found:
                    solution_found = True
                    final_epoch = epoch_no
                    

        return self.generations, self.fit_history, solution_found, final_epoch


    def reproduce(self, population):        
        new_generation = []

        for first_individual in population:                        
            new_individual = self.mutation(first_individual, self.environment, self.mutation_rate)

            new_generation.append(new_individual)
            new_generation.append(first_individual)

        return new_generation
