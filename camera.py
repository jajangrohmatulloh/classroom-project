import cv2
# import time


cap = cv2.VideoCapture(0)
count = 1
while cap.isOpened():
    status, frame = cap.read()
    cv2.imshow('Camera', frame)
    # cv2.imwrite('./data/images/jajang_melihat_hp.' +
    #             str(count) + '.jpg', frame)
    # count += 1
    # time.sleep(5)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('./data/images/jajang_melihat_hp.' +
                    str(count) + '.jpg', frame)
        count += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
