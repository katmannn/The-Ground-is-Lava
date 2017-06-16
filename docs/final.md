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

Our new addition to the agent is adding "eligibility traces" to the algorithm, thus turning it from plain Sarsa into what is called "Sarsa(lambda)." In addition to the Q table, we maintain an "E table" that is updated for every used state-action pair after every action, where we increment the E table entry for a state-action pair any time we use it, and is otherwise updated according to the following equation:

E(s,a)= gamma*lambda*E(s,a)

where gamma is the same discount factor described before and lambda is a parameter (between 0 and 1) controlling how much "credit" we would like to give to states far back in the past. The E table entry for s and a (The "eligibility trace" for s/a) measures "how far away" a given previously used state-action pair is from a current state s'. With this, we can take the reward for s' and not only update Q table for the previous state, but every visited state s up to that point with the following equation:

Q(s,a) = Q(s,a) + alpha*(r + gamma*Q(s',a') - Q(s, a))*E(s,a)

which is the same update equation for plain Sarsa except that the error is multiplied by the eligibility trace for s/a. Thanks to the manner in which eligibility traces are updated, we change the Q value for s/a by an amount inversely proportional to "how far back in the past" it is (which is what our E table measures). In other words, we "attribute" the reward gained at the current state to s based on how far back in the past it was. A state-action pair is "more eligible" for the reward gained at the current state if it was more closely related to it. Note: The eligibility trace is higher not only if the state was more recently visited, but more frequently visited. Our agent does not repeat states that often (though sometimes it does) so we are more focused on the "time"-based factor of it.

This is implemented in the file "sarsalambda1.py" All in all, this required only a few additional lines of code to the original Sarsa algorithm (In fact, we could have consolidated plain Sarsa and Sarsa(lambda) into one file). However, it made a huge difference in the agent's performance as discussed in the Evaluation section.
 
## Evaluation
In contrast to our evaluation from the status report, we have gathered additional data, and now have comparisons to make. We measure the performance of our agent based on the number of episodes it takes to converge, where we define "convergence" as reaching the goal state 3 times in a row.

The following graph says it all:

(LOL WE STILL NEED MORE DATA SO NO GRAPH YET BUT IT'S ALREADY PRETTY OBVIOUS THAT SARSA(LAMBDA) IS BETTER)

Sarsa(lambda) appears to drastically outperform plain Sarsa on our MDP. The intuitive reasoning for this, we believe, is simply that eligibility traces allow the reward for a given state to propogate backwards. Consider the following toy example:

<img src="ex1.png">

Obviously, the better decision from the start state is to move north to the goal (marked in green) than moving east to a dead-end (lava). Suppose the agent tends to move all the way east and fall into the lava (moving east from the start state, falling into (6,0) is the actually best option). In Sarsa(lambda), the negative reward obtained from doing so immediately propogates back to the state-action pair (0,0)-east, as an immediate consequence of the update rule. Hence, the agent sees that (0,0)-east (and likewise, (1,0)-east, (2,0)-east, etc.) is a bad idea quite quickly, and will prefer to try going north instead sooner. On the other hand, in plain Sarsa, only the state-action pair (5,0)-east immediately gets the negative reward. For the negative reward to propogate back to (0,0)-east the agent has to revisit (5,0)-east, which updates the value for (4,0)-east, restart, then revisit (4,0)-east, which updates the value for (3,0)-east, then revisit (3,0)-east, etc. Thus, it can take up to 5 extra episodes for (0,0)-east to be properly updated in Sarsa, while for Sarsa(lambda) it only takes 1 (Likewise, the positive reward obtained at the goal state propogates back faster in Sarsa(lambda) than it does for Sarsa). Now consider this for not just the start state, but every position in the maze, and it becomes clear why Sarsa(lambda) takes much fewer episodes to converge.

## References
