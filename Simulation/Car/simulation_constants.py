from math import pi

# World dimensions
WIDTH = 400
HEIGHT = 700
SIDEWALK_WIDTH = 21.5
MIDDLE_LEFT = (WIDTH / 2 + SIDEWALK_WIDTH) / 2
MIDDLE_RIGHT = WIDTH - MIDDLE_LEFT 

#  Sample time parameters
FREQUENCY = 60.0
SAMPLE_TIME = 1.0 / FREQUENCY

# Sprite locations
BACKGROUND_SPRITE = "Sprites/background.png"
CAR_SPRITE = "Sprites/car.png"

# Car parameters
CAR_WIDTH = 90
CAR_HEIGHT = 150
CAR_START = (MIDDLE_LEFT, HEIGHT/2 - CAR_HEIGHT)
CAR_ACCELERATION = 0.2
CAR_ANGLE_STEP = pi / 45
CAR_MAX_SPEED = 20
MAX_STEERING_WHEEL_ANGLE = pi / 10
INERTIA_PARAMETER_WHEEL = pi / 90
INERTIA_PARAMETER_SPEED = 0.015

# Sensor parameters
SENSOR_RANGE = 400
N_SENSOR = 20


# RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Comparison epsilon
eps = 1e-2

