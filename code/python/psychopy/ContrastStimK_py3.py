from __future__ import division # important
from psychopy import core, visual, event, monitors, data, gui
import random, math, sys
from os import path
import numpy as np

from labjack import ljm


#from psychopy.iohub.devices.daq.hw.labjack.win32.python27.pylabjack import u12 #comment back in
#from LabJackPython import u12
# go to API from the HELP drop menu to get information about the libraries and functions
# Demos -- timing -- TimeByFrames.py

#mon=monitors.Monitor('testmonitor')
mon= monitors.Monitor('stimMonitor')
mon.setDistance(17.0)
win=visual.Window([1920,1080], monitor=mon, fullscr=True, units='deg',waitBlanking=False, screen = 1)
win2=visual.Window([1920,1080], monitor=mon, fullscr=True, units='deg',waitBlanking=False, screen =2 )
# Laptop: [1024,7 68]
# Stimulus computer: [1920,1080]

#-------------------------------------------------------------------------#
                            
#-------------------------------------------------------------------------#

#||||#|||||||||||||||||#||||#
#||||#~~~~~~~~~~~~~~~~~#||||#
#||||#     Fill in     #||||#
#||||#~~~~~~~~~~~~~~~~~#||||#
#||||#|||||||||||||||||#||||#

info = {}
info['RefreshRate']=    60          # frames per second

#info['SF'] =            0.14        # cycles per degrees ---#--- Most sensitive for 0.04 cycles per degree (Niell & Stryker, 2008)
#info['TF'] =            2           # Optimal: 1.7 Hz (Niell & Stryker, 2008)
#info['size'] =          220

info['PreStim'] =       5           # seconds
info['StimLength']=     5           # seconds
info['ISI']=           20           # seconds

info['Position'] =     [0,0]        # coordinates

info['NumOfTrials'] =   6           # repetitions

info['orientations'] = 315

#orientations=[315]

#tf = [0.2,0.4,0.8,1.2,1.6,2,2.4]
contrastTrials = np.zeros(12)
contrastTrials[0:3] = 1
contrastTrials[3:6] = 2
contrastTrials[6:9] = 3
np.random.shuffle(contrastTrials)
print(contrastTrials)

tf = [2,2]
sf = [0.2,0.04]
size = [220,220]

nulpos=[0,0]
#position = [nulpos]
#position = [info['Position']]
#position = [nulpos,nulpos]
position = [info['Position'],nulpos]
#position = [info['Position'],info['Position'],nulpos,nulpos]

#Aquisition in Hz:
Aquisition = 10

info['mask'] =          'circle'
info['tex'] =           'sin'
# tex='sqr', high contrast || mask='raisedCos', like gauss, but than only at the very borders


###########################################################################
# list of combinations of directions:
# 0,180,90,270,45,225,135,315
# 0,45,90,135,180,225,270,315
# 0,90,45,135
# 0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# semi-random:
# 270,315,225,90,135,180,0,45
# 180,225,270,45,135,0,315,90
# 0,225,90,315,45,135,270,180

#-------------------------------------------------------------------------#
#~/^\~^~/\~^~/^\~^~/\~^~/^\~^~/\~^~/^\~^~/\~^~/^\~^~/\~^~/^\~^~/\~^~/^\~^~#
#-------------------------------------------------------------------------#

info['LenOri'] = len(tf)

#Calculate the amount of frames for aquisition:
nFrames = (((info['StimLength'] + info['ISI']) * info['LenOri']) * info['NumOfTrials']) + info['PreStim']
nFrames *= Aquisition
print('The amount of frames for aquisition is: ', nFrames)

info['ISI']*=info['RefreshRate']
info['StimLength']*=info['RefreshRate']
info['PreStim'] *= info['RefreshRate']
#info['TF'] /= info['RefreshRate']

info['NumOfStim'] = len(tf)


##########################################################################################################################
# --------------------------------------------Setting Up LabJack ------------------------------------------------------- #
#setup labjack t7
handle = ljm.openS("T7", "USB", "ANY")

digOut1 = 1000 #python library for labjack T7 uses this
              #funny address system check https://labjack.com/support/software/api/modbus/modbus-map
              #for details.
dataType = ljm.constants.FLOAT32

ljm.eWriteAddress(handle, digOut1, dataType, 0)
#setup labjack U12
#d = u12.U12(debug = False) #comment backin
#d.eDigitalOut(channel=1, state=0, writeD=0) #comment backin
#d.eDigitalOut(channel=3, state=0, writeD=0) #comment backin

