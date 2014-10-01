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
percentheightchange = 0.05      # percent change in height that is needed to update the height information
lastmotiontime = datetime.datetime.now()
maxoutofmotiontime = 60       # five mins
PIR = 22
LED = 17
TRIGGER = 23
ECHO = 24


def configureGPIO():
    print "Starting GPIO configuration ..."
    # use GPIO port numbers as pin references NOT the PCB pin number and supress GPIO warnings
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # init ports for usonic sensor
    GPIO.setup(ECHO, GPIO.IN)                # CONFIGURE THESE PROPERLY
    GPIO.setup(TRIGGER, GPIO.OUT)               # CONFIGURE THESE PROPERLY
    GPIO.output(TRIGGER, GPIO.LOW)
    time.sleep(0.3)                         # time for pin to settle - took advice from usonic forum but didn't test

    # init ports for motion sensor
    GPIO.setup(PIR, GPIO.IN)                # CONFIGURE THESE PROPERLY
    GPIO.setup(LED, GPIO.OUT)               # CONFIGURE THESE PROPERLY

    # init LED
    GPIO.output(LED, GPIO.HIGH)
    print "GPIO configuration complete"

def checkheight(self):
    # check height routine
    us = usonic.usonic(TRIGGER, ECHO)
    us.readdistance()

    distance = readdistance()
    if abs(distance - self.lastheight) > self.percentheightchange * self.lastheight:
        self.lastheight = distance

    # start new thread
    heightthread = threading.Timer(heightcheckinterval, checkheight)
    heightthread.start()
    pass

def checkmotion(self):
    # has the last inmotion time been longer than the acceptable interval for outofmotion?
    if datetime.datetime.now() - lastmotiontime > datetime.timedelta(maxoutofmotiontime, seconds):
        # since motion senses are automatically updated, and we've exceeded the outofmotion time, we must be outofmotion
        self.motionflag = False
        # send an update
        sendmotion(False)
    else:
        # we must still be in motion so send an update
        sendmotion(True)

    # start new thread
    motioncheckthread = threading.Timer(maxoutofmotiontime, checkmotion)
    motioncheckthread.start()

def sendheight(distance):
    jdata = json.dumps({"sensor": "stand", "time":str(datetime.datetime.now()), "distance": distance})
    print "Sending distance event to platform with following contents: %s" % jdata
    response = urllib2.urlopen("http://flocx.mattperkins.net/standup", jdata)
    print ("Response from sending height update: ")
    print response.read()
    pass

def sendmotion(state):
    jdata = json.dumps({"sensor": "motion", "time":str(datetime.datetime.now()), "motion": state})
    print "Sending motion event to platform with following contents: %s" % jdata
    response = urllib2.urlopen("http://flocx.mattperkins.net/standup", jdata)
    print ("Response from sending motion update: ")
    print response.read()

def sendhello():
    # send a formated message and wait for canned response
    # if response is correct, turn on/off an LED to show that things are working
    print "Platform responded"
    pass




# interrupt every 5 mins to send no-motion if motion flag isn't set

# send message on motion and no-motion flag

def main():
    # initialize everything

    # configure GPIO
    configureGPIO()

    # start timers
    # - interrupt every heightcheckinterval to check height
    heightthread = threading.Timer(heightcheckinterval, checkheight)
    heightthread.start()

    # - interrupt every maxoutofmotiontime to check motion
    motioncheckthread = threading.Timer(maxoutofmotiontime, checkmotion)
    motioncheckthread.start()

    # send hello message - THIS DOES NOTHING
    sendhello()

    # wait for stuff to happen
    while True:
        # wait to see motion and update lastmotiontime
        if GPIO(PIR, True):
            motionflag = True
            lastmotiontime = datetime.datetime.now()
        pass
    # release GPIO on keyboard interrupt (exit)