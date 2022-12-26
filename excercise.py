import streamlit as st
import cv2
from datetime import datetime

st.title('motion detector')

col1, col2 = st.columns(2)                                      # create two columns for buttons
start = col1.button('start camera')
stop = col2.button('stop camera')

st.info(f'{start=} {stop=}')

if start:
    camera = cv2.VideoCapture(0)                                # start webcam

    image = st.image([])                                        # prepare empty image object

    while not stop:                                             # loop until stop button is pressed
        check, frame = camera.read()                            # get next frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)      # convert BGR to RGB

        # create captions from current time
        now = datetime.now()
        captions = [
            dict(text=now.strftime('%A'), org=(10, 50), color=(255, 255, 255)),
            dict(text=now.strftime('%H:%M:%S'), org=(10, 100), color=(0, 255, 0))
        ]
        for caption in captions:
            cv2.putText(                                        # draw text on current frame
                img=frame_rgb,                                  # dest frame
                text=caption['text'],
                org=caption['org'],                             # bottom left corner of text
                fontFace=cv2.FONT_ITALIC,
                fontScale=1,
                color=caption['color'],
                thickness=2,
                lineType=cv2.LINE_AA
            )

        image.image(frame_rgb)                                  # update image with current frame

    camera.release()
