
import MalmoPython
import os
import sys
import time

import maze_gen2

DEFAULT_SIZE = 20

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
"""
        <DrawCuboid x1="-2" y1="46" z1="-2" x2="7" y2="50" z2="13" type="air" />            <!-- limits of our arena -->
        <DrawCuboid x1="-2" y1="45" z1="-2" x2="7" y2="45" z2="13" type="lava" />           <!-- lava floor -->
        <DrawCuboid x1="1"  y1="45" z1="1"  x2="3" y2="45" z2="17" type="sandstone" />      <!-- floor of the arena -->
        <DrawBlock x="4"  y="45" z="1" type="cobblestone" />    <!-- the starting marker -->
        <DrawBlock x="4"  y="45" z="7" type="lapis_block" />     <!-- the destination marker -->
"""

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
                    <Placement x="0" y="3.0" z="0" yaw="-90"/>
                    <Inventory>
                        <InventoryItem slot="0" type="diamond_pickaxe"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
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

e = maze_gen2.maze_gen((0,0), DEFAULT_SIZE, DEFAULT_SIZE)
def make_edge(edge):
    edgediff = (edge[1][0] - edge[0][0], edge[1][1] - edge[0][1])
    start = (edge[0][0]*2, edge[0][1]*2)
    mid = (start[0] + edgediff[0], start[1] + edgediff[1])
    end = (edge[1][0]*2, edge[1][1]*2)
    
    for ed in [start, mid, end]:
        my_mission.drawBlock(ed[0], 1, ed[1], "stone")
for i in e:
    make_edge(i)
    

# Attempt to start a mission:
max_retries = 3
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

# Loop until mission ends:
while world_state.is_mission_running:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission ended"
# Mission has ended.
