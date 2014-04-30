#__author__ = 'Michael Lynch'
# Temp Sensor functions

import os, glob, sys
from time import sleep

# Load the 1-wire modules (if modules are loaded on boot these two lines can be commented out)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Set up some variables
base_dir = '/sys/bus/w1/devices/'
device_file = '/w1_slave'

# Get all detected temp sensors
devices = glob.glob(base_dir + '28*')

# reads temp sensors raw information and returns it as a file
def read_temp_file(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


# gets temp sensor readings and returns information in a dictonary
# e.g. [{sensor1=22.4},{sensor2=22.8}]
def read_all():
    # create empty dictonary
    temp_dict ={}
    # for each detected sensor
    for  device in devices:
        device_dir = device + device_file
        raw_data = read_temp_file(device_dir)

        while raw_data[0].find('YES') == -1:
            sleep(0.1)
            raw_data = read_temp_file(device_dir)

        t_pos = raw_data[1].find('t=')
        if t_pos != -1:
            # get temperature reading from file
            temp = float(raw_data[1][t_pos+2:]) / 1000
            # add sensor name and temperature reading to dictonary
            temp_dict[device[28:]] = temp
    return temp_dict
