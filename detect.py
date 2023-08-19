import numpy as np
import cv2
import mysql.connector
from datetime import datetime, timedelta
from ultralytics import YOLO

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
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


def save_into_database(class_name, behavior, image, mode):
    if behavior in class_name:
        # image_base64 = base64.b64encode(buffer)
        _, buffer = cv2.imencode('.png', image)
        image_blob = buffer.tobytes()
        timestamp = datetime.now()
        
        if mode != 'attendance':
            behavior_text_index = class_name.find(behavior)
            name = class_name[:behavior_text_index - 1]
            behavior = class_name[behavior_text_index:]

            sql_query_insert = "INSERT INTO perilaku_murid_{} (nama, perilaku, gambar, timestamp) VALUES (%s, %s, %s, %s)".format('belajar' if mode == 'learn' else 'ujian')
            sql_query_bind = (name, behavior, image_blob, timestamp)
            sql_query_select = "SELECT timestamp FROM perilaku_murid_{} WHERE nama='{}' AND perilaku='{}' ORDER BY timestamp DESC LIMIT 1".format('belajar' if mode == 'learn' else 'ujian', name, behavior)
        else:
            now = timestamp.strftime('%H:%M:%S')
            midday = datetime(2007, 7, 7, 12, 0, 0).strftime('%H:%M:%S')
            school_hours = datetime(2007, 7, 7, 8, 0, 0).strftime('%H:%M:%S')
            home_time = datetime(2007, 7, 7, 17, 0, 0).strftime('%H:%M:%S')

            # Waktu Masuk
            if now < midday:
                punctuality = 'Terlambat' if now > school_hours else 'Tepat Waktu'

                sql_query_insert = "INSERT INTO kehadiran_murid (`nama`, `kategori waktu datang`, `waktu datang`, `gambar datang`) VALUES (%s, %s, %s, %s)"
                sql_query_bind = (class_name, punctuality, timestamp, image_blob)
                sql_query_select = "SELECT nama FROM kehadiran_murid WHERE nama = '%s' AND `waktu datang` BETWEEN '%s' AND '%s' LIMIT 1" %(class_name, timestamp.date(), timestamp.date() + timedelta(days=1))

            # Waktu Pulang
            else: 
                punctuality = 'Pulang Duluan' if now < home_time else 'Pulang Pada Waktunya'

                sql_query_insert = "UPDATE kehadiran_murid SET `waktu pulang` = %s, `kategori waktu pulang` = %s, `gambar pulang` = %s WHERE `nama` = %s AND `waktu datang` BETWEEN %s AND %s"
                sql_query_bind = (timestamp, punctuality, image_blob, class_name, timestamp.date(), timestamp.date() + timedelta(days=1))
                sql_query_select = "SELECT nama, `kategori waktu pulang` FROM kehadiran_murid WHERE `nama` = '%s' AND `waktu pulang` BETWEEN '%s' AND '%s' LIMIT 1" %(class_name, timestamp.date(), timestamp.date() + timedelta(days=1))
        
        cursor.execute("START TRANSACTION")
        # Get Today Timestamp | Get Last Timestamp(Is More 30s?)
        cursor.execute(sql_query_select)
        result = cursor.fetchone()
        print(result)
        if result == None:
            # if mode == 'attendance' and now > midday:
            #     return
            cursor.execute(sql_query_insert, sql_query_bind)
        else:
            if mode != 'attendance':
                is_more_30s = (datetime.now() - result[0]).total_seconds() > 30
                if is_more_30s:
                    cursor.execute(sql_query_insert, sql_query_bind)
            else:
                if mode != 'attendance':
                    cursor.execute(sql_query_insert, sql_query_bind)
        # cursor.execute(sql_query_insert, sql_query_bind)
        db.commit()


def detection(mode):
    if mode != 'attendance':
        model = './models/learn.pt' if mode == 'learn' else './models/exam.pt'
        model_behavior = YOLO(model)
        model_pose = YOLO('./models/yolov8n-pose.pt')
    else:
        model_person = YOLO('./models/person.pt')

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        _, frame = cap.read()

        if mode != 'attendance':
            results_behavior = model_behavior(frame)
            results_pose = model_pose(results_behavior[0].plot())
        else:
            results_person = model_person(frame)

        results = results_behavior[0] if mode != 'attendance' else results_person[0]
        image = results_pose[0].plot() if mode != 'attendance' else results_person[0].plot()

        cv2.imshow(mode.capitalize() + ' Mode', image)

        for index in results.boxes.cls:
            class_id = int(str(index.item()).split('.')[0])
            class_name = results.names.get(class_id)

            if mode == 'learn':
                save_into_database(class_name, 'Angkat Tangan',
                                   np.squeeze(image), 'learn')
                save_into_database(class_name, 'Main HP',
                                   np.squeeze(image), 'learn')
                save_into_database(class_name, 'Ngantuk',
                                   np.squeeze(image), 'learn')
                save_into_database(class_name, 'Tidur',
                                   np.squeeze(image), 'learn')
            elif mode == 'exam':
                save_into_database(class_name, 'Tengok Kiri Kanan',
                                   np.squeeze(image), 'exam')
                save_into_database(class_name, 'Main HP',
                                   np.squeeze(image), 'exam')
            else:
                save_into_database(class_name, class_name,
                                   np.squeeze(image), 'attendance')

        # print(results_behavior.pandas().xyxy[0].get('name')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


detection('attendance')
