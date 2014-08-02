#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import numpy
import random
import sys

def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from print statements
        return
    func_line_no = frame.f_lineno
    func_filename = co.co_filename
    caller = frame.f_back
    caller_line_no = caller.f_lineno
    caller_filename = caller.f_code.co_filename
    print 'Call to %s on line %s of %s from line %s of %s' % \
        (func_name, func_line_no, func_filename,
         caller_line_no, caller_filename)
    return

sys.settrace(trace_calls)
    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

m1f = GPIO.PWM(26, 2000)
m2f = GPIO.PWM(21, 2000)
m1b = GPIO.PWM(24, 2000)
m2b = GPIO.PWM(19, 2000)

def query(pin):
    GPIO.setup(pin, GPIO.OUT)
    ti = time.time()
       
    distlist = [0.0,0.0,0.0]
    ts=time.time()
        
    for k in range(3):
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

        distance = sorted(distlist)[1]
                
    return distance


def dMedian():
    checkSwitch()
    d1 = query(8)
    print str(d1)
    time.sleep(0.1)
    d2 = query(8)
    print str(d2)
    time.sleep(0.1)
    d3 = query(8)
    print str(d3)
    time.sleep(0.1)
    d4 = query(8)
    print str(d4)
    time.sleep(0.1)
    d5 = query(8)
    print str(d5)
    time.sleep(0.1)
    d6 = query(8)
    print str(d6)
    time.sleep(0.1)
    d7 = query(8)
    print str(d7)
    time.sleep(0.1)
    d8 = query(8)
    print str(d8)
    time.sleep(0.1)
    d9 = query(8)
    print str(d9)
    checkSwitch()
    
    dAll = [d1, d2, d3, d4, d5, d6, d7, d8, d9]
        
    #dAvg = numpy.mean(dAll)
    #dRange = (max(dAll)-min(dAll))
    
    global dMed
    dMed = numpy.median(dAll)
    global time2
    time2 = time.time()
    #print "Average: " + str(dAvg)
    #print "Range: " + str(dRange)
    #print str(dMed)

def PWMforwards():
    m1f.start(0)
    m2f.start(0)
    dMedian()
    checkSwitch()
    if dMed > 50:
        for dcf in range(0, 101, 10):
            m1f.ChangeDutyCycle(dcf)
            m2f.ChangeDutyCycle(dcf)
            time.sleep(0.1)
        PWMcheck()
    else:
        PWMturnright()

def PWMcheck():
    dMedian()
    time1 = time.time()
    checkSwitch()
    while dMed > 50:
        time.sleep(0.5)
        time2 = time.time()
        if int(time2-time1) > 10:
            PWMforwardsTurn()
        else:
            dMedian()
    else:
        PWMturnright()

def PWMturnright():
#    for dcf in range(100, -1, -5):
#        m1f.ChangeDutyCycle(dcf)
#        m2f.ChangeDutyCycle(dcf)
#        time.sleep(0.05)
    m1f.stop()
    m2f.stop()
    checkSwitch()
    time.sleep(0.25)
    m1b.start(100)
    m2b.start(100)
    time.sleep(0.75)
    m1b.stop()
    m2b.stop()
    checkSwitch()
    m2b.start(0)
    m1f.start(0)
    for dcf in range(0, 101, 10):
        m1f.ChangeDutyCycle(dcf)
        m2b.ChangeDutyCycle(dcf)
        time.sleep(0.1)
    checkSwitch()
    time.sleep(1)
    checkSwitch()
    for dcf in range(100, -1, -10):
        m1f.ChangeDutyCycle(dcf)
        m2b.ChangeDutyCycle(dcf)
        time.sleep(0.1)
    m1f.stop()
    m2b.stop()
    checkSwitch()
    PWMforwards()

def startRight():
    m1f.start(0)
    m2b.start(0)
    checkSwitch()
    for dcf in range(0, 51, 2):
        m1f.ChangeDutyCycle(dcf)
        m2b.ChangeDutyCycle(dcf)
        time.sleep(0.1)
    checkSwitch()
    time.sleep(1)
    for dcf in range(50, -1, -2):
        m1f.ChangeDutyCycle(dcf)
        m2b.ChangeDutyCycle(dcf)
        time.sleep(0.1)
    m1f.stop()
    m2b.stop()
    checkSwitch()
    PWMforwards()

def timer():
    time1 = time.time()
    global time2
    time2 = time.time()
    while int(time2-time1)<5:
        print str(time2-time1)
        PWMforwards()
    else:
        PWMforwardsTurn()

def PWMforwardsTurn():
    checkSwitch()
    for dcf in range(100, 75, -2):
        m1f.ChangeDutyCycle(dcf)
        time.sleep(0.1)
    time.sleep(1)
    checkSwitch()
    for dcf in range(75, 101, 2):
        m1f.ChangeDutyCycle(dcf)
        time.sleep(0.1)
    PWMcheck()

