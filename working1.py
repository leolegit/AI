from Robot import *
import json, time

def getPath(file_name):
    with open(file_name) as path_file:
        data = json.load(path_file)
    path = data        
    vecArray = [{'X': p['Pose']['Position']['X'], \
                 'Y': p['Pose']['Position']['Y']}\
                 for p in path]
    vecArray.reverse()
    return vecArray

    
def postSpeed(angularSpeed,linearSpeed):
    """Sends a speed command to the MRDS server"""
    mrds = http.client.HTTPConnection(MRDS_URL)
    params = json.dumps({'TargetAngularSpeed':angularSpeed,'TargetLinearSpeed':linearSpeed})
    mrds.request('POST','/lokarria/differentialdrive',params,HEADERS)
    response = mrds.getresponse()
    status = response.status
    #response.close()
    if status == 204:
        return response
    else:
        raise UnexpectedResponse(response)

robot = Robot()
path = getPath("Path-around-table.json")
speed = 0.7
aSpeed = 1.3
lookAhead = 1
timer = time.time()

while path:
    position = robot.getPosition()        
    newPosition = robot.carrotPoint(path, position, lookAhead)
    if newPosition:
        bearing = robot.getBearing((position['X'], position['Y']),
                                                   (newPosition['X'],newPosition['Y']))
        heading = robot.getHeading()        
        turnAmount = robot.turnAngle(bearing, heading)
        response = postSpeed(turnAmount*aSpeed, speed)
        time.sleep(0.15)

    response = postSpeed(0,0)
    finishTime = time.time()
    
totalTime = finishTime - timer
print ('Runtime was:', totalTime)