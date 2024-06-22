import cv2
import pytesseract

# Load image
image = cv2.imread('static/TN Car/9.jpeg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# Preprocess image
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)

# Find contours in the edged image
contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

# Initialize contour for the license plate
plate_contour = None

for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.018 * perimeter, True)
    if len(approx) == 4:
        plate_contour = approx
        break

# Draw contour around the plate
cv2.drawContours(image, [plate_contour], -1, (0, 255, 0), 3)

# Apply OCR on the plate region
x, y, w, h = cv2.boundingRect(plate_contour)
plate_roi = gray[y:y+h, x:x+w]
plate_text = pytesseract.image_to_string(plate_roi, config='--psm 11')

# Display the result
print("Detected Plate Number:", plate_text)
cv2.imshow('Detected Plate', plate_roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
