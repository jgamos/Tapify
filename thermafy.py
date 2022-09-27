import RPi.GPIO as GPIO
import paramiko
import subprocess
import logging
import lcddriver
import time
import os
import sh
import random
import string

from Adafruit_Thermal import *
from subprocess import Popen
from threading import Thread
from os.path import exists

printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)
display = lcddriver.lcd()
logging.getLogger("paramiko").setLevel(logging.WARNING)
paramiko.util.log_to_file("/home/pi/paramiko.log")

proxy = None
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.1.1', port=22, username='pi')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

def firstFunction():
        global counter
        global ts
        count = 1
        counter = 0
        ts = time.time()

        while True:
                if (count == 1):
                        GPIO.wait_for_edge(27, GPIO.RISING)
                        counter += 1
                        print("Coins comming ! (%s)") % counter
                        display.lcd_clear()
                        display.lcd_display_string("Credits:", 1)
                        display.lcd_display_string(str(counter), 2)
                        ts = time.time()

def secondFunction():
        global count
        global counter
        global ts

        while True:
                cts = ts + 20
                if (cts < time.time()):
                        print("Finished with %s coins") % counter
                        count = 0
                        randomString = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(6))
                        for i in range(1):
                        	print randomString
                        	GPIO.output(23, False)
                        	printer.wake()
                        	#display.lcd_clear()
                        	#display.lcd_display_string("Code:", 1)
                        	#display.lcd_display_string(str(randomString), 2)
                        	#time.sleep(30)

                        	if (counter == 1):
                        		stdin, stdout, stderr = client.exec_command('ip hotspot user add name=%s password=tapify profile=default limit-uptime=6m' % randomString)
                        		printer.inverseOn()
                        		printer.println("  WiFi Hotspot  ")
                        		printer.inverseOff()
                        		printer.feed(1)
                        		printer.justify('C')
                        		printer.println("Code: %s "% randomString)
                        		printer.println("Uptime: 6 min ")
                        		display.lcd_clear()
                                display.lcd_display_string("Uptime: 6 min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                        	if (counter == 2):
                        		stdin, stdout, stderr = client.exec_command('ip hotspot user add name=%s password=tapify profile=default limit-uptime=12m' % randomString)
                        		printer.inverseOn()
                        		printer.println("  WiFi Hotspot  ")
                        		printer.inverseOff()
                        		printer.feed(1)
                        		printer.justify('C')
                        		printer.println("Code: %s "% randomString)
                        		printer.println("Uptime: 12 min ")
                        		display.lcd_clear()
                                display.lcd_display_string("Uptime: 12 min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                        	if (counter == 3):
                        		stdin, stdout, stderr = client.exec_command('ip hotspot user add name=%s password=tapify profile=default limit-uptime=18m' % randomString)
                        		printer.inverseOn()
                        		printer.println("  WiFi Hotspot  ")
                        		printer.inverseOff()
                        		printer.feed(1)
                        		printer.justify('C')
                        		printer.println("Code: %s "% randomString)
                        		printer.println("Uptime: 18 min ")
                        		display.lcd_clear()
                                display.lcd_display_string("Uptime: 18 min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                        
                        counter = 0
                        count = 1
                        print("Done Processing")
                        printer.feed(3)
                        printer.sleep()
                        time.sleep(1)
                        

                if (counter == 0):
                        ts = time.time()
                        display.lcd_clear()
                        display.lcd_display_string("   Welcome to   ", 1)
                        display.lcd_display_string("  WiFi Hotspot  ", 2)
                        GPIO.output(23, True)
                        time.sleep(1)



try:
        t1 = Thread(target = firstFunction)
        t2 = Thread(target = secondFunction)

        t1.start()
        t2.start()

except KeyboardInterrupt:
        t1.stop()
        t2.stop()
        GPIO.cleanup()