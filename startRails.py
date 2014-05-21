#!/usr/bin/env python 
import subprocess
import os
import time


os.chdir('/home/pi/RasPiServer')
os.system('rails s')