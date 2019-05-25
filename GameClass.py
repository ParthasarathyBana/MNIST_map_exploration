__author__ = 'Caleytown'
import numpy as np

class Game:
    def __init__(self, map,goalLocation,navigator,robot):
        self.truthMap = map
        self.navigator = navigator
        self.robot = robot
        self.goal = goalLocation
        #get a map which is covered in grey
        self.exploredMap = np.ones(map.shape)*128
        self.updateMap(self.robot,self.exploredMap,self.truthMap)



    def tick(self):
        action = self.navigator.getAction(self.robot,self.truthMap)
        self.robot.move(action)
        self.updateMap(self.robot,self.exploredMap,self.truthMap)
        if self.robot.getLoc() == self.goal:
            return True
        else:
            return False

    def updateMap(self,robot, exploredMap, truthMap):
        for x in range(-1,2):
            for y in range(-1,2):
                if robot.getLoc()[0]+x > 27 or robot.getLoc()[0]+x < 0 or robot.getLoc()[1]+y > 27 or robot.getLoc()[1]+y < 0:
                    continue
                else:
                    exploredMap[robot.getLoc()[0]+x,robot.getLoc()[1]+y] = truthMap[robot.getLoc()[0]+x,robot.getLoc()[1]+y]

