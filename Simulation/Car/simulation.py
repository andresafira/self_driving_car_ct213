from simulation_constants import WIDTH, HEIGHT, CAR_HEIGHT, CAR_WIDTH, BACKGROUND_SPRITE, CAR_SPRITE, CAR_START
from simulation_constants import SAMPLE_TIME, eps, SENSOR_RANGE, SIDEWALK_WIDTH, MIDDLE_RIGHT, MIDDLE_LEFT
from simulation_constants import BLACK, WHITE, RED
from Utils.General import clip
from Utils.Geometry.Box import *
from Utils.Geometry.Position import Position
import pygame
from pygame.transform import scale, rotate
from pygame.image import load
from pygame.locals import *
from Car import Car
from math import pi, sin, cos, fabs


def dummy_simple_generator(num_dummy, step=500, side='right'):
    if side == 'left':
        first = MIDDLE_RIGHT
        second = MIDDLE_LEFT
    elif side == 'right':
        first = MIDDLE_LEFT
        second = MIDDLE_RIGHT
    else:
        raise Exception('Invalid side choice! Choose left or right side')
    dummies = []
    for i in range(num_dummy):
        if i % 2 == 0:
            pose = Position(Vector(first, HEIGHT/2 - CAR_HEIGHT + i * step), 0)
        else:
            pose = Position(Vector(second, HEIGHT/2 - CAR_HEIGHT + i * step), 0)
        dummies.append(Car(initial_position=pose, DUMMY=True, initial_speed=10))
    return dummies


class Simulation:
    def __init__(self, draw_Bounding_Box=True, draw_Sensors=True):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Car simulation")
        self.background_sprite = load(BACKGROUND_SPRITE)
        self.car_sprite = scale(load(CAR_SPRITE), (CAR_WIDTH*1.1, CAR_HEIGHT))
        self.car = Car()
        self.dummies = dummy_simple_generator(30, side='left')
        self.objects = []
        self.draw_BB = draw_Bounding_Box
        self.draw_S = draw_Sensors

    def reset(self):
        self.car.position.location.x, self.car.position.location.y = CAR_START
        self.car.position.rotation = 0
        self.car.speed = 0
        self.car.alive = True
        self.dummies.clear()
        self.dummies = dummy_simple_generator(20)

    def draw_sensors(self):
        theta = self.car.position.rotation
        for sensor in self.car.control_system:
            sensor_base = (sensor.base_center.x, HEIGHT / 2 + (CAR_WIDTH*fabs(sin(theta)) +
                                                               fabs(CAR_HEIGHT*cos(theta)))/2)
            sensor_edge = (sensor.edge.x, HEIGHT / 2 - sensor.edge.y + self.car.position.location.y +
                           (CAR_WIDTH*fabs(sin(theta)) + fabs(CAR_HEIGHT*cos(theta)))/2)
            sensor_end = (sensor.end_reading.x, HEIGHT / 2 - sensor.end_reading.y + self.car.position.location.y +
                          (CAR_WIDTH*fabs(sin(theta)) + fabs(CAR_HEIGHT*cos(theta)))/2)
            pygame.draw.line(self.screen, WHITE, sensor_base, sensor_end, width=3)
            if sensor.end_reading.distance(sensor.edge) > eps:
                pygame.draw.line(self.screen, RED, sensor_end, sensor_edge, width=3)

    def update_objects(self):
        self.objects.clear()
        for dummy in self.dummies:
            dummy.update()
        # ROAD Segment:
        left_side = Segment(Vector(SIDEWALK_WIDTH, self.car.position.location.y - 1.5 * SENSOR_RANGE),
                            Vector(SIDEWALK_WIDTH, self.car.position.location.y + 1.5 * SENSOR_RANGE))
        right_side = Segment(Vector(WIDTH - SIDEWALK_WIDTH, self.car.position.location.y - 1.5 * SENSOR_RANGE),
                             Vector(WIDTH - SIDEWALK_WIDTH, self.car.position.location.y + 1.5 * SENSOR_RANGE))
        self.objects.append(left_side)
        self.objects.append(right_side)
        for dummy in self.dummies:
            self.objects.append(dummy.bounding_box)

    def draw_bounding_box(self, car):
        box = car.unravel_box()
        P1 = box.vertices[0].x, HEIGHT/2 - box.vertices[0].y + self.car.position.location.y + CAR_HEIGHT / 2
        P2 = box.vertices[1].x, HEIGHT/2 - box.vertices[1].y + self.car.position.location.y + CAR_HEIGHT / 2
        P3 = box.vertices[2].x, HEIGHT/2 - box.vertices[2].y + self.car.position.location.y + CAR_HEIGHT / 2
        P4 = box.vertices[3].x, HEIGHT/2 - box.vertices[3].y + self.car.position.location.y + CAR_HEIGHT / 2

        pygame.draw.line(self.screen, WHITE, P1, P2)
        pygame.draw.line(self.screen, WHITE, P2, P3)
        pygame.draw.line(self.screen, WHITE, P3, P4)
        pygame.draw.line(self.screen, WHITE, P4, P1)

    def draw_car(self, car):
        sprite_copy = rotate(self.car_sprite, car.position.rotation * 180 / pi)
        if not self.car.alive:
            sprite_copy.set_alpha(50)
        self.screen.blit(sprite_copy, (car.position.location.x - sprite_copy.get_width() / 2,
                                       HEIGHT / 2 - car.position.location.y + self.car.position.location.y))
        if self.draw_BB:
            self.draw_bounding_box(car)

    def draw_scenario(self):
        self.screen.blit(self.background_sprite, (0, clip(self.car.position.location.y, HEIGHT)))
        self.screen.blit(self.background_sprite, (0, clip(self.car.position.location.y - HEIGHT, -HEIGHT)))
        for dummy in self.dummies:
            self.draw_car(dummy)
        if self.draw_S:
            self.draw_sensors()
        self.draw_car(self.car)

    def update(self):
        self.screen.fill(BLACK)
        self.car.update(self.objects)
        self.draw_scenario()
        self.update_objects()
        pygame.display.flip()
