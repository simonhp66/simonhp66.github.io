# Online Portfolio
This is a portfolio of work from the Geog5003M practical sessions.

# Agent based model introduction

The practical involves building an agent based model which interacts with its environment and where agents interact with each other.
The agents randomly move around an environment (a raster size 0-299 square, rather like a digital elevation model) and as they move they "eat" part of the environment and store it within themselves.
So over time the environment is gradually eaten down. When the agents are within a defined "neighbourhood distance" of each other they interact with each other by sharing their stores.
There are two models. The main model has a gui and an animation (guimodel.py) but some remaining bugs identified below.
There is also a simple version (simplemodel.py) which has no known bugs but no gui or animation. Both models use the same associated agentframework.py  

# Model enhancements
The model developed follows the structure guided by the instructions except with respect to the following enhancements.

**Agent naming and power:** Agents are given unique names so they can be more easily identified and each agent is given a "power rating" ranging from 1 (most powerful)to 6 (least powerful).
The agent names and powers have been loaded from a text file and are based on the names of English football teams and their respective divisions. 

**Agent moving:** The standard method of moving agents involves each agent moving both co-ordinates in an iteration. This means that an agent always moves in a diagonal fashion (rather like the bishop in a chess game). This also means that there are certain cells in the environment that an agent can never reach. If you think of the environment as like a chessboard all agents can play on either white squares or black ones but cannot change colours. With a small number of agents and heavy "grazing" of the environment this leads to a distinctive criss/cross pattern as either the white or black cells are repeatedly eaten. This is less apparent with a large number of agents as about half will be on each "colour".
The method of moving was therefore modified so that on each iteration an agent can move to any of the surrounding 8 cells or remain in the same place. 
In addition agents have been given the ability to "jump" after they have had an encounter with a more powerful agent so they have a chance to get away.

**Agent sharing:** This is where the power attribute is used. Agents meeting other agents that are less powerful than themselves "steal" 100 units from the less powerful agent.
If two agents meet of the same power then they share their units equally as described in the instructions. After being the victim of stealing an agent is able to "jump" on its next iteration. 

**Output:** The main output is an ordered "league table" of agents based on their score. This is printed and also saved to an excel file 
Due to the method of sharing the most powerful tend to end closer to the top of the league table.

#Installation and usage
The program can be run at the command line or within Spyder. At the command line you can optionally enter arguments for number of agents, number of iterations and neighboiurhood distance.
To run at the command line enter python modelname.py x y z (where x y and z are integers)
If no valid arguments are entered the model runs with defaults.
The maximum for agents is 95 (this is the number of agent names in the clubnames.txt file).
There is no maximum for iterations but it is recommended to enter less than 1000 as this increases the amount of time taken for the model to run (please see testing below)
There is no maximum for neighbourhood distance but the environment is a square with co-ordinates from 0 to 299 so the maximum theoretical number is 424
The simple model runs on its own with no further user interaction.
The GUI model creates a menu, you need to select run model from the drop down list and at the end you need to close the animation window.

To run the simplemodel.py in Spyder ensure that tools/preferences/ipyhton module/graphics is set to inline
To run the guimodel.py in Spyder ensure that tools/preferences/ipython module/graphics is set to tkinter
To run the guimodel.py in Spyder enter in the console %matplotlib qt and then %gui tk

#Inputs and outputs
The inputs are two text files (in.txt and clubnames.txt). In addition the initial co-ordinates of the agents are entered from a website. 
The outputs of both models are a league table (printed and saved to the excel file finaltable.xlsx) a text file with the environment after it has been eaten (environment.txt)
The simplemodel.py produces two plots - a before plot of the environment and an after plot of the eaten environment and the locations of the agents.
The guimodel.py produces an animation.   

#Further development
The simplemodel.py works as expected.
The guimodel.py has some remaining bugs. The number of iterations is more than expected. This is because the agent iterations and the animation iterations have separate threads.
So if you set iterations to 1 there are actually two iterations run. If you set iterations to two there are 6 iterations run.
The main function has been disabled. This is because it produces a number of error messages (although the code still runs).
Disabling main enables the program to run without error messages but the user has to close the animation window.

#Testing
The coding was tested as it was developed, primarily by printing out variables or iterations as the code runs.
In most cases the testing lines have been left in the code but commented out. 
**Specific tests**
In particular the move function was tested by making sure that the before and after co-ordinates made sense with one or two iterations.
The move function was also tested by running a high number of iterations and observing closely the patterns of "eaten" environment. IN this way one of the limitation of the original move function was discovered.
The store (remaned score) function was tested to ensure that it grew by an appropriate amount with small numbers of iterations. This is how the iteration problem with the guimodel was identified.
The sharing model was tested by printing out when a share took place and the before and after score of each sharing agent.
The jump mode of moving was tested to see when a jump move ocurred.
  
**Timing**
The code was also timed to establis its efficiency. A further development would involve running the code automatically with different arguments entered.
The output could then be plotted to show how the time taken changes with more agents and more iterations.
Timing of the guimodel does not make sense as it depends how quickly the user clicks on the dropdown menu (a further development would be to measure the time of individual functions and iteratioons)
The guimodel is slower because the number of iterations is multiplied in the animation function so it is advisable to keep iterations below 1000.

Typical times for the simple model are as follows (based on an average from 3 runs):
Agents 1   iterations       1 time  0.70 seconds
Agents 1   iterations      10 time  0.73 seconds
Agents 10  iterations       1 time  0.77 seconds
Agents 1   iterations     100 time  0.70 seconds
Agents 10  iterations     100 time  0.76 seconds
Agents 10  iteration     1000 time  0.93 seconds
Agents 95  iterations    1000 time 12.31 seconds
Agents 10  iteration    10000 time  2.32 seconds
Agents 10  iterations  100000 time 16.12 seconds
  
#Sources
The main structure of the code is guided by the course notes and the material shared on the collaboration thread. 
Various open source resources were consulted and in some cases snippets of code were copied and adapted for use in the model.This has been indicated by commenting in the code. 

#Contributing
Since this is simply a students practical work contributions are not expected.
If any one has ideas to solve the remaining problems identified in the guimodel.py they are welcome.

#License
There is an attached Harvard licence - see licence.txt file
