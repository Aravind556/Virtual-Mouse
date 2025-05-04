import streamlit as st
import cv2
import pyautogui
import numpy as np
import time
from PIL import Image
from HandTrackingModule import handDetector

# Streamlit UI
st.set_page_config(page_title="AI Virtual Mouse", layout="wide")
st.title("🖱 AI Virtual Mouse Controller")
st.markdown("Use hand gestures to control your mouse in real-time.")

# Adjustable parameters
frameR = st.slider("Frame Reduction", 50, 200, 100)
smoothening = st.slider("Smoothening", 1, 10, 5)
scroll_threshold = st.slider("Scroll Threshold", 10, 50, 25)
scroll_speed = st.slider("Scroll Speed", 1, 10, 5)

screen_w, screen_h = pyautogui.size()
frame_placeholder = st.empty()

# Control buttons
start = st.button("Start AI Mouse", key="start_button")
stop = st.button("Stop AI Mouse", key="stop_button")

# Runtime control flag
if 'run_mouse' not in st.session_state:
    st.session_state.run_mouse = False

if start:
    st.session_state.run_mouse = True
if stop:
    st.session_state.run_mouse = False

# Run only when started
if st.session_state.run_mouse:
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    detector = handDetector()
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    while st.session_state.run_mouse:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList, _ = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]  # Index finger
            x2, y2 = lmList[12][1:]  # Middle finger

            fingers = detector.fingersUp()

            # Move Mode
            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frameR, 640 - frameR), (0, screen_w))
                y3 = np.interp(y1, (frameR, 480 - frameR), (0, screen_h))

                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                pyautogui.moveTo(screen_w - clocX, clocY)
                plocX, plocY = clocX, clocY

            # Click Mode
            if fingers[1] == 1 and fingers[2] == 1:
                length, _, _ = detector.findDistance(8, 12, img, draw=False)
                if length < 40:
                    pyautogui.click()
                    time.sleep(0.2)

            # Scroll Mode
            if fingers[0] == 1 and sum(fingers[1:]) == 0:
                thumb_y = lmList[4][2]
                center_y = 480 // 2
                if thumb_y < center_y - scroll_threshold:
                    pyautogui.scroll(5 * scroll_speed)
                elif thumb_y > center_y + scroll_threshold:
                    pyautogui.scroll(-5 * scroll_speed)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(img_rgb, channels="RGB")

        # Break when Stop button is pressed externally
        if not st.session_state.run_mouse:
            cap.release()
            break