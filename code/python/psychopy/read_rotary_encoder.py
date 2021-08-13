from __future__ import division # important
from psychopy import core, visual, event, monitors, data, gui
import random, math, sys
from os import path
import numpy as np

from labjack import ljm

# --------------------------------------------Setting Up LabJack ------------------------------------------------------- #
#setup labjack t7
handle = ljm.openS("T7", "USB", "ANY")

digOut1 = 1000 #python library for labjack T7 uses this
              #funny address system check https://labjack.com/support/software/api/modbus/modbus-map
              #for details.

analogIn0 = 0
dataType = ljm.constants.FLOAT32

ljm.eWriteAddress(handle, analogIn0 dataType, 0)
ljm.d.readRegister(analogIn0)

# --------------------------------------------                   ------------------------------------------------------- #


#||||#|||||||||||||||||#||||#
#||||#~~~~~~~~~~~~~~~~~#||||#
#||||# Start programme #||||#
#||||#~~~~~~~~~~~~~~~~~#||||#
#||||#|||||||||||||||||#||||#



#while True:
    #ljm.eWriteAddress(handle, digOut1, dataType, 5)#analog out 5v
    ##read analog data from labjack
    #value = ljm.eReadName(handle, name, 0)
    ##check if there is an overflow for when the number is bigger than...
    #if value > 2^31:
    #   value = value-2^32; #everything bigger than 2^31 is negative (python overflow)
    
    ##ljm.eWriteAddress(handle, digOut1, dataType, 0)
    ### NB// 1700 is the end of the linear track -- will need a non
    ### manual way of getting this
    ### will need to update these when know size of ball (i.e. 4096 and 62.8)
    ### 62.8 refers to wheel circumference
    ### 4096 refers to counts per cycle (Kubler)
    #newPosition = (value/4096) * 62.8
    #timestamp = now
    #displacement = abs(newPosition - oldPosition)
    #if displacement < 2:
    #    LabJack.LJM.eWriteName(labjackhandle, 'DAC1', (displacement*5)/2)
    #else:
    #    LabJack.LJM.eWriteName(labjackhandle, 'DAC1', 5.0)
    #oldPosition = newPosition
    ##fwrite(fid, [timestamp, newPosition], 'double');

ljm.closeAll()