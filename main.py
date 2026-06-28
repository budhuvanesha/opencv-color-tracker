import cv2 
import numpy as np

cap = cv2.VideoCapture(0)


while True:
    success, frame = cap.read()

    if success == False:
        break
    
    height, width, channels = frame.shape

    left_border = int((1/3)*width)
    right_border = int((2/3)*width)
    upper_border = int((1/3)*height)
    lower_border = int((2/3)*height)

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([170, 160, 150])
    upper_red = np.array([180, 200, 250])
    mask = cv2.inRange(hsv_frame, lower_red,upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame, (left_border, 0), (left_border, height), (255, 0, 0), 1)
    cv2.line(frame, (right_border, 0), (right_border, height), (255, 0, 0), 1)
    cv2.line(frame, (0, upper_border), (width, upper_border), (255, 0, 0), 1)
    cv2.line(frame, (0, lower_border), (width, lower_border), (255, 0, 0), 1)
    
    if contours:
    
        largest_object = max(contours, key = cv2.contourArea)
        largest_area = (cv2.contourArea(largest_object))

        if largest_area > 500:

            x, y, w, h = cv2.boundingRect(largest_object)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            center_x = x + w // 2
            center_y = y + h // 2
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.putText(frame, f"Coordinates: {center_x}, {center_y}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

            if center_x <= left_border:
                h_direction = "Left"

            elif center_x <= right_border:
                h_direction = "Center"

            else:
                h_direction = "Right"

            if center_y <= upper_border:
                v_direction = "Top"

            elif center_y <= lower_border:
                v_direction = "Middle"

            else:
                v_direction = "Bottom"

            cv2.putText(frame, f"{h_direction}, {v_direction}", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)


    cv2.imshow("Output-1", hsv_frame)
    cv2.imshow("Output-2", frame)
    cv2.imshow("Output-3", mask)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()