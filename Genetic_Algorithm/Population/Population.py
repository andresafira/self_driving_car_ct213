from Genetic_Algorithm.Classifier.Classifier import Classifier
from Genetic_Algorithm.constants import N_WIN, N_START, FILE_PATH


class Population:
    def __init__(self, n_inputs, neurons_per_hidden, n_outputs, n_start=N_START):
        self.n_living = max(n_start, N_WIN)
        self.classifiers = [Classifier(n_inputs, neurons_per_hidden, n_outputs) for _ in range(self.n_living)]
        self.current_id = 0
        self.gen = 0
        self.gen_size = N_START
        self.best_classifier = None

    # The ask method will return the classification of a certain classifier to be tested on the simulation
    def ask(self, input_vector):
        return self.classifiers[self.current_id].classify(input_vector)

    # The tell method will give the value of the fitness of the classifier that was simulated
    def tell(self, fitness):
        self.classifiers[self.current_id].fitness = fitness
        self.current_id += 1
        if self.current_id >= self.n_living:
            self.gen += 1
            self.current_id = 0
            self.evolve()

    # Returns the pairs in order of fitness and, if there's an odd number,
    # makes a pair with the first and last classifier
    def get_crossover_pairs(self):
        length = len(self.classifiers)
        pairs = []
        i = 0
        for i in range(0, length, 2):
            pairs.append([self.classifiers[i], self.classifiers[i+1]])
        if i+1 <= length:
            pairs.append([self.classifiers[0], self.classifiers[-1]])
        return pairs

    # The evolve method will keep the n_win first classifiers and kill the rest.
    # The winners of each iteration will multiply
    def evolve(self):
        self.classifiers.sort(key=lambda x: -x.fitness)
        self.classifiers = self.classifiers[:N_WIN]
        self.best_classifier = self.classifiers[0]

        # Perform classifier crossover
        crossover_pairs = self.get_crossover_pairs()
        crossover_classifiers = []
        for pair in crossover_pairs:
            crossover_classifiers += Classifier.crossover(pair[0], pair[1])

        # Perform classifies mutation
        mutated_classifiers = []
        for i in range(N_WIN):
            mutated_classifiers += self.classifiers[i].mutate()

        self.classifiers += mutated_classifiers
        self.classifiers += crossover_classifiers

        self.n_living = len(self.classifiers)

    def register_best(self):
        self.classifiers[0].register_at(FILE_PATH)

    def create_from(self, path):
        for clf in self.classifiers[:len(self.classifiers)//2]:
            clf.create_from(path)
