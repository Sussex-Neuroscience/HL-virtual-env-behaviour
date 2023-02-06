from machine import Pin
import time

#declare pin variables
rot_a_pin = 15
rot_b_pin = 2
#add a pin as input for the trigger from recording device.

#define pins
rot_a = Pin(15,Pin.IN)
rot_b = Pin(2,Pin.IN)

rot_a_state_old = 0
rot_a_state_new = 0

#millis --> time1 = time.get

    ### 62.8 refers to wheel circumference
    ### 4096 refers to counts per cycle (Kubler)
    #newPosition = (value/4096) * 62.8

for i in range(1000):
    rot_a_state_old = rot_a.value()
    time.sleep_ms(5)
    rot_a_state_new =  rot_a.value()
    
    
    