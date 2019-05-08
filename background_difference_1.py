#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
print(cv2.__version__)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
print(cv2.__version__)

cap = cv2.VideoCapture(0)
ok = False
detected_frame = None
bbox = (0,0,0,0)
#bboxes = []
avg = None

while(True):
    bboxes = []
    # VideoCaptureから1フレーム読み込む
    ret, frame = cap.read()
    frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)))

    #frame = cv2.resize(frame,(int(frame.shape[1]/2),int(frame.shape[0]/2)))
    #加工なし画像を表示する
    #cv2.imshow('Raw Frame',frame)

    # 取り込んだフレームに対して差分をとって動いているところが明るい画像を作る
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if avg is None:
        avg = gray.copy().astype('float')
        continue
    cv2.accumulateWeighted(gray, avg, 0.7)
    mdframe = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
    #cv2.imshow('MotionDetected Frame', mdframe)

    #動いているエリアの面積を計算してちょうどいい検知結果を抽出する
    thresh = cv2.threshold(mdframe, 3, 255, cv2.THRESH_BINARY)[1] #動いている部分の2値化処理
    im_mask = cv2.medianBlur(thresh,5) #ごま塩ノイズの除去
    image, contours, hierarchy = cv2.findContours(im_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #輪郭を検出 
    # max_area = 0
    # target = None
    # for cnt in contours:
    #     area = cv2.contourArea(cnt)
    #     if max_area < area and area < 40000 and area > 4000:
    #         max_area = area
    #         target = cnt
    i = 0
    for cnt in contours:
        if i > 10 :
            break
        area = cv2.contourArea(cnt)
        i = i+1
        
   
    #  # 動いているエリアのうちそこそこの大きさのものがあればそれを矩形で表示する
    # if max_area <= 4000:
    #     areaframe = frame
    #     cv2.putText(areaframe, 'not detected', (0,50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255,0), 3, cv2.LINE_AA)
    # else:
    #     # 諸般の事情で矩形検出とした。
    #     x,y,w,h = cv2.boundingRect(target)
    #     areaframe = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    # 動いているエリアのうちそこそこの大きさのものがあればそれを矩形で表示する
    # ちょうどいいエリアがなかったら最後の動いているエリアがあるフレームとエリア情報を用いてトラッキングをする
    # どうしようもない時はどうしようもない旨を表示する
        if area <= 1000:
            #continue
            for bbox in bboxes :
                track = False
                if detected_frame is not None:
                    # インスタンスを作り直さなきゃいけないっぽい
                    tracker = cv2.TrackerKCF_create()
                    ok = tracker.init(detected_frame, bbox)
                    detected_frame = None

                # if ok:
                #     track, bbox = tracker.update(frame)
                track, bbox = tracker.update(frame)
                if track:
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)
                    
                # else:
                #     ok = False
            
        else:
            #areaframe = cv2.drawContours(frame, [target], 0, (0,255,0), 3)
            x,y,w,h = cv2.boundingRect(cnt)
            bbox = (x,y,w,h)
            bboxes.append(bbox)
            #print(bboxes)
            detected_frame = frame.copy()
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            frame = cv2.circle(frame,(int(x+w/2.0),int(y+h/2.0)),4,(0,0,255))
            

    cv2.imshow('MotionDetected Area Frame', frame)


    #キー入力を1ms待って、kが27(ESC)だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break
#キャプチャーをリリースしてウィンドウ全て閉じる     
cap.release()

cv2.destroyAllWindows()






