#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import numpy
import random
import sys
from time import sleep
from threading import Thread

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

m1f = GPIO.PWM(21, 50)
m2f = GPIO.PWM(26, 50)
m1b = GPIO.PWM(19, 50)
m2b = GPIO.PWM(24, 50)

m1b.start(0)
m2b.start(0)
m1f.start(0)
m2f.start(0)

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

# Starting the query function as a thread means it causes no delay on the rest of the program wile still giving constant results.
t = Thread(target=query)
t.setDaemon(True)
t.start()
    
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
        
def check():
    global turns
    distance = query()
#    print distance
    if distance < 30:
        randnum = random.randint(1, 10)
        if randnum <= 3:
            motor(-100, -100)
            time.sleep(1)
            motor(-100, 100)
            time.sleep(1.5)
            checkSwitch()
        else:
            motor(-100, -100)
            time.sleep(1)
            motor(100, -100)
            time.sleep(1.0 + random.random())
            checkSwitch()
            
def checkSwitch():
    active = not GPIO.input(7)
    if active:
        return
    else:
        motor(0, 0)
        start()
            
def start():
    while True:
        print "start"
        active = not GPIO.input(7)
        if active:
            for speed in range (0, 100, 3):
                motor(speed, speed)
                time.sleep(0.1)
            return
        else:
            time.sleep(2)
            
motor(0, 0)

start()

while True:
    checkSwitch()
    motor(100, 100)
    check()
    time.sleep(0.1)

motor (0, 0)

GPIO.cleanup()
