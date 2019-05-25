# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 17:41:05 2019

@author: Parthasarathy
"""

__author__ = 'Caleytown'

import gzip
import numpy as np
from PIL import Image
from RobotClass import Robot
from GameClass import Game
from RandomNavigator import RandomNavigator
from networkFolder.functionList import Map,WorldEstimatingNetwork,DigitClassifcationNetwork
import matplotlib.pyplot as plt
import copy

plt.close('all')
plt.ion()
#declare the neural network 1 and 2
uNet = WorldEstimatingNetwork()
classNet = DigitClassifcationNetwork()
# change value of x if you have to run step 
map = Map()
#print the number hidden in the map
#print(map.number)
#iterating 10 times

# define robot start position
robot = Robot(0,0)
reward = 0
# truth map 
data = map.map
if map.number in [0,1,2]:
    goal = [0,27]
elif map.number in [3,4,5]:
    goal = [27,27]
else:
    goal = [27,0]
# create a mask map 
mask_map = np.zeros((28,28))
fig =plt.figure()
sub_plt = fig.add_subplot(111)
all_goals = [[0,27],[27,27],[27,0]]
rgb = np.zeros((28,28,3), 'uint8')
rgb[..., 0] = data
rgb[..., 1] = data
rgb[..., 2] = data
plt_handler = sub_plt.imshow(rgb,cmap='gray')

reward_mask_map = np.zeros((28,28))
reward_mask_map[0,0] = -1

mask_map [0, 0] = 1
# get the class of robot to navigate on the map
navigator = RandomNavigator()
# creating the main objects for this game
game = Game(data,goal,navigator,robot) 

while True:
    best_info_qual = np.min(reward_mask_map)-100
    best_action = ''
    # check if there is info_qual at the initially and move to goal if available
    image = uNet.runNetwork(data,mask_map)
    char = classNet.runNetwork(image)[0]
    # get the list of possible actions you can take
    action_list = navigator.getAction(robot,data)##'put here action_list'####ensuring the positions are on map and returning possible actions
    #print("current robot location: "+repr(robot.getLoc()))
    expected_goal = []
    digit_prob = 0
    if max(char) > 0.85:
        
        #store the goal coordinates corresponding to each value of index(hidden number)
        digit_index = np.argmax(char)
        print('char='+repr(max(char)))
        print(digit_index)
        if digit_index in [0,1,2]:
            expected_goal = [0,27]
        elif digit_index in [3,4,5]:
            expected_goal = [27,27]
        elif digit_index in [6,7,8,9]: 
            expected_goal = [27,0]
        action_list2 = []
        print(expected_goal)
        for action in action_list:
            if robot.getLoc()[0] < expected_goal[0]:
                action_list2.append('right')
            elif robot.getLoc()[0]>expected_goal[0]:
                action_list2.append('left')
            elif robot.getLoc()[1]<expected_goal[1]:
                action_list2.append('up')
            elif robot.getLoc()[1]>expected_goal[1]:
                action_list2.append('down')
        action_list = action_list2
        digit_prob = digit_index
    if (robot.getLoc() == (expected_goal)) and (map.number == digit_prob):
        print('success')
        reward = reward + 100
        break
    elif robot.getLoc() in all_goals:
        reward = reward - 400
        continue
    print("reward = "+repr(reward))
                 
        #for each action
    for member in action_list:
        
        if member == 'left':
            #change my current position coordinates to new corrdinates
            ax = robot.getLoc()[0] - 1
            ay = robot.getLoc()[1] + 0
        elif member == 'right': 
            #change my current position coordinates to new corrdinates
            ax = robot.getLoc()[0] + 1 
            ay = robot.getLoc()[1] + 0
        elif member == 'up': 
            #change my current position coordinates to new corrdinates
            ax = robot.getLoc()[0] + 0
            ay = robot.getLoc()[1] + 1
        else:
            #change my current position coordinates to new corrdinates
            ax = robot.getLoc()[0] + 0
            ay = robot.getLoc()[1] - 1
        if mask_map[ay,ax] == 1:
            info_qual = 0
        else:
            #each assumption
            avg_list = []
            for i in [0, 255]:
                #assuming that it is returning an action
                # do this for each action
                # make a temporary copy of your maps
                temp_data = data.copy()
                temp_mask = mask_map.copy()
                temp_data[ay,ax] = i
                temp_mask[ay,ax] = 1
                image = uNet.runNetwork(temp_data,temp_mask)
                char = classNet.runNetwork(image)[0]
                avg_list.append(char)
            #you got the information cquality metric 
            info_qual = sum((abs(avg_list[0]-avg_list[1])))+(1*reward_mask_map[ay,ax])
            #print('current action = '+repr(member)+'info'+repr(info_qual))
        if info_qual >= best_info_qual:
            best_info_qual = info_qual
            best_action = member
    #print('info qual = ' + repr(best_info_qual)+ 'digit= '+repr(digit_index))
    robot.move(best_action)
    reward -= 1
    reward_mask_map[robot.getLoc()[1], robot.getLoc()[0]] -= 1
    mask_map[robot.getLoc()[1], robot.getLoc()[0]] = 1
    rgb[...,0] = mask_map*255
    plt_handler.set_data(rgb)
    #print(mask_map*255)
    sub_plt.imshow(rgb,cmap='gray')
    plt.draw()
    plt.pause(0.001)
    # assign rewards for each action   
#if robot.getLoc() == goal:
 #   reward = reward + 100
 #   break
#elif robot.getLoc() in all_goals:
 #   reward = reward - 400
    
        
#Image.fromarray(image).show()
#plt.imshow(image)
#plt.pause(0.0001)       
#data = map.getNewMap()

    


#for x in range(0,100):
#    game.tick()
#
#im = Image.fromarray(np.uint8(game.exploredMap)).show()
#plt.imshow(game.exploredMap)



#mask = np.zeros((28,28))
#for x in range(0,28):
#    for y in range(0,28):
#        if game.exploredMap[x,y] != 128:
#            mask[x,y] = 1

#image = uNet.runNetwork(game.exploredMap,mask)
#char = classNet.runNetwork(image)
#Image.fromarray(image).show()
    #plt.imshow(image)
    #plt.pause(0.0001)
#print(char.argmax())
#.show()

