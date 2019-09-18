"""
Example demonstrating how to communicate with Microsoft Robotic Developer
Studio 4 via the Lokarria http interface. 

Author: Erik Billing (billing@cs.umu.se)

Updated by Ola Ringdahl 2014-09-11
Updated by Lennart Jern 2016-09-06 (converted to Python 3)
Updated by Filip Allberg and Daniel Harr 2017-08-30 (actually converted to Python 3)
Updated by Thomas Johansson 2019-08-22 from Lokarriaexample.py to a class implementation
190904 thomasj fixed some errors in getHeading, getPosition. getHeading now returns and angle.
"""

import http.client, json, time
from math import *
import quaternion, Path

HEADERS = {"Content-type": "application/json", "Accept": "text/json"}
MRDS_URL = 'localhost:50000'

class UnexpectedResponse(Exception): pass

class Robot:
    def __init__(self, host = "bratwurst.ad.cs.umu.se", port = "50000"):   
#    def __init__(self, host = "127.0.0.1", port = "50000"):
        self.url = host + ':' + port
        
    def getHeading(self):
        """Returns the heading angle, in radians, counterclockwise from the x-axis
        Note that the sign changes at pi radians, i.e. the heading goes from 0
        to pi, then from -pi back to 0 for a complete circuit."""
        pose = self._getPose()['Pose']['Orientation']
        heading = quaternion.heading(pose) 
        return atan2(heading["Y"], heading["X"])
    
    def getPosition(self):
        """Returns the XY position as a two-element list"""
        pose = self._getPose()
        return pose['Pose']['Position']
    
    def setMotion(self, linearSpeed, turnrate):
        """ 
        Sends a speed and turn rate 
        command to the MRDS server
        speed is given in m/s, turn rate in radians/s
        """
        mrds = http.client.HTTPConnection(MRDS_URL)
        params = json.dumps({'TargetLinearSpeed':linearSpeed, 'TargetAngularSpeed':turnrate})
        mrds.request('POST','/lokarria/differentialdrive', params, HEADERS)
        response = mrds.getresponse()
        status = response.status
        #response.close()
        if status == 204:
            return response
        else:
            raise UnexpectedResponse(response)        
        
    
        
    # Local methods, not usually used outside of this class    
    def _getPose(self):     
        """Reads the current position and orientation from the MRDS"""
        mrds = http.client.HTTPConnection(MRDS_URL)
        mrds.request('GET','/lokarria/localization')
        response = mrds.getresponse()
        if (response.status == 200):
            poseData = response.read()
            response.close()
            return json.loads(poseData.decode())
        else:
            return UnexpectedResponse(response)        
        pass
    
    def getBearing(self, currentPosition, newPosition):
        x1, y1 = currentPosition
        x2, y2 = newPosition
        bearingAngle = atan2(y2-y1, x2-x1)
        return bearingAngle

    
    def turnAngle(self, bearing, heading):
        tAngle = bearing - heading
        return tAngle
    
    def getDistance(self, x, y):
        return sqrt((x**2) + (y**2))
    
    def carrotPoint(self, path, pose, lookAhead):
        for i in range(len(path)):
            newPosition = path[len(path)-1]
            distanceX = newPosition['X'] - pose['X']
            distanceY = newPosition['Y'] - pose['Y']
            
            distance = self.getDistance(distanceX, distanceY)
            
            if distance < lookAhead:
                path.pop()
            else:
                return newPosition