def stopAll():
    m1f.stop()
    m1b.stop()
    m2f.stop()
    m2b.stop()
    GPIO.cleanup()
    sys.exit()

def start():
    while True:
        input_state = GPIO.input(7)
        if input_state == False:
            print "Starting \"PWMforwards()\""
            PWMforwards()
        else:
            time.sleep(2)
                
def checkSwitch():
    input_state = GPIO.input(7)
    while input_state == False:
        return
    else:
        m1f.stop()
        m1b.stop()
        m2f.stop()
        m2b.stop()
        start()
        return

lefton = True
righton = False
def snake():
			""" Snake movement. """
			while count != 6:
				if lefton = True:
					count += 1
					while leftspeed != 100:
						m1f.ChangeDutyCycle(rspeed)
						time.sleep(0.05)
						m2f.ChangeDutyCycle(lspeed)
						time.sleep(0.05)
						rspeed += 10
						lspeed -= 10
						if leftspeed = 100:
							lefton = False
							righton = True
				
				if righton = True:
					while rightspeed != 100:
						m1f.ChangeDutyCycle(lspeed)
						time.sleep(0.05)
						m2f.ChangeDutyCycle(rspeed)
						time.sleep(0.05)
						rspeed += 10
						lspeed -= 10
						if rightspeed = 100:
							lefton = False
							righton = True		
		
start()

def dance_moves_random():
	while radom_on = True:
		count = 0
		randnum = random.randrange(1,8)
		
		if randnum = 1:
		    randtime = random.randrange(1,3)
			m1f.start(randtime)
			m2f.start(randtime)
		
		if randnum = 2:
			randtime = random.randrange(1,3)
			m1b.start(randtime)
			m2b.start(randtime)
			
		# turn right
		if randnum = 3:
			randtime = random.randrange(1,3)
			m1f.start(randtime)
			m2b.start(randtime)
			
		# turn left
		if randnum = 4:
			randtime = random.randrange(1,3)
			m1b.start(randtime)
			m2f.start(randtime)
		
		if randnum = 5:
			snake()
							
		if randnum = 6:
			m1f.start(1)
			m2f.start(1)
			time.sleep(0.5)
			m1f.start(1)
			m2b.start(1)
			time.sleep(0.5)
			m1b.start(1)
			m2b.start(1)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(1)
			m2f.start(1)
			time.sleep(0.5)
			m1f.start(1)
			m2b.start(1)
			time.sleep(0.5)
			m1b.start(1)
			m2b.start(1)
			time.sleep(0.5)
			m1f.start(1)
			m2b.start(1)
			time.sleep(0.5)
			m1f.start(1)
			m2f.start(1)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1b.start(1)
			m2b.start(1)
			time.sleep(0.5)
		
		if randnum = 7:
			m1f.start(3)
			m2f.start(3)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(3)
			m2f.start(3)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(3)
			m2f.start(3)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(2)
			m2f.start(2)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(2)
			m2f.start(2)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(2)
			m2f.start(2)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(2)
			m2f.start(2)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(1)
			m2f.start(1)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(1)
			m2f.start(1)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(1)
			m2f.start(1)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(1)
			m2f.start(1)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			m1f.start(1)
			m2f.start(1)
			time.sleep(0.5)
			m1f.start(2)
			m2b.start(2)
			time.sleep(0.5)
			
		if randnum = 8:
			m1f.ChangeDutyCycle(50)
			m2f.ChangeDutyCycle(0)
			m1f.start(1.5)
			time.sleep(0.00001)
			m2f.ChangeDutyCycle(10)
			m1f.start(1.5)
			m2f.start(1.5)
			time.sleep(0.00001)
			m2f.ChangeDutyCycle(20)
			m1f.start(1.5)
			m2f.start(1.5)
			time.sleep(0.00001)
			m2f.ChangeDutyCycle(30)
			m1f.start(1.5)
			m2f.start(1.5)
			time.sleep(0.00001)
			m2f.ChangeDutyCycle(40)
			m1f.start(1.5)
			m2f.start(1.5)
			time.sleep(0.00001)
			m2f.ChangeDutyCycle(50)
			m1f.start(1.5)
			m2f.start(1.5)
			time.sleep(0.00001)
			m2f.ChangeDutyCycle(60)
			m1f.start(1.5)
			m2f.start(1.5)
			time.sleep(0.00001)
			m2f.ChangeDutyCycle(70)
			m1f.start(1.5)
			m2f.start(1.5)
			time.sleep(0.00001)
			m2f.ChangeDutyCycle(80)
			m1f.start(1.5)
			m2f.start(1.5)
			time.sleep(0.00001)
			m2f.ChangeDutyCycle(90)
			m1f.start(1.5)
			m2f.start(1.5)
			time.sleep(0.00001)
			m2f.ChangeDutyCycle(100)
			m1f.start(1.5)
			m2f.start(1.5)
			
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
			
		
			
			
		
	

print "Something went wrong!"

GPIO.cleanup()
