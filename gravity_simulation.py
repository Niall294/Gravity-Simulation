import math
from typing import Any
from config import config
from starting_conditions import createOrbit
from board import showBoard

def main():
    """Refrence README for a description of the porgram and how to use it!"""

    # Redefine the variables to clean up the code and run 'createOrbit' to set the values according to chosenConditions.
    objects: list[Object] = []
    createOrbit()
    stepsPerFrame = config["simulationPresets"]["stepsPerFrame"]
    testMode = config["simulationPresets"]["testMode"]
    tickTime = config["simulationPresets"]["tickTime"]
    numObjects = int(len(config["conditionList"]) / 3) # How many objects are represented in conditionList
    for i in range(1, numObjects + 1, 1):
        p = config["conditionList"][f"position{i}"]
        v = config["conditionList"][f"velocity{i}"]
        m = config["conditionList"][f"mass{i}"]
        objects.append(Object(p, v, m))

    # Run the simulation tick by tick, updating each objects motion vectors. This approach to position and velocity being
    #  updated once per time step has a trade off: it lowers accuracy compared to integration but results in faster speeds
    #  and simplicity. This means that over long run times the program can become inaccurate, but they aren't noticable 
    #  until multiple minutes have passed. It allows the program to run in real time without other sacrafices.
    tick = 0
    while tick < 1e10: # Instead of doing 'while True', we set a limit to prevent an infinite loop
        # Update the acceleration vectors for each object using newtons law of gravitation.
        for i in range(0, len(objects)-1, 1):
            for j in range(i+1, len(objects), 1):
                computeAccelerations(objects, i, j)

        # Update the position and velocity vectors for each object using galileo's equations, and print the vectors
        #  before we change them (used for testing purposes).
        for object in objects:
            if testMode: printForTesting(object)
            computePositionsAndVelocities(object, tickTime)

        # Check that we are not in testMode, and that the window was not closed, then move forward one tick.
        if tick % stepsPerFrame == 0: # the board doesn't need to be drawn every frame
            if showBoard(objects): return # returns if the window is closed to stop the program
        if testMode:
            if input("Press enter to step forward one tick ('clear' to quit).") == "clear": return
        tick += 1

def getDistAndDir(Dy, Dx):
    """Finds the distance using the distance formula and the direction using arctangent. We use atan2 to ensure that
    we cover all angles - not just ones in the first quadrant (which is what 'atan' does). The positive x-axis is 0."""

    distance = math.sqrt((Dy ** 2) + (Dx ** 2))
    direction = math.atan2(Dy, Dx)
    return distance, direction

def polarToCartesian(magnitude, direction):
    """Takes in a polar vector and returns it as a cartesian vector."""
    return (magnitude * math.cos(direction), magnitude * math.sin(direction))

def computeAccelerations(objects, i, j):
    """Helper function to make main more clean."""

    # Set some variables for the position vectors and masses to make the code a bit more clean.
    Dx = objects[j].getPosition()[0] - objects[i].getPosition()[0]
    Dy = objects[j].getPosition()[1] - objects[i].getPosition()[1]
    mass1 = objects[i].getMass()
    mass2 = objects[j].getMass()
    G = config["simulationPresets"]["G"] # redefine G from config to be a tiny bit more clean

    # Get the distance between the objects and the angle between them to use in calculations. There needs to
    #  be a distinction between direction 1 and direction two or the objects would repulse each other which is
    #  the opposite of what we want.
    distance, direction1 = getDistAndDir(Dy, Dx)
    direction2 = direction1 + math.pi

    # Finds the force using Newtons law of gravitation and second law of motion and checks that the distance
    #  is not zero for the edge case. #* F=GMm/r^2
    if distance == 0: raise ValueError("\nTwo pointmasses are overlapping.\n")
    force = (G * mass1 * mass2) / (distance ** 2)

    # Set the acceleration for each object using the force and convert to a cartesian vector. #* F=ma
    newAX, newAY = polarToCartesian((force / mass1), direction1)
    curAX, curAY = objects[i].getAcceleration()
    objects[i].setAcceleration((newAX + curAX, newAY + curAY))

    newAX, newAY = polarToCartesian((force / mass2), direction2)
    curAX, curAY = objects[j].getAcceleration()
    objects[j].setAcceleration((newAX + curAX, newAY + curAY))

def computePositionsAndVelocities(object, tickTime):
    """Helper function to make main more clean."""

    # Update the position vector using the acceleration, velocity and previous position (position updates first
    #  as otherwise the accleration would be counted twice in the calculation of the position).
    positionX = object.getPosition()[0] + object.getVelocity()[0] * tickTime + 0.5 * object.getAcceleration()[0] * (tickTime ** 2)
    positionY = object.getPosition()[1] + object.getVelocity()[1] * tickTime + 0.5 * object.getAcceleration()[1] * (tickTime ** 2)
    object.setPosition((positionX, positionY)) #* x_f = x_i + (v_i * t) + (0.5 * a * t^2)

    # Update the velocity vector using the acceleration and previous velocity.
    velocityX = object.getVelocity()[0] + object.getAcceleration()[0] * tickTime
    velocityY = object.getVelocity()[1] + object.getAcceleration()[1] * tickTime
    object.setVelocity((velocityX, velocityY)) #* v_f = v_i + (a * t)

    # Set the acceleration to zero - this program adds the acceleration to itself in the previous for loop,
    #  this is to allow for mulitple objects to exert and acceleration on each object. But we want the
    #  acceleration to start back at zero by the next tick because it should not rely on the previous value,
    #  instead being defind by Newtons law of gravitation.
    object.setAcceleration((0, 0))

def printForTesting(object):
    print(object.getPosition())
    print(object.getVelocity())
    print(object.getAcceleration())
    print(object.getMass())
    print("\n")

class Object:
    """Each object is represetned as a point mass with a position vector, velocity vector, acceleration vector, and 
    mass that can be updated or returned at any time. (Would be named Object, but that is too close to )"""

    def __init__(self, position, velocity, mass):
        # Sets the initial conditions for each object, accleration is not set because it is overwritten every tick.
        if mass <= 0: raise ValueError("\nThe mass of an object must be greater than zero in this simulation.\n")
        self.position = position
        self.velocity = velocity
        self.acceleration = (0, 0)
        self.mass = mass

    def setPosition(self, position):
        # Sets the position vector to the value that was passed in.
        self.position = position[0], position[1]

    def setVelocity(self, velocity):
        # Sets the velocity vector to the value that was passed in.
        self.velocity = velocity[0], velocity[1]

    def setAcceleration(self, acceleration):
        # Sets the acceleration vector to the value that was passed in.
        self.acceleration = acceleration[0], acceleration[1]

    def getPosition(self):
        # Returns the current position vector.
        return self.position[0], self.position[1]
    
    def getVelocity(self):
        # Returns the current velocity vector.

        return self.velocity[0], self.velocity[1]
    
    def getAcceleration(self):
        # Returns the current acceleration vector.
        return self.acceleration[0], self.acceleration[1]

    def getMass(self):
        # Returns the current mass.
        return self.mass

if __name__ == "__main__":
    main()