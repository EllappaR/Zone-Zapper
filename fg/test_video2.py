import cv2
import pytesseract

# Load video
video_capture = cv2.VideoCapture('static/videos/pc6.mp4')

while True:
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
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # Initialize contour for the license plate
    plate_contour = None

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018 * perimeter, True)
        if len(approx) == 4:
            plate_contour = approx
            break

    if plate_contour is not None:
        # Draw contour around the plate
        cv2.drawContours(frame, [plate_contour], -1, (0, 255, 0), 3)

        # Apply OCR on the plate region
        x, y, w, h = cv2.boundingRect(plate_contour)
        plate_roi = gray[y:y+h, x:x+w]
        plate_text = pytesseract.image_to_string(plate_roi, config='--psm 11')
        print(plate_text)
        # Display the result
        cv2.putText(frame, plate_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
