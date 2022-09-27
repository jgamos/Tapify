import RPi.GPIO as GPIO
import paramiko
import subprocess
import logging
import lcddriver
import time
import os
import sh

from subprocess import Popen
from threading import Thread
from os.path import exists

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
                        display.lcd_display_string("Credits:       ", 1)
                        display.lcd_display_string(str(counter), 2)
                        ts = time.time()
                        f = open('/var/www/html/load.php','w')
                        message = """%s""" % counter
                        f.write(message)
                        f.close()

def secondFunction():
        global count
        global counter
        global ts
        global result
        global tracking
        global timer
        global hostname

        timer = 0
        tracking = ""
        result = ""
        hostname = ""
        button = ""
        database = ""
        monitor = ""

        while True:

                cts = ts + 20
                if (cts < time.time()):
                        print("Finished with %s coins") % counter
                        count = 0
                        # Tracing devices
                        if exists("/home/pi/temp/Device.txt") == True:
                                tracking = 1
                                print "Device detected"
                                # Check user in usermanager
                                mac_user = open('/home/pi/temp/Device.txt').read().strip()
                                command = 'tool user-manager user print where username=%s' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                                output = stdout.readlines()
                                file = open('/home/pi/temp/Radius.txt', 'w')
                                file.write(''.join(output))
                                file.close()
                                # Verify user if matching to the ongoing process
                                mac = open('/home/pi/temp/Device.txt').read().strip()
                                text = "%s" % (mac)
                                data = open("/home/pi/temp/Radius.txt").read()
                                if text in data:
                                        database = 1
                                        print "Existing in Radius"
                                else:
                                        database = 0
                                        print "Non-Existent in Radius"
                        elif exists("/home/pi/temp/Device.txt") == False:
                                tracking = 0
                        # End of Tracing devices

                # Coin = User Account Process
                        # 1 Coin
                        if (counter == 1 and tracking == 1 and database == 1):
                                print "Existing Account Usermanager"
                                display.lcd_clear()
                                display.lcd_display_string("Uptime: 6min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                                mac_user = open('/home/pi/temp/Device.txt').read().strip()
                                command = 'tool user-manager user create-and-activate-profile profile=6min customer=admin numbers=[find username=%s]' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                        elif (counter == 1 and tracking == 1 and database == 0):
                                print "New Account Usermanager"
                                display.lcd_clear()
                                display.lcd_display_string("Uptime: 6min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                                mac_user = open('/home/pi/temp/Device.txt').read().strip()
                                command = 'tool user-manager user add customer=admin username=%s password=123456' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                                command = 'tool user-manager user create-and-activate-profile profile=6min customer=admin numbers=[find username=%s]' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                        elif (counter == 1 and tracking == 0):
                                print ("No device detected")
                        # 2 Coins
                        if (counter == 2 and tracking == 1 and database == 1):
                                print "Existing Account Usermanager"
                                display.lcd_clear()
                                display.lcd_display_string("Uptime: 12min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                                mac_user = open('/home/pi/temp/Device.txt').read().strip()
                                command = 'tool user-manager user create-and-activate-profile profile=12min customer=admin numbers=[find username=%s]' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                        elif (counter == 2 and tracking == 1 and database == 0):
                                display.lcd_clear()
                                display.lcd_display_string("Uptime: 12min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                                mac_user = open('/home/pi/temp/Device.txt').read().strip()
                                command = 'tool user-manager user add customer=admin username=%s password=123456' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                                command = 'tool user-manager user create-and-activate-profile profile=12min customer=admin numbers=[find username=%s]' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                        elif (counter == 2 and tracking == 0):
                                print ("No device detected")
                        # 3 Coins
                        if (counter == 3 and tracking == 1 and database == 1):
                                print "Existing Account Usermanager"
                                display.lcd_clear()
                                display.lcd_display_string("Uptime: 18min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                                mac_user = open('/home/pi/temp/Device.txt').read().strip()
                                command = 'tool user-manager user create-and-activate-profile profile=18min customer=admin numbers=[find username=%s]' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                        elif (counter == 3 and tracking == 1 and database == 0):
                                display.lcd_clear()
                                display.lcd_display_string("Uptime: 18min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                                mac_user = open('/home/pi/temp/Device.txt').read().strip()
                                command = 'tool user-manager user add customer=admin username=%s password=123456' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                                command = 'tool user-manager user create-and-activate-profile profile=18min customer=admin numbers=[find username=%s]' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                        elif (counter == 3 and tracking == 0):
                                print ("No device detected")
                        # 4 Coins
                        if (counter == 4 and tracking == 1 and database == 1):
                                print "Existing Account Usermanager"
                                display.lcd_clear()
                                display.lcd_display_string("Uptime: 24min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                                mac_user = open('/home/pi/temp/Device.txt').read().strip()
                                command = 'tool user-manager user create-and-activate-profile profile=24min customer=admin numbers=[find username=%s]' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                        elif (counter == 4 and tracking == 1 and database == 0):
                                display.lcd_clear()
                                display.lcd_display_string("Uptime: 24min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                                mac_user = open('/home/pi/temp/Device.txt').read().strip()
                                command = 'tool user-manager user add customer=admin username=%s password=123456' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                                command = 'tool user-manager user create-and-activate-profile profile=24min customer=admin numbers=[find username=%s]' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                        elif (counter == 4 and tracking == 0):
                                print ("No device detected")
                        # 5 Coins
                        if (counter == 5 and tracking == 1 and database == 1):
                                print "Existing Account Usermanager"
                                display.lcd_clear()
                                display.lcd_display_string("Uptime: 30min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                                mac_user = open('/home/pi/temp/Device.txt').read().strip()
                                command = 'tool user-manager user create-and-activate-profile profile=30min customer=admin numbers=[find username=%s]' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                        elif (counter == 5 and tracking == 1 and database == 0):
                                display.lcd_clear()
                                display.lcd_display_string("Uptime: 30min    ", 1)
                                display.lcd_display_string("Device Connected", 2)
                                mac_user = open('/home/pi/temp/Device.txt').read().strip()
                                command = 'tool user-manager user add customer=admin username=%s password=123456' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                                command = 'tool user-manager user create-and-activate-profile profile=30min customer=admin numbers=[find username=%s]' % (mac_user)
                                stdin, stdout, stderr = client.exec_command(command)
                        elif (counter == 5 and tracking == 0):
                                print ("No device detected")

                        counter = 0
                        count = 1

                        if exists("/home/pi/temp/Device.txt") == True:
                                stdin, stdout, stderr = client.exec_command('system script run cancelled')
                                f = open('/var/www/html/load.php','w')
                                message = """%s""" % counter
                                f.write(message)
                                f.close()
                                sh.rm(sh.glob('/home/pi/temp/*'))
                                print("Done Processing")
                        elif exists("/home/pi/temp/Device.txt") == False:
                                f = open('/var/www/html/load.php','w')
                                message = """%s""" % counter
                                f.write(message)
                                f.close()
                                print "Nothing to do"
                # End of Coin Process Selection
                        
                # Counter routine
                if (counter == 0):
                        ts = time.time()
                        time.sleep(1)
                # End of Counter routine

                # Button Monitoring
                button_state = GPIO.input(26)
                if button_state == False:
                        button = 1
                        counter = 0
                        GPIO.output(18, True)
                        time.sleep(1)
                else:
                        GPIO.output(18, False)
                        button = 0

                if (button == 1 and monitor == 1):
                        sh.rm(sh.glob('/home/pi/temp/*'))
                        f = open('/var/www/html/load.php','w')
                        message = """%s""" % counter
                        f.write(message)
                        f.close()
                        print "Doing Some Cleanup"
                elif (button == 1 and monitor == 0):
                        f = open('/var/www/html/load.php','w')
                        message = """%s""" % counter
                        f.write(message)
                        f.close()
                        print "Doing Some Cleanup"
                # End of Button Monitoring

                # Device IP Monitoring (Enable Coin Acceptor)
                if exists("/home/pi/temp/Device.txt") == True:
                        monitor = 1
                        GPIO.output(23, True)
                elif exists("/home/pi/temp/Device.txt") == False:
                        monitor = 0
                        GPIO.output(23, False)
                        display.lcd_clear()
                        display.lcd_display_string("   Welcome to   ", 1)
                        display.lcd_display_string("  WiFi Hotspot  ", 2)
                # End of Device IP Monitoring

                # Expiration tracking
                one_minute_ago = time.time() - 60
                folder = '/home/pi/temp'
                os.chdir(folder)
                for somefile in os.listdir('.'):
                        st=os.stat(somefile)
                        mtime=st.st_mtime
                        if mtime < one_minute_ago:
                                timer = 1
                                sh.rm(sh.glob('/home/pi/temp/*'))
                                stdin, stdout, stderr = client.exec_command('system script run cancelled')
                                print "Cleaning Expired Device"
                                timer = 0
                                time.sleep(1)
                # End of Expiration tracking

try:
        t1 = Thread(target = firstFunction)
        t2 = Thread(target = secondFunction)

        t1.start()
        t2.start()

except KeyboardInterrupt:
        t1.stop()
        t2.stop()
        GPIO.cleanup()