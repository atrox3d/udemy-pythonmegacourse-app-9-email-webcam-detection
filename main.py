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

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(          # calculate difference between frame matrixes
                first_frame,
                gray_frame_gau
    )

    thresh_frame = cv2.threshold(       # classify frame
                delta_frame,
                60,                     # threshold
                255,                    # change to 255
                cv2.THRESH_BINARY       # algorythm
    )[1]                                # get second item

    dil_frame = cv2.dilate(             # clean frame
                thresh_frame,
                None,                   # config array
                iterations=2            # number of iterations
    )

    cv2.imshow('webcam', dil_frame)     # show webcam frame

    contours, chk = cv2.findContours(   # detect contours
                dil_frame,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(  # find contour rectangle
                contour
        )

        rectangle = cv2.rectangle(      # draw rectangle on frame
                frame,                  # original frame
                (x, y),                 # top-left corner
                (x + w, y + h),         # low-right corner
                (0, 255, 0),            # color
                3                       # width
        )

        if rectangle.any():             # change status to 1 if we have a rectangle
            status = 1

    status_list.append(status)
    status_list = status_list[-2:]      # cut the list, leaving last 2 items

    before, after = status_list         # extract statuses
    if before == 1 and after == 0:      # if objects exited from view
        sendmail()
    cv2.imshow("output", frame)

    key = cv2.waitKey(1)                # wait for keyboard press for a millisecond (0 == forever)
                                        # -1 == no key pressed
    if key == ord('q'):                 # 'q' == 113
        break

video.release()                         # close webcam

