#!/usr/bin/env python3
import cozmo
import random
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

'''
This iteration of the TEST MAZE main function will choose a random path through the TEST MAZE before beginning
movement of Cozmo.
'''
########## Main ##########
def main(robot: cozmo.robot.Robot):
    roll = random.randint(1, 4)

    # PATH 1: Shortest path through TEST MAZE
    if roll == 1:
        driveInches(robot, 9)  # Start Line to First "T"
        turnRight(robot)
        driveInches(robot, 9.95)  # First "T" to Second "T"
        turnLeft(robot)
        driveInches(robot, 10)  # Second "T" to Finish Line

    # PATH 2: Hit Dead End 1, then proceed to end of TEST MAZE
    elif roll == 2:
        driveInches(robot, 13.95)  # Start Line to Dead End 1
        robot.say_text("Dead end!").wait_for_completed()
        robot.turn_in_place(degrees(180)).wait_for_completed()
        driveInches(robot, 5)  # Dead End 1 back to First "T"
        turnLeft(robot)
        driveInches(robot, 9.95)  # First "T" to Second "T"
        turnLeft(robot)
        driveInches(robot, 10)  # Second "T" to Finish Line

    # PATH 3: Hit both dead ends before proceeding to end of TEST MAZE
    elif roll == 3:
        driveInches(robot, 13.95)  # Start Line to Dead End 1
        robot.say_text("Dead end!").wait_for_completed()
        robot.turn_in_place(degrees(180)).wait_for_completed()
        driveInches(robot, 5)  # Dead End 1 back to First "T"
        turnLeft(robot)
        driveInches(robot, 9.95)  # First "T" to Second "T"
        turnRight(robot)
        driveInches(robot, 4.7)  # Second "T" to Dead End 2
        robot.say_text("Another dead end!").wait_for_completed()
        robot.turn_in_place(degrees(178)).wait_for_completed()
        driveInches(robot, 14.2)  # Dead End 2 to Finish Line

    # PATH 4: Right at first "T", right into Dead End 2, then proceed to end of TEST MAZE
    elif roll == 4:
        driveInches(robot, 9)  # Start Line to First "T"
        turnRight(robot)
        driveInches(robot, 9.95)  # First "T" to Second "T"
        turnRight(robot)
        driveInches(robot, 4.7)  # Second "T" to Dead End 2
        robot.say_text("Dead end!").wait_for_completed()
        robot.turn_in_place(degrees(178)).wait_for_completed()
        driveInches(robot, 14.2)  # Second "T" to Finish Line

    # TODO uncomment the victoryDance() function call below (disabled for route testing efficiency)
    victoryDance(robot)

########## Run Program ##########
cozmo.run_program(main)
