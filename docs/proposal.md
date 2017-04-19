---
layout: default
title: Proposal
---

## Summary
We want to create an agent that can solve arbitrary mazes in reasonable time. These mazes can range from simple mazes (like the ones solved by Dijkstra's algorithm in Assignment #1) to more complicated, subgoal-oriented mazes (like in tutorial_8.py). The agent's percepts will be a limited list of blocks in the area to the front of it (meant to roughly match what the player would see from that perspective). 

## Algorithms
We expect to use some form of model-free reinforcement learning (temporal difference, Monte Carlo, or a mix)

## Evaluation
We can select a number of mazes and time how long it takes for a human (us) to solve, how long it takes a random agent to solve (i.e., an agent whose policy involves choosing an action from any given state uniformly at random), how long it takes a non-AI algorithm to solve (e.g. Dijkstra's algorithm) and compare them to how long it takes our agent to solve. For larger and more complicated mazes, like those in tutorial_8.py, alot of these methods are computationally infeasible, so having the agent solve them at all would be a win.

Sanity case: The type of mazes found in tutorial_7.py and assignment1.py. These mazes are simple and small enough that they can even be solved using a dynamic programming approach instead of model-free methods.

Moonshot case: The type of mazes found in tutorial_8.py are fairly complicated, especially given the time limit (Even I'm not really able to finish them very well. So if an agent can do it, that would be an accomplishment). 

## Appointment
Tuesday, April 25, 11:15 AM. 
