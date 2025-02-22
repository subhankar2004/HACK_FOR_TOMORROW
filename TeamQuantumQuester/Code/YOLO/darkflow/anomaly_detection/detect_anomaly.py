import time
import numpy as np

# Store previous positions to calculate speed
vehicle_positions = {}

def check_anomaly(label, x, y):
    global vehicle_positions

    timestamp = time.time()
    
    # If vehicle is already seen, calculate speed
    if label in vehicle_positions:
        prev_x, prev_y, prev_time = vehicle_positions[label]
        speed = np.sqrt((x - prev_x)**2 + (y - prev_y)**2) / (timestamp - prev_time)

        if speed > 50:  # Example threshold for over-speeding
            return "Over-speeding detected"
        
        if abs(y - prev_y) > 100:  # Example for wrong movement
            return "Wrong direction detected"

    # Update vehicle position
    vehicle_positions[label] = (x, y, timestamp)
    return None
