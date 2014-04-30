#__author__ = 'Michael Lynch'
# Servo Control
import RPi.GPIO as GPIO
import time

class ServoController:
    ZERO = 12.5         #Duty Cycle for 0deg
    ONE_EIGHTY = 2.5    #Duty Cycle for 180deg
    NINETY = 7.5        #Duty Cycle for 90deg
    CHANGETIME = 0.4    #Time that servo is active (in seconds)

    #define GPIO pin on creation
    def __init__(self,pin_num):
        self.pin_num = pin_num
        GPIO.setup(self.pin_num,GPIO.OUT)
           
    #set motor to 0 deg
    def zero(self):
        self.change(self.ZERO)
    #set motor to 180 deg
    def one_eighty(self):
        self.change(self.ONE_EIGHTY)
    #set motor to 90 deg
    def ninety(self):
        self.change(self.NINETY)
        
    # used to send PWM signal to servo
    def change(self,duty_cycle):
        self.pwm = GPIO.PWM(self.pin_num,50)
        self.pwm.start(duty_cycle)
        time.sleep(self.CHANGETIME)
        self.pwm.stop()
