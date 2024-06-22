
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
Actual_image = cv2.imread("static/cropped/plate_5.jpg")
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
print(v11)
