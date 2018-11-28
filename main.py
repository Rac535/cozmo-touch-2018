#!/usr/bin/env python3
'''
TODO : Fill out the hitWall() function with the reactions to each wall (probably don't need to do every single one)
       and put the appropriate textures or pictures on those walls in the physical maze.
       NOTE: Some of Cozmo's animations will cause him to shake around, and he'll end up misaligned. When he goes
             to make the nest 90 or 180 degree turn, he'll start driving into walls. Just be sure to test any
             animations you add.

TODO : Potential Idea: maybe reduce the amount of narrator's dialogue when doing multiple playthroughs. Maybe add
       an iterator in the main loop and skip some of the dialogue after 3 or so runs.

TODO : Idea: Make the cubes light up when the program expects input. This anki example i think explains it:
       https://github.com/anki/cozmo-python-sdk/blob/master/examples/tutorials/01_basics/09_cube_lights.py
       I currently do not set each cube as an individual object. I just redefine the
       cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped) each time I need input. - (Mike B.)

TODO : search this program for "TODO". I commented lots of speech and animations to speed up testing. - (Mike B)

TODO : Add lots of comments here for Dr. Miller to enjoy.

Team Name
Our Names
Dates
Project
Class
Python build used
SDK info / other info

Explanation of the program
'''

import random  # to roll for random pathing, animations, and speech options
import cozmo
import asyncio  # to catch timeout errors
from cozmo.util import degrees, distance_inches, speed_mmps


########## Speech & Animation Functions ##########
def victoryDance(robot):
    robot.play_audio(cozmo.audio.AudioEvents.MusicStyle80S1159BpmLoop)

    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
    robot.turn_in_place(degrees(170)).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()

    robot.play_audio(cozmo.audio.AudioEvents.MusicStyle80S1159BpmLoopStop)