# --------------------------------------------                   ------------------------------------------------------- #

##########################################################################################################################
#------------------------------------------------------------------------------------------------------------------------#
#|[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]||[*]|#
#------------------------------------------------------------------------------------------------------------------------#

#||||#|||||||||||||||||#||||#
#||||#~~~~~~~~~~~~~~~~~#||||#
#||||# Start programme #||||#
#||||#~~~~~~~~~~~~~~~~~#||||#
#||||#|||||||||||||||||#||||#

#d.eDigitalOut(channel=1, state=1, writeD=0) #comment backin

# initialise the gratings

gratingsLow = visual.GratingStim(win, units='deg', mask=info['mask'], tex=info['tex'], pos=info['Position'], ori=info['orientations'], contrast = 0.25)
gratingsHigh = visual.GratingStim(win, units='deg', mask=info['mask'], tex=info['tex'], pos=info['Position'], ori=info['orientations'], contrast = 1.)
gratingsLowMir = visual.GratingStim(win2, units='deg', mask=info['mask'], tex=info['tex'], pos=info['Position'], ori=45, contrast = 0.25)
gratingsHighMir = visual.GratingStim(win2, units='deg', mask=info['mask'], tex=info['tex'], pos=info['Position'], ori=45, contrast = 1.)
gratingsMid = visual.GratingStim(win, units='deg', mask=info['mask'], tex=info['tex'], pos=info['Position'], ori=info['orientations'], contrast = 0.63)
gratingsVLow = visual.GratingStim(win, units='deg', mask=info['mask'], tex=info['tex'], pos=info['Position'], ori=info['orientations'], contrast = 0.05)
gratingsMidMir = visual.GratingStim(win2, units='deg', mask=info['mask'], tex=info['tex'], pos=info['Position'], ori=45, contrast = 0.63)
gratingsVLowMir = visual.GratingStim(win2, units='deg', mask=info['mask'], tex=info['tex'], pos=info['Position'], ori=45, contrast = 0.05)

for frameN in range(info['PreStim']):
    win.flip()
    win2.flip()

for NumTrials in range(info['NumOfTrials']):

    oriN=0
    TF=0
    SF=0
    SIZE=0
    POSI=0
    if contrastTrials[NumTrials] == 1:
        gratings = gratingsLow
        gratingsMir = gratingsLowMir
        vo = 3
    elif contrastTrials[NumTrials] == 2:
        gratings = gratingsMid
        gratingsMir = gratingsMidMir
        vo = 4
    elif contrastTrials[NumTrials] == 3:
        gratings = gratingsHigh
        gratingsMir = gratingsHighMir
        vo = 5
    else:
        gratings = gratingsVLow
        gratingsMir = gratingsVLowMir
        vo = 2
    
    
    for thisTrial in range(info['NumOfStim']):
        ljm.eWriteAddress(handle, digOut1, dataType, vo)
        for frameN in range(info['StimLength']):
            
            # Cntrl & [ or ] to shift line in or out the loop
            
            gratings.setPhase(tf[TF]/info['RefreshRate'],'-') # the '+' is to make the 0.05 incremental, it increeases with every flip, otherwise it stays stanionary
            gratings.sf = sf[SF]
            gratings.size = size[SIZE]
            gratings.pos = position[POSI]
            gratingsMir.setPhase(tf[TF]/info['RefreshRate'],'+') # the '+' is to make the 0.05 incremental, it increeases with every flip, otherwise it stays stanionary
            gratingsMir.sf = sf[SF]
            gratingsMir.size = size[SIZE]
            gratingsMir.pos = position[POSI]
            #gratings.sf = info['SF']
            #grating.setSize(info['Size'])
            gratings.draw()
            win.flip()
            gratingsMir.draw()
            win2.flip()
           
            if event.getKeys(keyList=['escape','q']):
                ljm.eWriteAddress(handle, digOut1, dataType, 0)
                ljm.closeAll()
                win.close()
                win2.close()
                core.quit() # escape stimulus if you press 'q'
                win.flip()
                win2.flip()
        ljm.eWriteAddress(handle, digOut1, dataType, 0)
        
        for frameN in range(info['ISI']):
            win.flip()
            win2.flip()

        print (tf [TF])
        TF += 1
        SF += 1
        SIZE += 1
        POSI += 1
        
    
ljm.eWriteAddress(handle, digOut1, dataType, 0)
ljm.closeAll()