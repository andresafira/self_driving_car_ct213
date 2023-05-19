from Classifier.Classifier import Classifier
from constants import N_WIN, N_START, FILE_PATH


class Population:
    def __init__(self, n_inputs, neurons_per_hidden, n_outputs, n_start=N_START):
        self.n_living = max(n_start, N_WIN)
        self.classifiers = [Classifier(n_inputs, neurons_per_hidden, n_outputs) for _ in range(self.n_living)]
        self.current_id = 0
        self.gen = 0
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

    # The evolve method will keep the n_win first classifiers and kill the rest.
    # The winners of each iteration will multiply
    def evolve(self):
        self.classifiers.sort(key=lambda x: -x.fitness)
        self.classifiers = [self.classifiers[i] for i in range(N_WIN)]
        self.best_classifier = self.classifiers[0]
        for i in range(N_WIN):
            self.classifiers += self.classifiers[i].multiply()
        self.n_living = len(self.classifiers)

    def register_best(self):
        self.classifiers[0].register_at(FILE_PATH)
