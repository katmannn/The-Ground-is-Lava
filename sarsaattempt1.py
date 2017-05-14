
import MalmoPython
import os
import sys
import time
import json
import random

import maze_gen2
from collections import defaultdict

DEFAULT_SIZE = 3

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
            <ServerSection>
              <ServerInitialConditions>
                <Time>
                    <StartTime>12000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
              </ServerInitialConditions>
              <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;2*11;8;"/>
                  <ServerQuitFromTimeUp timeLimitMs="30000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="0.5" y="5.0" z="0.5" yaw="-90"/>
                    <Inventory>
                        <InventoryItem slot="0" type="diamond_pickaxe"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                  <DiscreteMovementCommands/>
                  <ObservationFromFullStats/>
                  <RewardForTouchingBlockType>
                    <Block reward="1000000000.0" type="lapis_block" behaviour="onceOnly"/>
                    <Block reward="-100.0" type="lava" behaviour="onceOnly"/>
                  </RewardForTouchingBlockType>
                  <RewardForSendingCommand reward="-1"/>
                  <AgentQuitFromTouchingBlockType>
                      <Block type="lapis_block" />
                      <Block type="lava" />
                  </AgentQuitFromTouchingBlockType>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

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


my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()
my_mission.forceWorldReset()

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

actions = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]
def init_q_state(q_table, state, actions=actions):
    for a in actions:
        q_table[state][a] = 0

q_table = defaultdict(dict)
init_q_state(q_table, (0,0))
q_table[(0,0)]["movesouth 1"] = 9
q_table[(0,0)]["moveeast 1"] = 9

num_visited = defaultdict(int)

def eps_greedy(actions, epsilon=0.1):
    r = random.random()
    if r < epsilon:
        r = random.randint(0, 3)
        return actions[r][0]
    else:
        return max(actions, key=lambda x: x[1])[0]

def update_q_table(q_table, s, a, r, snew, anew, alpha=0.1, gamma=0.95):
    q_table[s][a] += alpha*(r + gamma*q_table[snew][anew] - q_table[s][a])

# Attempt to start a mission:
num_repeats = 1000
for i in range(num_repeats):
    print
    print("Repeat %d of %d" % (i+1, num_repeats))

    my_mission_record = MalmoPython.MissionRecordSpec()

    max_retries = 1000
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_mission_record )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print "Error starting mission:",e
                exit(1)
            else:
                time.sleep(2)

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

    s = (0,0)
    num_visited[s] += 1
    a = eps_greedy(q_table[s].items(), 1/num_visited[s])
    #for ok in q_table.items():
        #print str(ok[0]) + ":", ok[1]

    # Loop until mission ends:
    time.sleep(0.5)
    num_steps = 0
    world_state = agent_host.getWorldState()
    while world_state.is_mission_running:
        sys.stdout.write(".")
        time.sleep(0.1)
        
        for error in world_state.errors:
            print "Error:",error.text

        time.sleep(0.5)
        agent_host.sendCommand(a)
        num_steps += 1

        obs_text = []
        breakloop = False
        count = 0
        while len(obs_text) == 0:
            world_state = agent_host.getWorldState()
            try:
                obs_text = world_state.observations[-1].text
            except:
                pass
            if len(obs_text) == 0 and world_state.is_mission_running == False:
                breakloop = True
                break
        if breakloop:
            break

        r = 0

        for reward in world_state.rewards:
            r += reward.getValue()

        obs = json.loads(obs_text)
        snew = (obs["XPos"], obs["ZPos"])
        if snew not in q_table:
            init_q_state(q_table, snew)
        
        dist = (abs(snew[0] - 0), abs(snew[1] - 0))
        dist = dist[0] + dist[1]
        r = r/(dist**2)
        
        num_visited[snew] += 1
        anew = eps_greedy(q_table[snew].items(), 1/num_visited[snew])
        update_q_table(q_table, s, a, r, snew, anew) #sarsa
        s = snew
        a = anew
        

    time.sleep(0.5)
    #if 
    print
    print "Mission ended"
# Mission has ended.
