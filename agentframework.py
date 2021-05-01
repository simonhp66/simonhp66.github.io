# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 18:46:15 2021

@author: Simon
"""
# The agent framework works with the associated agent based model.
# It defines the agents parameters and the move, eat and share functions.

import random

#creating the class, and the instance variables
class Agent:
    
    def __init__ (self, name, power, y, x, environment, agents):
        self.name = name # Unique name to idenify agents
        self.power= power # Used to enable more powerful to steal from less powerful
        self.x = x
        self.y = y
        self.environment = environment
        self.score = 0
        self.agents = agents
        self.jump = 0 #Used to enable less powerful agents to jump away

# Defining what is to be printed when you request each agent
    def __str__(self):
        return str(self.name)+"   Power "+str(self.power)+"   Score "+ str(self.score)+"  x"+ str(self.x)+ " y"+str(self.y)
   
    
# Move the agents 1 step
# Move method has been modified so they can move to any adjacent square
# or they can remain where they are
# Previous method only allowed diagonal moves
# Jump method enables agent to jump 20 places in x and y to escape if they have just met
# a more powerful agent and lost 100 score in the sharing process 
    def move(self):
        r = random.randint(1,9)
        if self.jump > 0: # Will be 1 if the agent has just lost 100 units in sharing
            m = 20 # Enables a bigger jump
            #print("Jumped",self.name)# Testing code
        else:    
            m = 1
        if r == 1:
            self.y +=m
            self.x -=m
        if r == 2:
            self.y +=m
            self.x =self.x #This line not needed but included for clarity
        if r == 3:
            self.y +=m
            self.x +=m
        if r == 4:
            self.y =self.y
            self.x -=m
        if r == 5:
            self.y =self.y
            self.x =self.x
        if r == 6:
            self.y =self.y
            self.x +=m
        if r == 7:
            self.y -=m
            self.x -=m
        if r == 8:
            self.y -=m
            self.x = self.x
        if r == 9:
            self.y -=m
            self.x +=m
# Ensure the agents remain within the Torus shape
        if self.y < 0:
            self.y = 299
        if self.x < 0:
            self.x = 299
        if self.y >299:
            self.y = 0
        if self.x> 299:
            self.x = 0

            
#Define the eating method for agents        
    def eat(self):
        if self.environment[self.y][self.x]>50:
            self.environment[self.y][self.x]-=50
            self.score += 50
 #Eat the last remaining units below 50
        else:
           self.score = self.score+self.environment[self.y][self.x]
           self.environment[self.y][self.x]=0

    
 #Make agents sick up at 150,150 when they get to 100 units  
 #       if self.score>99:
 #           self.environment[150][150]=self.environment[150][150]+self.score
 #           self.score=0
 
 
 
 # New method, agents with more power steal more score from agents with less power
 # If power is equal then traditional sharing method used
 # If an agent is unlucky to meet a more powerful agent
 # It is enabled to jump away on its next move
    def share(self,neighbourhood):
        for agent in self.agents:
            dist = self.pythagoras(agent)
            if dist < neighbourhood:
               # print("close, score before self", self.score, "other",agent.score)
                if agent.score>100 and self.power<agent.power:
                    self.score= self.score+100
                    agent.score= agent.score-100
                    self.jump = 0 #Turns off jump
                elif self.score>100 and self.power>agent.power:
                    self.score = self.score-100
                    agent.score= agent.score+100
                    self.jump=1 #Turns on jump, enabling agent to flee next turn 
                else:
                    self.score = int((self.score+agent.score)/2)
                    agent.score = self.score
                    self.jump = 0 # Turns off jump
                # print("score after self", self.score, "score after",agent.store)
            else:
                self.jump = 0 #Turns off jump
                #print("far", dist)
 
            
#Distance between function used in share method above
    def pythagoras(self,agent):
        self.ysquared = (self.y-agent.y)**2
        self.xsquared = (self.x-agent.x)**2
        self.distance = (self.ysquared+self.xsquared)**0.5
        return(self.distance)            
 
    
  
    
  
    
  
    
  
    
  
    