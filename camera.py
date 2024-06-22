# camera.py

import cv2
import PIL.Image
import numpy as np
from PIL import Image
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        
        self.video = cv2.VideoCapture("static/v5.mp4")
        self.k=1

        
    
    def __del__(self):
        self.video.release()
        
    
    def get_frame(self):
        success, image = self.video.read()
        #fn1="F"+str(self.k)+".jpg"
        #cv2.imwrite("static/dd/"+fn1, image)
        self.k+=1

        #open the main image and convert it to gray scale image
        #main_image = cv2.imread('static//r7.jpg')
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #open the template as gray scale image
        template = cv2.imread('static/upload/t1.jpg', 0)
        width, height = template.shape[::-1] #get the width and height
        #match the template using cv2.matchTemplate
        match = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        position = np.where(match >= threshold) #get the location of template in the image
        j=0
        for point in zip(*position[::-1]): #draw the rectangle around the matched template
           cv2.rectangle(image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)

           ff=open("check.txt","w")
           ff.write("1")
           ff.close()
           j+=1

   
        
        '''for (x, y, w, h) in faces:
            mm=cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imwrite("static/myface.jpg", mm)

            
            image = cv2.imread("static/myface.jpg")
            cropped = image[y:y+h, x:x+w]
            gg="f"+str(j)+".jpg"
            cv2.imwrite("static/faces/"+gg, cropped)

            ###
            if self.k<=40:
                self.k+=1
                fnn=""
                ff12=open("mask.txt","r")
                mst=ff12.read()
                ff12.close()
                if mst=="face":
                    fnn=uu+"_"+str(self.k)+".jpg"
                else:
                    fnn="m"+uu+"_"+str(self.k)+".jpg"

                ff2=open("det.txt","w")
                ff2.write(str(self.k))
                ff2.close()
                if uu1=="2":
                    cv2.imwrite("static/frame/"+fnn, cropped)
                #cv2.imwrite("https://iotcloud.co.in/testsms/upload/"+fnn, cropped)
                ###
                mm2 = PIL.Image.open('static/faces/'+gg)
                rz = mm2.resize((100,100), PIL.Image.ANTIALIAS)
                rz.save('static/faces/'+gg)
                #rz.save("https://iotcloud.co.in/testsms/upload/"+gg)
            j += 1

        ff4=open("img.txt","w")
        ff4.write(str(j))
        ff4.close()    '''

            

        

            
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
