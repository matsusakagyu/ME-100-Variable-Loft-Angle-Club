import network
import espnow
import urequests
import usocket as socket
from machine import Pin
import time
from time import sleep

sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  # For ESP8266

# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)

led_15 = Pin(15, Pin.OUT)

# Define the peer's MAC address (replace with actual MAC)

#peer = b'\xe8\x6b\xea\x37\xd4\x9c'  # MAC address of peer's wifi interface
peer = b'\x14\x2b\x2f\xaf\xf2\x48'
e.add_peer(peer)  # Must add_peer() before send()

e.send(peer, "Starting...")


while True:
    try:
        # Ask user for an angle between 0 and 180, or 'exit' to quit
        user_input = input("Enter a club number from 4-9: ")

        # Allow the user to exit the program
        if user_input.lower() == "exit":
            print("Exiting the program.")
            e.send(peer, "exit")
            break

        # Convert input to an integer
        num = int(user_input)

        # Check if the input is valid (within 0-180 range)
        if 4 <= num <= 9:
            message = (f"Moving club to {num} ")
        else:
            message = ("Invalid number! 4-9")
        print(message)
        e.send(peer, message)
        
    except ValueError:
        print("Invalid input! Please enter a valid number.")
   
        
while True:
    host, msg = e.irecv(1000)  # Wait for message with a timeout of 1000ms
    if msg:  # msg == None if timeout in recv()
        # Convert bytearray to string
        message_str = msg.decode('utf-8')  # Decode bytearray to string
        # Split the input data into lines
        line = message_str.split(' ')
        # Extract the values from each line
        height = float(line[0])
        if (height < 3.5):
            led_15.value(1)
        else:
            led_15.value(0)
        velocity = float(line[1])
        ax = -1*float(line[2])
        ay = -1*float(line[3])
        az = -1*float(line[4])
        # Print the extracted values
        print('Velocity: ', velocity, 'ax: ', ax, 'ay : ', ay, 'az: ', az) # Print the message locally
        time.sleep(0.01)
        
        
        