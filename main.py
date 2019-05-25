__author__ = 'Caleytown'

import gzip
import numpy as np
from PIL import Image
from RobotClass import Robot
from GameClass import Game
from RandomNavigator import RandomNavigator
from networkFolder.functionList import Map,WorldEstimatingNetwork,DigitClassifcationNetwork


map = Map()


data = map.map

print(map.number)


robot = Robot(0,0)
navigator = RandomNavigator()
game = Game(data,(27,27),navigator,robot)




for x in range(0,1000):
    print (robot.xLoc,robot.yLoc)
    game.tick()

im = Image.fromarray(np.uint8(game.exploredMap)).show()



uNet = WorldEstimatingNetwork()
classNet = DigitClassifcationNetwork()

mask = np.zeros((28,28))
for x in range(0,28):
    for y in range(0,28):
        if game.exploredMap[x,y] != 128:
            mask[x,y] = 1

image = uNet.runNetwork(game.exploredMap,mask)
char = classNet.runNetwork(image)
Image.fromarray(image).show()
print(char.argmax())
