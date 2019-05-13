import cv2

def init_avg(cap):
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray.copy().astype('float')