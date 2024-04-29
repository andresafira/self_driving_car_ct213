from simulation import Simulation
from simulation_constants import FREQUENCY, CAR_MAX_SPEED
import pygame


def main():
    sim = Simulation(side='left', draw_Bounding_Box=True, draw_Sensors=True)
    run = True
    learn = False

    while run:
        pygame.time.Clock().tick(FREQUENCY)
        sim.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if learn:
                    with open('keys_history.txt', 'w') as file:
                        for a in sim.car.keys_history:
                            file.write(str(a) + '\n')
                    with open('sensors_history.txt', 'w') as file:
                        for b in sim.car.sensors_history:
                            file.write(str(b) + '\n')
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            sim.car.accelerate()
            if learn:
                sim.car.keys_history.append([1, 0, 0, 0])
                read = sim.car.get_readings()
                read.append(sim.car.speed / CAR_MAX_SPEED)
                sim.car.sensors_history.append(read)
                num_iterations = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            sim.car.turn_left()
            if learn:
                sim.car.keys_history.append([0, 1, 0, 0])
                read = sim.car.get_readings()
                read.append(sim.car.speed / CAR_MAX_SPEED)
                sim.car.sensors_history.append(read)
                num_iterations = 0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            sim.car.turn_right()
            if learn:
                sim.car.keys_history.append([0, 0, 1, 0])
                read = sim.car.get_readings()
                read.append(sim.car.speed / CAR_MAX_SPEED)
                sim.car.sensors_history.append(read)
                num_iterations = 0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            sim.car.brake()
            if learn:
                sim.car.keys_history.append([0, 0, 0, 1])
                read = sim.car.get_readings()
                read.append(sim.car.speed / CAR_MAX_SPEED)
                sim.car.sensors_history.append(read)
                num_iterations = 0


if __name__ == "__main__":
    main()
