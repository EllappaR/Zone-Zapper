import cv2
import os,argparse
import pytesseract
from PIL import Image

path_main = 'static/d1'
for fname in os.listdir(path_main):

    # Load the image
    image = cv2.imread("static/d1/"+fname)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding to get a binary image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    min_area = 500
    max_area = 5000
    filtered_contours = [cnt for cnt in contours if min_area < cv2.contourArea(cnt) < max_area]

    # Draw rectangles around the filtered contours
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    cv2.imwrite("static/d2/"+fname, image)
    ##
    image = cv2.imread("static/d2/"+fname)
    h1=h+10
    w1=w+30
    
    
    cropped = image[y:y+h1, x:x+w1]
    gg="static/d2/f"+str(j)+".jpg"
    cv2.imwrite(""+gg, cropped)
