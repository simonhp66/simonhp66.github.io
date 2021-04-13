# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 10:58:11 2021

@author: Simon
"""
#This is the practical project to build an agent based model

import random
import operator
import matplotlib.pyplot

#Add empty list for saving agents coordinates
agents = []
east = []

#Create a random integer between 0 and 99 and assign to y and then to x
#They are stored in the agents list in position [0][0] for y
#and in position [0][1] for x
#This is a list within a list

agents.append([random.randint(0,99),random.randint(0,99)])

print (agents)

#Generate a random number and use this to change the y coordinate
if random.random() <0.5:
   agents [0][0] +=1
else:
    agents[0][0]-=1  

    
#Generate a random number and use this to change the x coordinate
if random.random() <0.5:
    agents [0][1] +=1
else:
    agents[0][1]-=1  

#Generate a random number and use this to change the y coordinate
if random.random() <0.5:
   agents [0][0] +=1
else:
    agents[0][0]-=1  

    
#Generate a random number and use this to change the x coordinate
if random.random() <0.5:
    agents [0][1] +=1
else:
    agents[0][1]-=1  

print(agents)


#Agent Number 1
agents.append([random.randint(0,99),random.randint(0,99)])

print(agents)

#Generate a random number and use this to change the y coordinate
if random.random() <0.5:
   agents [1][0]+=1
else:
    agents[1][0]-=1  

    
#Generate a random number and use this to change the x coordinate
if random.random() <0.5:
    agents [1][1] +=1
else:
    agents[1][1]-=1  

#Generate a random number and use this to change the y coordinate
if random.random() <0.5:
   agents [1][0] +=1
else:
    agents[1][0]-=1  

    
#Generate a random number and use this to change the x coordinate
if random.random() <0.5:
    agents [1][1] +=1
else:
    agents[1][1]-=1  

print(agents)
print(max(agents,key=operator.itemgetter(1)))
east.append(max(agents,key=operator.itemgetter(1)))
print(east)

matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)
matplotlib.pyplot.scatter(agents[0][1],agents[0][0])
matplotlib.pyplot.scatter(agents[1][1],agents[1][0])
matplotlib.pyplot.scatter(east[0][1],east[0][0],color='red')
matplotlib.pyplot.show()


