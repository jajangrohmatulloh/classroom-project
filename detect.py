import torch
import numpy as np
import cv2
import mysql.connector
from datetime import datetime
from ultralytics import YOLO

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="testpython"
# )

# mycursor = db.cursor()


def personDetection():
    model = YOLO('yolov8n-pose.pt')

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        check, frame = cap.read()
        results = model(frame)

        cv2.imshow('YOLO', results[0].plot())

    # if 'awake' in results.pandas().xyxy[0].value_counts('name'):
    #     print('awake')
    # mycursor.execute(
    #     "INSERT INTO test_table(name, indicate, timestamp) values('JR', 'bangun', '{}')".format(datetime.now()))
    # db.commit()
    # if 'ngantuk' in results.pandas().xyxy[0].value_counts('name'):
    #     print('ngantuk')
    # mycursor.execute(
    #     "INSERT INTO test_table(name, indicate, timestamp) values('JR', 'tidur', '{}')".format(datetime.now()))
    # db.commit()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
