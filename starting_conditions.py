from math import pi, sqrt, sin, cos, tan
from config import config

def createOrbit():
    """This function creates an orbit based on the 'chosenConditions' dict. It accounts for all three types of orbits 
    (eliptical, parobolic, and hyperbolic) and sets the values in 'conditionList' using the parameters."""

    # Import important functions from gravity_simulation here to prevent a loop of imports.
    from gravity_simulation import getDistAndDir, polarToCartesian

    # If there is a preset selected set that instead of doing the computation.
    chosenPreset: str = config["chosenConditions"]["chosenPreset"]
    if chosenPreset != "":
        print(f"Running preset: '{chosenPreset}'.")
        for key in config["conditionList"]: # Use the keys to match the presets dict to the conditionList dict.
            config["conditionList"][key] = config["presets"][chosenPreset][key]
        config["boardConfigs"]["sizeModifier"] = config["presets"][chosenPreset]["sizeModifier"]
        return # We don't need to run the rest of this function as we are using a preset.

    
    # Redefine the variables to clean up the code.
    periapsis = config["chosenConditions"]["periapsisDistance"]
    tilt = config["chosenConditions"]["tiltAngle"]
    e = config["chosenConditions"]["eccentricity"]
    G = config["simulationPresets"]["G"]
    
    centralPos = config["chosenConditions"]["centralPosition"]
    orbitingPos = (centralPos[0] + periapsis * cos(tilt), centralPos[1] + periapsis * sin(tilt))
    centralMass = config["chosenConditions"]["centralMass"]
    orbitingMass = config["chosenConditions"]["orbitingMass"]

    # Calculate some values that we can get from other passed in vars.
    dist, theta = getDistAndDir(orbitingPos[1], orbitingPos[0]) # 'orbitingPos' is relative to centralPos so this works.
    semiMajor = (periapsis * (1 + e * cos(tilt - theta))) / (1 - (e ** 2)) #? Polar equation for an elipse
    config["boardConfigs"]["sizeModifier"] = (semiMajor + dist) / 250 # 250 is a magic number for good sizing


    # Run the computation for each of the different types of orbit.
    if 0 <= e < 1: # Elyptical Orbit
        v = sqrt(G * centralMass * (2/periapsis - 1/semiMajor)) #? vis-viva equation for an elipse
        d_v = theta + pi/2 # (-1 * (b ** 2) * Dx) / ((a ** 2) * Dy)
    
    elif e == 1: # Parobolic Orbit
        v = sqrt((2 * G * centralMass) / periapsis) #? vis-viva equation for a parabola
        d_v = theta + pi/2
    
    elif e > 1: # Hyperbolic Orbit
        v = sqrt(G * centralMass * (2/periapsis + 1/semiMajor)) #? vis-viva equation for a hyperbola
        d_v = theta + pi/2 # (b * sqrt((Dx ** 2) + (a ** 2))) / a

    else: # Catch the error case.
        raise IndexError("Eccentricity must be greater than or equal to 0.")
    

    # Convert the vector from polar to cartesian cordinates to set the velocity vector of the orbiting body. Then use 
    #  conservation of momentum to set the velocity of the center body (which although relatively low, keeps the orbit
    #  consistent for longer).
    if d_v > 2 * pi: d_v -= 2 * pi # Set to correct range if it exceeds 2pi 
    orbitingVelocity = polarToCartesian(v, d_v)
    centralVelocity = (-1 * orbitingVelocity[0] * orbitingMass / centralMass, -1 * orbitingVelocity[1] * orbitingMass / centralMass)

    # Set the values in 'conditionList' to the ones we calculated.
    config["conditionList"]["position1"] = orbitingPos
    config["conditionList"]["position2"] = centralPos
    config["conditionList"]["velocity1"] = orbitingVelocity
    config["conditionList"]["velocity2"] = centralVelocity
    config["conditionList"]["mass1"] = orbitingMass
    config["conditionList"]["mass2"] = centralMass

if __name__ == "__main__":
    from gravity_simulation import main
    main()