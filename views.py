__author__ = 'mperkins'

import threading
import time
import RPi.GPIO as GPIO
import urllib2
import json
import datetime
import usonic

def initialize(self):
    # GLOBAL
    # - motion flag
    # - height check interval
    self.heightcheckinterval = 60                   # five mins
    self.motionflag = False                         # default is "motion not detected"
    self.lastheight = 0.00
    self.percentheightchange = 0.05                 # percent change in height that is needed to update the height information
    self.lastmotiontime = datetime.datetime.now()
    self.maxoutofmotiontime = 60                    # five mins
    self.PIR = 22
    self.LED = 17
    self.TRIGGER = 23
    self.ECHO = 24


def configureGPIO(self):
    print "Starting GPIO configuration ..."
    # use GPIO port numbers as pin references NOT the PCB pin number and supress GPIO warnings
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # init ports for usonic sensor
    GPIO.setup(self.ECHO, GPIO.IN)                  # CONFIGURE THESE PROPERLY
    GPIO.setup(self.TRIGGER, GPIO.OUT)              # CONFIGURE THESE PROPERLY
    GPIO.output(self.TRIGGER, GPIO.LOW)
    time.sleep(0.3)                                 # time for pin to settle - took advice from usonic forum but didn't test

    # init ports for motion sensor
    GPIO.setup(self.PIR, GPIO.IN)                   # CONFIGURE THESE PROPERLY
    GPIO.setup(self.LED, GPIO.OUT)                  # CONFIGURE THESE PROPERLY

    # init LED
    GPIO.output(self.LED, GPIO.HIGH)
    print "GPIO configuration complete"

def checkheight(self):
    # check height routine
    us = usonic.usonic(self.TRIGGER, self.ECHO)           # initialize object
    distance = us.readdistance(self.TRIGGER, self.ECHO)   # get distance

    if abs(distance - self.lastheight) > self.percentheightchange * self.lastheight:
        self.lastheight = distance

    # start new thread
    heightthread = threading.Timer(self.heightcheckinterval, checkheight)
    heightthread.start()


def checkmotion(self):
    # has the last inmotion time been longer than the acceptable interval for outofmotion?
    if datetime.datetime.now() - self.lastmotiontime > datetime.timedelta(seconds=self.maxoutofmotiontime):
        print "In Checkmotion: timediff of last motion was too long. Must be out of motion. now: %s, last: %s, delta: %d" \
              % (str(datetime.datetime.now()), str(self.lastmotiontime), datetime.datetime.now() - self.lastmotiontime)
        # since motion senses are automatically updated, and we've exceeded the outofmotion time, we must be outofmotion
        self.motionflag = False
    # send an update
    sendmotion(self.motionflag)
    print "In Checkmotion: just send motion update of %s" % self.motionflag


    # start new thread
    motioncheckthread = threading.Timer(self.maxoutofmotiontime, checkmotion)
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

def main(self):
    # initialize everything
    initialize(self)

    # configure GPIO
    configureGPIO(self)

    # start timers
    # - interrupt every heightcheckinterval to check height
    heightthread = threading.Timer(self.heightcheckinterval, checkheight)
    heightthread.start()

    # - interrupt every maxoutofmotiontime to check motion
    motioncheckthread = threading.Timer(self.maxoutofmotiontime, checkmotion)
    motioncheckthread.start()

    # send hello message - THIS DOES NOTHING
    sendhello()

    # wait for stuff to happen
    while True:
        # wait to see motion and update lastmotiontime
        if GPIO(self.PIR, True):
            motionflag = True
            lastmotiontime = datetime.datetime.now()
        pass
    # release GPIO on keyboard interrupt (exit)