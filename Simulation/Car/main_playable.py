from simulation import Simulation
from simulation_constants import SAMPLE_TIME, CAR_START, FREQUENCY
import pygame

sim = Simulation()
run = True
num_iterations = 0

while run:
    # pygame.time.wait(int(1000 * SAMPLE_TIME))
    pygame.time.Clock().tick(FREQUENCY)
    sim.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('keys_history.txt', 'w') as file:
                for a in sim.car.keys_history:
                    file.write(str(a) + '\n')
            with open('sensors_history.txt', 'w') as file:
                for b in sim.car.sensors_history:
                    file.write(str(b) + '\n')
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            sim.moving_road = not sim.moving_road
            if not sim.moving_road:
                sim.car.position.location.y = CAR_START[1]
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        sim.car.accelerate()
        if num_iterations >= 0:
            sim.car.keys_history.append([1, 0, 0, 0])
            read = sim.car.get_readings()
            read.append(sim.car.speed)
            sim.car.sensors_history.append(read)
            num_iterations = 0
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        sim.car.turn_right()
        if num_iterations >= 0:
            sim.car.keys_history.append([0, 0, 1, 0])
            read = sim.car.get_readings()
            read.append(sim.car.speed)
            sim.car.sensors_history.append(read)
            num_iterations = 0
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        sim.car.brake()
        if num_iterations >= 0:
            sim.car.keys_history.append([0, 0, 0, 1])
            read = sim.car.get_readings()
            read.append(sim.car.speed)
            sim.car.sensors_history.append(read)
            num_iterations = 0
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        sim.car.turn_left()
        if num_iterations >= 0:
            sim.car.keys_history.append([0, 1, 0, 0])
            read = sim.car.get_readings()
            read.append(sim.car.speed)
            sim.car.sensors_history.append(read)
            num_iterations = 0

    num_iterations += 1
