#!/usr/bin/env python3
'''
Team Name: Cozmo without a Cause

Developers
    Ramon Crayton
    Andrew Dillon
    Mike Beckering
    Tom Downs
    Corey Sanders

Project Info
    Cozmo's Night at the Museum
    Created: 10/10/2018
    Presented: 12/3/2018
    Developed for: UMSL Course FS18-CS4500-E01 - Introduction to the Software Profession
    GitHub repository:
        https://github.com/Rac535/cozmo-touch-2018
    Pulled knowledge and bits of code from Anki's examples:
        https://github.com/anki/cozmo-python-sdk/tree/master/examples

Environment
    Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)]
    PyCharm 2018.2.2 (Community Edition)
    Build #PC-182.4129.34, built on August 21, 2018
    JRE: 1.8.0_152-release-1248-b8 amd64
    JVM: OpenJDK 64-Bit Server VM by JetBrains s.r.o
    Windows 10 10.0
    Uses Anki's Cozmo SDK:
        http://cozmosdk.anki.com/docs/
    And associated API:
        http://cozmosdk.anki.com/docs/api.html
    Built and tested using Andriod OS on a Samsung Galaxy S8 with Android Debug Bridge:
        https://developer.android.com/studio/command-line/adb

Program Behavior
    This is a description of code logic. For additional information regarding game rules, setup and installation,
    see the programmer's guide and user's guide documents in the repository:
        https://github.com/Rac535/cozmo-touch-2018

    The main program runs in a loop until an input timeout is detected or the user decides to quit. Cube id's are
    imported for consistency. User is prompted to select a game mode or quit. The automatic game mode has several
    pre-determined possible routes that are rolled for at the start. The manual mode has branches to different
    functions based on user choices. If the user taps cube3 AKA the Reset button when prompted for input, the
    program will fall out of any of the branching functions and return to the bottom of the main program loop.

    The maze is essentially a 4x4 grid of 5" by 5" squares. Both modes use the
    grid system to determine Cozmo's location, and the characteristics of the walls in each grid slot. When Cozmo
    hits a wall, the hitWall() function is called and passed the grid location, and that function executes the
    appropriate behavior for Cozmo. Cozmo will never fail to reach the exit in either mode, barring physical
    interference.

    After Cozmo reaches the exit, the "narrator" will ask the user to place Cozmo back at the start and tap any
    cube to continue. At this point, the program will wait for any cube tap, and then will return to the top of
    the main program loop with the options to run automatic mode, manual mode, or quit.

    Additional comments and explanations can be found throughout the program.
'''

import random  # to roll for random pathing, animations, and speech options
import cozmo  # must use the cozmo robot
import asyncio  # to catch timeout errors
from cozmo.util import degrees, distance_inches, speed_mmps  # for robot navigation commands
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id  # for consistent cube tap differentiation

########## Global Variables ##########

# These are the 3 cube objects, each will have their own ID. Used to determine
# which cube has been tapped by a user, and for causing the cubes to light up individually.
cube1 = 0  # looks like a paperclip, labeled "1" under one of the grabbable corners
cube2 = 0  # looks like a lamp / heart
cube3 = 0  # looks like the letters 'ab' over 'T'

########## Speech & Animation Functions ##########

# Turn on cube lights
def lightCubes(robot):
    global cube1, cube2, cube3
    cube1.set_lights(cozmo.lights.green_light)
    cube2.set_lights(cozmo.lights.green_light)
    cube3.set_lights(cozmo.lights.red_light)

# Turn off cube lights
def darkCubes(robot):
    global cube1, cube2, cube3
    cube1.set_lights_off()
    cube2.set_lights_off()
    cube3.set_lights_off()

# Plays victory music and causes Cozmo to do a short dance
def victoryDance(robot):
    robot.play_audio(cozmo.audio.AudioEvents.MusicStyle80S1159BpmLoop)

    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
    robot.turn_in_place(degrees(170)).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()

    robot.play_audio(cozmo.audio.AudioEvents.MusicStyle80S1159BpmLoopStop)


