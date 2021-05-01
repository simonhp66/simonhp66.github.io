# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 10:58:11 2021

@author: Simon
"""
# INTRODUCTION (please see README file for more details)
# This is the practical project to build an agent based model
# This is a simple version without GUI or animation
# It requires the associated file called agentframework.py
# It can run at the command line or within spyder
# INPUTS/OUTPUTS
# The inputs are from a text file (in.txt, clubnames.txt) and a website indicated at line 76
# The outputs are a plot of the agents and the eaten environment, an excel file (finaltable.xlsx),
# and a text file (environment.txt)
# The model can run at the command line using sys (with three ints added after the filename to represent
# number of agents (max 95), number of iterations and neighbour distance)
# If no arguments are entered using sys there are defaults that will run 
# SOURCES AND MODIFICATIONS TO STANDARD MODEL
# The basic structure of the code is as shown in course materials and in the online forum
# The model runs as a tournament between agents with the final table showing the winner
# The code has been modified to include agent names and powers
# The moving and sharing methods have been modified
# The input and output have been modified 
# WHAT DOESNT WORK AS EXPECTED
# All works as expected (ensure Tools/Preferences/iPython console/graphics is set to inline)


import random
import operator
import matplotlib
import matplotlib.pyplot
import time
from operator import itemgetter, attrgetter
import agentframework
import csv
import sys
import requests
from bs4 import BeautifulSoup
import xlsxwriter

print ("Start")
start = time.time() #Used for measuring how long it takes at the end
 
  
#This code opens the file and defines the reader, the new line separator
#in the dataset, and the format of the data with one decimal place
f = []
f = open('in.txt', newline='')
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
environment = [] #Create empty list
for row in reader: #Fill the list with 2D data row by row
   environment.append(row)
f.close() #Close the file


# This code opens a file and obtains data of football team names and divisions
# It is used to give each agent a unique name and a 'power' used when it 
# meets other agents (Note max 95 names). Code adapted from code found on stack overflow.
g = []
g = open('clubnames.txt', newline='')
reader = csv.reader(g, dialect="excel-tab")

football = [] #Create empty list
for row in reader: #Fill the list with names and power 2D format row by row
   football.append(row)

for i in range(len(football)): 
    football[i][0]= football[i][0].rstrip(' A.F.C.') #Strip out suffix
    football[i][1]=int(football[i][1]) #Convert string number to integer
g.close() #Close the file



#Scraping data from the web to intialise agents with Y and X (max 99 agents)
url ="https://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})


#Plot the environment data, before it is eaten
matplotlib.pyplot.imshow(environment)
matplotlib.pyplot.axis([0,299,0,299])
matplotlib.pyplot.show()


# Variables to be defined
# Variables loaded below using sys, otherwise defaults are used (see lines below)
# Three int arguments are loaded using sys in order number of agents, iterations 
# and neighbourhood distance 
if len(sys.argv)==4:
    print("Number of agents", sys.argv[1])
    num_of_agents = int(sys.argv[1])
    print("Number of iterations", sys.argv[2])
    num_of_iterations = int(sys.argv[2])
    print("Neighbourhood distance", sys.argv[3])
    neighbourhood = int(sys.argv[3])
else:
    print("Valid data not entered using sys, using defaults")
    num_of_agents = 10 #This is where one can manually change the number of agents, max 95
    num_of_iterations = 100 # Manually change iterations, more means slower (advise<1000) 
    neighbourhood = 30 # Manually change neighbourhood distance here (more than 424 is nonsensical)
    print("Number of agents", num_of_agents)
    print("Number of iterations", num_of_iterations)
    print("Neighbourhood distance", neighbourhood)
    
#Add empty list for saving agents coordinates
agents = []

# Make the agents
# Note that x and y data read from the web only covered 0 to 99 range
# But the environment is 0 to 299
# So in order to use the whole environment co-ordinates are multiplied by 3
# Alternative would be to have them all start in one corner of the environment
for i in range(num_of_agents):
    name = football[i][0] #Adding a unique name to each agent, from football club names
    power = football [i][1] #Giving each agent a "power", lower is stronger
    y = int(td_ys[i].text)*3 #Loading Y, multiply by 3 to use whole environment
    x = int(td_xs[i].text)*3 #Loading X, multiply by 3 to use whole environment
    # Creating a list of agents and each agent is able to see the environment
    # and interact with other agents
    agents.append(agentframework.Agent (name, power, y, x, environment, agents))
"""
#Check their initial location, used for testing
print ("INITIAL COORDINATES Y, X, SCORE")
for i in range (num_of_agents):
    print(agents[i])
