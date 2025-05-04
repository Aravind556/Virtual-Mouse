import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui  

######################
wCam, hCam = 640, 480
frameR = 100     #Frame Reduction
smoothening = 7  #random value
scroll_sensitivity = 5  # Scroll sensitivity factor
scroll_threshold = 20     # Deadzone around the center line
######################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Initialize pyautogui
pyautogui.FAILSAFE = False  

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()  

try:
    while True:
        # Step1: Find the landmarks
        success, img = cap.read()
        if not success or img is None:
            print("Failed to capture frame")
            continue
            
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)


        center_y = hCam // 2
        cv2.line(img, (0, center_y), (wCam, center_y), (0, 255, 255), 2)  # Center line
        cv2.line(img, (0, center_y - scroll_threshold), (wCam, center_y - scroll_threshold), (0, 255, 255), 1)  # Upper threshold
        cv2.line(img, (0, center_y + scroll_threshold), (wCam, center_y + scroll_threshold), (0, 255, 255), 1)  # Lower threshold

        #Getting the tip of the index and middle finger
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # Check which fingers are up
            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                        (255, 0, 255), 2)

            # Only Index Finger: Moving Mode
            if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0:
                # Step5: Convert the coordinates
                x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

                # Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # Move Mouse
                pyautogui.moveTo(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            #Both Index and middle are up: Clicking Mode
            if fingers[1] == 1 and fingers[2] == 1:
                #Find distance between fingers
                length, img, lineInfo = detector.findDistance(8, 12, img)

                #Click mouse if distance short
                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()
                    
            # Only Thumb finger is up: Horizontal Line-Based Scrolling Mode
            if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                # Get thumb position
                thumb_x, thumb_y = lmList[4][1:]
                
                # Highlight thumb in scrolling mode
                cv2.circle(img, (thumb_x, thumb_y), 15, (0, 255, 0), cv2.FILLED)
                
                # Check thumb position relative to center line
                if thumb_y < center_y - scroll_threshold:
                    # Thumb is above threshold - scroll up
                    scroll_amount = int(5 * scroll_sensitivity)
                    pyautogui.scroll(scroll_amount)
                    cv2.putText(img, f"SCROLLING UP ({scroll_amount})", (thumb_x-20, thumb_y-30), 
                               cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                    # Draw arrow indicator
                    cv2.arrowedLine(img, (50, 100), (50, 50), (0, 255, 0), 4)
                    
                elif thumb_y > center_y + scroll_threshold:
                    # Thumb is below threshold - scroll down
                    scroll_amount = -int(5 * scroll_sensitivity)
                    pyautogui.scroll(scroll_amount)
                    cv2.putText(img, f"SCROLLING DOWN ({-scroll_amount})", (thumb_x-20, thumb_y-30), 
                               cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                    # Draw arrow indicator
                    cv2.arrowedLine(img, (50, 100), (50, 150), (0, 255, 0), 4)
                    
                else:
                    # Thumb is in the threshold area - no scrolling
                    cv2.putText(img, "NO SCROLL (IN DEADZONE)", (thumb_x-20, thumb_y-30), 
                               cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        # Step11: Frame rate
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (28, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)

        # Step12: Display
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Added proper exit with 'q'
            break
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    # Clean up
    cap.release()
    cv2.destroyAllWindows()