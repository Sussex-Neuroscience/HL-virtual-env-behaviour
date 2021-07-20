# HL-virtual-env-behaviour
A behavioural task for mice in virtual environments

---
## requirements:

### Software:    
- Psychopy
- 3D virtual environment system (currently Matlab)

### Hardware:  
- Raspberry Pi
- LabJack
- 2P setup

---
## project log


## **19/07/2021** Psychopy

- Currenlty the system uses Psychopy2, which is built on Python2. As Python 2 support ended more than [year ago](https://www.python.org/doc/sunset-python-2/) the first thing to do for this project is port all code that still used Python2 to Python3. Luckly, Psychopy most recent version is already python3 and there is a prepared conda environmet for it. So it should be easy to install and translate Python2 to Python3.

The tutorial to install Psychopy3 is [here](https://www.psychopy.org/download.html) (scroll down to the Miniconda/anaconda bit of the page).

## **19/07/2021** LabJack

- The current system uses a library from Psychopy to control labjack. I don't know if this library is present on the current implementation of Psychopy, but the company making labjack has also created a python wrapper to control its devices. So this could be an alternative. if there is in psychopy a library to control LJ, I would just use that, as it diminishes the number of dependencies of the project.  
