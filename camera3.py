# camera.py

import cv2
import PIL.Image
import numpy as np
from PIL import Image
import pytesseract




class VideoCamera3(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        
        self.video = cv2.VideoCapture(0)
        self.k=1

        self.detected_plate_image = None
        self.detected_plate_text = ""

        # Counter to keep track of saved images
        self.save_counter = 1

    
    def __del__(self):
        self.video.release()
        
    
    def get_frame(self):
        success, frame = self.video.read()
        cv2.imwrite("static/getimg.jpg", frame)

        ##
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
            #print(plate_text)
            if self.save_counter==5:
                ff=open("static/vno.txt","w")
                ff.write(plate_text)
                ff.close()
            
            # If a new plate is detected, update the detected_plate_image and detected_plate_text
            if plate_text != self.detected_plate_text:
                self.detected_plate_text = plate_text
                self.detected_plate_image = plate_roi
                if self.save_counter<=5:
                    # Save the detected plate image
                    plate_filename = f"plate_{self.save_counter}.jpg"
                    cv2.imwrite("static/cropped/"+plate_filename, self.detected_plate_image)
                    #print(f"Saved Plate Image as: {plate_filename}")

                    # Increment the save counter
                    
                    self.save_counter += 1
        j+=1
        ##

        '''pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        Actual_image = cv2.imread("static/getimg.jpg")
        #Sample_img = cv2.resize(Actual_image,(400,350))
        Image_ht,Image_wd,Image_thickness = Actual_image.shape
        Sample_img = cv2.cvtColor(Actual_image,cv2.COLOR_BGR2RGB)
        texts = pytesseract.image_to_data(Sample_img) 
        mytext=""
        prevy=0



        for cnt,text in enumerate(texts.splitlines()):
            
            if cnt==0:
                continue
            text = text.split()
            if len(text)==12:
                x,y,w,h = int(text[6]),int(text[7]),int(text[8]),int(text[9])
                if(len(mytext)==0):
                    prey=y
                if(prevy-y>=10 or y-prevy>=10):
                    #print(mytext)
                    s=1
                    #mytext=""
                mytext = mytext + text[11]+" "
                prevy=y

        v11=mytext
        ff=open("static/vno.txt","w")
        ff.write(v11)
        ff.close()'''
            
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
