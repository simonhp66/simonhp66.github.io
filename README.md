# onlineportfolio
This is a portfolio of work from the Geog5003M practical sessions.

The practical involves building an agent based model which interacts with its environment and where agents interact with each other. The model developed follows the structure guided by the instructions except with respect to the following enhancements.

Agent naming and power: Agents are given unique names so they can be more easily identified and each agent is given a "power" ranging from 1 (most powerful)to 6 (least powerful). The agent names and powers have been loaded from an excel file and are based on the names of English football teams and their respective divisions. 

Agent moving: The standard method of moving agents involves each agent moving both co-ordinates in an iteration. This means that an agent always moves in a diagonal fashion (rather like the bishop in a chess game). This also means that there are certain cells in the environment that an agent can never reach. If you think of the environment as like a chessboard all agents can play on either white squares or black ones but cannot change colours. With a small number of agents and heavy "grazing" of the environment this leads to a distinctive criss/cross pattern as either the white or black cells are repeatedly eaten. This is less apparent with a large number of agents as about half will be on each "colour".
The method of moving was therefore modified so that on each iteration an agent can move to any of the surrounding 8 cells or remain in the same place. 
In addition agents with more than 1000 score were given the ability to move two squares in any direction. 

Agent sharing: This is where the power attribute is used. Agents meeting other agents that are less powerful than themselves "steal" 100 units from the less powerful agent. If two agents meet of the same power then they share their units equally as described in the instructions. 

Output: The output is an ordered "league table" of agents based on their score. Due to the method of sharing the most powerful tend to end closer to the top of the league table.

Installation
Include instructions here about how to run it

Usage
Examples of how it works

Contributing
Since this is simply a students practical work contributions are not permitted.

License
To be determined
