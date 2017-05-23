
import MalmoPython
import os
import sys
import time
import json
import random
import math

import maze_gen2
from collections import defaultdict

DEFAULT_SIZE = 3

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

#missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
#            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
#            
#              <About>
#                <Summary>Hello world!</Summary>
#              </About>
#              
#            <ServerSection>
#              <ServerInitialConditions>
#                <Time>
#                    <StartTime>12000</StartTime>
#                    <AllowPassageOfTime>false</AllowPassageOfTime>
#                </Time>
#                <Weather>clear</Weather>
#              </ServerInitialConditions>
#              <ServerHandlers>
#                  <FlatWorldGenerator generatorString="3;2*11;8;"/>
#                  <ServerQuitFromTimeUp timeLimitMs="30000"/>
#                  <ServerQuitWhenAnyAgentFinishes/>
#                </ServerHandlers>
#              </ServerSection>
#              
#              <AgentSection mode="Survival">
#                <Name>MalmoTutorialBot</Name>
#                <AgentStart>
#                    <Placement x="0.5" y="5.0" z="0.5" yaw="-90"/>
#                    <Inventory>
#                        <InventoryItem slot="0" type="diamond_pickaxe"/>
#                    </Inventory>
#                </AgentStart>
#                <AgentHandlers>
#                  <DiscreteMovementCommands/>
#                  <ObservationFromFullStats/>
#                  <ObservationFromGrid>
#                    <Grid name="floor3x3">
#                        <min x="-1" y="-1" z="-1"/>
#                        <max x="1" y="-1" z="1"/>
#                    </Grid>
#                  </ObservationFromGrid>
#                  <RewardForTouchingBlockType>
#                    <Block reward="1000000000.0" type="lapis_block" behaviour="onceOnly"/>
#                    <Block reward="-100.0" type="lava" behaviour="onceOnly"/>
#                  </RewardForTouchingBlockType>
#                  <RewardForSendingCommand reward="-1"/>
#                  <AgentQuitFromTouchingBlockType>
#                      <Block type="lapis_block" />
#                      <Block type="lava" />
#                  </AgentQuitFromTouchingBlockType>
#                </AgentHandlers>
#              </AgentSection>
#            </Mission>'''

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

#loading mission file
mission_file = "sarsaattempt1.xml"
with open(mission_file, 'r') as f:
    print "Loading mission from %s" % mission_file
    missionXML = f.read()
    my_mission = MalmoPython.MissionSpec(missionXML, True)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

#################
#MAZE GENERATION#
#################
size = (DEFAULT_SIZE, DEFAULT_SIZE)
if len(sys.argv) == 1:
    pass
elif len(sys.argv) == 2:
    size = ( int(sys.argv[1]), int(sys.argv[1]) )
elif len(sys.argv) == 3:
    size = ( int(sys.argv[1]), int(sys.argv[2]) )
else:
    print "Usage:", sys.argv[0], "[rowsize [colsize]]"

e = maze_gen2.maze_gen((0,0), size[0], size[1])
def make_edge(edge):
    edgediff = (edge[1][0] - edge[0][0], edge[1][1] - edge[0][1])
    start = (edge[0][0]*2, edge[0][1]*2)
    mid = (start[0] + edgediff[0], start[1] + edgediff[1])
    end = (edge[1][0]*2, edge[1][1]*2)
    
    for ed in [start, mid, end]:
        my_mission.drawBlock(ed[0], 1, ed[1], "stone")
        my_mission.drawBlock(ed[0], 2, ed[1], "stone")
        my_mission.drawBlock(ed[0], 3, ed[1], "stone")
for i in e:
    make_edge(i)

final_coords = ( (size[0]-1)*2, (size[1]-1)*2 )
my_mission.drawBlock(final_coords[0], 3, final_coords[1], "lapis_block")
###############
###############

#We want to reset the world everytime we run this program (so we don't
#use a previously created maze) but for every episode within a run
#of the program we don't want to reset the world (because it takes too
#long). Malmo has no way to set the forceReset flag off as far as I'm
#aware of, so we create a separate mission object that has the same
#parameters (the maze in particular) as the current mission object and
#leave the forceReset flag unset for the new one. We run my_mission
#on the first episode to reset the world ("erasing" any mazes from previou
#programs and run my_mission2 thereafter so we don't reset the world from 
#then on
my_mission2 = MalmoPython.MissionSpec(my_mission.getAsXML(False), True)
my_mission_record2 = MalmoPython.MissionRecordSpec()
my_mission.forceWorldReset()

