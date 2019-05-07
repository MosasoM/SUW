#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math

# フレーム差分の計算
def frame_sub(img1, img2, img3, th):
    # フレームの絶対差分
    diff1 = cv2.absdiff(img1, img2)
    diff2 = cv2.absdiff(img2, img3)

    # 2つの差分画像の論理積
    diff = cv2.bitwise_and(diff1, diff2)

    # 二値化処理
    diff[diff < th] = 0
    diff[diff >= th] = 255
    
    # メディアンフィルタ処理（ゴマ塩ノイズ除去）
    mask = cv2.medianBlur(diff, 3)

    return  mask


def main():
    # カメラのキャプチャ
    cap = cv2.VideoCapture(0)
    
    # フレームを3枚取得してグレースケール変換
    frame1 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
    frame2 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
    frame3 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)

    while(cap.isOpened()):
        ret , frame =cap.read()
    
        # フレーム間差分を計算
        mask = frame_sub(frame1, frame2, frame3, th=30)

        #image, contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #輪郭を検出
        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 輪郭を検出
        max_area = 0
        target = None
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if max_area < area and area < 10000 and area > 500:
                max_area = area
                target = cnt
    
        # 動いているエリアのうちそこそこの大きさのものがあればそれを矩形で表示する
        if max_area <= 500:
            areaframe = frame
            cv2.putText(areaframe, 'not detected', (0,50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255,0), 3, cv2.LINE_AA)
        else:
            # 検出物に長方形を描画
            x,y,w,h = cv2.boundingRect(target)
            center = (x+int(w/2),y+int(h/2))
            areaframe = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            # 検出物に円を描画
            # (x,y),radius = cv2.minEnclosingCircle(target)
            # center = (int(x),int(y))
            # radius = int(radius)
            # areaframe = cv2.circle(frame,center,radius,(0,255,0),2)
            areaframe = cv2.circle(frame,center, 3, (0,0,255), -1)


        # 結果を表示
        cv2.imshow("Frame2", frame2)
        cv2.imshow("Mask", mask)
        cv2.imshow('MotionDetected Area Frame', frame)

        # 3枚のフレームを更新
        frame1 = frame2
        frame2 = frame3
        frame3 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
            
        # escキーが押されたら途中終了
        k = cv2.waitKey(1)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()