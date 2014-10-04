__author__ = 'mperkins'

import threading
import time
import RPi.GPIO as GPIO
import urllib2
import json
import datetime
import usonic


class pi:

    def __init__(self):
        # GLOBAL
        # - motion flag
        # - height check interval
        self.heightcheckinterval = 5                   # five mins
        self.motionflag = False                         # default is "motion not detected"
        self.lastheight = 0.00
        self.percentheightchange = 0.05                 # percent change in height that is needed to update the height information
        self.lastmotiontime = datetime.datetime.now()
        self.maxoutofmotiontime = 5                    # five mins
        self.PIR = 17
        self.LED = 22
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
        #print "initialize ULTRA SONIC object"
        us = usonic.usonic(self.TRIGGER, self.ECHO)           # initialize object
        #print "get distance ..."
        distance = us.readdistance(self.TRIGGER, self.ECHO)   # get distance
        #print distance

        if abs(distance - self.lastheight) > self.percentheightchange * self.lastheight:
            # distance has changed
            self.lastheight = distance
            print "The new DISTANCE is: %s" % str(distance)
        else:
            print "The DISTANCE HASN'T CHANGED"

        # send an update
        pi.sendheight(self.lastheight)

        # start new thread
        heightthread = threading.Timer(self.heightcheckinterval, self.checkheight)
        heightthread.daemon = True
        heightthread.start()


    def checkmotion(self):
        # has the last inmotion time been longer than the acceptable interval for outofmotion?
        if datetime.datetime.now() - self.lastmotiontime > datetime.timedelta(seconds=self.maxoutofmotiontime):
            #print "In Checkmotion: timediff of last motion was too long. Must be out of motion. now: %s, last: %s, delta: %d" \
            #      % (str(datetime.datetime.now()), str(self.lastmotiontime), datetime.datetime.now() - self.lastmotiontime)
            # since motion senses are automatically updated, and we've exceeded the outofmotion time, we must be outofmotion
            self.motionflag = False
        # send an update
        pi.sendmotion(self.motionflag)
        print "In Checkmotion: just send motion update of %s" % self.motionflag


        # start new thread
        motioncheckthread = threading.Timer(self.maxoutofmotiontime, self.checkmotion)
        motioncheckthread.daemon = True
        motioncheckthread.start()


    def sendheight(self, distance):
        jdata = json.dumps({"sensor": "stand", "time":str(datetime.datetime.now()), "distance": distance})
        print "Sending HEIGHT event to platform with following contents: %s" % jdata
        try:
            response = urllib2.urlopen("http://flocx.mattperkins.net/standup", jdata)
            print ("Response from sending height update: ")
            print response.read()
        except urllib2.HTTPError, e:
            print "Didn't get a response from HEIGHT message sent to http://flocx.mattperkins.net/standup"
            print e




    def sendmotion(self, state):
        jdata = json.dumps({"sensor": "motion", "time":str(datetime.datetime.now()), "motion": state})
        try:
            print "Sending MOTION event to platform with following contents: %s" % jdata
            response = urllib2.urlopen("http://flocx.mattperkins.net/standup", jdata)
            print ("Response from sending motion update: ")
            print response.read()
        except urllib2.HTTPError, e:
            print "Didn't get a response from MOTION message sent to http://flocx.mattperkins.net/standup"
            print e

    def sendhello(self):
        # send a formated message and wait for canned response
        # if response is correct, turn on/off an LED to show that things are working
        print "Platform responded"


    def main(self):
        # initialize everything
        #initialize()
        #def initialize(self):

        # configure GPIO
        pi.configureGPIO()

        # start timers
        # - interrupt every heightcheckinterval to check height
        print "Starting height timer ..."
        heightthread = threading.Timer(self.heightcheckinterval, pi.checkheight)
        heightthread.daemon = True
        heightthread.start()

        # - interrupt every maxoutofmotiontime to check motion
        print "Starting motion timer ..."
        motioncheckthread = threading.Timer(self.maxoutofmotiontime, pi.checkmotion)
        motioncheckthread.daemon = True
        motioncheckthread.start()

        # send hello message - THIS DOES NOTHING
        pi.sendhello()

        # wait for stuff to happen
        print "Starting infinite while loop ... "
        while True:
            # wait to see motion and update lastmotiontime
            if GPIO.input(self.PIR):
                self.motionflag = True
                self.lastmotiontime = datetime.datetime.now()
                GPIO.output(self.LED, True)
            else:
                GPIO.output(self.LED, False)

        # release GPIO on keyboard interrupt (exit)
    
if __name__ == "__main__":
    print "Directing to main()"
    try:
        pi = pi()
        pi.main()
    except KeyboardInterrupt:
        print "Killing threads and closing GPIO ..."
    finally:
        GPIO.cleanup()
        print "GPIO cleanup done"

