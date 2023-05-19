import numpy as np
import random
from constants import MUT_SCALE, N_OF_SONS


class Layer:
    def __init__(self, n_neurons, n_inputs):
        self.weights = np.random.randn(n_neurons, n_inputs)
        self.biases = np.random.randn(n_neurons)
        self.nodes = np.zeros(n_neurons)
        self.n_neurons = n_neurons
        self.n_inputs = n_inputs

    # relu activation function
    def activation(self):
        self.nodes = np.maximum(self.nodes, 0)

    def normalize_exp(self):
        self.nodes = self.nodes / np.max(self.nodes)
        self.nodes = np.exp(self.nodes)
        self.nodes = self.nodes / sum(self.nodes)

    def normalize_max(self):
        nodes_max = np.max(self.nodes)
        self.nodes = np.array([1 if self.nodes[i] == nodes_max else 0 for i in range(len(self.nodes))])

    def forward(self, input_vector, is_last_layer=False):
        self.nodes = np.matmul(self.weights, input_vector) + self.biases
        self.activation()
        # if is_last_layer:
        #     self.normalize_max()
        # else:
        #     self.activation()
        return self.nodes

    def mutate_from(self, other):
        for i in range(other.weights.shape[0]):
            for j in range(other.weights.shape[1]):
                self.weights[i][j] = other.weights[i][j] * random.uniform(1 - MUT_SCALE, 1 + MUT_SCALE)
            self.biases[i] = other.biases[i] * random.uniform(1 - MUT_SCALE, 1 + MUT_SCALE)


class Brain:
    def __init__(self, n_inputs, neurons_per_hidden, n_outputs):
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_hidden = len(neurons_per_hidden)
        self.layers = [Layer(neurons_per_hidden[0], n_inputs)]

        for i in range(1, self.n_hidden):
            self.layers.append(Layer(neurons_per_hidden[i], neurons_per_hidden[i-1]))

        self.layers.append(Layer(n_outputs, neurons_per_hidden[-1]))

    def parse(self, inputs_vector):
        output = inputs_vector
        for i in range(self.n_hidden):
            output = self.layers[i].forward(output)
        output = self.layers[-1].forward(output, is_last_layer=True)
        return output

    def mutate_from(self, other):
        for i, layer in enumerate(other.layers):
            self.layers[i].mutate_from(layer)

    def create_from(self, filename):
        with open(filename, "r") as file:
            txt = file.read()
            txt = txt.split('\n')
            elements = txt[0].split(' ')
            self.n_inputs, self.n_hidden, self.n_outputs = (int(e) for e in elements)
            self.layers = []

            current_line = 0
            for i in range(self.n_hidden + 1):
                current_line += 3
                weights = txt[current_line].split(' ')
                current_line += 1
                x_weights = int(weights[-2])
                y_weights = int(weights[-1])
                weights = np.zeros((x_weights, y_weights))
                biases = np.zeros((x_weights, ))
                for x in range(x_weights):
                    line = txt[current_line].split(' ')
                    for y in range(y_weights):
                        weights[x][y] = float(line[y])
                    current_line += 1
                current_line += 1
                line = txt[current_line].split(' ')
                for x in range(x_weights):
                    biases[x] = float(line[x])
                new_layer = Layer(x_weights, y_weights)
                new_layer.weights = weights
                new_layer.biases = biases
                self.layers.append(new_layer)

    def register_at(self, filename):
        with open(filename, "w") as file:
            file.write(f"{self.n_inputs} {self.n_hidden} {self.n_outputs}\n")
            for count, layer in enumerate(self.layers):
                file.write("#"*30 + "\n" + f"Layer {count}\n")
                x_weight = len(layer.weights)
                y_weight = len(layer.weights[0])
                file.write(f"weights: {x_weight} {y_weight}\n")
                for i in range(len(layer.weights)):
                    for j in range(len(layer.weights[0])):
                        file.write(f"{layer.weights[i][j]} ")
                    file.write("\n")
                file.write(f"biases: {x_weight}\n")
                for i in range(len(layer.biases)):
                    file.write(f"{layer.biases[i]} ")
                file.write("\n")


class Classifier:
    def __init__(self, n_inputs, neurons_per_hidden, n_outputs):
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.neurons_per_hidden = neurons_per_hidden
        self.brain = Brain(n_inputs, neurons_per_hidden, n_outputs)
        self.fitness = 0
        self.classification = None

    def create_from(self, filename):
        self.brain.create_from(filename)

    def register_at(self, filename):
        self.brain.register_at(filename)
        self.fitness = 0
        self.classification = None
        self.n_inputs = self.brain.n_inputs
        self.n_outputs = self.brain.n_outputs

    def multiply(self):
        sons = []
        for son in range(N_OF_SONS):
            new_son = Classifier(self.n_inputs, self.neurons_per_hidden, self.n_outputs)
            new_son.brain.mutate_from(self.brain)
            sons.append(new_son)
        return sons

    def classify(self, input_vector):
        self.classification = self.brain.parse(input_vector)
        return self.classification
