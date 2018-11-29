import random  # to roll for random pathing, animations, and speech options
import cozmo
import sys
import time
import asyncio  # to catch timeout errors
from cozmo.util import degrees, distance_inches, speed_mmps
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id

cube1 = 0
cube2 = 0
cube3 = 0

def getInput(robot):
    global cube1
    global cube2
    global cube3
    # This try/except will wait 15 seconds for a cube tap before reminding the user that it's waiting.
    # After one minute of inactivity, the game will shut down.
    x = 0
    while 1:
        try:
            cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped, timeout=15)
            break
        except asyncio.TimeoutError:
            x+=1
            print("No selection made.")
            if x == 4:
                print("Input timeout detected. Shutting down.")
                return 3
            robot.say_text("Please make a selection."
                           , use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

    print("Cube ", end="")
    print(cube.obj.object_id, end="")
    print(" tap detected.\n", end="")

    if cube.obj.object_id == 1:
        return 1
    elif cube.obj.object_id == 2:
        return 2
    elif cube.obj.object_id == 3:
        return 3


def cozmo_program(robot: cozmo.robot.Robot):
    global cube1
    global cube2
    global cube3
    cube1 = robot.world.get_light_cube(LightCube1Id)  # looks like a paperclip
    cube2 = robot.world.get_light_cube(LightCube2Id)  # looks like a lamp / heart
    cube3 = robot.world.get_light_cube(LightCube3Id)  # looks like the letters 'ab' over 'T'

    if cube1 is not None:
        cube1.set_lights(cozmo.lights.red_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube1Id cube - check the battery.")

    if cube2 is not None:
        cube2.set_lights(cozmo.lights.green_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube2Id cube - check the battery.")
        print("Couldn't find cube2")
    if cube3 is not None:
        cube3.set_lights(cozmo.lights.blue_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube3Id cube - check the battery.")

    # Keep the lights on for 10 seconds until the program exits
    time.sleep(3)

    print(LightCube1Id)
    print(LightCube2Id)
    print(LightCube3Id)
    input = getInput(robot)
    print(input)
    input = getInput(robot)
    print(input)
    input = getInput(robot)
    print(input)
    input = getInput(robot)
    print(input)
    input = getInput(robot)
    print(input)

    getInput




cozmo.run_program(cozmo_program)