from cv2 import cv2
import numpy as np
vid = cv2.VideoCapture("angle.mp4")

_, prev_frame = vid.read()
prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)


while 1:
    _, frame = vid.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff = (frame.astype(np.int16) - prev_frame.astype(np.int16))/(1+np.maximum(frame.astype(np.int16), prev_frame.astype(np.int16)))*255
    cv2.imshow("asdfg", frame)
    cv2.imshow("asdf", np.abs(diff).astype(np.uint8))

    prev_frame = frame
    key=cv2.waitKey(10000)
    if key == ord("w"):
        continue
    if key == ord("q"):
        break

# 804 156
# 858 156