from Utils.Geometry.Vector import Vector
from Utils.Geometry.Position import Position
from Utils.Geometry.Box import Segment, Box
from Utils.General import sgn, interpolate_cycle
from simulation_constants import CAR_ACCELERATION, CAR_MAX_SPEED, CAR_ANGLE_STEP, CAR_START, CAR_WIDTH, CAR_HEIGHT
from simulation_constants import MAX_STEERING_WHEEL_ANGLE, INERTIA_PARAMETER_WHEEL, INERTIA_PARAMETER_SPEED
from simulation_constants import SAMPLE_TIME, eps
from simulation_constants import SENSOR_RANGE, N_SENSOR
from math import cos, sin, pi, fabs, sqrt


class Sensor:
    def __init__(self, base_angle, car_position):
        self.base_angle = base_angle
        self.angle = None
        self.base_center = None
        self.edge = None
        self.segment = None
        self.end_reading = None
        self.reading = 0.0
        self.update(car_position)

    def update(self, car_position):
        self.angle = self.base_angle + car_position.rotation
        self.base_center = car_position.location
        self.edge = self.base_center + Vector(-sin(self.angle), cos(self.angle)) * SENSOR_RANGE
        self.segment = Segment(self.base_center, self.edge)

    def analyse(self, world_objects):
        intersection_points = []
        for obj in world_objects:
            if type(obj) == Segment:
                point = self.segment.check_collision(obj)
                if point is not None:
                    intersection_points.append(point)
            elif type(obj) == Box:
                points = obj.check_collision_segment(self.segment)
                if points is not None:
                    intersection_points = intersection_points + points
        if len(intersection_points) == 0:
            self.reading = 0.0
            self.end_reading = self.edge
        else:
            first_intersection = max(intersection_points, key=lambda x: (self.edge - x).abs())
            self.reading = (first_intersection - self.edge).abs()
            self.end_reading = self.base_center + Vector(-sin(self.angle), cos(self.angle)) * (SENSOR_RANGE - self.reading)


class Car:
    def __init__(self, initial_position=Position(Vector(CAR_START[0], CAR_START[1]), 0), initial_speed=0, DUMMY=False):
        self.DUMMY = DUMMY
        self.position = initial_position
        self.speed = initial_speed
        self.bounding_box = self.unravel_box()
        self.alive = True
        if not self.DUMMY:
            self.control_system = [Sensor(angle, self.position) for angle in interpolate_cycle(N_SENSOR)]
            self.steering_wheel_angle = 0

    def accelerate(self):
        self.speed += CAR_ACCELERATION
        self.speed = min(self.speed, CAR_MAX_SPEED)

    def brake(self):
        self.speed -= CAR_ACCELERATION
        self.speed = max(self.speed, -CAR_MAX_SPEED)

    def turn_right(self):
        self.steering_wheel_angle += CAR_ANGLE_STEP
        self.steering_wheel_angle = min(self.steering_wheel_angle, MAX_STEERING_WHEEL_ANGLE)

    def turn_left(self):
        self.steering_wheel_angle -= CAR_ANGLE_STEP
        self.steering_wheel_angle = max(self.steering_wheel_angle, -MAX_STEERING_WHEEL_ANGLE)

    def move(self):
        speed_translation = self.speed * cos(self.steering_wheel_angle)
        speed_rotation = self.speed * sin(self.steering_wheel_angle)
        self.position.location = self.position.location + Vector(-sin(self.position.rotation),
                                                                 cos(self.position.rotation)) * speed_translation
        increment = Vector(speed_rotation * cos(self.position.rotation) / 2,
                           speed_rotation * sin(self.position.rotation) / 2)
        self.position.location = self.position.location + increment
        self.position.rotation = self.position.rotation - speed_rotation / CAR_WIDTH
        self.steering_wheel_angle -= sgn(self.steering_wheel_angle) * INERTIA_PARAMETER_WHEEL
        if fabs(self.steering_wheel_angle) < 3 * eps * pi:
            self.steering_wheel_angle = 0
        self.speed -= sgn(self.speed) * INERTIA_PARAMETER_SPEED
        if fabs(self.speed) < eps:
            self.speed = 0

    def update(self, world_objects=None):
        if not self.alive:
            return
        if self.DUMMY:
            self.position.location.y += self.speed
            self.bounding_box = self.unravel_box()
            return
        self.move()
        for sensor in self.control_system:
            sensor.update(self.position)
            sensor.analyse(world_objects)
        if self.get_min_obstacle() <= 1.01 * sqrt((CAR_WIDTH/2)**2 + (CAR_HEIGHT/2)**2):
            self.bounding_box = self.unravel_box()
            if self.bounding_box.check_collision(world_objects):
                self.alive = False

    def get_readings(self):
        return [sensor.reading / SENSOR_RANGE for sensor in self.control_system]

    def unravel_box(self):
        theta = self.position.rotation
        P1 = self.position.location + Vector(-sin(theta) * CAR_HEIGHT/2 - cos(theta) * CAR_WIDTH/2,
                                             cos(theta) * CAR_HEIGHT/2 - sin(theta) * CAR_WIDTH/2)
        P2 = P1 + Vector(cos(theta), sin(theta)) * CAR_WIDTH
        P3 = P2 + Vector(sin(theta), -cos(theta)) * CAR_HEIGHT
        P4 = P1 + Vector(sin(theta), -cos(theta)) * CAR_HEIGHT
        return Box(P1, P2, P3, P4)

    def get_min_obstacle(self):
        return SENSOR_RANGE - max(self.control_system, key=lambda x: x.reading).reading
