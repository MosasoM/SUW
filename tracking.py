#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
def frame_resize(frame, n=2):
    """
    スクリーンショットを撮りたい関係で1/4サイズに縮小
    """
    return cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)))
 # トラッカーを選択する
def select_tracker():
    print("Which Tracker API do you use?")
    print("0: Boosting")
    print("1: MIL")
    print("2: KCF")
    print("3: TLD")
    print("4: MedianFlow")
    print("5: GOTURN")
    choice = input("Please select your tracker number: ")
 
    if choice == '0':
        tracker = cv2.TrackerBoosting_create()
    if choice == '1':
        tracker = cv2.TrackerMIL_create()
    if choice == '2':
        tracker = cv2.TrackerKCF_create()
    if choice == '3':
        tracker = cv2.TrackerTLD_create()
    if choice == '4':
        tracker = cv2.TrackerMedianFlow_create()
    # if choice == '5':
    #     tracker = cv2.MultiTracker_create()
 
 
    return tracker

tracker = select_tracker()
tracker_name = str(tracker).split()[0][1:]
 
cap = cv2.VideoCapture(0)
 
#webカメラの軌道に時間がかかる場合
import time
time.sleep(1)
 
ret, frame = cap.read()
 
roi = cv2.selectROI(frame, False)
 
ret = tracker.init(frame, roi)
 
while True:
 
    ret, frame = cap.read()
 
    success, roi = tracker.update(frame)
 
    (x,y,w,h) = tuple(map(int,roi))
 
    if success:
        p1 = (x, y)
        p2 = (x+w, y+h)
        cv2.rectangle(frame, p1, p2, (0,255,0), 3)
    else :
        cv2.putText(frame, "Tracking failed!!", (500,400), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),3)
 
    cv2.imshow(tracker_name, frame)
 
    k = cv2.waitKey(1) & 0xff
    if k == 27 :
        break
 
cap.release()
cv2.destroyAllWindows()