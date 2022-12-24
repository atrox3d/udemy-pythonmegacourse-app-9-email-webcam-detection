import cv2
import time
from mailer import sendmail

video = cv2.VideoCapture(0)             # get webcam
time.sleep(1)                           # give webcam time to start

first_frame = None
status_list = []
while True:
    status = 0
    check, frame = video.read()         # get check and frame
    # print(f'{check=}')

    # image preprocessing:
    grayframe = cv2.cvtColor(           # convert to grayscale to lower the amount of data in the matrix
                frame,
                cv2.COLOR_BGR2GRAY
    )

    gray_frame_gau = cv2.GaussianBlur(  # blur image
                grayframe,
                (21, 21),               # blur amount
                0                       # standard deviation
    )

    # first_frame = first_frame or gray_frame_gau
    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # classify frame
    thresh_frame = cv2.threshold(
                delta_frame,
                60,                     # threshold
                255,                    # change to 255
                cv2.THRESH_BINARY       # algorythm
    )[1]                                # get second item

    # clean frame
    dil_frame = cv2.dilate(
                thresh_frame,
                None,                   # config array
                iterations=2            # number of iterations
    )
    # show webcam frame
    cv2.imshow('webcam', dil_frame)

    contours, check = cv2.findContours(
                dil_frame,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(
                frame,                  # original frame
                (x, y),                 # top-left corner
                (x + w, y + h),         # low-right corner
                (0, 255, 0),            # color
                3                       # width
        )
        if rectangle.any():
            status = 1

    status_list.append(status)
    status_list = status_list[-2:]
    # print
    if status_list[0] == 1 and status_list[1] == 0:
        sendmail()
    cv2.imshow("output", frame)

    key = cv2.waitKey(1)                # wait for keyboard press for a millisecond (0 == forever)
    # print(f'{key=}')                    # -1 == no key pressed
    if key == ord('q'):                 # 'q' == 113
        # print(f'{key=} is "q"')
        break

video.release()                         # close webcam

