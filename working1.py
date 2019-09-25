from Robot import *
import json, time



robot = Robot()
path = robot.getPath("Path-to-bed.json")
speed = 0.7
aSpeed = 1.7
lookAhead = 1
start = time.time()

while path:
    """Get robots position and finds a new waypoint"""
    position = robot.getPosition()        
    newPosition = robot.carrotPoint(path, position, lookAhead)
    if newPosition:
        """If a new waypoint was found, get bearing and heading angle 
        and calculate turning amount. Then make the robot turn and move in the right
        direction"""
        bearing = robot.getBearing((position['X'], position['Y']),
                                                   (newPosition['X'],newPosition['Y']))
        heading = robot.getHeading()        
        turnAmount = robot.turnAngle(bearing, heading)
        response = robot.postSpeed(turnAmount*aSpeed, speed)
        time.sleep(0.15)

    response = robot.postSpeed(0,0)
    finish = time.time()
    
"""Calculates the total running time """    
total = finish - start
print ('Runtime was:', total)