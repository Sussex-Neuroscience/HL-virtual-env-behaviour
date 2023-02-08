from machine import Pin
import time

#declare pin variables
rotAPin = 15
rotBPin = 2
stopButtonPin = 16
triggerOutPin = 17
#add a pin as input for the trigger from recording device.

#define pins
rotA = Pin(rotAPin,Pin.IN)
rotB = Pin(rotBPin,Pin.IN)
stopButton = Pin(stopButtonPin,Pin.IN)
triggerOut = Pin(triggerOutPin,Pin.OUT)


oldRotAstate = 0
newRotAstate = 0
#rot_a_state_new = 0

#millis --> time1 = time.get
#according to rotary encoder detection 
    ### 62.8 refers to wheel circumference
    ### 1024 refers to counts per cycle (Kubler)
    ### 2*pi*r total circunference
    ### minimal steps are 62.8/1024

cyclesRevolution = 1024
wheelCircun = 62.8

startStep = time.ticks_ms() # get millisecond counter
endStep = startStep

while 1:
#while stopButtonPin == 0:
    StartStep=time.ticks_ms()
    while newRotAstate == oldRotAstate:
        newRotAstate = rotA.value()
        triggerOut.value(0)
        
        
    if newRotAstate == 1 and oldRotAstate == 0:
        print("rising edge")
        
        endStep = time.ticks_ms()
        
        duration = endStep-StartStep
        print(duration)
        triggerOut.value(1)
        
    oldRotAstate = newRotAstate
    

    
    
    