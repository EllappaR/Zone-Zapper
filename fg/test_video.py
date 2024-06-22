import cv2
import pytesseract

# Function to preprocess the image
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)
    return edged

# Function to detect and extract number plate
def detect_number_plate(image):
    contours, _ = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    plate_contour = None
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018 * perimeter, True)
        if len(approx) == 4:
            plate_contour = approx
            break
   
    if plate_contour is not None:
        x, y, w, h = cv2.boundingRect(plate_contour)
        plate_roi = gray[y:y+h, x:x+w]
        plate_text = pytesseract.image_to_string(plate_roi, config='--psm 11')
        cv2.drawContours(image, [plate_contour], -1, (0, 255, 0), 3)
        cv2.putText(image, plate_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

# Open video capture
cap = cv2.VideoCapture('static/c1.mp4')  # Replace 'video.mp4' with your video file path

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
   
    # Preprocess the frame
    #edged = preprocess_image(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)
   
    # Detect and extract number plate
    detect_number_plate(edged)
   
    # Display the frame
    cv2.imshow('Number Plate Detection', frame)
   
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
