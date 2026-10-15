import cv2
import numpy as np
import pyttsx3
import time
import winsound  # Built-in audio module on Windows

camera = cv2.VideoCapture(1) #Designates video channel 1 as an object named camera
tts = pyttsx3.init()

#   ===VARIABLES===
Kernal_Resolution = 7
Lower_Hue = 120
Upper_Hue = 255
Lower_Value = 30
Upper_Value = 255
Minimum_Contour_Area = 500
Minimum_Aspect_Ratio = 1.0
Maximum_Aspect_Ratio = 1.25
Minimum_Extent = 0.78
Maximum_Extent = 0.95
Box_Colour = (0, 255, 0)
Box_Thickness = 2
Time_Between_Alerts = 3

#The following 4 lines dictate the colour range that will be considered as "red" by the program
lower_red1 = np.array([0, Lower_Hue, Lower_Value])
upper_red1 = np.array([10, Upper_Hue, Upper_Value])
lower_red2 = np.array([160, Lower_Hue, Lower_Value])
upper_red2 = np.array([180, Upper_Hue, Upper_Value])

#The following 2 lines dictate the colour range that will be considered as "blue" by the program
lower_blue = np.array([100, Lower_Hue, Lower_Value])
upper_blue = np.array([130, Upper_Hue, Upper_Value])

#The following 2 lines dictate the colour range that will be considered as "green" by the program
lower_green = np.array([35, Lower_Hue, Lower_Value])
upper_green = np.array([85, Upper_Hue, Upper_Value])

#The following 2 lines dictate the colour range that will be considered as "yellow" by the program
lower_yellow = np.array([20, Lower_Hue, Lower_Value])
upper_yellow = np.array([35, Upper_Hue, Upper_Value])

last_spoken_time = 0

