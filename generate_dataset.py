import MalmoPython
import itertools
import sys
import os
import time
import random
from object_constructors import *
from PIL import Image

def get_settings():
	which_object = ""
	while which_object != 'tree' and which_object != 'house' and which_object != 'art' and which_object != 'mansion':
		print()
		print("Set the correct object in the experimental world.")
		print("-------------------------------------------------")
		which_object = input("Which object do you wish to take images of? Choose from: 'tree', 'house', 'mansion', or 'art'  ")

	x_dimension = 0
	while not x_dimension:
		print()
		print("Set the X pixelsize")
		print("-------------------------------------------------")
		x_dimension = int(input("What is the pixelsize of your image in the X axis?  "))

	y_dimension = 0
	while not y_dimension:
		print()
		print("Set the Y pixelsize")
		print("-------------------------------------------------")
		y_dimension = int(input("What is the pixelsize of your image in the Y axis?  "))

	return which_object, x_dimension, y_dimension

def add_object(which_object, x = 0, z = 0):
	if which_object == "tree":
		return gen_tree(x,z)

	elif which_object == "house":
		return gen_house(x,z, True)

	elif which_object == 'mansion':
		return gen_house(x,z, False)

	elif which_object == "art":	
		return gen_art_sphere(x,z)

	elif which_object == "nothing":
		return gen_sapling(x,z)

def generate_positions(d1,d2,d3):
	coordinates = [
	(0,d1,180),
	(0,d2,180),
	(0,d3,180),
	(0,d4,180),
	(-d1,d1,-130),
	(-d2,d2,-130),
	(-d3,d3,-130),
	(-d4,d4,-130),
	(-d1,0,-85),
	(-d2,0,-85),
	(-d3,0,-85),
	(-d4,0,-85),
	(-d1,-d1,-45),
	(-d2,-d2,-45),
	(-d3,-d3,-45),
	(-d4,-d4,-45),
	(0,-d1,-5),
	(0,-d2,-5),
	(0,-d3,-5),
	(0,-d4,-5),
	(d1,-d1,40),
	(d2,-d2,40),
	(d3,-d3,40),
	(d3,-d3,40),
	(d1,0,85),
	(d2,0,85),
	(d3,0,85),
	(d4,0,85),
	(d1,d1,135),
	(d2,d2,135),
	(d3,d3,135),
	(d4,d4,135),
	]

	print("Created " + str(len(coordinates)) + " vantage points.")
	return coordinates

def generate_focus_points():
	focus_points = []
	yaws = [-30,0,30]
	pitches = [10,0,-25]
	for i in yaws:
		for j in pitches:
			focus_points.append((i,j))
	return focus_points

objects = ['tree','house','mansion','art','nothing']
for i in objects:
	which_object = i
#which_object,x_dimension,y_dimension = get_settings()
#Settings:
#which_object = 'art'
	x_dimension = 640
	y_dimension = 480
	d1 = 6
	d2 = 9
	d3 = 12
	d4 = 2

	mission_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
			<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">        
					
				<About>
					<Summary>Costa del Sol</Summary>
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
						<!-- removed ';decoration' at the end of the generatorstring below -->
						<FlatWorldGenerator generatorString="3;7,2*3,2;1"/>
					
						<DrawingDecorator>

							''' + add_object(which_object) + '''
						</DrawingDecorator>   

					</ServerHandlers>
				</ServerSection>
										
				<AgentSection mode="Survival">
						
					<Name>Steve</Name>
										
					<AgentStart>
					
						<Placement x="-5" y="4" z="0" yaw="0"/>
					
					</AgentStart>
					
					<AgentHandlers>

						<MissionQuitCommands/>
						
						<ObservationFromFullStats/>
						
						<AbsoluteMovementCommands />
					
					</AgentHandlers>
					
				</AgentSection>
								
			</Mission>
			'''

	#This sets up the API objects.
	agent_host = MalmoPython.AgentHost()
	try:
		agent_host.parse( sys.argv )
	except RuntimeError as e:
		print('ERROR:',e)
		print(agent_host.getUsage())
		exit(1)
	if agent_host.receivedArgument("help"):
		print(agent_host.getUsage())
		exit(0)

	#Build a mission and give it the configuration of the world. Note that we can change that later with Python code.
	my_mission = MalmoPython.MissionSpec(mission_XML, True)
	my_mission_record = MalmoPython.MissionRecordSpec()

	agent_host.setVideoPolicy(MalmoPython.VideoPolicy.LATEST_FRAME_ONLY)
	my_mission.requestVideo(x_dimension,y_dimension)
	my_mission.forceWorldReset()

	# Attempt to start a mission:
	max_retries = 3
	for retry in range(max_retries):
	    try:
	        agent_host.startMission( my_mission, my_mission_record )
	        break
	    except RuntimeError as e:
	        if retry == max_retries - 1:
	            print("Error starting mission:",e)
	            exit(1)
	        else:
	            time.sleep(2)

	# Loop until mission starts:
	print("Waiting for the mission to start ",)
	world_state = agent_host.getWorldState()
	while not world_state.has_mission_begun:
	    sys.stdout.write(".")
	    time.sleep(0.1)
	    world_state = agent_host.getWorldState()
	    for error in world_state.errors:
	        print("Error:",error.text)

	positions = generate_positions(4,8,10)
	focus_points = generate_focus_points()
	print(focus_points)
	time.sleep(5)

	shot = 230
	for pos in positions:

		x,z,yaw = pos
		agent_host.sendCommand('tp {0} 4 {1}'.format(x,z))
		agent_host.sendCommand('setYaw {0}'.format(yaw))
		#agent should now face the tree.

		for focus in focus_points:
			yaw2, pitch = focus 
			agent_host.sendCommand('setYaw {0}'.format(yaw+yaw2))
			agent_host.sendCommand('setPitch {0}'.format(pitch))
			
			world_state = agent_host.peekWorldState()
			while world_state.is_mission_running and all (e.text=='{}' for e in world_state.observations):
				world_state = agent_host.peekWorldState()
			
			assert len(world_state.video_frames) > 0, 'No video frames!? We just checked for them.'
			frame = world_state.video_frames[-1]
			image = Image.frombytes('RGB', (frame.width, frame.height), bytes(frame.pixels) )		
			
			#The below line saves the images to the given path.
			image.save("Snapshots/{0}s/{0}{1}.jpg".format(which_object,shot))
			shot += 1

	print("Done!")
	agent_host.sendCommand("quit 1")

	# Loop until mission ends:
	while world_state.is_mission_running:
	    sys.stdout.write(".")
	    time.sleep(0.1)
	    world_state = agent_host.getWorldState()
	    for error in world_state.errors:
	        print("Error:",error.text)

	print()
	print("Mission ended")
	# Mission has ended.
