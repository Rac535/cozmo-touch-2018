#!/usr/bin/env python3
'''
TODO : Add lots of comments here for Dr. Miller to enjoy.
TODO : Add code from manual mode to this program?
Team Name
Our Names
Dates
Project
Class
Python build used
SDK info / other info

Explanation of the program
'''

import random
import cozmo
from cozmo.util import degrees, distance_inches, speed_mmps

########## Speech & Animation Functions ##########
def victoryDance(robot):
    robot.play_audio(cozmo.audio.AudioEvents.MusicStyle80S1159BpmLoop)

    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
    robot.turn_in_place(degrees(180)).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()

    robot.play_audio(cozmo.audio.AudioEvents.MusicStyle80S1159BpmLoopStop)

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

#  path1 is right, left, out
def path1(robot):
    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoop)

    #start forward
    driveInches(robot, 6.5)
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabTiger).wait_for_completed()
    robot.say_text("woah, at least that was soft").wait_for_completed()

    turnRight(robot)
    driveInches(robot, 11)
    robot.say_text("Ouch! this is hard!").wait_for_completed()
    robot.say_text("Now where do I go!").wait_for_completed()
    
    turnLeft(robot)
    driveInches(robot, 10.75)
    robot.say_text("Hello?").wait_for_completed()
    robot.say_text("Cozmo wondered where everyone went",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()

    turnLeft(robot)
    driveInches(robot, 6)
    
    turnRight(robot)
    robot.say_text("I can see the exit sign!",duration_scalar=0.6 ).wait_for_completed()
    robot.say_text("Cozmo is almost there",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    driveInches(robot, 5.25)
    
    #PounceOnMotion = _BehaviorType(name='PounceOnMotion', id=6)  # I think this was commented when I started -(Mike B)
    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    victoryDance(robot)

#  path2 is left, left, dead end, and out
def path2(robot):
    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoop)

    #start forward
    driveInches(robot, 6.5)
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabTiger).wait_for_completed()
    robot.say_text("woah, at least that was soft").wait_for_completed()
    
    turnLeft(robot)
    driveInches(robot, 5.5)
    
    turnLeft(robot)
    driveInches(robot, 6)
    robot.say_text("Ouch! this is hard!").wait_for_completed()
    robot.say_text("Cozmo was scared. How was he going to get out of the museum?",
                   use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()

    robot.turn_in_place(degrees(180)).wait_for_completed()
    driveInches(robot, 16.25)
    robot.say_text("whew! this is much softer!").wait_for_completed()
    robot.say_text("Cozmo bumped into something soft",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.say_text("Cozmo remembers that there was a soft couch in the east wing",
                   use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.say_text("He must be in the east wing",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    
    turnRight(robot)
    driveInches(robot, 6)
    
    turnRight(robot)
    driveInches(robot, 6.25)
    
    turnLeft(robot)
    driveInches(robot, 6.75)
    
    turnLeft(robot)
    driveInches(robot, 3)
    robot.say_text("I can see the exit sign!",duration_scalar=0.6 ).wait_for_completed()
    robot.say_text("Cozmo is almost there",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    driveInches(robot, 6)

    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    #PounceOnMotion = _BehaviorType(name='PounceOnMotion', id=6)
    victoryDance(robot)

    return
    
#  path3 is right, right, dead end, and out
def path3(robot):
    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoop)

    #start forward

    driveInches(robot, 6.5)
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabTiger).wait_for_completed()
    robot.say_text("woah, at least that was soft").wait_for_completed()
    robot.say_text("Which way!").wait_for_completed()

    #robot.play_audio(cozmo.audio.AudioEvents.Sfx_Constellation_Star)
    
    turnRight(robot)
    driveInches(robot, 11.25)
    robot.say_text("Ouch! this is hard!").wait_for_completed()
    robot.say_text("Now where do I go!").wait_for_completed()

    turnRight(robot)
    driveInches(robot, 6.6)
    
    robot.say_text("Ouch! This is hard too!").wait_for_completed()
    robot.say_text("Hmm").wait_for_completed()

    #cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped)

    turnRight(robot)
    driveInches(robot, 6.25)
    robot.say_text("woah, at least that was soft").wait_for_completed()
    robot.say_text("I guess I'll turn around.").wait_for_completed()

    robot.turn_in_place(degrees(180)).wait_for_completed()
    driveInches(robot, 6.75)
    
    turnLeft(robot)
    driveInches(robot, 17)

    turnLeft(robot)
    driveInches(robot, 7)

    turnRight(robot)
    robot.say_text("we're almost there",use_cozmo_voice=False).wait_for_completed()

    driveInches(robot, 5)

    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    victoryDance(robot)

#  path4 is left, right, and out
def path4(robot):
    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoop)

    #start forward
    driveInches(robot, 6.5)
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabTiger).wait_for_completed()
    robot.say_text("woah, at least that was soft").wait_for_completed()
    robot.say_text("Which way!").wait_for_completed()
    
    turnLeft(robot)
    driveInches(robot, 5.5)
    
    turnRight(robot)
    driveInches(robot, 11)
    robot.say_text("This is soft!").wait_for_completed()
    robot.say_text("Cozmo remembers that there was a soft couch in the east wing",
                   use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.say_text("He must be in the east wing",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    
    turnRight(robot)
    driveInches(robot, 6)
    
    turnRight(robot)
    driveInches(robot, 6.25)

    turnLeft(robot)
    driveInches(robot, 6.75)

    turnLeft(robot)
    driveInches(robot, 3)
    robot.say_text("I can see the exit sign!",duration_scalar=0.4 ).wait_for_completed()
 
    robot.say_text("Cozmo is almost there",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    #robot.say_text("So ",use_cozmo_voice=False,duration_scalar=0.8).wait_for_completed()
    #robot.say_text("Close ",use_cozmo_voice=False,duration_scalar=0.4).wait_for_completed()

    driveInches(robot, 7)
    
    #PounceOnMotion = _BehaviorType(name='PounceOnMotion', id=6)
    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    victoryDance(robot)

    return
    
########## Main ##########
def main(robot: cozmo.robot.Robot):

    robot.say_text("Cozmo went on a field trip with his class and fell asleep. Oh no, his class left "
                   "and the museum closed",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.say_text("Can you help Cozmo get out of the museum?",
                   use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.say_text("The lights are off so cozmo will have to rely on his sense of touch",
                   use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoop)  # Music plays while Cozmo navigates through the maze

    roll = random.randint(1, 4)
    if roll == 1:
        path1(robot)
    elif roll == 2:
        path2(robot)
    elif roll == 3:
        path3(robot)
    elif roll == 4:
        path4(robot)

    robot.say_text("Cozmo finally made it out of the museum",
                   use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.say_text("Cozmo learned that day that if you can't see",
                   use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.say_text("you might be able to feel your way out of a situation",
                   use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()

    robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)

    resetNarration(robot)
    robot.world.wait_for(cozmo.objects.EvtObjectTapped)
    
########## Run Program ##########
cozmo.run_program(main)