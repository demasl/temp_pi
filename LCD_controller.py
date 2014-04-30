#!/usr/bin/python

#__author__ = 'Michael Lynch'
# LCD Controller

# The wiring for each LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

# import libraries
import RPi.GPIO as GPIO
import time

# Define PINs
LCD_RS = 7
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

class LCDController:
  
  # run on creation of a new LCDController object.
  def __init__(self,enable):
    # set LCD enable pin
    self.enable = enable
    GPIO.setup(self.enable, GPIO.OUT)
    # setup all required GPIO pins
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    # init LCD display
    self.lcd_init()

  def lcd_display(self,room,temp):
    self.lcd_byte(LCD_LINE_1, LCD_CMD)
    self.lcd_string(str(room))
    self.lcd_byte(LCD_LINE_2, LCD_CMD)
    self.lcd_string(str(temp))

  def lcd_init(self):
    # Initialise display
    self.lcd_byte(0x33,LCD_CMD)
    self.lcd_byte(0x32,LCD_CMD)
    self.lcd_byte(0x28,LCD_CMD)
    self.lcd_byte(0x0C,LCD_CMD)
    self.lcd_byte(0x06,LCD_CMD)
    self.lcd_byte(0x01,LCD_CMD)
    
  def lcd_string(self,message):
    # Send string to display
    message = message.ljust(LCD_WIDTH," ")
    for i in range(LCD_WIDTH):
      self.lcd_byte(ord(message[i]),LCD_CHR)
      
  def lcd_byte(self,bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
    # Define GPIO to LCD mapping
    GPIO.output(LCD_RS, mode) # RS
    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
      GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
      GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
      GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
      GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    self.toggle_enable()
    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
      GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
      GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
      GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
      GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    self.toggle_enable()
    
  # used to toggle enable pin for LCD
  def toggle_enable(self):
    time.sleep(E_DELAY)
    GPIO.output(self.enable, True)
    time.sleep(E_PULSE)
    GPIO.output(self.enable, False)
    time.sleep(E_DELAY)