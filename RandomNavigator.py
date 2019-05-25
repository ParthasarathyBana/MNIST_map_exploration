__author__ = 'Caleytown'
import numpy as np
from random import randint
from PIL import Image
from RobotClass import Robot
from GameClass import Game
from networkFolder.functionList import Map,WorldEstimatingNetwork,DigitClassifcationNetwork
import copy
from softmax import softmax
from operator import sub


class RandomNavigator:
    #def __init__(self):
    
    def getAction(self,robot,map):
        acts = [[0,-1],[1,0],[-1,0],[0,1]]
        nbrs = []
        action_list = []
        for i in range(4):
            ax = robot.getLoc()[0] + acts[i][0]
            ay = robot.getLoc()[1] + acts[i][1]
            if ax<0 or ax>27 or ay<0 or ay>27:
                continue
            nbrs.append([acts[i][0],acts[i][1]])
        print("neighbors_list" + repr(nbrs))
        for i in range(len(nbrs)):
            if nbrs[i][1]>0:
                action_list.append('up')
            elif nbrs[i][1]<0:
                action_list.append('down')
            elif nbrs[i][0]>0:
                action_list.append('right')
            elif nbrs[i][0]<0:
                action_list.append('left')
        print("action list:"+repr(action_list))
        return action_list


    # def getAction(self,robot,map):
    #     randNumb = randint(0,3)
    #     if randNumb == 0:
    #         if robot.getLoc()[0]-1 < 0:
    #             randNumb = randNumb + 1
    #         else:
    #             return 'left'
    #     if randNumb == 1:
    #         if robot.getLoc()[0]+1 > 27:
    #             randNumb = randNumb + 1
    #         else:
    #             return 'right'
    #     if randNumb == 2:
    #         if robot.getLoc()[1]+1 > 27:
    #             randNumb = randNumb + 1
    #         else:
    #             return 'down'
    #     if randNumb == 3:
    #         if robot.getLoc()[1]-1 < 0:
    #             randNumb = 0
    #         else:
    #             return 'up'