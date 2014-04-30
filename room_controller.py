#__author__ = 'Michael Lynch'
# Room Controller

# import library for GPIO
import RPi.GPIO as GPIO
#import user defined classes
from servo_control import ServoController
from LCD_controller import LCDController


class RoomController:

    # runs when new RoomController is created
    def __init__(self,room_no,room_name,servo_pin,light_pin,lcd_pin,sensor):
        self.room_no = room_no
        self.room_name = room_name
        # create servocontroller object using given GPIO pin
        self.servo = ServoController(servo_pin)
        self.light_pin = light_pin
        # create lcdcontroller object using given GPIO pin
        self.lcd = LCDController(lcd_pin)
        self.sensor = sensor
        # set-up GPIO pin for light
        GPIO.setup(light_pin,GPIO.OUT)
        # set initial conditions to light off and window closed
        self.light_off()
        self.win_close()
        self.win = False

    # turn on light, relay switches on low
    def light_on(self):
        GPIO.output(self.light_pin, False)
        
    # turn off light
    def light_off(self):
        GPIO.output(self.light_pin, True)
        
    # send temperature sensor reading to LCD rounded to one decimal place
    def update_lcd(self,temp):
        self.lcd.lcd_display(self.room_name,"%.1f"%(temp))

    # returns temp sensor serial number 
    def get_sensor_id(self):
        return self.sensor
    
    # returns room number
    def get_room_no(self):
        return self.room_no

    # sets servo to 180deg to open window
    def win_open(self):
        self.servo.one_eighty()
        self.win = True
        
    # sets servo to 0deg to close window
    def win_close(self):
        self.servo.zero()
        self.win = False
        
    # returns true if window is open else false
    def win_state(self):
        return self.win
