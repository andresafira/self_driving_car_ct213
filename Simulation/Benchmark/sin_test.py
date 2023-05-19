import numpy as np
import matplotlib.pyplot as plt
from Population import Population as Pop


# The classifiers will try to predict a sine function
def score(x, y):
    y_expected = np.sin(x)
    return -sum((y_expected - y)**2)


num_iterations = 100
num_tries = 10

num_tests = 10
X = np.arange(0., 2*np.pi, 2*np.pi/num_tests)
history = []
decision_maker = Pop.Population(num_tests, [10, 10], num_tests)
gen_size = decision_maker.n_living
for i in range(num_iterations*gen_size):
    fitness = 0
    for j in range(num_tries):
        y = decision_maker.ask(X)
        fitness += score(X, y)
    decision_maker.tell(fitness/num_tries)
    if i % gen_size == 0 and i > 0:
        history.append(decision_maker.best_classifier.fitness)
decision_maker.register_best()
plt.xlabel('Generation')
plt.ylabel('Best Deviation')
plt.title('Fitting sin(x)')
plt.plot(history)
plt.show()
