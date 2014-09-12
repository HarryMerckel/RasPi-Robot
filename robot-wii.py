#!/usr/bin/python

# Created by Harry Merckel

# Based on:
    # wii_remote_1.py
    # Connect a Nintendo Wii Remote via Bluetooth
    # and  read the button states in Python.
    # Project URL :
    # http://www.raspberrypi-spy.co.uk/?p=1101
    # Author : Matt Hawkins
    # Date   : 30/01/2013

# Uses heavily edited and improved code from https://github.com/chrisalexander/initio-pirocon-test/blob/master/sonar.py

# Import required Python libraries

import cwiid
import time
import RPi.GPIO as GPIO
import numpy
import random
import sys
from threading import Thread

button_delay = 0.1

print 'Press 1 + 2 on your Wii Remote now ...'
time.sleep(1)

# Connect to the Wii Remote. If it times out then try again until it does work.

def connect():
    global wii
    while True:
        try:
            print "Trying connection"
            wii=cwiid.Wiimote()
        except RuntimeError:
            print "Error opening wiimote connection"
            time.sleep(4)
            continue
        else:
            print "Connection made"
            return

connect()
            
print 'Wii Remote connected...\n'
print 'Press some buttons!\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

wii.rpt_mode = cwiid.RPT_BTN
 
# Setting up the GPIO pins for the motors and override switch
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(21, GPIO.OUT) # Motor 1 - forwards
GPIO.setup(19, GPIO.OUT) # Motor 1 - backwards
GPIO.setup(26, GPIO.OUT) # Motor 2 - forwards
GPIO.setup(24, GPIO.OUT) # Motor 2 - backwards
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Override switch

# Setting up PWM for speed control and starting motors at 0 so no output. Pins are as default on the PiRoCon
#  board and 50Hz is fine for both the Pi and the control board.
m1f = GPIO.PWM(21, 50)
m1b = GPIO.PWM(19, 50)
m2f = GPIO.PWM(26, 50)
m2b = GPIO.PWM(24, 50)

m1f.start(0)
m1b.start(0)
m2f.start(0)
m2b.start(0)

# I changed the pin used on the PiRoCon for the ultrasonic distance sensor, so I left this as an easy to change variable
pin = 8

def query():
    while True:
        GPIO.setup(pin, GPIO.OUT)
        ti = time.time()
        global distance
        distlist = [0.0] * 10

        # This takes 5 very quick readings from the ultrasonic sensor. Takes the median of 5 results to get rid of anomalous results.
        while True:
            # Output a very short pulse as a ping to the sensor, then switches to input waiting for a response
            GPIO.output(pin, 1)
            time.sleep(0.00001)
            GPIO.output(pin, 0)
            time0 = time.time()
            GPIO.setup(pin, GPIO.IN)

            # Waiting for return to start
            time1=time0
            while ((GPIO.input(pin) == 0) and ((time1 - time0) < 0.02)):
                time1 = time.time()

            time1 = time.time()
            time2 = time1

            # Timing and waiting for return to finish
            while ((GPIO.input(pin) == 1) and ((time2 - time1) < 0.02)):
                time2 = time.time()
            time2 = time.time()

            time3 = (time2-time1)

            # Calculation of distance -> return time * speed of sound (m/s) / 2 (ping has to go to and from object) * 100 (m to cm)
            cDistance = time3*343/2*100

            GPIO.setup(pin, GPIO.OUT)
            # Removing the oldest datapoint in the list and adding the new one for an accurate reading as possible
            del distlist[0]
            distlist.append(cDistance)
            # Taking the mean of the 10 rolling results
            distance = numpy.mean(distlist)
            # Used in testing to check the readings
            #print distance
            time.sleep(0.02)

# Starting the query function as a thread means it causes no delay on the rest of the program wile still giving constant and accurate results.
t = Thread(target=query)
t.setDaemon(True)
t.start()
    
# This function is to simplify the motor control instead of having to use the ChangeDutyCycle function throughout the program.
def motor (l, r):
    if l > 0:
        m1f.ChangeDutyCycle(l)
        m1b.ChangeDutyCycle(0)
    else:
        m1f.ChangeDutyCycle(0)
        m1b.ChangeDutyCycle(-l)
    if r > 0:
        m2f.ChangeDutyCycle(r)
        m2b.ChangeDutyCycle(0)
    else:
        m2f.ChangeDutyCycle(0)
        m2b.ChangeDutyCycle(-r)

# Checks if a connection is made on pin 7 (switch) as an emergency stop and restarts program.
def checkSwitch():
    active = not GPIO.input(7)
    if active:
        return
    else:
        motor(0, 0)
        start()

# The start function checks for the switch every two seconds if it's off.
def start():
    while True:
        active = not GPIO.input(7)
        if active:
            print "..."
            return
        else:
            time.sleep(2)
            
motor(0, 0)

start()
# And finally, the loop that runs it all!

while True:
    checkSwitch()
    motor(0,0)
    buttons = wii.state['buttons']
    # If Plus and Minus buttons pressed together then rumble and quit.
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):    
        print '\nClosing connection ...'
        wii.rumble = 1
        time.sleep(1)
        wii.rumble = 0
        exit(wii)    
    
    # First checking if the direction buttons and the movement buttons are pressed and acting
    #  accordingly, restarting to loop so nothing strange happens.
    # This is also checking the distance detected by the ultrasonic sensor and stopping forward
    #  movement if it is less than 15cm from an object.
    
    if (buttons - cwiid.BTN_UP - cwiid.BTN_2 == 0):
        if (distance > 15):
            motor(0,100)
            time.sleep(button_delay)
            continue
        else:
            motor(-100,100)
            time.sleep(button_delay)
            continue
        continue

    if (buttons - cwiid.BTN_UP - cwiid.BTN_1 == 0):
        motor(0,-100)
        time.sleep(button_delay)
        continue
        
    if (buttons - cwiid.BTN_DOWN - cwiid.BTN_2 == 0):
        if (distance > 15):
            motor(100,0)
            time.sleep(button_delay)
            continue
        else:
            motor(100,-100)
            time.sleep(button_delay)
            continue
        continue
        
    if (buttons - cwiid.BTN_DOWN - cwiid.BTN_1 == 0):
        motor(-100,0)
        time.sleep(button_delay)
        continue

    # Check if other buttons are pressed by doing a bitwise AND of the buttons number
    # and the predefined constant for that button.
    if (buttons & cwiid.BTN_UP):
        # Up is actually Left when holing the WiiMote horizontally, so we turn the bot left. Left = Down, Right = Up, Down = Right, Up = Left.
        motor(-100,100)
        time.sleep(button_delay)
        continue
        
    if (buttons & cwiid.BTN_DOWN):
        motor(100,-100)
        time.sleep(button_delay)
        continue
        
    if (buttons & cwiid.BTN_1):
        motor(-100,-100)
        time.sleep(button_delay)
        continue

    if (buttons & cwiid.BTN_2):
        if (distance > 15):
            motor(100,100)
            time.sleep(button_delay)
            continue
        else:
            motor(0,0)
            wii.rumble = 1
            time.sleep(0.5)
            wii.rumble = 0
            time.sleep(button_delay)
            continue
        continue    

motor (0, 0)

GPIO.cleanup()