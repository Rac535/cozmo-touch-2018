#!/usr/bin/env python3
'''
This is a WiP. Goal is to get Cozmo to turn a direction based on what cube is tapped.
Right now, he just continues the correct route when any cube is tapped. See comments in main().
'''
import cozmo
from cozmo.util import degrees, distance_inches, speed_mmps

########## Speech & Animation Functions ##########
def victoryDance(robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
    robot.turn_in_place(degrees(180)).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
    robot.say_text("Yay for computer science!").wait_for_completed()

########## Utility Functions ##########
def driveInches(robot, inches):
    robot.drive_straight(distance_inches(inches), speed_mmps(80)).wait_for_completed()

def turnDegrees(robot, nDegrees):
    robot.turn_in_place(degrees(nDegrees)).wait_for_completed()

def turnRight(robot):
    turnDegrees(robot, -90)

def turnLeft(robot):
    turnDegrees(robot, 90)

########## Main ##########
def main(robot: cozmo.robot.Robot):
    driveInches(robot, 9)
    robot.say_text("Which way!").wait_for_completed()
    cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped) # Tapping any cube will send him the correct way for now

    num = cube.obj # this doesn't work to grab the cube number. I'm probably missing some basic OOP skills here

    '''
    # TODO
    # Figure out which cube was tapped and give the next command accordingly
    # API states: wait_for() function returns the instance of the event's "EvtObjectTapped" class,
    # which includes a "obj" attribute, which identifies which cube has been tapped.
    # I'm not sure how to grab that returned information. If I could, I would do something like this:

    if <wait_for() function's returned obj value> == <the value representing cube # 1>:
        turnLeft(robot)
    elif <wait_for() function's returned obj value> == <the value representing cube # 2>:
        driveInches(robot, 5)
    elif <wait_for() function's returned obj value> == <the value representing cube # 3>:
        turnRight(robot)
    else:
        robot.say_text("Couldn't detect cube tap").wait_for_completed()
    
    # But note that I would disallow making a turn that would take the robot backwards or into a wall.
    # At the first "T" in the maze, I would allow only right or straight. If they go straight into the dead end,
    # I would code the robot to drive to the dead end, turn around, make the correct turn, head to the
    # next "T", and give the option to pick left or right. Really gotta limit choices for these pre-K kids,
    # plus it makes the programming easier. At each turn, I would 
    # loop over robot.world.wait_for(cozmo.objects.EvtObjectTapped) until an acceptable cube is tapped.
    '''

    turnRight(robot)
    driveInches(robot, 9.95)  # First "T" to Second "T"
    robot.say_text("Now where do I go!").wait_for_completed()
    cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped) # Tapping any cube will send him the correct way for now
    turnLeft(robot)
    driveInches(robot, 10)  # Second "T" to Finish Line

########## Run Program ##########
cozmo.run_program(main)
