import cv2,time
import pandas as pd
from datetime import datetime
video = cv2.VideoCapture(0)
first_frame = None
status_list = [None,None]
times=[]
df = pd.DataFrame(columns=['Start','End'])
while True:
    status = 0
    check, frame = video.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray= cv2.GaussianBlur(gray,(21,21),0)

    if(first_frame is None):
        first_frame = gray
        continue
    delta_frame = cv2.absdiff(first_frame,gray)
    threshold_frame = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame,None,iterations=10)
    (_,cnts,_) = cv2.findContours(threshold_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in cnts:
        if cv2.contourArea(contour)<10000:
            continue
        status = 1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),5)
    status_list.append(status)
    if(status_list[-2]==0 and status_list[-1]==1):
        times.append(datetime.now())
    if (status_list[-1] == 0 and status_list[-2] == 1):
        times.append(datetime.now())
    key = cv2.waitKey(1)
    if key==ord('q'):
        if status ==1:
            times.append(datetime.now())
        break
    cv2.imshow('capturing', gray)
    cv2.imshow('Gray Frame',gray)
    cv2.imshow('Delta Frame',delta_frame)
    cv2.imshow('Threshold Frame',threshold_frame)
    cv2.imshow('Color frame',frame)
for i in range(0,len(times),2):
    df = df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
df.to_csv('times.csv',index=False)
video.release()
cv2.destroyAllWindows()
