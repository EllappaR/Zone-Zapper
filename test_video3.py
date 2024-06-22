import cv2
import pytesseract

# Load video
video_capture = cv2.VideoCapture('static/videos/pc2.mp4')

# Initialize variables to store the detected plate image and text
detected_plate_image = None
detected_plate_text = ""

# Counter to keep track of saved images
save_counter = 0

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
   
    if not ret:
        break

    # Preprocess frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    # Initialize contour for the license plate
    plate_contour = None
    j=1
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018 * perimeter, True)
        if len(approx) == 4:
            plate_contour = approx
            break

    if plate_contour is not None:
        # Draw contour around the plate
        cv2.drawContours(frame, [plate_contour], -1, (0, 255, 0), 3)
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

        # Apply OCR on the plate region
        x, y, w, h = cv2.boundingRect(plate_contour)
        plate_roi = gray[y:y+h, x:x+w]
        plate_text = pytesseract.image_to_string(plate_roi, config='--psm 11')
        print(plate_text)
        
        # If a new plate is detected, update the detected_plate_image and detected_plate_text
        if plate_text != detected_plate_text:
            detected_plate_text = plate_text
            detected_plate_image = plate_roi
            if save_counter<=5:
                # Save the detected plate image
                plate_filename = f"plate_{save_counter}.jpg"
                cv2.imwrite("static/cropped/"+plate_filename, detected_plate_image)
                print(f"Saved Plate Image as: {plate_filename}")

                # Increment the save counter
                
                save_counter += 1
    j+=1
   
    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture
video_capture.release()
cv2.destroyAllWindows()
