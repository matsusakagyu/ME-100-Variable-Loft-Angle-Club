from time import sleep
import qwiic_lsm6ds0
import board

# Initialize the Qwiic LSM6DS0 sensor
sensor = qwiic_lsm6ds0.QwiicLsm6ds0()

# Make sure the sensor is connected and working
if sensor.connected:
    print("LSM6DS0 connected!")
else:
    print("LSM6DS0 not connected!")

# Initialize the sensor (optional, depending on your setup)
sensor.begin()

# Function to read sensor data
def read_sensor():
    accel = sensor.acceleration()  # Returns a tuple of (x, y, z)
    gyro = sensor.gyroscope()     # Returns a tuple of (x, y, z)
    return accel, gyro

# Main loop to continuously read data
while True:
    accel, gyro = read_sensor()
    print(f"Accel: {accel}, Gyro: {gyro}")
    sleep(0.1)  # Sleep to reduce print frequency
    
import serial
import matplotlib.pyplot as plt
import numpy as np

# Set up serial connection to the ESP32 (adjust COM port)
ser = serial.Serial('COMx', 115200)  # Replace 'COMx' with your ESP32 serial port

# Create lists to store data
accel_x, accel_y, accel_z = [], [], []
gyro_x, gyro_y, gyro_z = [], [], []

# Set up the plot
fig, ax = plt.subplots(3, 2, figsize=(10, 6))
ax = ax.flatten()

# Continuously read data from serial and plot
while True:
    line = ser.readline().decode('utf-8').strip()  # Read line from serial
    if line.startswith("Accel"):
        # Example format: "Accel: (1.23, 2.34, 3.45), Gyro: (0.01, -0.02, 0.03)"
        parts = line.split(", Gyro:")
        accel_data = parts[0][7:-1]  # Extracting values after 'Accel: '
        gyro_data = parts[1][1:-1]  # Extracting values after 'Gyro: '

        # Convert to float and append to lists
        ax_data = tuple(map(float, accel_data.split(", ")))
        gx_data = tuple(map(float, gyro_data.split(", ")))

        accel_x.append(ax_data[0])
        accel_y.append(ax_data[1])
        accel_z.append(ax_data[2])
        gyro_x.append(gx_data[0])
        gyro_y.append(gx_data[1])
        gyro_z.append(gx_data[2])

        # Update plots
        ax[0].plot(accel_x, label="Accel X")
        ax[1].plot(accel_y, label="Accel Y")
        ax[2].plot(accel_z, label="Accel Z")
        ax[3].plot(gyro_x, label="Gyro X")
        ax[4].plot(gyro_y, label="Gyro Y")
        ax[5].plot(gyro_z, label="Gyro Z")

        for i in range(6):
            ax[i].legend(loc="upper right")

        plt.pause(0.1)  # Pause to allow plot to update

ser.close()  # Close the serial port when done
