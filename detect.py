import numpy as np
import cv2
import mysql.connector
from datetime import datetime
from ultralytics import YOLO
import base64


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="murid"
)

mycursor = db.cursor()

mycursor.execute('SELECT * FROM perilaku_murid_belajar')

results = mycursor.fetchall()

for data in results:
    test = base64.b64encode(data[3])
    with open("imageToSave.png", "wb") as fh:
        fh.write(data[3])
# with open('./students/cell/test.png', 'rb') as f:
#     mycursor.execute(
#         f"""INSERT INTO perilaku_murid_belajar(nama, perilaku, gambar, timestamp) VALUES('test', 'dfgjfdgf', '{f.read()}', '{datetime.now()}')""")
#     db.commit()
# thedata = open('test.png', 'rb').read()
print(test)

# mycursor.execute(sql, ('nama', 'perilaku', thedata, datetime.now()))
# db.commit()

# test = open('PIL.png', 'rb').read()


def save_into_database(class_name, behavior, image, cursor=None, db=None):
    if behavior in class_name:
        _, buffer = cv2.imencode('.png', image)
        # im = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # stream = io.BytesIO()
        # im.save(stream, format="png")
        # imagebytes = stream.getvalue()
        # img = im.tobytes('hex', 'rgb')
        image_blob = buffer.tobytes()
        # buf = io.BytesIO()
        # image_blob.save(buf, format='JPEG')
        # byte_im = buf.getvalue()
        # image_base64 = base64.b64encode(buffer)

        behavior_text_index = class_name.find(behavior)
        timestamp = str(datetime.now())
        # cv2.imwrite(
        #     f"""./students/{class_name[:behavior_text_index - 1]}/{class_name}.{class_name[behavior_text_index:]}{timestamp}.png""", image)
        # cv2.imwrite('imageToSave.png', image)

        # print('name:' + class_name[:behavior_text_index - 1])
        # print('behavior:' + class_name[behavior_text_index:])
        # print(image_base64)
        # cursor.execute(
        #     f"""INSERT INTO perilaku_murid_belajar(nama, perilaku, gambar, timestamp) VALUES('{class_name[:behavior_text_index - 1]}', '{class_name[behavior_text_index:]}', {test}, '{timestamp}')""")
        sql_query = "INSERT INTO perilaku_murid_belajar (nama, perilaku, gambar, timestamp) VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql_query, (class_name[:behavior_text_index - 1],
                         class_name[behavior_text_index:], image_blob, datetime.now()))
        db.commit()


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
        _, buffer = cv2.imencode('.png', np.squeeze(image))

        cv2.imshow('YOLO', image)

        for index in results_pose[0].boxes.cls:
            class_id = int(str(index.item()).split('.')[0])
            class_name = results_pose[0].names.get(class_id)
            save_into_database(class_name, 'phone',
                               np.squeeze(image), mycursor, db)

        # print(results_behavior.pandas().xyxy[0].get('name')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # print(base64.b64encode(buffer.tobytes()))
    # with open("imageToSave.png", "wb") as fh:
    #     fh.write(buffer.tobytes())

    cap.release()
    cv2.destroyAllWindows()


personDetection()
