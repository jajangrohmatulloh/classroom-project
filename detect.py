import numpy as np
import cv2
import mysql.connector
from datetime import datetime
from ultralytics import YOLO

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="murid"
)

cursor = db.cursor()

# mycursor.execute('SELECT * FROM perilaku_murid_belajar')

# results = mycursor.fetchall()

# for data in results:
#     test = base64.b64encode(data[3])
#     with open("imageToSave.png", "wb") as fh:
#         fh.write(data[3])
# print(test)


def save_into_database(class_name, behavior, image):
    if behavior in class_name:
        _, buffer = cv2.imencode('.png', image)
        image_blob = buffer.tobytes()
        # image_base64 = base64.b64encode(buffer)
        behavior_text_index = class_name.find(behavior)
        name = class_name[:behavior_text_index - 1]
        behavior = class_name[behavior_text_index:]
        timestamp = datetime.now()

        # sql_query = "INSERT INTO perilaku_murid_belajar (nama, perilaku, gambar, timestamp) VALUES (%s, %s, %s, %s)"
        # cursor.execute(sql_query, (name,
        #                            behavior, image_blob, timestamp))
        # db.commit()


def detection(mode):
    if mode == 'absence':
        print('test')
        model_person = YOLO('./models/yolov8n.pt')
    elif mode == 'learn':
        model_behavior = YOLO('runs/detect/train5/weights/best.pt')
        model_pose = YOLO('./models/yolov8n-pose.pt')
    elif mode == 'exam':
        model_behavior = YOLO('runs/detect/train5/weights/best.pt')
        model_pose = YOLO('./models/yolov8n-pose.pt')

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        _, frame = cap.read()

        if mode == 'absence':
            results_person = model_person(frame)
        else:
            results_behavior = model_behavior(frame)
            results_pose = model_pose(results_behavior[0].plot())

        results = results_person[0] if mode == 'absence' else results_pose[0]
        image = results.plot()

        cv2.imshow('YOLO', image)

        for index in results.boxes.cls:
            class_id = int(str(index.item()).split('.')[0])
            class_name = results.names.get(class_id)
            save_into_database(class_name, 'person',
                               np.squeeze(image))

        # print(results_behavior.pandas().xyxy[0].get('name')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


detection('absence')
