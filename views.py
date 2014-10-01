__author__ = 'mperkins'

import threading
import time
import RPi.GPIO as GPIO
import urllib2
import json
import datetime
import usonic

# GLOBAL
# - motion flag
# - height check interval
heightcheckinterval = 60      # five mins
motionflag = False  # default is "motion not detected"
lastheight = 0.00
lastmotiontime = time.now()
maxoutofmotiontime = 60       # five mins
PIR = 23
LED = 24

def configureGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR, GPIO.IN)                # CONFIGURE THESE PROPERLY
    GPIO.setup(LED, GPIO.OUT)               # CONFIGURE THESE PROPERLY
    pass

def checkheight():
    # check height routine
    # - configure GPIO
    # - perform distance measurement
    # - send height to service tier
    # start new thread
    heightthread = threading.Timer(heightcheckinterval, checkheight)
    heightthread.start()
    pass

def checkmotion():
    # is motion pin high
    if time.now() - lastmotiontime > maxoutofmotiontime:
        # since motion senses are automatically updated, and we've exceeded the outofmotion time, we must be outofmotion
        motionflag = False
    # send update home
    sendmotion(True)

    # start new thread
    motioncheckthread = threading.Timer(maxoutofmotiontime, checkmotion)
    motioncheckthread.start()

def sendheight(distance):
    jdata = json.dumps({"sensor": "stand", "time":str(datetime.datetime.now()), "distance": distance})
    print "Sending distance event to platform with following contents: %s" % jdata
    response = urllib2.urlopen("http://flocx.mattperkins.net/standup", jdata)
    print ("Message from platform: ")
    print response.read()
    pass

def sendmotion(state):
    jdata = json.dumps({"sensor": "motion", "time":str(datetime.datetime.now()), "motion": state})
    print "Sending motion event to platform with following contents: %s" % jdata
    response = urllib2.urlopen("http://flocx.mattperkins.net/standup", jdata)
    print ("Message from platform: ")
    print response.read()
    pass

def sendhello():
    # send a formated message and wait for canned response
    # if response is correct, turn on/off an LED to show that things are working
    print "Platform responded"
    pass




# interrupt every 5 mins to send no-motion if motion flag isn't set

# send message on motion and no-motion flag

def main():
    # initialize variables
    # configure GPIO
    configureGPIO()
    # start timers
    # - interrupt every 5 mins to check height
    heightthread = threading.Timer(heightcheckinterval, checkheight)
    heightthread.start()
    # - interrupt every 5 mins to check motion
    motioncheckthread = threading.Timer(maxoutofmotiontime, checkmotion)
    motioncheckthread.start()
    # send hello message
    sendhello()
    # wait for stuff to happen
    while True:
        if GPIO(PIR, True):
            motionflag = True
            lastmotiontime = time.now()
        pass
    # release GPIO on keyboard interrupt (exit)