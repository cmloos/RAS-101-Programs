import cv2
import numpy as np
import pyttsx3
import time
import winsound  # Built-in audio module on Windows

# --- PRE-RENDER SPEECH AUDIO AT STARTUP ---
print("Generating audio alert file...")
tts = pyttsx3.init()
tts.save_to_file("Red Square", "red_square.wav")
tts.runAndWait()
print("Audio ready!")

def play_alert():
    """Plays the pre-rendered audio file asynchronously without blocking the loop."""
    # SND_ASYNC plays audio in the background so the camera feed doesn't freeze
    winsound.PlaySound("red_square.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

# --- CAMERA SETUP & TIMING VARIABLES ---
cap = cv2.VideoCapture(1)  # Change to 0 if webcam doesn't open

last_spoken_time = 0
cooldown_seconds = 3.0  # Seconds to wait before repeating

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Convert frame BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define red color bounds (handles HSV wrap-around at 0 and 180)
    lower_red1 = np.array([0, 10, 10])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 10, 10])
    upper_red2 = np.array([180, 255, 255])

    # Combine both red masks
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Clean up noise and sharpen block edges
    kernel = np.ones((7, 7), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    red_square_found = False

    for cnt in contours:
        if cv2.contourArea(cnt) < 500:
            continue

        area = cv2.contourArea(cnt)
        rect = cv2.minAreaRect(cnt)  # Get minimum area rotated rectangle
        (w, h) = rect[1]
        rect_area = w * h

        if rect_area > 0:
            extent = float(area) / rect_area
            aspect_ratio = max(w, h) / max(min(w, h), 1)

            # Square check based on area fill & aspect ratio (handles rounded/tilted blocks)
            if 1.0 <= aspect_ratio <= 1.25 and 0.78 <= extent <= 0.95:
                red_square_found = True

                # Get rotated box points for drawing
                box = cv2.boxPoints(rect)
                box = np.int32(box)
                cx, cy = int(rect[0][0]), int(rect[0][1])

                # Draw green bounding shape and text label on the frame
                cv2.drawContours(frame, [box], 0, (0, 255, 0), 3)
                cv2.putText(frame, "Red Square", (cx - 40, cy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # --- VOICE TRIGGER LOGIC ---
    current_time = time.time()

    # Play alert if square is detected and the cooldown period has passed
    if red_square_found and (current_time - last_spoken_time > cooldown_seconds):
        last_spoken_time = current_time
        play_alert()

    # Display status text on video stream
    status = "Red Square Detected!" if red_square_found else "Searching..."
    cv2.putText(frame, status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show live stream
    cv2.imshow("Webcam Red Square Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()