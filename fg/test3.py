'''# text recognition
import cv2
import pytesseract

# read image
img = cv2.imread('bb247.jpg')

# configurations
config = ('-l eng --oem 1 --psm 3')

# pytessercat
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
text = pytesseract.image_to_string(img, config=config)
print(text)
# print text
text = text.split('\n')
print(text)'''
#####################################
import cv2
import pytesseract 

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


Actual_image = cv2.imread("test/s1.jpg")
Sample_img = cv2.resize(Actual_image,(400,350))
Image_ht,Image_wd,Image_thickness = Sample_img.shape
Sample_img = cv2.cvtColor(Sample_img,cv2.COLOR_BGR2RGB)
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
            print(mytext)
            mytext=""
        mytext = mytext + text[11]+" "
        prevy=y


print(mytext)