def victorySpeech(robot):
    robot.say_text("Cozmo finally made it out of the museum",
                   use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    robot.say_text("Cozmo learned that day that if you can't see",
                   use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    robot.say_text("you might be able to feel your way out of a situation",
                   use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()


def exitNarration(robot):
    robot.say_text("Thank you for playing.", use_cozmo_voice=False,
                   duration_scalar=0.6).wait_for_completed()
    robot.say_text("Goodbye!.").wait_for_completed()

def resetNarration(robot):
    robot.say_text("Please place cozmo at the start location.", use_cozmo_voice=False,
                   duration_scalar=0.6).wait_for_completed()
    robot.say_text("Tap any cube when ready to continue.", use_cozmo_voice=False,
                   duration_scalar=0.6).wait_for_completed()

# hitWall contains cozmo's reactions for each wall. Takes a string "wall", defining what wall Cozmo hit (i.e. A1).
def hitWall(robot, wall):
    if wall == "A1":
        # wall A1 is the the dead end left of the start point (corner).
        # Hard wall.
        robot.say_text("Ouch! this is hard!").wait_for_completed()
        robot.say_text("Cozmo was scared. How was he going to get out of the museum?",
                       use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

    elif wall == "A2":
        print("No wall response.")

    elif wall == "A4":
        # Couch wall? Soft.
        robot.say_text("Oh my! this is much softer!").wait_for_completed()
        robot.say_text("Cozmo bumped into something soft", use_cozmo_voice=False,
                       duration_scalar=0.6).wait_for_completed()
        robot.say_text("Cozmo remembers that there was a soft couch in the east wing",
                       use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
        robot.say_text("He must be in the east wing", use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

    elif wall == "B2":
        # wall B2 is the first wall Cozmo hits.
        # Soft wall.
        robot.say_text("woah, at least that was soft").wait_for_completed()

    elif wall == "B3":
        print("No wall response.")

    elif wall == "B4":
        print("No wall response.")

    elif wall == "C1":
        robot.say_text("woah, at least that was soft").wait_for_completed()
        robot.say_text("I guess I'll turn around.").wait_for_completed()

    elif wall == "C3":
        print("No wall response.")

    elif wall == "C4":
        print("No wall response.")

    elif wall == "D1A":
        # Hard wall.
        robot.say_text("Ouch! This is hard too!").wait_for_completed()
        robot.say_text("Hmm").wait_for_completed()

    elif wall == "D1B":
        print("No wall response.")

    elif wall == "D2":
        # wall D2 is the first wall to hit after taking the first right.
        # Hard wall.
        robot.say_text("Ouch! this is hard!").wait_for_completed()
        robot.say_text("Now where do I go!").wait_for_completed()

    elif wall == "D4":
        robot.say_text("Hello?").wait_for_completed()
        robot.say_text("Cozmo wondered where everyone went", use_cozmo_voice=False,
                       duration_scalar=0.6).wait_for_completed()


def playIntro(robot):
    robot.say_text("Cozmo went on a field trip with his class and fell asleep. Oh no, his class left "
                   "and the museum closed", use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    robot.say_text("Can you help Cozmo get out of the museum?",
                   use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    robot.say_text("The lights are off so cozmo will have to rely on his sense of touch",
                   use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()


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
# These functions are used as a choice branch by the manual mode

# getInput() waits for the user to tap a cube, and returns the cube id
# 1 = left, 2 = right, 3 = reset the game
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

    print(cube.obj.object_id)



# choiceLeft() is called when the user selects Left as the first choice
def choiceLeft(robot):
    turnLeft(robot)
    driveInches(robot, 5.5)
    hitWall(robot, "A2")
    robot.say_text("Which way!").wait_for_completed()
    input = getInput(robot)
    if input == 1:
        robot.say_text("Left!").wait_for_completed()
        choiceLeftLeft(robot)
    elif input == 2:
        robot.say_text("Right!").wait_for_completed()
        choiceLeftRight(robot)


# choiceRight() is called when the user selects Right as the first choice
def choiceRight(robot):
    turnRight(robot)
    driveInches(robot, 11)
    hitWall(robot, "D2")
    robot.say_text("Which way!").wait_for_completed()
    input = getInput(robot)
    if input == 1:
        robot.say_text("Left!").wait_for_completed()
        choiceRightLeft(robot)
    elif input == 2:
        robot.say_text("Right!").wait_for_completed()
        choiceRightRight(robot)

# choiceRightLeft() is called when the user chooses Right, then Left
def choiceRightLeft(robot):
    turnLeft(robot)
    driveInches(robot, 10.75)
    hitWall(robot, "D4")
    turnLeft(robot)
    driveInches(robot, 6)
    hitWall(robot, "C4")
    turnRight(robot)
    robot.say_text("Hey! I see the exit!").wait_for_completed()
    driveInches(robot, 6)
    # exit reached
    robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)
    victoryDance(robot)
    victorySpeech(robot)


# choiceRightRight() is called when the user chooses Right, then Right again
def choiceRightRight(robot):
    turnRight(robot)
    driveInches(robot, 6.6)
    hitWall(robot, "D1A")
    turnRight(robot)
    driveInches(robot, 6.25)
    hitWall(robot, "C1")
    robot.turn_in_place(degrees(180)).wait_for_completed()
    driveInches(robot, 6.75)
    hitWall(robot, "D1B")
    turnLeft(robot)
    driveInches(robot, 17)
    hitWall(robot, "D4")
    turnLeft(robot)
    driveInches(robot, 7)
    hitWall(robot, "C4")
    turnRight(robot)
    robot.say_text("There's the exit sign!").wait_for_completed()
    driveInches(robot, 6)
    # exit reached
    robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)
    victoryDance(robot)
    victorySpeech(robot)


# choiceLeftLeft() is called when the user chooses Left, then Left again
def choiceLeftLeft(robot):
    turnLeft(robot)
    driveInches(robot, 6)
    hitWall(robot, "A1")
    robot.turn_in_place(degrees(180)).wait_for_completed()
    driveInches(robot, 16.25)
    hitWall(robot, "A4")
    turnRight(robot)
    driveInches(robot, 6)
    hitWall(robot, "B4")
    turnRight(robot)
    driveInches(robot, 6.25)
    hitWall(robot, "B3")
    turnLeft(robot)
    driveInches(robot, 6.75)
    hitWall(robot, "C3")
    turnLeft(robot)
    driveInches(robot, 3)
    robot.say_text("I see the way out!").wait_for_completed()
    driveInches(robot, 6)
    # exit reached
    robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)
    victoryDance(robot)
    victorySpeech(robot)


# choiceLeftLeft() is called when the user chooses Left, then Right
def choiceLeftRight(robot):
    turnRight(robot)
    driveInches(robot, 11)
    hitWall(robot, "A4")
    turnRight(robot)
    driveInches(robot, 6)
    hitWall(robot, "B4")
    turnRight(robot)
    driveInches(robot, 6.25)
    hitWall(robot, "B3")
    turnLeft(robot)
    driveInches(robot, 6.75)
    hitWall(robot, "C3")
    turnLeft(robot)
    driveInches(robot, 3)
    robot.say_text("I see the exit sign!").wait_for_completed()
    driveInches(robot, 6)
    # exit reached
    robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)
    victoryDance(robot)
    victorySpeech(robot)


#  path1 is right, left, out
def autoPath1(robot):
    # start forward
    driveInches(robot, 6.5)
    hitWall(robot, "B2")

    turnRight(robot)
    driveInches(robot, 11)
    hitWall(robot, "D2")

    turnLeft(robot)
    driveInches(robot, 11.5)
    hitWall(robot, "D4")

    turnLeft(robot)
    driveInches(robot, 6.5)
    hitWall(robot, "C4")

    turnRight(robot)
    robot.say_text("I can see the exit sign!", duration_scalar=0.6).wait_for_completed()
    robot.say_text("Cozmo is almost there", use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    driveInches(robot, 6.25)

    # PounceOnMotion = _BehaviorType(name='PounceOnMotion', id=6)  # I think this was commented when I started -(Mike B)
    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    victoryDance(robot)


#  path2 is left, left, dead end, and out
def autoPath2(robot):
    # start forward
    driveInches(robot, 6.5)
    hitWall(robot, "B2")

    turnLeft(robot)
    driveInches(robot, 5.5)
    hitWall(robot, "A2")

    turnLeft(robot)
    driveInches(robot, 6)
    hitWall(robot, "A1")

    robot.turn_in_place(degrees(180)).wait_for_completed()
    driveInches(robot, 16.25)
    hitWall(robot, "A4")

    turnRight(robot)
    driveInches(robot, 6)
    hitWall(robot, "B4")

    turnRight(robot)
    driveInches(robot, 6.25)
    hitWall(robot, "B3")

    turnLeft(robot)
    driveInches(robot, 6.75)
    hitWall(robot, "C3")

    turnLeft(robot)
    driveInches(robot, 3)
    robot.say_text("I can see the exit sign!", duration_scalar=0.6).wait_for_completed()
    robot.say_text("Cozmo is almost there", use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    driveInches(robot, 8)

    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    # PounceOnMotion = _BehaviorType(name='PounceOnMotion', id=6)
    victoryDance(robot)

    return


#  path3 is right, right, dead end, and out
def autoPath3(robot):
    # start forward

    driveInches(robot, 6.5)
    hitWall(robot, "B2")

    # robot.play_audio(cozmo.audio.AudioEvents.Sfx_Constellation_Star)

    turnRight(robot)
    driveInches(robot, 11.25)
    hitWall(robot, "D2")

    turnRight(robot)
    driveInches(robot, 6.6)
    hitWall(robot, "D1A")

    turnRight(robot)
    driveInches(robot, 6.25)
    hitWall(robot, "C1")

    robot.turn_in_place(degrees(180)).wait_for_completed()
    driveInches(robot, 6.75)
    hitWall(robot, "D1B")

    turnLeft(robot)
    driveInches(robot, 17)
    hitWall(robot, "D4")

    turnLeft(robot)
    driveInches(robot, 7)
    hitWall(robot, "C4")

    turnRight(robot)
    robot.say_text("we're almost there", use_cozmo_voice=False).wait_for_completed()

    driveInches(robot, 6.5)

    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    victoryDance(robot)


#  path4 is left, right, and out
def autoPath4(robot):
    # start forward
    driveInches(robot, 6.5)
    hitWall(robot, "B2")

    turnLeft(robot)
    driveInches(robot, 5.5)
    hitWall(robot, "A2")

    turnRight(robot)
    driveInches(robot, 11)
    hitWall(robot, "A4")

    turnRight(robot)
    driveInches(robot, 6)
    hitWall(robot, "B4")

    turnRight(robot)
    driveInches(robot, 6.25)
    hitWall(robot, "B3")

    turnLeft(robot)
    driveInches(robot, 6.75)
    hitWall(robot, "C3")

    turnLeft(robot)
    driveInches(robot, 3)
    robot.say_text("I can see the exit sign!", duration_scalar=0.6).wait_for_completed()
    robot.say_text("Cozmo is almost there", use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    # robot.say_text("So ",use_cozmo_voice=False,duration_scalar=0.8).wait_for_completed()
    # robot.say_text("Close ",use_cozmo_voice=False,duration_scalar=0.4).wait_for_completed()

    driveInches(robot, 8)

    # PounceOnMotion = _BehaviorType(name='PounceOnMotion', id=6)
    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    victoryDance(robot)

    return


########## Main ##########
def main(robot: cozmo.robot.Robot):
    quitProgram = 0  # this flag is set to 1 when the user tapes cube3 to quit
    robot.say_text("Welcome." , use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

    # autoPath4(robot)  # TODO: Remove this line. Used for testing with a dead cube. -(Mike B.)
    # return  # TODO: Remove this line. Used for testing with a dead cube. -(Mike B.)

    # main program loop, repeats until user quits or input timeout occurs
    while quitProgram == 0:
        robot.say_text("Please tap a cube to select game mode, or tap reset to quit."
                       , use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

        # wait for user to tap a cube
        modeSelect = getInput(robot)

        # user selected automatic maze traversal
        if modeSelect == 1:
            playIntro(robot)
            robot.say_text("Automatic mode selected.",
                           use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
            robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoop)
            roll = random.randint(1, 4)
            if roll == 1:
                autoPath1(robot)
            elif roll == 2:
                autoPath2(robot)
            elif roll == 3:
                autoPath3(robot)
            elif roll == 4:
                autoPath4(robot)

            victorySpeech(robot)

            robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)

        # user selected manual maze traversal
        elif modeSelect == 2:
            robot.say_text("Manual mode selected.",
                           use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
            playIntro(robot)
            robot.say_text("Tap a cube when Cozmo asks where to go.",
                           use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
            robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoop)
            driveInches(robot, 6.5)
            hitWall(robot, "B2")
            robot.say_text("Which way!").wait_for_completed()

            input = getInput(robot)
            if input == 1:
                robot.say_text("Left!").wait_for_completed()
                choiceLeft(robot)
            elif input == 2:
                robot.say_text("Right?").wait_for_completed()
                choiceRight(robot)

        elif modeSelect == 3:
            quitProgram = 1
            robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)
            exitNarration(robot)

        # if the user has not decided to quit the program:
        # play the reset narration and wait for user to tap, indicating cozmo is in the start position
        if modeSelect != 3:
            x = 0
            resetNarration(robot)
            # try loop will wait for user input, reminding user every 15 seconds.
            # if one minute passes without input, program will exit
            while 1:
                try:
                    robot.world.wait_for(cozmo.objects.EvtObjectTapped, timeout=20)
                    break
                except asyncio.TimeoutError:
                    x += 1
                    print("Awaiting any cube tap.")
                    if x == 4:
                        print("Input timeout detected. Shutting down.")
                        quitProgram = 1
                        exitNarration(robot)

                    resetNarration(robot)

        robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)


########## Run Program ##########
cozmo.run_program(main)
