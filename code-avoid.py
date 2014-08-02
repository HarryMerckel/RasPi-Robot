#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import numpy
import random
import sys
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

m1f = GPIO.PWM(21, 2000)
m2f = GPIO.PWM(26, 2000)
m1b = GPIO.PWM(19, 2000)
m2b = GPIO.PWM(24, 2000)

m1b.start(0)
m2b.start(0)
m1f.start(0)
m2f.start(0)

pin = 8

def query():
    GPIO.setup(pin, GPIO.OUT)
    ti = time.time()
       
    distlist = [0.0] * 5
    ts=time.time()
        
    for k in range(5):
        GPIO.output(pin, 1)
        time.sleep(0.00001)
        GPIO.output(pin, 0)
        t0=time.time()
        GPIO.setup(pin, GPIO.IN)
           
        t1=t0
        while ((GPIO.input(pin)==0) and ((t1-t0) < 0.02)):
            t1=time.time()

        t1=time.time()
        t2=t1

        while ((GPIO.input(pin)==1) and ((t2-t1) < 0.02)):
            t2=time.time()
        t2=time.time()

        t3=(t2-t1)

        distance=t3*343/2*100
        distlist[k]=distance

        GPIO.setup(pin, GPIO.OUT)
        tf = time.time() - ts

        distance = sorted(distlist)[2]
                
    return distance
    
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
    distance = query()
    print distance
    if distance < 30:
        motor(-100, -100)
        time.sleep(0.5)
        motor(100, -100)
        time.sleep(3)
        motor(100, 100)

motor (0, 0)

while True:
    motor(100, 100)
    check()
    time.sleep(0.1)

motor (0, 0)

GPIO.cleanup()
