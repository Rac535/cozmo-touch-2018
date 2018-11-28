#!/usr/bin/env python3
'''
TODO : Add lots of comments here for Dr. Miller to enjoy.
TODO : Possibly place this code inside the main program and allow user to select which mode to play: auto or manual.
Team Name
Our Names
Dates
Project
Class
Python build used
SDK info / other info

Explanation of the program
'''
import cozmo
from cozmo.util import degrees, distance_inches, speed_mmps

########## Speech & Animation Functions ##########
def victoryDance(robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
    robot.turn_in_place(degrees(180)).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()

def resetNarration(robot):
    robot.say_text("Please place cozmo in the starting location.", use_cozmo_voice=False,
                   duration_scalar=0.6).wait_for_completed()
    robot.say_text("Tap any cube when ready to continue.", use_cozmo_voice=False,
                   duration_scalar=0.6).wait_for_completed()

########## Utility Functions ##########
def driveInches(robot, inches):
    robot.drive_straight(distance_inches(inches), speed_mmps(80)).wait_for_completed()

def turnDegrees(robot, nDegrees):
    robot.turn_in_place(degrees(nDegrees)).wait_for_completed()

def turnRight(robot):
    turnDegrees(robot, -90)

def turnLeft(robot):
    turnDegrees(robot, 90)

########## Routing Functions ##########

# getInput() waits for the user to tap a cube, and returns the cube id
# 1 = left, 2 = right, 3 = reset the game
def getInput(robot):
    #  wait for cube press to continue - possibly add a timeout?
    cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped)
    print("Cube ", end="")
    print(cube.obj.object_id, end="")
    print(" tap detected.\n", end="")

    if cube.obj.object_id == 1:
        return 1
    elif cube.obj.object_id == 2:
        return 2
    elif cube.obj.object_id == 3:
        return 3

def choiceLeft(robot):
    turnLeft(robot)
    driveInches(robot, 5.5)
    input = getInput(robot)
    if input == 1:
        choiceLeftLeft(robot)
    elif input == 2:
        choiceLeftRight(robot)
    elif input == 3:
        resetNarration(robot)
        cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped)

def choiceRight(robot):
    turnRight(robot)
    driveInches(robot, 11)
    input = getInput(robot)
    if input == 1:
        choiceRightLeft(robot)
    elif input == 2:
        choiceRightRight(robot)
    elif input == 3:
        resetNarration(robot)
        cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped)

def choiceRightLeft(robot):
    turnLeft(robot)
    driveInches(robot, 10.75)
    turnLeft(robot)
    driveInches(robot, 6)
    turnRight(robot)
    driveInches(robot, 5.25)
    # exit reached

def choiceRightRight(robot):
    turnRight(robot)
    driveInches(robot, 6.6)
    turnRight(robot)
    driveInches(robot, 6.25)
    robot.turn_in_place(degrees(180)).wait_for_completed()
    driveInches(robot, 6.75)
    turnLeft(robot)
    driveInches(robot, 17)
    turnLeft(robot)
    driveInches(robot, 7)
    turnRight(robot)
    driveInches(robot, 5)
    # exit reached

def choiceLeftLeft(robot):
    turnLeft(robot)
    driveInches(robot, 6)
    robot.turn_in_place(degrees(180)).wait_for_completed()
    driveInches(robot, 16.25)
    turnRight(robot)
    driveInches(robot, 6)
    turnRight(robot)
    driveInches(robot, 6.25)
    turnLeft(robot)
    driveInches(robot, 6.75)
    turnLeft(robot)
    driveInches(robot, 3)
    driveInches(robot, 6)
    # exit reached

def choiceLeftRight(robot):
    turnRight(robot)
    driveInches(robot, 11)
    turnRight(robot)
    driveInches(robot, 6)
    turnRight(robot)
    driveInches(robot, 6.25)
    turnLeft(robot)
    driveInches(robot, 6.75)
    turnLeft(robot)
    driveInches(robot, 3)
    driveInches(robot, 7)
    # exit reached

########## Main ##########
def main(robot: cozmo.robot.Robot):
    #  TODO: Add music and additional narration, unless moving this code to the main program.
    driveInches(robot, 6.5)
    robot.say_text("Which way!").wait_for_completed()

    input = getInput(robot)
    if input == 1:
        choiceLeft(robot)
    elif input == 2:
        choiceRight(robot)
    elif input == 3:
        resetNarration(robot)
        cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped)
        #TODO: have this loop back to start of program
        return

    resetNarration(robot)
    cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped)



########## Run Program ##########
cozmo.run_program(main)
