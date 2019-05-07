#!/usr/bin/env python
# -*- coding: utf-8 -*-

#背景差分で変化があった部分のみ検出し、重心などをプロットするプログラム 

import cv2
import numpy as np
import random
import sys

width_of_img = 860
height_of_img = 680 
fps = 30

cap = cv2.VideoCapture(0)
cap.set(3,width_of_img) # WIDTH
cap.set(4,height_of_img) # HEIGHT
cap.set(5,fps) # FPS
avg = None

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    # 画像をグレースケールで読み込み
    pre_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(pre_gray,5) #ごま塩ノイズの除去  
    # 前処理（平準化フィルターを適用した場合）
    # 前処理が不要な場合は下記行をコメントアウト
    blur_src = cv2.GaussianBlur(gray, (5, 5), 2)

    #背景差分
    if avg is None:
        avg = blur_src.copy().astype('float')
        continue
    cv2.accumulateWeighted(blur_src, avg, 0.7)
    mdframe = cv2.absdiff(blur_src, cv2.convertScaleAbs(avg))
    cv2.imshow('MotionDetected Frame', mdframe)

    # 二値変換
    # 前処理を使用しなかった場合は、blur_srcではなくgray_srcに書き換えるする

    mono_src = cv2.threshold(mdframe, 30, 255, cv2.THRESH_BINARY)[1]

    cv2.imshow('mono',mono_src)
    # ラベリング結果書き出し用に二値画像をカラー変換
    color_src01 = cv2.cvtColor(mono_src, cv2.COLOR_GRAY2BGR)
    color_src02 = cv2.cvtColor(mono_src, cv2.COLOR_GRAY2BGR)

    # ラベリング処理
    label = cv2.connectedComponentsWithStats(mono_src)

    # オブジェクト情報を項目別に抽出
    n = label[0] - 1
    data = np.delete(label[2], 0, 0)
    center = np.delete(label[3], 0, 0)

    # オブジェクト情報を利用してラベリング結果を画面に表示
    for i in range(n):
 
        # 各オブジェクトの外接矩形を赤枠で表示
        x0 = data[i][0]
        y0 = data[i][1]
        x1 = data[i][0] + data[i][2]
        y1 = data[i][1] + data[i][3]
        cv2.rectangle(color_src01, (x0, y0), (x1, y1), (0, 0, 255))
        cv2.rectangle(color_src02, (x0, y0), (x1, y1), (0, 0, 255))

        # 各オブジェクトのラベル番号と面積に黄文字で表示
        cv2.putText(color_src01, "ID: " +str(i + 1), (x1 - 20, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
        cv2.putText(color_src01, "S: " +str(data[i][4]), (x1 - 20, y1 + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))

        # 各オブジェクトの重心座標をに黄文字で表示
        cv2.putText(color_src02, "X: " + str(int(center[i][0])), (x1 - 30, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
        cv2.putText(color_src02, "Y: " + str(int(center[i][1])), (x1 - 30, y1 + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))

    # 結果の表示
    cv2.imshow("color_src01", color_src01)
    cv2.imshow("color_src02", color_src02)

    k = cv2.waitKey(1)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()