while True:
    got_image, captured_frame =  camera.read() #Creates a boolean and a frame object based on the output of camera.read()

    if not got_image: #If no frame was obtained from camera.read(), then this for loop will break the run out of the while loop
        print("Camera is inactive") #Prints to terminal that the camera is isn't functioning and is the reason for the end of the run
        break

    hsv_frame = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2HSV) #Converts all pixels in the captured frames to HSV values

    #The following three lines create two colour masks for red, before combining them into a single mask
    red_mask_part_1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    red_mask_part_2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask_part_1, red_mask_part_2)

    #The following three lines create colour masks for blue, green, and yellow respectively.
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

    kernel = np.ones((Kernal_Resolution, Kernal_Resolution), np.uint8) #Sets up a kernel for "pixel sifting"

    #The following code goes through the masks for each colour and dialates the pixels before eroding them in order to reduce noise
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)

    #The following code counts the number of contours in each of the colour masks
    red_mask_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_mask_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_mask_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellow_mask_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #The following booleans will be used to know when a square is found with any of the four colours
    red_square_found = False
    blue_square_found = False
    green_square_found = False
    yellow_square_found = False

    #The number of squares is reset to zero before being counted by the next 4 for functions
    red_square_count = 0
    blue_square_count = 0
    green_square_count = 0
    yellow_square_count = 0

    for cnt in red_mask_contours: #This for loop will check each contour to see if it counts as a red square
        if cv2.contourArea(cnt) < Minimum_Contour_Area:
            continue

        area = cv2.contourArea(cnt)
        rectangle = cv2.minAreaRect(cnt)
        (width, height) = rectangle[1]
        rectangle_area = width * height

        if rectangle_area > 0:
            extent = float(area) / rectangle_area
            aspect_ratio = max(width, height) / max(min(width, height), 1)

            if Minimum_Aspect_Ratio < aspect_ratio < Maximum_Aspect_Ratio and Minimum_Aspect_Ratio < aspect_ratio < Maximum_Aspect_Ratio:
                red_square_found = True

                box = cv2.boxPoints(rectangle)
                box = np.int32(box)
                cx, cy = int(rectangle[0][0]), int(rectangle[0][1])

                cv2.drawContours(captured_frame, [box], 0, Box_Colour, Box_Thickness)
                cv2.putText(captured_frame, f"Red Square: {int(rectangle_area)}px", (cx - 40, cy - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                red_square_count += 1

    for cnt in blue_mask_contours: # This for loop will check each contour to see if it counts as a blue square
        if cv2.contourArea(cnt) < Minimum_Contour_Area:
            continue

        area = cv2.contourArea(cnt)
        rectangle = cv2.minAreaRect(cnt)
        (width, height) = rectangle[1]
        rectangle_area = width * height

        if rectangle_area > 0:
            extent = float(area) / rectangle_area
            aspect_ratio = max(width, height) / max(min(width, height), 1)

            if Minimum_Aspect_Ratio < aspect_ratio < Maximum_Aspect_Ratio and Minimum_Aspect_Ratio < aspect_ratio < Maximum_Aspect_Ratio:
                blue_square_found = True

                box = cv2.boxPoints(rectangle)
                box = np.int32(box)
                cx, cy = int(rectangle[0][0]), int(rectangle[0][1])

                cv2.drawContours(captured_frame, [box], 0, Box_Colour, Box_Thickness)
                cv2.putText(captured_frame, f"Blue Square: {int(rectangle_area)}px", (cx - 40, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                blue_square_count += 1

    for cnt in green_mask_contours: # This for loop will check each contour to see if it counts as a green square
        if cv2.contourArea(cnt) < Minimum_Contour_Area:
            continue

        area = cv2.contourArea(cnt)
        rectangle = cv2.minAreaRect(cnt)
        (width, height) = rectangle[1]
        rectangle_area = width * height

        if rectangle_area > 0:
            extent = float(area) / rectangle_area
            aspect_ratio = max(width, height) / max(min(width, height), 1)

            if Minimum_Aspect_Ratio < aspect_ratio < Maximum_Aspect_Ratio and Minimum_Aspect_Ratio < aspect_ratio < Maximum_Aspect_Ratio:
                green_square_found = True

                box = cv2.boxPoints(rectangle)
                box = np.int32(box)
                cx, cy = int(rectangle[0][0]), int(rectangle[0][1])

                cv2.drawContours(captured_frame, [box], 0, Box_Colour, Box_Thickness)
                cv2.putText(captured_frame, f"Green Square: {int(rectangle_area)}px", (cx - 40, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                green_square_count += 1

    for cnt in yellow_mask_contours: # This for loop will check each contour to see if it counts as a blue square
        if cv2.contourArea(cnt) < Minimum_Contour_Area:
            continue

        area = cv2.contourArea(cnt)
        rectangle = cv2.minAreaRect(cnt)
        (width, height) = rectangle[1]
        rectangle_area = width * height

        if rectangle_area > 0:
            extent = float(area) / rectangle_area
            aspect_ratio = max(width, height) / max(min(width, height), 1)

            if Minimum_Aspect_Ratio < aspect_ratio < Maximum_Aspect_Ratio and Minimum_Aspect_Ratio < aspect_ratio < Maximum_Aspect_Ratio:
                yellow_square_found = True

                box = cv2.boxPoints(rectangle)
                box = np.int32(box)
                cx, cy = int(rectangle[0][0]), int(rectangle[0][1])

                cv2.drawContours(captured_frame, [box], 0, Box_Colour, Box_Thickness)
                cv2.putText(captured_frame, f"Yellow Square: {int(rectangle_area)}px", (cx - 40, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                yellow_square_count += 1

    # cv2.imshow("Red Mask", red_mask)
    # cv2.imshow("Blue Mask", blue_mask)
    # cv2.imshow("Green Mask", green_mask)
    # cv2.imshow("Yellow Mask", yellow_mask)
    cv2.putText(captured_frame, f"R:{int(red_square_count)} B:{int(blue_square_count)} G:{int(green_square_count)} Y:{int(yellow_square_count)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow("Camera Feed", captured_frame) #Displays the captured_frame object in its own designated window
    cv2.waitKey(1) #Prevents windows from assuming that the new window isn't responding

    current_time = time.time()

    if (red_square_found or blue_square_found or green_square_found or yellow_square_found) and (current_time - last_spoken_time > Time_Between_Alerts):
        last_spoken_time = current_time
        tts.say(f"There are {int(red_square_count)} red squares, {int(blue_square_count)} blue squares, {int(green_square_count)} green squares, and {int(yellow_square_count)} yellow squares.")
        tts.runAndWait()



camera.release()
cv2.destroyAllWindows()