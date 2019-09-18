from math import *
from Robot import *
from Path import *

def getPath(file_name):
    with open(file_name) as path_file:
        data = json.load(path_file)
    path = data        
    vecArray = [{'X': p['Pose']['Position']['X'], \
                 'Y': p['Pose']['Position']['Y']}\
                 for p in path]
    return vecArray


def createPath():
    """Puts the positions of the path in a reversed list and returns the list"""
    vecArray = []
    
    with open('Path-around-table.json') as path_file:
        data = json.load(path_file)
        
        for i in range (len(data)):
            vecArray.append(data[i]['Pose']['Position'])
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

#while path != path[:-1]:
if __name__ == '__main__':
    print('Sending commands to MRDS server', MRDS_URL)

    robot = Robot()
    #path = createPath("Path-around-table.json")
    path=createPath()
    speed = 0.7
    aSpeed = 1.2
    lookAhead = 1
    
    
    while path:
        position = robot.getPosition()
        heading = robot.getHeading()
        newPosition = robot.carrotPoint(path, position, lookAhead)
        if newPosition:
            distance = robot.getDistance((newPosition['X'] - position['X']),
                                       (newPosition['Y'] - position['Y']))
            bearing = robot.getBearing((position['X'], position['Y']),
                                                   (newPosition['X'],newPosition['Y']))
            turnAmount = robot.turnAngle(bearing, heading)
            response = postSpeed(turnAmount*aSpeed, speed)
            #response = robot.setMotion(speed, turnAmount)
            time.sleep(0.15)
    
        response = postSpeed(0,0)