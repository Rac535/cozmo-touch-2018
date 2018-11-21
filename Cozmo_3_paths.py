#!/usr/bin/env python3
'''
This is a WiP. Goal is to get Cozmo to turn a direction based on what cube is tapped.
Right now, he just continues the correct route when any cube is tapped. See comments in main().
'''
import cozmo
from cozmo.util import degrees, distance_inches, speed_mmps

########## Speech & Animation Functions ##########
def victoryDance(robot):
    robot.play_audio(cozmo.audio.AudioEvents.MusicStyle80S1159BpmLoop)

    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
    robot.turn_in_place(degrees(180)).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
    robot.say_text("Yay for computer science!").wait_for_completed()
    robot.play_audio(cozmo.audio.AudioEvents.MusicStyle80S1159BpmLoopStop)



########## Utility Functions ##########
def driveInches(robot, inches):
    robot.drive_straight(distance_inches(inches), speed_mmps(80)).wait_for_completed()

def turnDegrees(robot, nDegrees):
    robot.turn_in_place(degrees(nDegrees)).wait_for_completed()

def turnRight(robot):
    turnDegrees(robot, -90)

def turnLeft(robot):
    turnDegrees(robot, 90)
    
    
def path1(robot):    
   
    #start forward
    driveInches(robot, 9)
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabTiger).wait_for_completed()   
    robot.say_text("woah, at least that was soft").wait_for_completed()
    robot.say_text("Which way!").wait_for_completed()
    cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped) # Tapping any cube will send him the correct way for now
    print(cube)
    num = cube.obj # this doesn't work to grab the cube number. I'm probably missing some basic OOP skills here


    turnRight(robot)
    driveInches(robot, 9.95)  # First "T" to Second "T"
    robot.say_text("Ouch! this is hard!").wait_for_completed()
    robot.say_text("Now where do I go!").wait_for_completed()
    cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped) # Tapping any cube will send him the correct way for now
    
    turnLeft(robot)
    driveInches(robot, 10)  # Second "T" to Finish Line
  
    turnLeft(robot)
    driveInches(robot, 10)  # Second "T" to Finish Line
    
    turnRight(robot)
    driveInches(robot, 10)  # Second "T" to Finish Line 
    
    #PounceOnMotion = _BehaviorType(name='PounceOnMotion', id=6)
    victoryDance(robot)
    
def path2(robot):    
    #start forward

    driveInches(robot, 9)
    #robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabTiger).wait_for_completed()   
    robot.say_text("woah, at least that was soft").wait_for_completed()
    robot.say_text("Which way!").wait_for_completed()
    #cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped) # Tapping any cube will send him the correct way for now
    #print(cube)
    #num = cube.obj # this doesn't work to grab the cube number. I'm probably missing some basic OOP skills here

    robot.play_audio(cozmo.audio.AudioEvents.Sfx_Constellation_Star)
    
    turnRight(robot)
    driveInches(robot, 9.95)  # First "T" to Second "T"
    robot.say_text("Ouch! this is hard!").wait_for_completed()
    robot.say_text("Now where do I go!").wait_for_completed()
    #cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped) # Tapping any cube will send him the correct way for now

    turnRight(robot)
    driveInches(robot, 6)  # Second "T" to Finish Line
    
    robot.say_text("Ouch! this is hard!").wait_for_completed()
    robot.say_text("Now where do I go!").wait_for_completed()
    #cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped)

    turnRight(robot)
    driveInches(robot, 10)  # Second "T" to Finish Line
    
    robot.say_text("woah, at least that was soft").wait_for_completed()
    robot.say_text("Which way!").wait_for_completed()
    
    turnRight(robot)
    turnRight(robot)
    driveInches(robot, 10)  # Second "T" to Finish Line 
    
    turnLeft(robot)
    driveInches(robot, 20)  # Second "T" to Finish Line
    turnLeft(robot)
    
    robot.say_text("we're almost there",use_cozmo_voice=False).wait_for_completed()
    turnRight(robot)
    driveInches(robot, 5)  # Second "T" to Finish Line 


def path3(robot):    
    #start forward
    
    driveInches(robot, 9)
    #robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabTiger).wait_for_completed()   
    robot.say_text("woah, at least that was soft").wait_for_completed()
    robot.say_text("Which way!").wait_for_completed()
    #cube = robot.world.wait_for(cozmo.objects.EvtObjectTapped) # Tapping any cube will send him the correct way for now
    #print(cube)
    #num = cube.obj # this doesn't work to grab the cube number. I'm probably missing some basic OOP skills here

    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoop)
    
    
    turnLeft(robot)
    driveInches(robot, 10)  # Second "T" to Finish Line
    
    turnLeft(robot)
    driveInches(robot, 10) 
    robot.say_text("Ouch! this is hard!").wait_for_completed()
    robot.say_text("Cozmo was scared. How was he going to get out of the mueseum?",use_cozmo_voice=False).wait_for_completed()
    
    turnRight(robot)
    turnRight(robot)
    driveInches(robot, 20)
    robot.say_text("whew! this is much softer!").wait_for_completed()
    robot.say_text("Cozmo bumped into something soft",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.say_text("Cozmo remembers that there was a soft couch in the east wing",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.say_text("He must be in the east wing",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()

    
    turnRight(robot)
    driveInches(robot, 10)
    
    turnRight(robot)
    driveInches(robot, 10)
    
    
    turnLeft(robot)
    driveInches(robot, 10) 
    
    
    turnLeft(robot)
    driveInches(robot, 10)
    robot.say_text("I can see the exit sign!",duration_scalar=0.6 ).wait_for_completed()
 
    robot.say_text("Cozmo is almost there",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    driveInches(robot, 10)  # Second "T" to Finish Line 
    
    
    #PounceOnMotion = _BehaviorType(name='PounceOnMotion', id=6)
    victoryDance(robot)
    
    robot.play_audio(cozmo.audio.AudioEvents.MusicFunLoopStop)
    return
    
    
########## Main ##########
def main(robot: cozmo.robot.Robot):
    robot.say_text("Cozmo went on a field trip with his class and fell asleep. Oh no, his class left and the museum closed",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.say_text("Can you help Cozmo get out of the museum?",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()
    robot.say_text("The lights are off so cozmo will have to rely on his sense of touch",use_cozmo_voice=False,duration_scalar=0.6).wait_for_completed()

    
    
    path3(robot)
    robot.play_audio(cozmo.audio.AudioEvents.MusicGlobalStop)
    
########## Run Program ##########
cozmo.run_program(main)