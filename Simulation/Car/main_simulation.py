import matplotlib.pyplot as plt

from Genetic_Algorithm.Population.Population import Population
from simulation import Simulation
from simulation_constants import SAMPLE_TIME, FREQUENCY, N_SENSOR, SAMPLE_TIME, CAR_MAX_SPEED
from math import fabs
import pygame

MAX_SIMULATION_TIME = 20

sim = Simulation()
run = True

clock = pygame.time.Clock()
clock.tick(10 * FREQUENCY)
current_time = 0

Pop = Population(N_SENSOR + 1, [2 * N_SENSOR // 3, N_SENSOR // 3], 4)
try:
    Pop.create_from('best_classifier.txt')
except:
    pass
i = 0
back_speed = 1
speed = 0
score = 0
history = []
while run:
    clock.tick(100)

    # Close the program if the quit button was pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            # Pop.register_best()
    back_speed = speed
    sim.update()
    speed = sim.car.speed

    if current_time > MAX_SIMULATION_TIME or (not sim.car.alive) or (speed <= 0 and back_speed <= 0):
        i += 1
        current_time = 0
        Pop.tell(sim.car.position.location.y + score)
        if i == Pop.gen_size:
            i = 0
            print('changed generation and best score was ', Pop.best_classifier.fitness)
            history.append(Pop.best_classifier.fitness)
        sim.reset()
        score = 0

    read = sim.car.get_readings()
    input_vector = read + [sim.car.speed / CAR_MAX_SPEED]

    clf_move = Pop.ask(input_vector)

    if clf_move[0] == 1:
        sim.car.accelerate()
    if clf_move[1] == 1:
        sim.car.brake()
    if clf_move[2] == 1:
        sim.car.turn_right()
    if clf_move[3] == 1:
        sim.car.turn_left()

    score -= fabs(sim.car.speed) * sum(read) / 10

    current_time += SAMPLE_TIME

# plt.plot(history)
# plt.show()
# with open('history_3.txt', 'w') as file:
#     for a in history:
#         file.write(str(a) + '\n')
