import numpy as np
import matplotlib.pyplot as plt
from Population import Population as Pop


# The classifiers will try to predict the 2 variable function z = x^2+y^2
def score(x, y):
    y_expected = sum(x**2)
    return -(y_expected - y)**2/len(x)**2


num_iterations = 1000
num_tries = 50
history = []
n_dim = 4
decision_maker = Pop.Population(n_dim, [20, 20, 20], 1)
gen_size = decision_maker.n_living
for i in range(num_iterations*gen_size):
    fitness = 0
    for j in range(num_tries):
        x = 10*np.random.rand(n_dim)-5
        y = decision_maker.ask(x)
        fitness += score(x, y[0])
    decision_maker.tell(fitness/num_tries)
    if i % gen_size == 0 and i > 0:
        print(i/gen_size)
        history.append(decision_maker.best_classifier.fitness)
decision_maker.register_best()
plt.plot(history)
plt.xlabel('Generation')
plt.ylabel('Best Deviation')
plt.title(f'Fitting {n_dim}-dimensional paraboloid')
plt.show()