"""
    
#Move,eat,share and shuffle the agents
for j in range(num_of_iterations):
    random.shuffle(agents) #To avoid systematic artifacts arising
    #print("Main iteration") # For testing
    for i in range(num_of_agents):
        #print("Agent iteration") #For testing
        agents[i].move() # Defined in agent framework
        agents[i].eat() #Defined in agent framework
        agents[i].share(neighbourhood) #Defined in agent framework

#Print the final agent coordinates and environment
matplotlib.pyplot.ylim(0, 299)
matplotlib.pyplot.xlim(0, 299)
matplotlib.pyplot.imshow(environment)
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i].x ,agents[i].y)
matplotlib.pyplot.show() 

print("Iterations complete, calculating scores")

"""
# Used for testing, ensure coordinates are different from initial
# Score should increase 50 per iteration (before sharing)
print("FINAL COORDINATES")# Used for testing 
for i in range (num_of_agents):
    print(agents[i])
"""
    
# Printing out an ordered list of the winning agents and their score
# The idea is that this is some kind of tournament
table = []
for i in range(num_of_agents):
    table.append((agents[i].name, agents[i].score))
    table1 = sorted(table, key=itemgetter(1), reverse=True) #Sort based on score
print("FINAL TABLE") 
for i in range(num_of_agents):
    print(table1[i])
    
# Writing the final table to an excel file (adapted from code on stack overflow)
# Excel file needs to be closed whilst running the code
with xlsxwriter.Workbook('finaltable.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, data in enumerate(table1):
        worksheet.write_row(row_num, 0, data)

# Writing the final environment list to a text file (adapted from code on stack overflow)
# Text file needs to be closed while running the code
with open('environment.txt', 'w') as testfile:
    for row in environment:
        testfile.write(' '.join([str(a) for a in row]) + '\n')

# Calculate the total score of all agents aggregated together
total_score = []
for i in range(num_of_agents):
    total_score.append(agents[i].score)
total = sum(total_score)
print("This is the total score of all teams aggregated ", total)
    
#Timing of code to measure code efficiency
end = time.time()
time_elapsed = end-start
print("TIMING")
print ("time elapsed", "%.4f" % time_elapsed,"seconds")

print("End")

"""
# Code below was used in testing as the code was developed
# Mostly printing specific items to ensure they were as expected
print("Testing data")
print(agents[0].environment[agents[0].y][agents[0].x])
print(agents[0].environment[1][0])
print(agents[1].environment[0][0])
print(agents[1].environment[1][0])
print("Store")
#Create a list of agents and their stores
storelist = []
storetotal = 0
for i in range(num_of_agents):
    storelist.append(agents[i].store)
    storetotal = storetotal + (agents[i].store)
print(storelist)
print("Storetotal", storetotal)

#Testing prints

print(environment[0][0], environment[0][1], environment[0][2])
print(agents[0].y,agents[0].x,agents[0].store)
print("Agent 0 variables",agents[0].y,agents[0].x,agents[0].store,agents[0].agents[1].y)
print(agents)
print(agents[1].environment[0][0])
print(agents[1].environment[1][0])
# Check if sicking up function works
print("central store",environment[150][150])
"""

