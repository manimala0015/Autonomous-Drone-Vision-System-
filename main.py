import cv2
import numpy as np
# Initialize the video capture (0 for default webcam, change if using external cam or drone feed)
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
   # Resize the frame (optional)
    frame = cv2.resize(frame, (640, 480))
    # Convert BGR to HSV for better color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define HSV range for red color (adjust based on environment)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
      # Create a binary mask where red is detected
    mask = cv2.inRange(hsv, lower_red, upper_red)
   # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Draw contours and determine object position
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # Ignore small areas
            x, y, w, h = cv2.boundingRect(cnt)
            cx = x + w // 2
            cy = y + h // 2
           # Draw rectangle and center point
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
            # Position logic
            if cx < 213:
                position = "Left"
            elif cx > 426:
                position = "Right"
            else:
                position = "Center"
         cv2.putText(frame, f"Object: {position}", (10, 30),
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
  # Display frames
    cv2.imshow("Drone Camera", frame)
    cv2.imshow("Red Mask", mask)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
      
