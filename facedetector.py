from centerface import CenterFace
import cv2
import string
import random
import pymysql


# Create a connection object
dbServerName    = "localhost"
port            = 3306
dbUser          = "root"
dbPassword      = ""
dbName          = "face_db"

conn = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,db=dbName, port=port)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def face_store_db(faceid):
    try:
        print("Connection Establised")

        # Create a cursor object
        cursor = conn.cursor()

        # Create a new record
        sql = "INSERT INTO `faces` (`face-id`) VALUES (%s)"
        cursor.execute(sql, (faceid))
        conn.commit()

    except Exception as e:
        print("Exeception occured:{}".format(e))

        


def detect(frame):
    h, w = frame.shape[:2]
    centerface = CenterFace(h, w)
    dets, lms = centerface(frame, threshold=0.5)
    for det in dets:
        boxes, score = det[:4], det[4]
        cv2.rectangle(frame, (int(boxes[0]), int(boxes[1])), (int(boxes[2]), int(boxes[3])), (2, 255, 0), 1)

        x, y, w, h = int(boxes[0]), int(boxes[1]), int(boxes[2]), int(boxes[3])
        cropped_face = frame[y:h, x:w]
        faceid = 'face-'+str(id_generator())+'.jpeg'

        try:
            cv2.imwrite('./faces/'+ str(faceid), cropped_face)
            face_store_db(faceid)
            
        except Exception as e:
            print("Exeception occured:{}".format(e))

    for lm in lms:
        cv2.circle(frame, (int(lm[0]), int(lm[1])), 2, (0, 0, 255), -1)
        cv2.circle(frame, (int(lm[2]), int(lm[3])), 2, (0, 0, 255), -1)
        cv2.circle(frame, (int(lm[4]), int(lm[5])), 2, (0, 0, 255), -1)
        cv2.circle(frame, (int(lm[6]), int(lm[7])), 2, (0, 0, 255), -1)
        cv2.circle(frame, (int(lm[8]), int(lm[9])), 2, (0, 0, 255), -1)

    return frame

