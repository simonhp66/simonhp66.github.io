# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 10:58:11 2021

@author: Simon
"""
# INTRODUCTION (please see README file for more details)
# This is the practical project to build an agent based model
# This version includes animation and a GUI (there is also a simple version without GUI and ani)
# It requires the associated file called agentframework.py
# INPUTS/OUTPUTS
# The inputs are from a text file (in.txt, clubnames.txt) and a website indicated at line 78
# The GUI requires you to click on the agent model menu and then run model from the dropdown list
# The outputs are an animation, an excel file (finaltable.xlsx), a text file (environment.txt)
# The model can run at the command line using sys (with three ints added after the filename to represent
# number of agents (max 95), number of iterations and neighbour distance) 
# SOURCES AND MODIFICATIONS TO STANDARD MODEL
# The basic structure of the code is as shown in course materials and in the online forum
# The model runs as a tournament between agents with the final table showing the winner
# The code has been modified to include agent names and powers
# The moving and sharing methods have been modified
# The input and output have been modified 
# WHAT DOESNT WORK AS EXPECTED
# The animation code works visually but results in more iterations being run than intended 
# So the scores at the end are higher than would be expected
# The GUI creates two plots one of which is blank
# The main function causes many error messages and has been disabled, but the code runs despite this

import random
import operator
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import matplotlib.animation
import tkinter
import time
from operator import itemgetter, attrgetter
import agentframework
import csv
import sys
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process
import xlsxwriter

print ("Start")
start = time.time() #Used for measuring how long it takes
 
  
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
# meets other agents (Note max 95 names)
g = []
g = open('clubnames.txt', newline='')
reader = csv.reader(g, dialect="excel-tab")

football = [] #Create empty list
for row in reader: #Fill the list with names and power 2D format row by row
   football.append(row)

for i in range(len(football)): 
    football[i][0]= football[i][0].rstrip(' F.C.') #Strip out suffix
    football[i][1]=int(football[i][1]) #Convert string number to integer
g.close() #Close the file


#Scraping data from the web to intialise agents with Y and X (max 99 agents)
url ="https://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})

"""
#Plot the environment data, before it is eaten
matplotlib.pyplot.imshow(environment)
matplotlib.pyplot.axis([0,299,0,299])
matplotlib.pyplot.show()
"""

# Variables to be defined
# Variables loaded below using sys, otherwise defaults are used (see lines below)
# Three arguments are loaded using sys in order number of agents, iterations 
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
    num_of_agents = 10 # Manually change the number of agents here (max 95)
    num_of_iterations = 100 # Manually change iterations here (more=slower, recommend <1000)
    neighbourhood = 30 # Manually change neighbourhood distance here (more than 424 is nonsensical)
    print("Number of agents", num_of_agents)
    print("Number of iterations", num_of_iterations)
    print("Neighbourhood distance", neighbourhood)
    
    
#Add empty list for saving agents coordinates
agents = []

#Set up frame for animation
fig =matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

#Make the agents
for i in range(num_of_agents):
    name = football[i][0] #Adding a unique name to each agent
    power = football [i][1] #Giving each agent a "power", lower is stronger
    y = int(td_ys[i].text)*3 #Loading Y, multiply by 3 to use whole environment
    x = int(td_xs[i].text)*3 #Loading X, multiply by 3 to use whole environment
    # Creating a list of agents and each agent is able to see the environment
    # and interact with other agents
    agents.append(agentframework.Agent (name, power, y, x, environment, agents))
"""    
#Check their initial location, used for testing
print ("INITIAL COORDINATES Y, X, STORE")
for i in range (num_of_agents):
    print(agents[i].name, " Y", agents[i].y, " X", agents [i].x, " Score",agents[i].score)
"""
# Animation code
carry_on = True

def update(frame_number):
    fig.clear()
    global carry_on
    
#Move,eat,share and shuffle the agents
    for j in range(num_of_iterations):
        #print("Main iteration")
        random.shuffle(agents) #To avoid systematic artifacts arising, taken out for animation
        for i in range(num_of_agents):
            #print("Individual agent iteration")
            agents[i].move() # Defined in agent framework
            agents[i].eat() #Defined in agent framework
            agents[i].share(neighbourhood) #Defined in agent framework
 
#Animation code (stopping part)
#    if random.random() < 0.01: #Changed to 0.01 to allow animation to run longer
#        carry_on = False
#        print("Random Stopping condition") #Find out the reason for stopping

    matplotlib.pyplot.imshow(environment)
    matplotlib.pyplot.axis([0,299,0,299])
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x, agents[i].y)

def gen_function(b=[0]):
    a = 0
    global carry_on        
    
    while (a < num_of_iterations) & (carry_on):
        yield a #Returns control and awaits next call
        a = a+1
        if a == num_of_iterations: #Find out the reason for stopping
            print("Iterations complete, calculating scores")
            
            
            #Printing final co-ordinates, used for testing  
            #print("FINAL COORDINATES")
            #for i in range (num_of_agents):
            #    print(agents[i])
               
                
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
            # Excel file needs to be closed during running of the code
            with xlsxwriter.Workbook('finaltable.xlsx') as workbook:
                worksheet = workbook.add_worksheet()
            
                for row_num, data in enumerate(table1):
                    worksheet.write_row(row_num, 0, data)

            # Writing the final environment list to a text file (adapted from code on stack overflow)
            # Text file needs to be closed during running of the code
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
            #Less relevant in this version of the model as user actions influence the total time
            end = time.time()
            time_elapsed = end-start
            print("TIMING")
            print ("time elapsed", "%.4f" % time_elapsed,"seconds")

# Animation code
def runAnimation():
    animation = matplotlib.animation.FuncAnimation(fig,
                                                   update, interval=1, repeat=False, frames=gen_function)

    #matplotlib.pyplot.show()
    wait_fig()
    return



def wait_fig():
    if matplotlib.pyplot.isinteractive():
        matplotlib.pyplot.ioff()
        matplotlib.pyplot.show(block=False)
    else:
        matplotlib.pyplot.show(block=False)
    matplotlib.pyplot.pause(3)
    matplotlib.pyplot.close()
    return

def main(): # Note that main is disabled at the last line below
    if __name__ != '__main__': return
    
    p = Process(target=runAnimation())
    p.start()
    print('hello', flush=True)
    p.join #suppress this code if you want ani executed in parallel with subsequent code
    for i in range(3):
        print('world', flush=True)
        time.sleep(1)
    matplotlib.pyplot.close()
        
    print("End")

def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, repeat=False, frames=gen_function)
    canvas.draw()

# Create GUI
root = tkinter.Tk()
root.wm_title("Agent Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu =tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Agent model", menu=model_menu)
model_menu.add_command(label ="Run model", command=run)


def exiting():
    root.quit()
    root.destroy()

root.protocol('WM_DELETE_WINDOW', exiting)

tkinter.mainloop() #Wait for interaction

"""
# With main disabled the program works
# With main enabled it also works but produces many error messages
# Seems to be related to tkinter  
main()    
"""  
  

"""
#plot the environment after agents have eaten it   
matplotlib.pyplot.ylim(0, 299)
matplotlib.pyplot.xlim(0, 299)
matplotlib.pyplot.imshow(environment)
"""

"""
# The code below was used in testing as the code was developed 
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
# Testing sicking up process
print("central store",environment[150][150])
"""

