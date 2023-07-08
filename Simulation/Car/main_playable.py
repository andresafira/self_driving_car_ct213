from simulation import Simulation
from simulation_constants import SAMPLE_TIME, CAR_START, FREQUENCY
import pygame

sim = Simulation()
run = True

while run:
    # pygame.time.wait(int(1000 * SAMPLE_TIME))
    pygame.time.Clock().tick(FREQUENCY)
    sim.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            sim.moving_road = not sim.moving_road
            if not sim.moving_road:
                sim.car.position.location.y = CAR_START[1]
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        sim.car.accelerate()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        sim.car.turn_right()
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        sim.car.brake()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        sim.car.turn_left()
