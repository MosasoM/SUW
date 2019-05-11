import cv2
def detect(gray,avg):
    cv2.accumulateWeighted(gray, avg, 0.7)
    mdframe = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # 動いているエリアの面積を計算してちょうどいい検知結果を抽出する
    thresh = cv2.threshold(mdframe, 3, 255, cv2.THRESH_BINARY)[1]  # 動いている部分の2値化処理
    im_mask = cv2.medianBlur(thresh, 5)  # ごま塩ノイズの除去
    _,contours, hierarchy = cv2.findContours(im_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 輪郭を検出

    return contours,hierarchy