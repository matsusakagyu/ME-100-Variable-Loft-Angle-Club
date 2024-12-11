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
    
while True:
    host, msg = e.irecv(1000)  # Wait for a message with a timeout of 1000 ms
    if msg:  # If a message was received
        message_str = msg.decode('utf-8')  # Decode bytearray to string
        parts = message_str.split(' ')  # Split the message into parts
        
        # Check if the message is 'exit' before processing angle
        if message_str.strip().lower() == 'exit':
            print("Exiting loop and resetting the ESP32...")
            machine.reset()  # Reset the ESP32 and stop the program
        
        # Check if there's enough parts to process the angle
        elif len(parts) > 3:  # Ensure there's at least 4 parts (index 3 is the angle)
            angle_str = parts[3]

            try:
                angle = int(angle_str)  # Attempt to convert the angle to an integer
                if 0 <= angle <= 180:  # Check if the angle is valid
                    print(f"Moving servo to {angle} degrees")
                    set_servo_angle(angle)
                else:
                    print("Invalid angle! Please enter a value between 0 and 180.")
            except ValueError:
                print(f"Invalid angle value: '{angle_str}' is not a number!")
        else:
            print("Invalid message format! Ensure the message contains a valid angle.")
        time.sleep(2)
    else:
        print("No message received, continuing to listen...")
        time.sleep(5)  # Short sleep to avoid overloading the processor