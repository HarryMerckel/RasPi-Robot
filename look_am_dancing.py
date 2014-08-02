@@ -0,0 +1,88 @@
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
        
motor (0, 0)

def chaha_chaha():
    motor(50, 50)
	time.sleep(0.5)
	motor(-50, 50)
	time.sleep(0.5)
	motor(-50, -50)
	time.sleep(0.5)
	motor(50, -50)
	time.sleep(0.5)
	motor(50, 50)
	time.sleep(0.5)
	motor(-50, 50)
	time.sleep(0.5)
	motor(-50, -50)
	time.sleep(0.5)
	motor(-50, 50)
	time.sleep(0.5)
	motor(50, 50)
	time.sleep(0.5)
	motor(-50, -50)
	time.sleep(0.5)
	
def zigzag():
    motor(100, 100)
	time.sleep(0.5)
	motor(-100, 100)
	time.sleep(0.5)
	motor(-100, -100)
	time.sleep(0.5)
	motor(100, -100)
	time.sleep(0.5)
	motor(100, 100)
	time.sleep(0.5)
	motor(-100, 100)
	time.sleep(0.5)
	motor(-100, -100)
	time.sleep(0.5)
	motor(-100, 100)
	time.sleep(0.5)
	motor(100, 100)
	time.sleep(0.5)
	motor(100, -100)
	time.sleep(0.5)
	motor(-100, -100)
	
def snake():
    motor(100, 100)
    time.sleep(0.5)
	motor(80, 100)
	time.sleep(0.5)
	motor(60, 100)
	time.sleep(0.5)
	motor(80, 80)
	time.sleep(0.5)
	motor(100,60)
	time.sleep(0.5)
	motor(80, 80)
	time.sleep(0.5)
	motor(80, 100)
	time.sleep(0.5)
	motor(60, 100)
	time.sleep(0.5)
	motor(80, 80)
	time.sleep(0.5)
	motor(100,60)
	time.sleep(0.5)
	motor(80, 80)
	time.sleep(0.5)
	motor(60, 100)
	time.sleep(0.5)
	motor(80, 80)
	time.sleep(0.5)
	motor(100, 60)
	time.sleep(0.5)
	motor(80, 80)
	time.sleep(0.5)
	motor(60, 100)
	time.sleep(0.5)
	motor(80, 80)
	time.sleep(0.5)
	motor(100, 60)
	time.sleep(0.5)
	motor(80, 80)
	time.sleep(0.5)
	motor(60, 100)
	time.sleep(0.5)
	motor(80, 80)
	time.sleep(0.5)
	motor(100, 60)
	time.sleep(0.5)
	motor(80, 80)
	time.sleep(0.5)
	motor(60, 100)
	time.sleep(0.5)
	motor(80, 80)
	time.sleep(0.5)
	motor(100, 60)
	time.sleep(0.5)
	motor(100, 80)
	time.sleep(0.5)
	motor(100, 100)
	

			
def square_spiral():
	count = 2
	while count != 0.5:
		motor(75,75)
		time.sleep(count)
		motor(75,100)
		time.sleep(1)
		motor(75,75)
		time.sleep(count)
		motor(75,100)
		time.sleep(1)
		motor(75,75)
		time.sleep(count)
		motor(75,100)
		time.sleep(1)
		motor(75,75)
		time.sleep(count)
		motor(75,100)
		count -= 0.5
		
def swirl():
	count = 100
	while count != 100:
		motor(count,20)
		time.sleep(1)
		count += 10		
			
			
def forward():
	motor(100, 100)
	
def backwards():
	motor(-100, -100)
	
def left():
	motor(-100, 100)
	
def right():
	motor(100, -100)
	
while running == True:

choise = input("manual/random input")
if choise == "random":
	random()
if choise =="manual":
	manual()
	
def manual()
	input = input("lets dance")
	if input = "help":
		print("right, left, foward, backward, swirl, square_spiral, snake, zigzag, chaha_chaha, 1up_2back, slide_away, belly_dance, twitch, egtptian;)")
	if input = "right"
		right()
	if input = "left"
		left()
	if input = "forward"
		forward()
	if input = "backward"
		backward()
	if input = "swirl"
		swirl()
	if input = "square_spiral"
		square_spiral()
	if input = "snake"
		snake()
	if input = "zigzag"
		zigzag()
	if input = "chaha_chaha"
		chaha_chaha()
	if input ="1up_2back"
		1up_2back()
	if input = "slide_away"
		slide_away()
	if input = "belly_dance"
		belly_dance()
	if input = "random_move"
		random_move()
	if input = "twitch"
		twitch()
	if input = "egtptian"
	 egtptian()
	

def random():
	randnum = random.ranrange(1, 15)

	if randnum = 1:
		right()
	if randnum = 2:
		left()
	if randnum = 3:
		backwards()
	if randnum = 4:
		forward()
	if randnum = 5:
		swirl()
	if randnum = 6:
		square_spiral()
	if randnum = 7:
		chaha_chaha()
	if randnum = 8:
		snake()
	if randnum = 9:
		zigzag()
	if randum = 10:
		1up_2back()
	if randnum = 11:
		slide_away()
	if randnum = 12:
		belly_dance()
	if randnum = 13:
		twitch()
	if randnum = 14:
		random_move()
	if randnum = 15:
		egtptian()
		
		
def 1up_2back():
	motor(100, 100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(100, 100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(100, 100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(100, 100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(100, 100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	
def slide_away()
	motor(100, -50)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(-100, 100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(-100, 100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(-100, 100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(-100, 100)
	time.sleep(0.1)
	motor(-100, -100)
	time.sleep(0.1)
	motor(-100, 100)
	time.sleep(0.1)
	
	
def belly_dance():
	randnum = random.ranrange(1,2)
	if randnum = 1:
		motor(100,0)
	if randnum = 2:
		motor(0,100)

def twitch():
	motor(100,-100)
	motor(-100,100)
	time.sleep(0.25)
	motor(100,-100)
	motor(-100,100)
	time.sleep(0.25)
	motor(-100,100)
	motor(100,-100)
	time.sleep(0.25)
	motor(-100,100)
	morot(100,-100)
	time.sleep(0.25)
	
def random_move():
	count = 0
	while count != 20:
		randnum = random.randrange(1,4)
		if randnum = 1:
			forward()
			
		if randnum = 2:
			backward()
			
		if randnum = 3:
			left()
			
		if randnum = 4:
			right()
		count += 1
	
def egtptian
	motor(100,100)
	time.sleep(0.1)
	motor(100,100)
	time.sleep(0.1)
	motor(100,100)
	time.sleep(0.1)
	motor(100,-100)
	time.sleep(3)
	motor(100,100)
	time.sleep(0.1)
	motor(100,100)
	time.sleep(0.1)
	motor(100,100)
	time.sleep(0.1)
	motor(100,100)
	time.sleep(0.1)
	motor(100,100)
	time.sleep(0.1)
	motor(100,100)
	time.sleep(0.1)
	motor(100,-100)
	time.sleep(3)
	motor(100,100)
	time.sleep(0.1)
	motor(100,100)
	time.sleep(0.1)
	motor(100,100)
	time.sleep(0.1)
	motor (0, 0)

GPIO.cleanup()