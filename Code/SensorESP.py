import network
import espnow
from hcsr04 import HCSR04
import time
from time import sleep
from machine import Pin
from machine import I2C
from binascii import hexlify

# Initialize WLAN interface for ESP-NOW
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  # For ESP8266

# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)

peer = b'\x14\x2b\x2f\xaf\xf2\x48'  # MAC address of peer's wifi interface
e.add_peer(peer)

#IMU I2C initialization
i2c = I2C(1,scl=Pin(14),sda=Pin(22),freq=400000)

for i in range(len(i2c.scan())):
	print(hex(i2c.scan()[i]))

#IMU helper
def WHOAMI(i2caddr):
	whoami = i2c.readfrom_mem(i2caddr,0x0F,1)
	print(hex(int.from_bytes(whoami,"little")))

def Temperature(i2caddr):
	temperature = i2c.readfrom_mem(i2caddr,0x20,2)
	if int.from_bytes(temperature,"little") > 32767:
		temperature = int.from_bytes(temperature,"little")-65536
	else:
		temperature = int.from_bytes(temperature,"little")

def Zaccel(i2caddr):
	zacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2C,2),"little")
	if zacc > 32767:
		zacc = zacc -65536
	return zacc / 16393  # Return the computed acceleration

def Xaccel(i2caddr):
	xacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x28,2),"little")
	if xacc > 32767:
		xacc = xacc -65536
	return xacc / 16393  # Return the computed acceleration
		
def Yaccel(i2caddr):
	yacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2A,2),"little")
	if yacc > 32767:
		yacc = yacc -65536
	return yacc / 16393  # Return the computed acceleration

sensor = HCSR04(trigger_pin=12, echo_pin=13, echo_timeout_us=10000)
sensor2 = HCSR04(trigger_pin=27, echo_pin=33, echo_timeout_us=10000)
led_15 = Pin(15, Pin.OUT)
distance2_0 = 0

buff=[0xA0]
i2c.writeto_mem(i2c.scan()[i],0x10,bytes(buff))
i2c.writeto_mem(i2c.scan()[i],0x11,bytes(buff))
time.sleep(0.01)

while True:
    distance = sensor.distance_cm() / 2.54  # Read the distance in inches from the sensor
    distance2 = sensor2.distance_cm()
    velocity = float((distance2 - distance2_0)/0.5/44.704)
    #WHOAMI(i2c.scan()[i])
    #Temperature(i2c.scan()[i])
    ax = Xaccel(i2c.scan()[i])
    ay = Yaccel(i2c.scan()[i])
    az = Zaccel(i2c.scan()[i])
        
    message = f'{distance} {velocity} {ax} {ay} {az}'  # Send both distance and oscillating value
    
    print('Velocity: ', velocity, 'ax: ', ax, 'ay: ', ay, 'az: ', az) # Print the message locally
    e.send(peer, message)
        
    distance2_0 = distance2
    
    sleep(0.001)