import cv2 
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    print(hsv_frame[240,320])

    lower_red = np.array([0, 160, 150])
    upper_red = np.array([180, 200, 250])
    mask = cv2.inRange(hsv_frame, lower_red,upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    #cv2.imshow("Output-1", hsv_frame)
    cv2.imshow("Output-2", frame)
    cv2.imshow("Output-3", mask)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()