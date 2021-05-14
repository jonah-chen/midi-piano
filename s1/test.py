import numpy as np
from time import perf_counter, time_ns
import matplotlib.pyplot as plt
from daq import VideoGet
from cv2 import cv2

def find_key(*ptr):
    vid = VideoGet().start()
    prev_frame = np.zeros((1080,1920,))

    right_key = np.zeros((54,96))
    right_img = None

    wrong_key = np.zeros((54,96))
    wrong_img = None

    # First try to detect the correct key
    while 1:
        frame = vid.frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame,(7,7),0)
        diff = (frame.astype(np.int16) - prev_frame.astype(np.int16))/(1+np.maximum(frame.astype(np.int16), prev_frame.astype(np.int16)))*255

        cv2.imshow("frame", frame)
        cv2.imshow("diff", np.abs(diff).astype(np.uint8))
        
        # 1080 x 1920 -> 54 x 96
        candidates = np.array([[np.sum(diff[20*i : 20*(i+1), 20*j: 20*(j+1)]**2) for j in range(96)] for i in range(54)])

        max1 = sum([np.max(candidates[i]) for i in range(54)])
        max2 = sum([np.max(right_key[i]) for i in range(54)])

        if max1 > max2:
            right_key = candidates
            right_img = frame
        
        prev_frame = frame

        key=cv2.waitKey(1)
        if key == ord("w"): # press w to rezero
            prev_frame = frame
            right_key = np.zeros((54,96))
        
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
    
    # try to detect the wrong key
    while 1:
        frame = vid.frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame,(7,7),0)
        diff = (frame.astype(np.int16) - prev_frame.astype(np.int16))/(1+np.maximum(frame.astype(np.int16), prev_frame.astype(np.int16)))*255

        cv2.imshow("frame", frame)
        cv2.imshow("diff", np.abs(diff).astype(np.uint8))
        
        # 1080 x 1920 -> 54 x 96
        candidates = np.array([[np.sum(diff[20*i : 20*(i+1), 20*j: 20*(j+1)]**2) for j in range(96)] for i in range(54)])

        max1 = sum([np.max(candidates[i]) for i in range(54)])
        max2 = sum([np.max(wrong_key[i]) for i in range(54)])

        if max1 > max2:
            wrong_key = candidates
            wrong_img = frame

        prev_frame = frame

        key=cv2.waitKey(1)
        if key == ord("w"): # press w to rezero
            prev_frame = frame
            right_key = np.zeros((54,96))
        
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
    
    plt.imshow(np.abs(right_img-wrong_img))
    plt.show()

    plt.imshow(right_key-wrong_key, interpolation='nearest')
    plt.show()
    

def callibrate(diff, y, x, radius = 3):
    return np.sum(diff[y-radius:y+radius,x-radius:x+radius])



e4, eb4 = [], []
y = []

vid = VideoGet().start()
start_time = time_ns()

prev_frame = vid.frame
prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_frame = cv2.GaussianBlur(prev_frame,(5,5),0)

d = False

while 1:
    if not d:
        start = perf_counter()

    frame = vid.frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame,(5,5),0)
    y.append(time_ns()-start_time)
    d = (frame == prev_frame).all()
    if d:
        print("same")
    
    diff = (frame.astype(np.int16) - prev_frame.astype(np.int16))/(1+np.maximum(frame.astype(np.int16), prev_frame.astype(np.int16)))*255
    cv2.imshow("asdfg", frame)
    cv2.imshow("asdf", np.abs(diff).astype(np.uint8))

    prev_frame = frame

 
    e4.append(callibrate(diff, 377, 770))
    eb4.append(callibrate(diff, 373, 736))

    # 555, 363
    key=cv2.waitKey(1)
    if key == ord("w"):
        e4 = []
        eb4 = []
        y = []
        # note3 = []
        # note4 = []
        # note5 = []
        # note6 = []
        prev_frame = frame
    if key == ord("q"):
        break
    
    if not d:
        end = perf_counter()

        print(f"frame time: {1e3*(end-start):.1f}ms @ {end}")

vid.stop()
cv2.destroyAllWindows()

print(np.array(y)/1000000)

plt.plot(y, np.array(e4), label="e4")
# plt.yscale("log")
plt.plot(y, np.array(eb4), label="eb4")
# plt.plot(np.array(note3)**3/2.59e11, label="note3")
# plt.plot(np.array(note4)**3/2.59e11, label="note4")
# plt.plot(np.array(note5)**3/2.59e11, label="note5")
# plt.plot(np.array(note6)**3/2.59e11, label="note6")
 # 1040 614

plt.legend()
plt.show()