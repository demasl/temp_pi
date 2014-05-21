#!/usr/bin/env python

# import libraries
import RPi.GPIO as GPIO
import time
import urllib2

# import user files
from room_controller import RoomController
from LCD_controller import LCDController
import temp_sensor
import interface

# Set pin numbering scheme
GPIO.setmode(GPIO.BCM)

# Set time between readings (in seconds)
TIME_INTERVAL = 5

#Constants for outside temperature
OUTSIDE_NO = 5
OUTSIDE_NAME = "Outside"
OUTSIDE_LCD_E = 31
OUTSIDE_SENSOR = "4bc1bef"

#Room 1 Constants
ROOM_1_NO = 1
ROOM_1_NAME = "Living Room"
ROOM_1_LCD_E = 8
ROOM_1_SERVO_S = 15
ROOM_1_LIGHT_E = 10
ROOM_1_SENSOR = "4bc2a83"

#Room 2 Constants
ROOM_2_NO = 2
ROOM_2_NAME = "Kitchen"
ROOM_2_LCD_E = 28
ROOM_2_SERVO_S = 14
ROOM_2_LIGHT_E = 22
ROOM_2_SENSOR = "4bd4c02"

#Room 3 Constants
ROOM_3_NO = 3
ROOM_3_NAME = "Bedroom 1"
ROOM_3_LCD_E = 30
ROOM_3_SERVO_S = 11
ROOM_3_LIGHT_E = 27
ROOM_3_SENSOR = "4bcab8e"

#Room 4 Constants
ROOM_4_NO = 4
ROOM_4_NAME = "Bedroom 2"
ROOM_4_LCD_E = 29
ROOM_4_SERVO_S = 9
ROOM_4_LIGHT_E = 17
ROOM_4_SENSOR = "4bd7551"

# create room objects
room_1 = RoomController(ROOM_1_NO,ROOM_1_NAME,ROOM_1_SERVO_S,ROOM_1_LIGHT_E,ROOM_1_LCD_E,ROOM_1_SENSOR)
room_2 = RoomController(ROOM_2_NO,ROOM_2_NAME,ROOM_2_SERVO_S,ROOM_2_LIGHT_E,ROOM_2_LCD_E,ROOM_2_SENSOR)
room_3 = RoomController(ROOM_3_NO,ROOM_3_NAME,ROOM_3_SERVO_S,ROOM_3_LIGHT_E,ROOM_3_LCD_E,ROOM_3_SENSOR)
room_4 = RoomController(ROOM_4_NO,ROOM_4_NAME,ROOM_4_SERVO_S,ROOM_4_LIGHT_E,ROOM_4_LCD_E,ROOM_4_SENSOR)

# add room objects to list
rooms = [room_1,room_2,room_3,room_4]

#setup LCD for outside temperature display
OUTSIDE_LCD = LCDController(OUTSIDE_LCD_E)


# wait until server is running before running main code.
checker = True
while checker:
        try:
                data = urllib2.urlopen('http://localhost:3000/checkOk')
                if data.read() == 'ok':
                        checker = False                
        except :
                time.sleep(10)

def main():
    # read all temperature sensors
    temps = temp_sensor.read_all()
    # send readings to server
    interface.logTemps(OUTSIDE_NO,temps[OUTSIDE_SENSOR])
    for room in rooms:
        interface.logTemps(room.get_room_no(),temps[room.get_sensor_id()])
        
    #send data to LCD for outside temperature
    OUTSIDE_LCD.lcd_display(OUTSIDE_NAME,"%.1f"%(temps[OUTSIDE_SENSOR]))
        
    # check temperature for each room and adjust light/servo as needed    
    for room in rooms:
        # get user desired temperature
        set_temp = int(interface.readTemp(room.get_room_no()))
        # get current temperature sensor reading rounded to nearet integer
        read_temp = int(round(temps[room.get_sensor_id()]))
        # update LCD display for room
        room.update_lcd(temps[room.get_sensor_id()])
        #print(room.win_state())
        #print("Room : %s, Set Temp : %d, Read Temp : %d"%(room.get_room_no(),set_temp,read_temp))

        # temp tolerence set to +-0.5 deg.
        # Example: Desired temp = 22, reading between 21.5 to 22.4 is deemed as equal to desired temp. 
        
        # if current temp = desired temp
        if(read_temp==set_temp):
            room.light_off()
            # check if window is open
            if(room.win_state()):
                room.win_close()
        # if current temp < desired temp
        elif(read_temp<set_temp):
            # check if window is open
            if(room.win_state()):
                room.win_close()
            room.light_on()
        # if current temp > desired temp
        else:
            room.light_off()
            # check if window is closed
            if(room.win_state()==False):
                room.win_open()
              
try:
    # loop until interuptted
    while True:
        main()
        time.sleep(TIME_INTERVAL)
except KeyboardInterrupt:
    # reset all GPIO pins
    GPIO.cleanup()
