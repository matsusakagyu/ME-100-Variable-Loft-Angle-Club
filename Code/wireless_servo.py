import network
import espnow
import machine
import time
from machine import Pin

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

e = espnow.ESPNow()s
e.active(True)

# Set up PWM on GPIO 23 (change this if you're using a different pin)
face_servo_pin = machine.Pin(12)
pin_pin = machine.Pin(15)
pwm_face = machine.PWM(face_servo_pin, freq=50)  # Standard servo frequency of 50Hz
pwm_pin = machine.PWM(pin_pin, freq=50)  # Standard servo frequency of 50Hz

# Function to map the angle (0-180 degrees) to PWM duty cycle (40 to 115)
def map_angle_to_duty_cycle(angle):
    min_duty = 40
    max_duty = 115
    return int(min_duty + (angle / 180) * (max_duty - min_duty))

# Function to set the servo angle
def set_servo_angle(angle):
    duty_face = map_angle_to_duty_cycle(angle)
    duty_pin_out = map_angle_to_duty_cycle(90)
    duty_pin_in = map_angle_to_duty_cycle(30)
    pwm_pin.duty(duty_pin_out)
    time.sleep(2)
    pwm_face.duty(duty_face)
    time.sleep(2)
    pwm_pin.duty(duty_pin_in)
    
angles_dict = {
    5: 20,    # For input 1, angle 0 degrees
    6: 40,   # For input 2, angle 30 degrees
    7: 65,   # For input 3, angle 60 degrees
    8: 85,   # For input 4, angle 90 degrees
    9: 115,  # For input 5, angle 120 degrees
    'P': 145   # For input 6, angle 150 degrees
}
    
while True:
    host, msg = e.irecv(1000)  # Wait for a message with a timeout of 1000 ms
    if msg:  # If a message was received
        message_str = msg.decode('utf-8')  # Decode bytearray to string
        parts = message_str.split(' ')  # Split the message into parts
        
        # Check if the message is 'exit' before processing angle
        if message_str.strip().lower() == 'exit':
            print("Exiting loop and resetting the ESP32...")
            machine.reset()  # Reset the ESP32 and stop the program
        # Check if there's enough parts to process the club identifier (at least 4 parts)
        elif len(parts) > 3:  # Ensure there's at least 4 parts (index 3 is the club identifier)
            club_identifier = parts[3].upper()  # Convert to uppercase to handle both 'p' and 'P'

            if club_identifier.isdigit():  # If the input is a number (5-9)
                club_identifier = int(club_identifier)
            
            # Check if the club identifier is valid (exists in angles_dict)
            if club_identifier in angles_dict:
                angle = angles_dict[club_identifier]
                print(f"Moving servo to {angle} degrees for club {club_identifier}")
                set_servo_angle(angle)
            else:
                print(f"Invalid club identifier: '{club_identifier}'. Please enter a valid club (5-9 or 'P').")
                time.sleep(0.1)
                
        else:
            print("Invalid message format! Ensure the message contains a valid club identifier.")
        
        time.sleep(2)
    else:
        print("No message received, continuing to listen...")
        time.sleep(5)  # Short sleep to avoid overloading the processor