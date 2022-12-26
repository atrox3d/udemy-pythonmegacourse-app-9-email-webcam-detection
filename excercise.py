import streamlit as st
import cv2
import time

st.title('motion detector')

col1, col2 = st.columns(2)                                      # create two columns for buttons
start = col1.button('start camera')
stop = col2.button('stop camera')

start
stop
if start:
    camera = cv2.VideoCapture(0)                                # start webcam

    image = st.image([])                                        # prepare empty image object

    while not stop:                                             # loop until stop button is pressed
        check, frame = camera.read()                            # get next frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)      # convert BGR to RGB

        text = now = time.strftime("%b %d, %Y %H:%M:%S")        # prepare time text
        cv2.putText(                                            # draw text on current frame
            img=frame_rgb,                                      # dest frame
            text=text,
            org=(0, 50),                                        # bottom left corner of text
            fontFace=cv2.FONT_ITALIC,
            fontScale=1,
            color=(255, 255, 255),
            thickness=2,
            lineType=cv2.LINE_AA
        )

        image.image(frame_rgb)                                  # update image with current frame

    camera.release()
