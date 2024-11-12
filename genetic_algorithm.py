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
            # Add the fitness of the population to the fit_history list
            population_fit = [self.fitness(x, self.environment) for x in population]
            # Add the fitness of the population to the fit_history list
            self.fit_history.append(population_fit)
            
            # Sort the population by fitness
            population.sort(key=lambda x: self.fitness(x, self.environment))
            population = population[:self.pop_size]
            # Add the fitness of the population to the fit_history list
            population = self.reproduce(population)
            # Add the new population to the generations list
            self.generations.append(population)

            if not stop_at_zero:
                continue

            # if we find a solution we stop
            if any(num == 0 for num in population_fit) and not solution_found:
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
