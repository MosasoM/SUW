import cv2
import others
import detect_move
import numpy as np

print(cv2.__version__)

cap = cv2.VideoCapture(0)
ok = False
detected_frame = None
bbox = (0,0,0,0)
center =(0,0)

avg = others.init_avg(cap)



color = (0,0,255)
r = 20
people =np.array([0,0])


img = cv2.imread("sea.jpg",cv2.IMREAD_UNCHANGED)
zero = np.zeros((img.shape[0],img.shape[1]),img.dtype)
img = cv2.merge((img,zero))
fish = cv2.imread("18438.png",cv2.IMREAD_UNCHANGED)
fish_scale_inv = 4
orgHeight = fish.shape[0]
orgWidth = fish.shape[1]
resized = (orgWidth//fish_scale_inv, orgHeight//fish_scale_inv)
fish = cv2.resize(fish,resized)
mask = fish[:,:,3]
fish_lb = [100,100]
flag = False
flag1 = False

while (True):
    bboxes = []
    ret, frame = cap.read()
    frame = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    contours,hierarchy = detect_move.detect(gray,avg)
    i = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= 1500:
            areaframe = frame
            cv2.putText(areaframe, 'motion', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
            x, y, w, h = cv2.boundingRect(cnt)
            bbox = (x, y, w, h)
            bboxes.append(bbox)
            detected_frame = frame.copy()
            center = (int(x + w / 2.0), int(y + h / 2.0))
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            frame = cv2.circle(frame, center , 4, (0, 0, 255),-1)

    cv2.imshow('MotionDetected Area Frame', frame)

    # キー入力を1ms待って、kが27(ESC)だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break
# キャプチャーをリリースしてウィンドウ全て閉じる
cap.release()

cv2.destroyAllWindows()