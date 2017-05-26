---
layout: default
title: Status
---
## Project Summary
We are creating an agent that learns to solve mazes.

## Approach
Our main algorithm is the Sarsa algorithm, which is described in Figure 6.9 on p. 146 of the book. The MDP is simple; it's basically a gridworld. Every state is a position on the grid of the maze and there are 4 possible actions from each state allowing it to move one block north, west, east, or south. In other words, the states are in the form "(int, int)" and the actions are in the form "move____ 1." (Actually, the states are (int+0.5, int+0.5), but that's just a techical detail). 

We maintain a table of Q values for each visited state (adding new states to the table as we discover them) and use the sarsa algorithm to update the Q values at every time step:

Q(s,a) = Q(s,a) + alpha*(r + gamma*Q(s', a') - Q(s, a))

s' and a' are the state arrived at by taking action a from s, and a' is the action chosen from state s' (using an epsilon greedy policy. More on that later). alpha is the learning rate (currently set to 0.8 in the code) and gamma is the discount factor (currently set to 0.9 in the code). An important "heuristic" we added for the agent was to not only discount states by the number of timesteps (which is what gamma does) but by the distance from the start state. We divide the reward obtained from a state s by the manhattan distance of s from the start state. This encourages the agent to move away from the start state, and since the goal is the furthest block away from the start in the mazes we generate, implicitly encourages the agent to "find" the goal. This is why in the video, it looks like the agent is getting "closer" to the goal as episodes go on.



## Video of Full Run
<iframe width="854" height="480" src="https://www.youtube.com/embed/fx8xDqEMQd0" frameborder="0" allowfullscreen></iframe>

(Video is only of run due to time constraint).

Layout of specific maze in the video.

<img src="http://i.imgur.com/ZlDZljQ.png">

Mazes are randomly generated for each run using the Prim-Dijkstra algorithm.
