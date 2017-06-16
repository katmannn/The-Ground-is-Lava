---
layout: default
title:  Final Report
---

## Video


## Project Summary


## Approaches
We will provide here a brief recap of what was discussed in the "Approach" section of our status report, and then discuss our new addition.

The MDP our agent learns is a gridworld where the agent only knows its current position (represented as a tuple) and can take actions that allow it to move a single block north, east, south, or west. Our base algorithm is the "Sarsa" algorithm (which we will henceforth call "plain Sarsa" to distinguish it from the "Sarsa(lambda)" algorithm discussed later), which--for every new state visited--provides the following update rule for the Q table:

Q(s,a) = Q(s,a) + alpha(r + gammaQ(s’, a’) - Q(s, a))

where s’ is the state arrived at by taking action a from s, and a’ is the action chosen from state s’ according to an epsilon greedy policy. As usual, r denotes the reward, alpha functions as learning rate, and gamma functions as the discount factor. Our epsilon-greedy policy randomly chooses an action from state s with probability 1/N(s) where N(s) is the number of times we've visited state s, and greedily chooses an action otherwise. We also discussed the crucial "Manhattan distance" heuristic we endowed the agent with, in which we discount states by their distance from the start state, in order to encourage the agent to move in the direction of the goal.

Everything described thus far is implemented in the file "sarsa1.py", with few changes since the status report.

The mazes are generated using a randomized Prim-Jarnik minimum spanning tree algorithm, as described here: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim.27s_algorithm. This is implemented in maze_gen2.py (and subsequently called in the malmo files).




## Evaluation


## References
