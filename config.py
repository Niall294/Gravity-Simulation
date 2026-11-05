from typing import TypedDict, Tuple, Any
from math import pi

class chosenConditions(TypedDict):
    chosenPreset: str
    eccentricity: float
    periapsisDistance: float
    tiltAngle: float
    centralMass: float
    orbitingMass: float
    centralPosition: Tuple[float, float]

class conditionList(TypedDict): # Every option can also be None state as they are not meant to be preset
    position1: tuple[float, float] | None
    velocity1: tuple[float, float] | None
    mass1: float | None
    position2: tuple[float, float] | None
    velocity2: tuple[float, float] | None
    mass2: float | None

class simulationPresets(TypedDict):
    G: float
    tickTime: float
    stepsPerFrame: int
    testMode: bool
    presetIndex: int

class boardConfigs(TypedDict):
    radius: float
    boardSize: int
    trailLength: int
    backgroundColor: str
    borderColor: str
    defaultColor: str
    edgeColor: str
    sizeModifier: float | None # Can also be None as this can be automatically be determined if the user chooses

class presets(TypedDict):
    Earth_Moon_System: dict[str, tuple[float, float] | float]
    Sun_Mecury_System: dict[str, tuple[float, float] | float]

class AppConfig(TypedDict):
    chosenConditions: chosenConditions
    conditionList: conditionList
    presets: presets
    simulationPresets: simulationPresets
    boardConfigs: boardConfigs

config: AppConfig = {
    #! The variables in 'chosenConditions' are the primary settings one will want to modify to run the simulation!
    "chosenConditions": { #? Choose certain starting conditions for the particles in the siulation.
        "chosenPreset": "Sun_Mecury_System", # Choose which dict in 'presets' to use for the simulation (no preset -> "").
        "eccentricity": 0.5, # The eccentricity of the orbit
        "periapsisDistance": 1e5, # The periapsis of the orbit
        "tiltAngle": 3*pi/4, # - radians {0 --> 2pi} - The tilt from the x-axis of the orbit 
        "centralMass": 3.301e15, # The mass of the central object
        "orbitingMass": 3.301e5, # The mass of the orbiting object
        "centralPosition": (0.0, 0.0) # The starting position of the central body, recomended at 0,0 for viewing experience
    },
    "conditionList": { #? Automatically get every starting condition, even the ones not specified in 'chosenConditions'.
        "position1": None,
        "velocity1": None,
        "mass1": None,
        "position2": None,
        "velocity2": None,
        "mass2": None
    },
    "simulationPresets": { #? Choose the arbitary constants we would like to use in the simulation
        "G": 6.6743e-11, # The gravitational constant used in the simulation, '6.6743e-11' is the real world value.
        "tickTime": 5.0, # The length of time between each tick. #! Values > 1.0 directly lower the accuracy of the sim.
        "stepsPerFrame": 3600, # The number of ticks between each frame rendered in the simulation to increase speed.
        "testMode": False, # Runs the loop one tick and then pauses, used soley for testing purposes.
        "presetIndex": -1 # Which starting conditions to use: presets or custom starting conditions (-1 -> custom values).
    },
    "boardConfigs": { #? Choose how the simulation is shown on the screen.
        "radius": 1.0, # The radius of the circle we draw to represent each object in the simulation.
        "boardSize": 1000, # The actual size of the board.
        "trailLength": 200, # The length of the trail behind each object in the simulation.
        "backgroundColor": '#0d1117', # Background color in the simulation.
        "borderColor": '#3a3f4b', # Border color in the simulation.
        "defaultColor": '#4fc3f7', # Circles color in the simulation.
        "edgeColor": '#e0f7fa', # Edge color of each drawn circle.
        "sizeModifier": None # Scalar for how large the simulation is, automatically set if not chosen here.
    },
    "presets": { #? The presets than can be chosen to be used in the simulation.
        "Earth_Moon_System": { # This system is a circle
            "sizeModifier": 1794500,
            "position1": (-4412000.0, 0.0),
            "velocity1": (0.0, -13.07),
            "mass1": 5.972e+24,
            "position2": (358900000.0, 0.0),
            "velocity2": (0.0, 1075.7),
            "mass2": 7.342e+22
        },
        "Sun_Mecury_System": { # This system is an elipse
            "sizeModifier": 1794500,
            "position1": (-4412000.0, 0.0),
            "velocity1": (0.0, -13.07),
            "mass1": 5.972e+24,
            "position2": (358900000.0, 0.0),
            "velocity2": (0.0, 1075.7),
            "mass2": 7.342e+22
        }
    }
}

if __name__ == "__main__":
    from gravity_simulation import main
    main()