import machine
import time

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

# Main loop: Read user input and move the servo
while True:
    try:
        # Ask user for input (numbers 5-9 or 'P'), or 'exit' to quit
        user_input = input("Enter the club you would like (P through 5) or 'exit' to quit: ")

        # Allow the user to exit the program
        if user_input.lower() == "exit":
            print("Exiting the program.")
            break

        # Check if the input is numeric (for 5-9) or a valid string ('P')
        if user_input.isdigit():
            input_value = int(user_input)
        else:
            input_value = user_input.upper()  # Convert input to uppercase if it's a string (to handle 'p' or 'P')

        # Check if the input is valid (should be in the dictionary keys)
        if input_value in angles_dict:
            angle = angles_dict[input_value]
            print(f"Moving servo to {angle} degrees")
            set_servo_angle(angle)
        else:
            print("Invalid input! Please enter a number between 5 and 9, or 'P'.")
        
    except ValueError:
        print("Invalid input! Please enter a valid number or 'P'.")

    # Add a small delay before prompting again
    time.sleep(0.1)