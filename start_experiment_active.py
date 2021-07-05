import RPi.GPIO as GPIO
import time
import picamera
import sys
import os
import threading
import random
from cameraThread import CameraThread
from mockThread import MockThread
from rewardThread import RewardThread
import datetime


#Config GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up for the capicitive sensor (i.e. licksensor)
inPin = 20
outPin = 21
timeout = 10000

# Set up Servo motor to deliver reward
rewardPin = 02
GPIO.setup(rewardPin, GPIO.OUT)
pwm=GPIO.PWM(rewardPin, 50)

# Set up PiCamera as well as the thread that will handle the camera
lightPin = 04
GPIO.setup(lightPin,GPIO.OUT)
camera = picamera.PiCamera()
camera.rotation=180
cameraThread = None

# Set up reward trigger pin
rewardTrigPin = 25
GPIO.setup(rewardTrigPin, GPIO.IN)
triggered = 0

# Set up pin to trigger start of an experiment
triggerPin = 26
GPIO.setup(triggerPin, GPIO.IN)

# Distractor motor
voltPin = 32
rewardMockPin = 24
# GPIO.setup(rewardMockPin, GPIO.IN)
lickPin = 24
GPIO.setup(lickPin , GPIO.OUT)


def CapRead(inPin,outPin):
    """ Determines the output of the capicitive sensor attached to inPin (+) and
    outPin (-). """
    allTotal = 0
    for j in range(0,10):
        total = 0
        # set Send Pin Register low
        GPIO.setup(outPin, GPIO.OUT)
        GPIO.output(outPin, GPIO.LOW)

        # set receivePin Register low to make sure pullups are off
        GPIO.setup(inPin, GPIO.OUT)
        GPIO.output(inPin, GPIO.LOW)
        GPIO.setup(inPin, GPIO.IN)

        # set send Pin High
        GPIO.output(outPin, GPIO.HIGH)

        # while receive pin is LOW AND total is positive value
        while( GPIO.input(inPin) == GPIO.LOW and total < timeout ):
            total+=1

        if ( total > timeout ):
            return -2 # total variable over timeout

         # set receive pin HIGH briefly to charge up fully - because the while loop above will exit when pin is ~ 2.5V
        GPIO.setup( inPin, GPIO.OUT )
        GPIO.output( inPin, GPIO.HIGH )
        GPIO.setup( inPin, GPIO.IN )

        # set send Pin LOW
        GPIO.output( outPin, GPIO.LOW )

        # while receive pin is HIGH  AND total is less than timeout
        while (GPIO.input(inPin)==GPIO.HIGH and total < timeout) :
            total+=1

        if ( total >= timeout ):
            total = -2

        allTotal += total
    return allTotal


def calibrateCapSensor(inPin, outPin, its):
    """ Calibrates the capicitive sensor before the start of an experiment, to
    know the baseline resistance. The baseline is used later to compare lick
    events to.
    """
    print('Calibrating Sensor...')
    allTotal = 0
    for x in range(its):
        allTotal += CapRead(inPin,outPin)
    print('Calibration complete')
    return allTotal/its

def setDir(isForward, pwm, pinNo):
    """ Set the direction of the servo motor.
    """
    if isForward:
	duty = 5
    else:
	duty = 10
    pwm.ChangeDutyCycle(duty)

def stopPwm(pwm, pinNo):
    """ Stop the servo motor.
    """
    duty = 7.5
    pwm.ChangeDutyCycle(duty)

def deliverReward(startTime, pwm, rewardPin):
    """ Function that operates the servo motor to deliver the reward. This
    function will be executed on a thread as to now stop the recording during
    the experiment"""
    pwm.start(0)
    timepoint = time.time()-startTime
    setDir(1,pwm,rewardPin)
    time.sleep(0.25)
    setDir(0,pwm,rewardPin)
    time.sleep(0.1)
    pwm.stop()
    time.sleep(1)

# Run the experiment
try:
    while True:
        # This if loop pauses the code until the camera has been properly
        # closed. This is to ensure multiple experiments can be run one after
        # another
        if cameraThread is not None:
            cameraThread.join()

        isRecording = False # Keeps track of whether an experiment is ongoing
        GPIO.output(lickPin,GPIO.LOW)

        # Calibrating capicitive sensor
        thresh = calibrateCapSensor(inPin, outPin, 200)*1.5


        # Prep for measuring
        startTime = 0

        # Set up camera
        camera.resolution = (1920, 1080)
        camera.framerate = 15
        stopper = threading.Event() # Used to stop the camera thread
        cameraThread = CameraThread(lightPin, camera, record, stopper)

        #Set up reward thread (reward motor will run on this)
	    rewardTrigger = threading.Event()
        rewardStopper = threading.Event()
	    rewardThread = RewardThread(pwm, rewardPin, rewardStopper,rewardTrigger)


        print('Waiting for trigger...') # User information

        # Wait for a trigger so recording is synchronized with environment and
        # 2P scope
        while not isRecording:
            if GPIO.input(triggerPin):
    	           isRecording = True
                   break

        # Start experiment
        print('Experiment Started')

        now = datetime.datetime.now()
        eventFile = open(now.strftime("%H%M")+'licks'+'.csv', 'w')
        startTime = time.time()

        # Record Camera on a Thread
        cameraThread.setFileName(now.strftime("%H%M"))
        cameraThread.start()

        # Start reward thread
        rewardThread.start()

	    count = 0
	    rewarded = 0
        thresh = 120 # Should probably be done by a calibration (used to be through calibrateCapSensor function)
        # Keep recording as long as there isn't another trigger signal
        while isRecording:
            # Stop recording when receiving input on the trigger pin second time
            if time.time()-startTime > 1 and GPIO.input(triggerPin):
    	        isRecording = False
                break

            value = CapRead(inPin, outPin) # Read the lick sensor
	        print(value)
	        if value > thresh:
		        GPIO.output(lickPin, GPIO.HIGH) # alert computer the mouse has licked
	        else:
		        GPIO.output(lickPin,GPIO.LOW)
            # if the mouse licked and is not already being given reward start reward thread
		    if not rewarded and GPIO.input(rewardTrigPin):
		        rewardTrigger.set()
		        rewarded = 1
		        print('Rewarded')


            # Write time and capacitive sensor value
            eventFile.write('{}, {} \n'.format(time.time()-startTime, value))
		    rewarded = 0

        stopper.set() # When experiment is stopped, end the camera thread
	    rewardStopper.set()
except KeyboardInterrupt:
        print 'Interrupted'
        GPIO.output(4,0)
        camera.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
