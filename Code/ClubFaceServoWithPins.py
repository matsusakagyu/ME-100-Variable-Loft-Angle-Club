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

# Main loop: Read user input and move the servo
while True:
    try:
        # Ask user for an angle between 0 and 180, or 'exit' to quit
        user_input = input("Enter the servo angle (0-180) or 'exit' to quit: ")

        # Allow the user to exit the program
        if user_input.lower() == "exit":
            print("Exiting the program.")
            break

        # Convert input to an integer
        angle = int(user_input)

        # Check if the input is valid (within 0-180 range)
        if 0 <= angle <= 180:
            print(f"Moving servo to {angle} degrees")
            set_servo_angle(angle)
        else:
            print("Invalid angle! Please enter a value between 0 and 180.")
        
    except ValueError:
        print("Invalid input! Please enter a valid number.")

    # Add a small delay before prompting again
    time.sleep(0.1)