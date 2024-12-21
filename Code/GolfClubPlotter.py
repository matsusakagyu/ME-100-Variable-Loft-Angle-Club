import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(10, 15))
max_points = 100
distance_data, velocity_data, ax_data, ay_data, az_data = [], [], [], [], []

def update_plot(frame):
    try:
        with open('/Users/benjaminkao/Documents/ME-100-Variable-Loft-Angle-Club/Code/metrics.txt', 'r') as f:
            line = f.read().strip()
        
        distance, velocity, ax, ay, az = map(float, line.split(','))
        
        distance_data.append(distance)
        velocity_data.append(velocity)
        ax_data.append(ax)
        ay_data.append(ay)
        az_data.append(az)
        
        if len(distance_data) > max_points:
            distance_data.pop(0)
            velocity_data.pop(0)
            ax_data.pop(0)
            ay_data.pop(0)
            az_data.pop(0)
        
        ax1.clear()
        ax1.plot(distance_data)
        ax1.set_ylabel('Distance (cm)')
        
        ax2.clear()
        ax2.plot(velocity_data)
        ax2.set_ylabel('Velocity (mph)')
        
        ax3.clear()
        ax3.plot(ax_data)
        ax3.set_ylabel('Accel X (g)')
        
        ax4.clear()
        ax4.plot(ay_data)
        ax4.set_ylabel('Accel Y (g)')
        
        ax5.clear()
        ax5.plot(az_data)
        ax5.set_ylabel('Accel Z (g)')
    except Exception as e:
        print(f"Error: {e}")

ani = FuncAnimation(fig, update_plot, interval=100)
plt.tight_layout()
plt.show()
