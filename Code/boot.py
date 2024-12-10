# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import network
import time
import ntptime
import machine

#esp.osdebug(None)
print('running boot')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# change PASSWORD to the code you received from Berkeley-IoT as your password when you registered your ESP32
password = 'PASSWORD'

# attempt to connect 30 times
# print a fail message or a success message
if wlan.isconnected():
    print('connected')
    wlan.disconnect()
    time.sleep(1)
    print('disconnected')
    
if not wlan.isconnected():
    print('connecting to network...')
    # you can connect to other networks by editing the next line with suitable network_name and password
    wlan.connect('Berkeley-IoT', password)
    time.sleep(2)

    tries = 0
    while not wlan.isconnected() and tries < 30:
        print('...')
        wlan.connect('Berkeley-IoT', password)

        time.sleep(2)
        tries = tries + 1
    print('network config:', wlan.ifconfig())
    
    
    if wlan.isconnected():
        print("WiFi connected at", wlan.ifconfig()[0])
    else:
        print("Mission failed")
 
        
# print current date and time using real-time clock

print("inquire NTP server for the time")
ntptime.settime()

now = time.localtime(time.time())

print("Local Time synchronized with NTP")

year, month, day, hour, minute, second, _,_ = now
formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day, hour, minute, second)
print(formatted_time)