# Narrator's voice telling the player that Cozmo has won
def victorySpeech(robot):
    robot.say_text("Cozmo finally made it out of the museum",
                   use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    robot.say_text("Cozmo learned that day that if you can't see",
                   use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    robot.say_text("you might be able to feel your way out of a situation",
                   use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()


# Narrator and Cozmo speak when the user decides to quit, or an input timeout occurs
def exitNarration(robot):
    robot.say_text("Thank you for playing.", use_cozmo_voice=False,
                   duration_scalar=0.6).wait_for_completed()
    robot.say_text("Bye bye!.").wait_for_completed()


# Narrator's voice asks the user to reset Cozmo and tap a cube. Called after Cozmo finishes the maze
def resetNarration(robot):
    robot.say_text("Please place cozmo at the start location.", use_cozmo_voice=False,
                   duration_scalar=0.6).wait_for_completed()
    robot.say_text("Tap any cube when ready to continue.", use_cozmo_voice=False,
                   duration_scalar=0.6).wait_for_completed()


# hitWall contains cozmo's reactions for each wall. Takes a string "wall", defining what wall Cozmo hit (i.e. A1)
# then sends commands to Cozmo that cause him to display reactions appropriate to the wall type (hard / soft)
def hitWall(robot, wall):
    if wall == "A1":
        # wall A1 is the the dead end left of the start point (corner).
        # Soft wall (Felt)
        robot.say_text("Soft.").wait_for_completed()
        robot.say_text("But I'm still lost.").wait_for_completed()
        robot.say_text("Cozmo was scared. How was he going to get out of the museum.",
                       use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

    elif wall == "A2":
        # Hard wall (brick)
        robot.say_text("Ouch! This wall is hard!").wait_for_completed()

    elif wall == "A4":
        # Couch wall. Soft.
        robot.say_text("Very soft.").wait_for_completed()
        robot.say_text("It's a couch!").wait_for_completed()
        robot.say_text("Cozmo remembers that there was a soft couch in the east wing",
                       use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
        robot.say_text("He must be there.", use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

    elif wall == "B2":
        # wall B2 is the first wall Cozmo hits.
        # Soft wall.
        robot.say_text("woah, I hit something soft").wait_for_completed()

    elif wall == "B3":
        # Hard wall (brick)
        robot.say_text("Hard as bricks!").wait_for_completed()

    elif wall == "B4":
        robot.say_text("Soft.").wait_for_completed()

    elif wall == "C1":
        robot.say_text("Feels like a dead end.").wait_for_completed()

    elif wall == "C3":
        robot.say_text("Soft again. I think I know where I am!").wait_for_completed()

    elif wall == "C4":
        print("No wall response.")

    elif wall == "D1A":
        # Soft wall.
        robot.say_text("This feels soft.").wait_for_completed()
        robot.say_text("Hmm").wait_for_completed()

    elif wall == "D1B":
        print("No wall response.")

    elif wall == "D2":
        # wall D2 is the first wall to hit after taking the first right.
        # Hard wall. Anchor.
        robot.say_text("Ouch! this is hard!").wait_for_completed()

    elif wall == "D4":
        # Fireplace
        robot.say_text("Ouch!").wait_for_completed()
        robot.say_text("The fireplace!").wait_for_completed()
        robot.say_text("Cozmo remembered the fireplace near the entrance.", use_cozmo_voice=False,
                       duration_scalar=0.6).wait_for_completed()

# Short Narration of Cozmo's back-story before the game begins
def playIntro(robot):
    robot.say_text("Cozmo went on a field trip with his class and fell asleep. Oh no, his class left "
                   "and the museum closed", use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    robot.say_text("Can you help Cozmo get out of the museum?",
                   use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    robot.say_text("The lights are off so cozmo will have to rely on his sense of touch",
                   use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

########## Utility Functions ##########

# takes the robot object and a number (int or float), and causes Cozmo to drive straight, that far
def driveInches(robot, inches):
    robot.drive_straight(distance_inches(inches), speed_mmps(80)).wait_for_completed()

# takes the robot object and turns in place the specified number of degrees
def turnDegrees(robot, nDegrees):
    robot.turn_in_place(degrees(nDegrees)).wait_for_completed()

# takes the robot object and turns right 90 degrees
def turnRight(robot):
    turnDegrees(robot, -90)

# takes the robot object and turns left 90 degrees
def turnLeft(robot):
    turnDegrees(robot, 90)

########## Routing Functions ##########

# getInput() waits for the user to tap a cube, and returns the cube id. Returns None after timeout catch.
def getInput(robot):
    global cube1, cube2, cube3
    lightCubes(robot)
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
                darkCubes(robot)
                return None
            robot.say_text("Please make a selection."
                           , use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

    if cube.obj.object_id == cube1.object_id:
        print("Cube 1 pressed.")
    elif cube.obj.object_id == cube2.object_id:
        print("Cube 2 pressed.")
    elif cube.obj.object_id == cube3.object_id:
        print("Cube 3 pressed.")

    darkCubes(robot)
    return(cube.obj.object_id)

# choiceLeft() is called when the user selects Left as the first choice
def choiceLeft(robot):
    driveInches(robot, -.25)
    turnLeft(robot)
    driveInches(robot, 5.5)
    hitWall(robot, "A2")
    robot.say_text("Which way!").wait_for_completed()
    input = getInput(robot)
    if input == cube1.object_id:
        robot.say_text("Left again!").wait_for_completed()
        choiceLeftLeft(robot)
    elif input == cube2.object_id:
        robot.say_text("Right!").wait_for_completed()
        choiceLeftRight(robot)

# choiceRight() is called when the user selects Right as the first choice
def choiceRight(robot):
    driveInches(robot, -.25)
    turnRight(robot)
    driveInches(robot, 11)
    hitWall(robot, "D2")
    robot.say_text("Which way!").wait_for_completed()
    input = getInput(robot)
    if input == cube1.object_id:
        robot.say_text("Left!").wait_for_completed()
        choiceRightLeft(robot)
    elif input == cube2.object_id:
        robot.say_text("Right!").wait_for_completed()
        choiceRightRight(robot)

# choiceRightLeft() is called when the user chooses Right, then Left
def choiceRightLeft(robot):
    turnLeft(robot)
    driveInches(robot, 12)
    hitWall(robot, "D4")
    turnLeft(robot)
    driveInches(robot, 6)
    hitWall(robot, "C4")
    turnRight(robot)
    robot.say_text("Yup I see the exit!").wait_for_completed()
    driveInches(robot, 7)
    # exit reached
    robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)
    victoryDance(robot)
    victorySpeech(robot)

# choiceRightRight() is called when the user chooses Right, then Right again
def choiceRightRight(robot):
    turnRight(robot)
    driveInches(robot, 6.6)
    hitWall(robot, "D1A")
    driveInches(robot, -.25)
    turnRight(robot)
    driveInches(robot, 6.25)
    hitWall(robot, "C1")
    robot.turn_in_place(degrees(180)).wait_for_completed()
    driveInches(robot, 6.75)
    hitWall(robot, "D1B")
    turnLeft(robot)
    driveInches(robot, 17.25)
    hitWall(robot, "D4")
    turnLeft(robot)
    driveInches(robot, 7)
    hitWall(robot, "C4")
    turnRight(robot)
    robot.say_text("There's the exit sign!").wait_for_completed()
    driveInches(robot, 7.25)
    # exit reached
    robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)
    victoryDance(robot)
    victorySpeech(robot)

# choiceLeftLeft() is called when the user chooses Left, then Left again
def choiceLeftLeft(robot):
    turnLeft(robot)
    driveInches(robot, 6)
    hitWall(robot, "A1")
    driveInches(robot, -.25)
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
    driveInches(robot, -.25)
    turnLeft(robot)
    driveInches(robot, 3)
    robot.say_text("I see the way out!").wait_for_completed()
    driveInches(robot, 8.75)
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
    driveInches(robot, -.25)
    turnLeft(robot)
    driveInches(robot, 3)
    robot.say_text("I see the exit sign!").wait_for_completed()
    driveInches(robot, 8)
    # exit reached
    robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)
    victoryDance(robot)
    victorySpeech(robot)

#  path1 is right, left, out
def autoPath1(robot):
    # start forward
    driveInches(robot, 6.5)
    hitWall(robot, "B2")
    driveInches(robot, -.25)

    turnRight(robot)
    driveInches(robot, 11)
    hitWall(robot, "D2")

    turnLeft(robot)
    driveInches(robot, 12.25)
    hitWall(robot, "D4")

    turnLeft(robot)
    driveInches(robot, 6.5)
    hitWall(robot, "C4")

    turnRight(robot)
    robot.say_text("I can see the exit sign!", duration_scalar=0.6).wait_for_completed()
    robot.say_text("Cozmo is almost there", use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
    driveInches(robot, 7)

    # PounceOnMotion = _BehaviorType(name='PounceOnMotion', id=6)  # I think this was commented when I started -(Mike B)
    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    victoryDance(robot)

#  path2 is left, left, dead end, and out
def autoPath2(robot):
    # start forward
    driveInches(robot, 6.5)
    hitWall(robot, "B2")
    driveInches(robot, -.25)

    turnLeft(robot)
    driveInches(robot, 5.5)
    hitWall(robot, "A2")

    turnLeft(robot)
    driveInches(robot, 6)
    hitWall(robot, "A1")
    driveInches(robot, -.25)

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
    driveInches(robot, -.25)

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
    driveInches(robot, -.25)

    turnRight(robot)
    driveInches(robot, 11.25)
    hitWall(robot, "D2")

    turnRight(robot)
    driveInches(robot, 6.6)
    hitWall(robot, "D1A")
    driveInches(robot, -.25)

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
    robot.say_text("There's the exit!").wait_for_completed()
    robot.say_text("Cosmo was almost there", use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

    driveInches(robot, 6.5)

    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    victoryDance(robot)

#  path4 is left, right, and out
def autoPath4(robot):
    # start forward
    driveInches(robot, 6.5)
    hitWall(robot, "B2")
    driveInches(robot, -.25)

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
    driveInches(robot, -.25)

    turnLeft(robot)
    driveInches(robot, 3)
    robot.say_text("I can see the exit sign!").wait_for_completed()
    robot.say_text("Cozmo is almost there", use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

    driveInches(robot, 8.75)

    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    victoryDance(robot)

    return

########## Main ##########
def main(robot: cozmo.robot.Robot):
    quitProgram = 0  # this flag is set to 1 when the user tapes cube3 to quit
    # Store cube objects in order to compare their cube id's, whatever they are, to input tap cube id's
    global cube1, cube2, cube3
    cube1 = robot.world.get_light_cube(LightCube1Id)
    cube2 = robot.world.get_light_cube(LightCube2Id)
    cube3 = robot.world.get_light_cube(LightCube3Id)
    print(cube1.object_id)
    print(cube2.object_id)
    print(cube3.object_id)
    robot.say_text("Welcome." , use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

    # main program loop, repeats until user quits or input timeout occurs
    while quitProgram == 0:
        robot.say_text("Please tap a cube to select game mode, or tap reset to quit."
                       , use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()

        # wait for user to tap a cube
        modeSelect = getInput(robot)
        # if no input was received (input timeout occurred), or user chose to quit:
        if modeSelect is None or modeSelect == cube3.object_id:
            quitProgram = 1  # stop main loop from restarting
            robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)
            exitNarration(robot)  # say goodbye

        # user selected automatic maze traversal
        if modeSelect == cube1.object_id:
            robot.say_text("Automatic mode selected.",
                           use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
            #playIntro(robot) # TODO uncomment
            robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoop)  # start music

            # choose a path randomly
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
            robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)  # stop all music

        # user selected manual maze traversal
        elif modeSelect == cube2.object_id:
            robot.say_text("Manual mode selected.",
                           use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
            #playIntro(robot) # TODO uncomment
            robot.say_text("Tap a cube when Cozmo asks where to go.",
                           use_cozmo_voice=False, duration_scalar=0.6).wait_for_completed()
            robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoop)  # start music
            driveInches(robot, 6.5)  # initial movement
            hitWall(robot, "B2")  # initial wall hit
            driveInches(robot, -.25)
            robot.say_text("Which way!").wait_for_completed()

            # from here, function branching begins based on user input
            input = getInput(robot)
            if input == cube1.object_id:
                robot.say_text("Turning Left!").wait_for_completed()
                choiceLeft(robot)
            elif input == cube2.object_id:
                robot.say_text("Turning Right").wait_for_completed()
                choiceRight(robot)

        # When this point is reached, either a maze run has completed, or the user has decided to quit.
        # if the user has not decided to quit the program, do the following:
        # play the reset narration and wait for user to tap, indicating cozmo is in the start position
        # If the user has decided to quit, the quitProgram flag has been set, this "if" is skipped, program ends.
        if modeSelect != cube3.object_id:
            x = 0
            resetNarration(robot)
            # try loop will wait for user input, reminding user every 15 seconds.
            # if one minute passes without input, program will exit
            while 1:
                try:
                    lightCubes(robot)
                    robot.world.wait_for(cozmo.objects.EvtObjectTapped, timeout=20)
                    darkCubes(robot)
                    break
                except asyncio.TimeoutError:
                    x += 1
                    print("Awaiting any cube tap.")
                    if x == 4:
                        darkCubes(robot)
                        print("Input timeout detected. Shutting down.")
                        quitProgram == 1
                        exitNarration(robot)

                    resetNarration(robot)

        robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)

########## Run Program ##########
cozmo.run_program(main)