#Our agent shold be able to move in 4 directions
actions = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]

#This takes a state and initializes it in the Q table (setting the values
#to all be equal to 0 initially)
def init_q_state(q_table, state, actions=actions):
    for a in actions:
        q_table[state][a] = 0

#Create a Q table and initialize the start state
q_table = defaultdict(dict)
init_q_state(q_table, (0.5,0.5))

#Create a separate dict to keep track of the number of times we've
#visited each state
num_visited = defaultdict(int)

#Given a list of action-value pairs, choose an action with an
#epsilon-greedy policy
def eps_greedy(actions, epsilon=0.1):
    r = random.random()
    if r < epsilon:
        r = random.randint(0, 3)
        return actions[r][0]
    else:
        return max(actions, key=lambda x: x[1])[0]

#Updating a Q table w/ the sarsa update
def update_q_table(q_table, s, a, r, snew, anew, alpha=0.3, gamma=0.9):
    q_table[s][a] += alpha*(r + gamma*q_table[snew][anew] - q_table[s][a])

def get_state_from_world(world_state):
    try:
        obs = json.loads(world_state.observations[-1].text)
    except:
        return (None, None)
    xpos = obs["XPos"]
    zpos = obs["ZPos"]
    return (xpos, zpos)

# Attempt to start a mission:
num_repeats = 10000 #(number of episodes)
for i in range(num_repeats):
    print
    print("Repeat %d of %d" % (i+1, num_repeats))

    my_mission_record = MalmoPython.MissionRecordSpec()

    #Attempt to start the mission
    max_retries = 20
    for retry in range(max_retries):
        try:
            if i == 0:
                agent_host.startMission( my_mission, my_mission_record )
            else:
                agent_host.startMission( my_mission2, my_mission_record2 )
            break
        except RuntimeError as e:
            print "Error starting mission:",e

    # Loop until mission starts:
    print "Waiting for the mission to start ",
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        sys.stdout.write(".")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print "Error:",error.text

    print
    print "Mission running ",



    #print start state's q table at the beginning of each episode
    #for debugging purposes

    # Loop until mission ends:
    time.sleep(0.5)
    num_steps = 0

    world_state = agent_host.getWorldState()
    xpos, zpos = get_state_from_world(world_state)
    
    s = (xpos,zpos)
    num_visited[s] += 1 #We have visited this state once

    #choose action from start state with epsilon greedy policy w/
    #epsilon = 1/number of times this state has been visited
    if s not in q_table:
        init_q_state(q_table, s)
    a = eps_greedy(q_table[s].items(), 1/(math.log(num_visited[s]+2)))

    print(q_table[s])

    while world_state.is_mission_running:
        sys.stdout.write(".")
        time.sleep(0.1)
        
        for error in world_state.errors:
            print "Error:",error.text

        #Take an action
        agent_host.sendCommand(a)
        num_steps += 1
        
        breakloop = False

        while True:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
            newxpos, newzpos = get_state_from_world(world_state)
            if newxpos == None or newzpos == None:
                breakloop = True
                break
            if newxpos != xpos or newzpos != zpos:
                xpos = newxpos
                zpos = newzpos
                break
            print "Stuck"

        r = 0
        if len(world_state.rewards) > 0:
            r += world_state.rewards[-1].getValue()
        else:
            break
        
        snew = (xpos, zpos)

        print snew,r
        print

        #If we've never seen this state before,
        #add it to the Q table and initialize it
        if snew not in q_table:
            init_q_state(q_table, snew)
        
        #calculate "Manhattan Distance" from start state
        dist = (abs(snew[0] - 0.5), abs(snew[1] - 0.5))
        dist = dist[0] + dist[1]

        #Discount rewards by DISTANCE from the start state (unlike gamma,
        #which discounts by time)
        #So if the agent dies further away from the goal, it gets less
        #negative reward
        r = r/(dist+1)
        
        #choose new action according to epsilon greedy policy with
        #epsilon = 1/log(number of times we visited the state)
        anew = eps_greedy(q_table[snew].items(), 1/(math.log(num_visited[snew]+2)))
        update_q_table(q_table, s, a, r, snew, anew) #sarsa update to q table
        
        
        s = snew
        a = anew

        if breakloop:
            time.sleep(0.1)
            break


    time.sleep(0.5)
    #if 
    print
    print "Mission ended"
# Mission has ended.
