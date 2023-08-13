import torch
import numpy as np
import cv2
import mysql.connector
from datetime import datetime
from ultralytics import YOLO
import base64

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="testpython"
# )

# mycursor = db.cursor()


def save_into_database(class_name, behavior, image, cursor=None, db=None):
    if behavior in class_name:
        _, buffer = cv2.imencode('.png', image)
        image_base64 = base64.b64encode(buffer)
        behavior_text_index = class_name.find(behavior)
        # print('name:' + class_name[:behavior_text_index - 1])
        # print('behavior:' + class_name[behavior_text_index:])
        # print(image_base64)
        # cursor.execute(
        #     f"""INSERT INTO test_table(name, perilaku, gambar, timestamp) VALUES('{class_name[:behavior_text_index - 1]}', '{class_name[behavior_text_index:]}', '{image_base64}', '{datetime.now()}')""")
        # db.commit()


def personDetection():
    model_behavior = YOLO('runs/detect/train5/weights/best.pt')
    # model_pose = YOLO('./models/yolov8n-pose.pt')
    model_pose = YOLO('./models/yolov8n.pt')

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        _, frame = cap.read()

        results_behavior = model_behavior(frame)
        results_pose = model_pose(results_behavior[0].plot())

        image = results_pose[0].plot()

        cv2.imshow('YOLO', image)

        for index in results_pose[0].boxes.cls:
            class_id = int(str(index.item()).split('.')[0])
            class_name = results_pose[0].names.get(class_id)
            save_into_database(class_name, 'phone',
                               np.squeeze(image))

        # print(results_behavior.pandas().xyxy[0].get('name')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


personDetection()
