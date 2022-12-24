import cv2
import time

video = cv2.VideoCapture(0)             # get webcam
time.sleep(1)                           # give webcam time to start

while True:
    check, frame = video.read()         # get check and frame
    print(f'{check=}')
    cv2.imshow('webcam', frame)         # show webcam frame

    key = cv2.waitKey(1)                # wait for keyboard press for a millisecond (0 == forever)
    print(f'{key=}')                    # -1 == no key pressed
    if key == ord('q'):                 # 'q' == 113
        print(f'{key=} is "q"')
        break

video.release()                         # close webcam

