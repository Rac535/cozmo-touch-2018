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

    '''
    print("Cube ", end="")
    #print(cube.obj.object_id, end="")
    print(cube.obj, end="")
    print(" tap detected.\n", end="")
    '''

    return cube.obj.object_id


def cozmo_program(robot: cozmo.robot.Robot):
    # TODO: use these values
    cube1 = robot.world.get_light_cube(LightCube1Id)  # looks like a paperclip
    cube2 = robot.world.get_light_cube(LightCube2Id)  # looks like a lamp / heart
    cube3 = robot.world.get_light_cube(LightCube3Id)  # looks like the letters 'ab' over 'T'

    if cube1 is not None:
        cube1.set_lights(cozmo.lights.red_light)
        print("cube1 (red, paperclip) LightCube1Id is ", end="")
        print(LightCube1Id)
        print("cube1.object_id is ", end="")
        print(cube1.object_id)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube1Id cube - check the battery.")

    if cube2 is not None:
        cube2.set_lights(cozmo.lights.green_light)
        print("cube2 (green, heart) LightCube2Id is ", end="")
        print(LightCube2Id)
        print("cube2.object_id is ", end="")
        print(cube2.object_id)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube2Id cube - check the battery.")
        print("Couldn't find cube2")

    if cube3 is not None:
        cube3.set_lights(cozmo.lights.blue_light)
        print("cube3 (blue, fraction) LightCube3Id is ", end="")
        print(LightCube3Id)
        print("cube3.object_id is ", end="")
        print(cube3.object_id)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube3Id cube - check the battery.")

    # Keep the lights on for 10 seconds until the program exits
    time.sleep(3)

    for x in range (1, 6):
        input = getInput(robot)
        if input == cube1.object_id:
            print("Cube 1 pressed.")
        elif input == cube2.object_id:
            print("Cube 2 pressed.")
        elif input == cube3.object_id:
            print("Cube 3 pressed.")




cozmo.run_program(cozmo_program)