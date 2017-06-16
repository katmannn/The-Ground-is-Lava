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

Our new addition to the agent is adding "eligibility traces" to the algorithm, thus turning it from plain Sarsa into what is called "Sarsa(lambda)." In addition to the Q table, we maintain an "E table" that is updated for every visited state after every action, where we increment the E table entry for a state any time we visit it, and is otherwise updated according to the following equation:

E(s,a)= gamma*lambda*E(s,a)

where gamma is the same discount factor described before and lambda is a parameter (between 0 and 1) controlling how much credit we would like to give to states far back in the past. The E table entry for s measures "how far away" a given previously visited state is from a current state s'. With this, we can take the reward for s' and not only update Q table for the previous state, but every visited state s up to that point with the following equation:

Q(s,a) = Q(s,a) + alpha*(r + gamma*Q(s',a') - Q(s, a))*E(s,a)

which is the same update equation for plain Sarsa except that the error is multiplied by the eligibility trace for s. Thanks to the manner in which eligibility traces are updated, we change the Q value for s by an amount inversely proportional to "how far back in the past" it is (which is what our E table measures). In other words, we "attribute" the reward gained at the current state to s based on how far back in the past it was. A state is "more eligible" for the reward gained at the current state if it was more closely related to it. (Note: The eligibility trace is higher not only if the state was more recently visited, but more frequently visited. Our agent does not repeat states that often--though sometimes it does--so we are more focused on the "time"-based factor of it).

This is implemented in the file "sarsalambda1.py" All in all, this required only a few additional lines of code to the original Sarsa algorithm (In fact, we could have consolidated plain Sarsa and Sarsa(lambda) into one file). However, it made a huge difference in the agent's performance as discussed in the Evaluation section.
 
## Evaluation


## References
