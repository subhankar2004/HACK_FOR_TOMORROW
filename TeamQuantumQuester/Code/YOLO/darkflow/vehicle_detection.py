import cv2
import time
import os
import numpy as np
from darkflow.net.build import TFNet
from anomaly_detection.detect_anomaly import check_anomaly
from alert_system import send_alert

options = {
    'model': './cfg/yolo.cfg',        
    'load': './bin/yolov2.weights',  
    'threshold': 0.3                 
}

tfnet = TFNet(options)
inputPath = os.getcwd() + "/test_images/"
outputPath = os.getcwd() + "/output_images/"
logPath = os.getcwd() + "/logs/anomalies.log"

vehicle_positions = {}

def detectVehicles(filename):
    global tfnet, inputPath, outputPath, vehicle_positions
    img = cv2.imread(inputPath + filename, cv2.IMREAD_COLOR)
    result = tfnet.return_predict(img)

    anomalies_detected = []

    for vehicle in result:
        label = vehicle['label']
        if label in ["car", "bus", "bike", "truck", "rickshaw"]:
            top_left = (vehicle['topleft']['x'], vehicle['topleft']['y'])
            bottom_right = (vehicle['bottomright']['x'], vehicle['bottomright']['y'])
            center_x = (top_left[0] + bottom_right[0]) // 2
            center_y = (top_left[1] + bottom_right[1]) // 2
            
            # Check for anomaly
            anomaly_type = check_anomaly(label, center_x, center_y)
            if anomaly_type:
                anomalies_detected.append((label, anomaly_type))

            img = cv2.rectangle(img, top_left, bottom_right, (0,255,0), 3)
            img = cv2.putText(img, label, top_left, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)

    outputFilename = outputPath + "output_" + filename
    cv2.imwrite(outputFilename, img)

    # If anomalies found, send an alert
    if anomalies_detected:
        send_alert(anomalies_detected)

    print(f"Output image stored at: {outputFilename}")

for filename in os.listdir(inputPath):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        detectVehicles(filename)

print("Vehicle detection completed.")
