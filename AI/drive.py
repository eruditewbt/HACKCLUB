# This code simulates a self-driving car agent that makes decisions based on the environment's state.
# It uses sensors to detect traffic lights, obstacles, speed limits, and the car's current speed and direction.
import random
import logging

# defining the environment
class RoadEnvironment:
    def __init__(self):
        self.traffic_light = 'green'     # Could be 'green', 'yellow', or 'red'
        self.obstacle_ahead = False
        self.speed_limit = 60  # in km/h
        self.steer_direction = 'forward'
        self.speed = 0 # in km/h
        self.directional_change = False

# defining the sensors
class CarSensors:
    def __init__(self, env):
        self.env = env

    def detect_traffic_light(self):
        return self.env.traffic_light

    def detect_obstacle(self):
        return self.env.obstacle_ahead

    def read_speed_limit(self):
        return self.env.speed_limit
    
    def detect_steer_direction(self):
        return self.env.steer_direction
    
    def detect_directional_change(self):
        return self.env.directional_change
    
    def read_speed(self):
        return self.env.speed

# defining the actuator
class CarActuators:
    def __init__(self, env):
        self.env = env

    def steer(self, direction):
        print(f"Steering {direction}")
        self.env.steer_direction = direction

    def change_direction( self, direction):
        print(f"changing direction to  {direction}")
        self.env.steer_direction = direction

    def point(self, direction):
        if direction:
            print(f"Pointers in Action: {direction} ")
        else:
            print(f"Pointers in Action: general pointing... ")

    def accelerate(self):
        print("Accelerating...")
        self.env.speed += 1

    def brake(self):
        print("Braking...")
        self.env.speed -= 1

# defining an agent function
class SelfDrivingAgent:
    def __init__(self, sensors, actuators):
        self.sensors = sensors
        self.actuators = actuators

    def decide_and_act(self):
        light = self.sensors.detect_traffic_light()
        obstacle = self.sensors.detect_obstacle()
        direction = self.sensors.detect_steer_direction()
        speed = self.sensors.read_speed()
        speed_limit = self.sensors.read_speed_limit()
        directional_change = self.sensors.detect_directional_change()

        if light == 'red' or obstacle:
            self.actuators.brake()
        elif light == 'yellow':
            self.actuators.brake()
        elif directional_change:
            self.actuators.point(direction)
            if direction == 'backward' or direction == 'forward':
                while (speed > 0):
                    self.actuators.brake()
                    speed = self.sensors.read_speed()

            else:
                self.actuators.brake()
            self.actuators.change_direction(direction)
            self.actuators.steer(direction)

        else:
            while (speed < speed_limit):
                self.actuators.accelerate()
                speed = self.sensors.read_speed()
            while (speed >= speed_limit):
                self.actuators.brake()
                speed = self.sensors.read_speed()

            self.actuators.steer(direction)

# simulate the agent


# while(True):
#     # get the current environment and simulate it
#     quit = input('do you want to quit? y for Yes, n for No: ')
#     if quit != 'y' or quit != 'Y' or 'yes' or "Yes":
#         break
#     # Create the environment
#     env = RoadEnvironment()
#     env.traffic_light = input('enter the traffic light status: ')
#     env.obstacle_ahead = input('signify if theres an obstacle ahead. True or False: ')
#     env.speed = input('enter the current speed: ')
#     env.steer_direction = input('signify the steer direction: ')
#     env.directional_change = input('signify if theres a directional change. True or False: ')


#     # Set up the agent
#     sensors = CarSensors(env)
#     actuators = CarActuators(env)
#     agent = SelfDrivingAgent(sensors, actuators)

#     # Run decision
#     agent.decide_and_act()
#     print(f"Current Speed: {env.speed} km/h")

def random_env():
    env = RoadEnvironment()
    env.traffic_light = random.choice(['green', 'yellow', 'red'])
    env.obstacle_ahead = random.choice([True, False])
    env.speed = random.randint(0, 100)
    env.steer_direction = random.choice(['forward', 'backward', 'left', 'right'])
    env.directional_change = random.choice([True, False])
    return env

for _ in range(10):  # Run 10 automated simulations
    env = random_env()
    # print states 
    print (f"Traffic Light: {env.traffic_light}, Obstacle Ahead: {env.obstacle_ahead}, Speed: {env.speed} km/h, Steer Direction: {env.steer_direction}, Directional Change: {env.directional_change}")

    # Set up the agent
    sensors = CarSensors(env)
    actuators = CarActuators(env)
    agent = SelfDrivingAgent(sensors, actuators)
    agent.decide_and_act()

# Set up logging
    logging.basicConfig(filename='simulation.log', level=logging.INFO)

    speed = sensors.read_speed()
    light = sensors.detect_traffic_light()
    obstacle = sensors.detect_obstacle()
    direction = sensors.detect_steer_direction()
    directional_change = sensors.detect_directional_change()
    speed_limit = sensors.read_speed_limit()
    # Log the actions taken by the agent
    logging.info(f"Light: {light}, Obstacle: {obstacle}, Speed: {speed}, Speed Limit {speed_limit}, Direction: {direction}, Directional Change: {directional_change}, Action: ...")
