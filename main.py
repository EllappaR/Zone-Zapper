# main.py
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from camera import VideoCamera
from camera2 import VideoCamera2
from camera3 import VideoCamera3

import os
import base64
import cv2
import pandas as pd
import numpy as np
import imutils
from flask import send_file
from werkzeug.utils import secure_filename
import pytesseract

import mysql.connector
import hashlib
import datetime
from datetime import date
import time
from random import seed
from random import randint
from PIL import Image
import stepic
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="trace_me"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'


@app.route('/')
def index():

    #path_main = 'static/dataset'
    #for fname in os.listdir(path_main):
    #    print(fname)
        
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('add_tc'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/login_tc', methods=['GET', 'POST'])
def login_tc():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM traffic_control WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            ff=open("static/traffic.txt","w")
            ff.write(uname)
            ff.close()
            
            session['username'] = uname
            return redirect(url_for('tc_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_tc.html',msg=msg)

@app.route('/login_rto', methods=['GET', 'POST'])
def login_rto():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM tm_rto WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('add_info'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_rto.html',msg=msg)

@app.route('/login_vo', methods=['GET', 'POST'])
def login_vo():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('vo_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_vo.html',msg=msg)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/det.txt","w")
    ff.write("")
    ff.close()

    mycursor = mydb.cursor()

    if request.method=='POST':
       
        email=request.form['email']
        
        mycursor.execute("update admin set email=%s",(email,))
        mydb.commit()

        
        return redirect(url_for('admin'))

    mycursor.execute("SELECT * FROM admin")
    data = mycursor.fetchone()
                                        
    return render_template('web/admin.html',msg=msg,data=data)

@app.route('/add_rto', methods=['GET', 'POST'])
def add_rto():
    msg=""
    mess=""
    email=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM tm_rto")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    
        
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']

        uname="R"+str(maxid)
        rn=randint(1000,9999)
        pass1=str(rn)

        mess="Dear "+name+", RTO Admin ID:"+uname+", Password:"+pass1
        
        sql = "INSERT INTO tm_rto(id,name,mobile,email,location,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,location,uname,pass1)
        mycursor.execute(sql, val)
        mydb.commit()            
        print(mycursor.rowcount, "Registered Success")
        msg="success"
        #return redirect(url_for('add_rto',act='1'))

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from tm_rto where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_rto'))
        

    mycursor.execute("SELECT * FROM tm_rto")
    data = mycursor.fetchall()

    return render_template('web/add_rto.html',msg=msg,act=act,data=data,mess=mess,email=email)



@app.route('/add_tc', methods=['GET', 'POST'])
def add_tc():
    msg=""
    mess=""
    email=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM traffic_control")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    
        
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        
        
        area=request.form['area']
        city=request.form['city']

        uname="T"+str(maxid)
        pass1="1234"


        mess="Dear "+name+", Traffic Police ID:"+uname+", Password:"+pass1
        
        sql = "INSERT INTO traffic_control(id,name,mobile,email,area,city,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,area,city,uname,pass1)
        mycursor.execute(sql, val)
        mydb.commit()            
        #print(mycursor.rowcount, "Registered Success")
        msg="success"
        #return redirect(url_for('add_tc',act='1'))

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from traffic_control where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_tc'))
        

    mycursor.execute("SELECT * FROM traffic_control")
    data = mycursor.fetchall()

    return render_template('web/add_tc.html',msg=msg,act=act,data=data,mess=mess,email=email)


@app.route('/add_info', methods=['GET', 'POST'])
def add_info():
    msg=""
    fn=""
    email=""
    mess=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM register")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    
        
    if request.method=='POST':
        
        name=request.form['name']
        vno=request.form['vno']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        rdate=request.form['rdate']
        

        vno=request.form['vno']
        vcolor=request.form['vcolor']
        vname=request.form['vname']
        vmodel=request.form['vmodel']
        vtype=request.form['vtype']
        file = request.files['file']
        file2 = request.files['file2']

        uname="V"+str(maxid)
        rn=randint(1000,9999)
        pass1=str(rn)

        filename=file.filename
        photo="C"+str(maxid)+filename
        file.save(os.path.join("static/vehicle", photo))

        filename2=file2.filename
        dno="D"+str(maxid)+filename2
        file2.save(os.path.join("static/vehicle", dno))


        mess="Dear "+name+", Vehicle Owner ID:"+uname+", Password:"+pass1

        
        sql = "INSERT INTO register(id,name,vno,filename,gender,dob,address,mobile,email,register_date,vtype,vmodel,vcolor,uname,pass,vname,driving) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)"
        val = (maxid,name,vno,photo,gender,dob,address,mobile,email,rdate,vtype,vmodel,vcolor,uname,pass1,vname,dno)
        mycursor.execute(sql, val)
        mydb.commit()            
        print(mycursor.rowcount, "Registered Success")
        msg="success"
        #return redirect(url_for('add_info',act='1'))

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from register where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_info'))
        

    mycursor.execute("SELECT * FROM register")
    data = mycursor.fetchall()

    return render_template('web/add_info.html',msg=msg,act=act,data=data,email=email,mess=mess)

@app.route('/edit_info', methods=['GET', 'POST'])
def edit_info():
    msg=""
    vid=request.args.get("vid")
    fn=""
    email=""
    mess=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        
        name=request.form['name']
        vno=request.form['vno']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        rdate=request.form['rdate']
        
        vcolor=request.form['vcolor']
        vname=request.form['vname']
        vmodel=request.form['vmodel']
        vtype=request.form['vtype']

        mycursor.execute("update register set name=%s,vno=%s,gender=%s,dob=%s,address=%s,mobile=%s,email=%s,register_date=%s,vcolor=%s,vname=%s,vmodel=%s,vtype=%s where id=%s",(name,vno,gender,dob,address,mobile,email,rdate,vcolor,vname,vmodel,vtype,vid))
        mydb.commit()
        msg="success"
        
       

    mycursor.execute("SELECT * FROM register where id=%s",(vid,))
    data = mycursor.fetchone()

    return render_template('web/edit_info.html',msg=msg,act=act,data=data,email=email,mess=mess)

@app.route('/edit_tc', methods=['GET', 'POST'])
def edit_tc():
    msg=""
    vid=request.args.get("vid")
    fn=""
    email=""
    mess=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        area=request.form['area']
        
        city=request.form['city']
       
        mycursor.execute("update traffic_control set name=%s,mobile=%s,email=%s,area=%s,city=%s where id=%s",(name,mobile,email,area,city,vid))
        mydb.commit()
        msg="success"
        
       

    mycursor.execute("SELECT * FROM traffic_control where id=%s",(vid,))
    data = mycursor.fetchone()

    return render_template('web/edit_tc.html',msg=msg,act=act,data=data)


@app.route('/edit_rto', methods=['GET', 'POST'])
def edit_rto():
    msg=""
    vid=request.args.get("vid")
    fn=""
    email=""
    mess=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']
    
       
        mycursor.execute("update tm_rto set name=%s,mobile=%s,email=%s,location=%s where id=%s",(name,mobile,email,location,vid))
        mydb.commit()
        msg="success"
        
       

    mycursor.execute("SELECT * FROM tm_rto where id=%s",(vid,))
    data = mycursor.fetchone()

    return render_template('web/edit_rto.html',msg=msg,act=act,data=data)

@app.route('/view_vo', methods=['GET', 'POST'])
def view_vo():
    msg=""
    fn=""
    
    act=request.args.get("act")
    mycursor = mydb.cursor()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from register where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_vo'))

    
    mycursor.execute("SELECT * FROM register order by id desc")
    data = mycursor.fetchall()

    return render_template('web/view_vo.html',msg=msg,act=act,data=data)


@app.route('/tc_home', methods=['GET', 'POST'])
def tc_home():
    msg=""
    uname=""
    photo=""
    st=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']

    mycursor=mydb.cursor()
    mycursor.execute("SELECT * FROM traffic_control where uname=%s",(uname,))
    data = mycursor.fetchone()

    f3=open("cdata.txt","w")
    f3.write("")
    f3.close()

    ff1=open("sms.txt","w")
    ff1.write("1")
    ff1.close()

    '''if request.method=='POST':
       
        mycursor.execute("SELECT max(id)+1 FROM detection")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            photo="F"+str(maxid)+filename
            file.save(os.path.join("static/test", photo))
        
        f1=open("file.txt","w")
        f1.write(photo)
        f1.close()

        ft=photo.split(".")
        if ft[1]=="jpg" or ft[1]=="png" or ft[1]=="mp4":
            st="1"
            sql = "INSERT INTO detection(id,vno,fine,tc,filename,file_type) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (maxid,'','500',uname,photo,ftype)
            mycursor.execute(sql, val)
            mydb.commit()
            vid=str(maid)
            print(mycursor.rowcount, "Registered Success")
            
            #return redirect(url_for('detection',vid=str(maxid)))
            if ft[1]=="mp4":
                msg="video"
            else:
                msg="image"

        else:
            msg="fail"

    
    
    mycursor.execute("SELECT * FROM detection order by id desc")
    data2 = mycursor.fetchall()'''
    
    return render_template('web/tc_home.html',msg=msg,data=data)

@app.route('/detect_img', methods=['GET', 'POST'])
def detect_img():
    msg=""
    uname=""
    fn=""
    cimg=""
    np_text=""
    st=""
    uu=""
    vid=""

    mycursor=mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM detection")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
            

    if request.method=='POST':
        file = request.files['file']
        try:
            fname = file.filename
            ft=fname.split(".")
            if ft[1]=="jpg" or ft[1]=="png" or ft[1]=="jpeg":
                
                
                
                filename = secure_filename(fname)
                img="F"+str(maxid)+filename
                fn=img
                file.save(os.path.join("static/test", img))

                image = cv2.imread("static/test/"+img)
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
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                
                plate_roi = gray[y:y+h, x:x+w]
                plate_text = pytesseract.image_to_string(plate_roi, config='--psm 11')
                cv2.imwrite("static/test/R"+img, image)

                
                cimg="C"+img
                cv2.imwrite("static/test/"+cimg, plate_roi)
                
                print(plate_text)
                
                ff=open("static/np_img.txt","w")
                ff.write(img)
                ff.close()

                ff=open("static/code.txt","r")
                code=ff.read()
                ff.close()

                original_string = plate_text
                text = ''.join(letter for letter in original_string if letter.isalnum())
                np_text=text

                txt=np_text[0:2]
                p1=len(np_text)
                x=0
                cd=code.split(",")
                for cdd in cd:
                    if txt==cdd:
                        x+=1
                print(p1)
                print(x)

                ff=open("static/vno.txt","w")
                ff.write(np_text)
                ff.close()
                if p1>=9 and p1<=10 and x>0:
                    st="1"
                    '''mycursor.execute("SELECT count(*) FROM register where vno=%s",(np_text,))
                    cnt = mycursor.fetchone()[0]
                    if cnt>0:
                        uu="1"
                        mycursor.execute("SELECT * FROM register where vno=%s",(np_text,))
                        rw = mycursor.fetchone()
                        vid=rw[0]
                    #p2=np_text.split(" ")'''
                    
                  
                else:
                    st="2"

            else:
                st="2"
        except:
            st="2"
    
        

    return render_template('web/detect_img.html',msg=msg,st=st,np_text=np_text,cimg=cimg,fn=fn,uu=uu,vid=vid)

@app.route('/detect_video', methods=['GET', 'POST'])
def detect_video():
    msg=""
    uname=""
    fn=""
    cimg=""
    np_text=""
    st=""

    mycursor=mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM detection")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
            

    if request.method=='POST':
        file = request.files['file']
        try:
            fname = file.filename
            ft=fname.split(".")
            if ft[1]=="mp4":

                filename = secure_filename(fname)
                
                fn=filename
                file.save(os.path.join("static/upload", fn))
                
                ff=open("file.txt","w")
                ff.write("static/upload/"+fn)
                ff.close()
                st="1"
                
            else:
                st="2"
        except:
            st="2"
    
        

    return render_template('web/detect_video.html',msg=msg,st=st,fn=fn)

@app.route('/pro', methods=['GET', 'POST'])
def pro():
    msg=""
    uname=""
    fn=""
    cimg=""
    np_text=""
    st=""

    return render_template('web/pro.html',msg=msg,st=st,fn=fn)

@app.route('/pro2', methods=['GET', 'POST'])
def pro2():
    msg=""
    uname=""
    fn=""
    cimg=""
    np_text=""
    st=""
    uu=""
    vid=""
    mycursor=mydb.cursor()
    ff=open("static/vno.txt","r")
    plate_text=ff.read()
    ff.close()
    print(plate_text)
    
    ff=open("static/np_img.txt","r")
    cc=ff.read()
    ff.close()
    cimg="C"+cc
                
    ff=open("static/code.txt","r")
    code=ff.read()
    ff.close()

    original_string = plate_text
    text = ''.join(letter for letter in original_string if letter.isalnum())
    np_text=text
    p1=len(np_text)
    txt=np_text[0:2]

    if txt=="TW":
        print("s")
        v1=np_text[2:p1]
        np_text="TN"+v1
    
    x=0
    print(txt)
    cd=code.split(",")
    for cdd in cd:
        if txt==cdd or txt=="TW":
            x+=1
    print(p1)
    print(x)
    print(np_text)
    if p1>=9 and p1<=10 and x>0:
        st="1"
        mycursor.execute("SELECT count(*) FROM register where vno=%s",(np_text,))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            uu="1"
            mycursor.execute("SELECT * FROM register where vno=%s",(np_text,))
            rw = mycursor.fetchone()
            vid=rw[0]
        #p2=np_text.split(" ")
        
      
    else:
        st="2"

    return render_template('web/pro2.html',msg=msg,st=st,cimg=cimg,fn=fn,np_text=np_text,uu=uu,vid=vid)


@app.route('/process', methods=['GET', 'POST'])
def process():
    msg=""
    uname=""
    fn=""
    cimg=""
    np_text=""
    st=""

    return render_template('web/process.html',msg=msg,st=st,fn=fn)

@app.route('/process2', methods=['GET', 'POST'])
def process2():
    msg=""
    uname=""
    fn=""
    cimg=""
    np_text=""
    st=""
    uu=""
    vid=""
    mycursor=mydb.cursor()
    ff=open("static/vno.txt","r")
    plate_text=ff.read()
    ff.close()
    print(plate_text)
    

    ff=open("static/code.txt","r")
    code=ff.read()
    ff.close()

    original_string = plate_text
    text = ''.join(letter for letter in original_string if letter.isalnum())
    np_text=text
    p1=len(np_text)
    txt=np_text[0:2]

    if txt=="TW":
        print("s")
        v1=np_text[2:p1]
        np_text="TN"+v1
    
    x=0
    print(txt)
    cd=code.split(",")
    for cdd in cd:
        if txt==cdd or txt=="TW":
            x+=1
    print(p1)
    print(x)
    print(np_text)
    if p1>=9 and p1<=10 and x>0:
        st="1"
        mycursor.execute("SELECT count(*) FROM register where vno=%s",(np_text,))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            uu="1"
            mycursor.execute("SELECT * FROM register where vno=%s",(np_text,))
            rw = mycursor.fetchone()
            vid=rw[0]
        #p2=np_text.split(" ")
        
      
    else:
        st="2"

    return render_template('web/process2.html',msg=msg,st=st,fn=fn,np_text=np_text,uu=uu,vid=vid)


@app.route('/detect_cam', methods=['GET', 'POST'])
def detect_cam():
    msg=""
    uname=""
    fn=""
    cimg=""
    np_text=""
    st=""

    ff=open("static/vno.txt","w")
    ff.write("")
    ff.close()

    mycursor=mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM detection")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
            

    if request.method=='POST':
        file = request.files['file']
        try:
            fname = file.filename
            ft=fname.split(".")
            if ft[1]=="mp4":

                filename = secure_filename(fname)
                
                fn=filename
                file.save(os.path.join("static/upload", fn))
                
                ff=open("file.txt","w")
                ff.write("static/upload/"+fn)
                ff.close()
                st="1"
                
            else:
                st="2"
        except:
            st="2"
    
        

    return render_template('web/detect_cam.html',msg=msg,st=st,fn=fn)



@app.route('/process3', methods=['GET', 'POST'])
def process3():
    msg=""
    uname=""
    fn=""
    cimg=""
    np_text=""
    st=""

    return render_template('web/process3.html',msg=msg,st=st,fn=fn)

@app.route('/process4', methods=['GET', 'POST'])
def process4():
    msg=""
    uname=""
    fn=""
    cimg=""
    np_text=""
    st=""
    uu=""
    vid=""
    mycursor=mydb.cursor()
    ff=open("static/vno.txt","r")
    plate_text=ff.read()
    ff.close()
    print(plate_text)

    ff=open("static/code.txt","r")
    code=ff.read()
    ff.close()

    original_string = plate_text
    text = ''.join(letter for letter in original_string if letter.isalnum())
    np_text=text
    p1=len(np_text)
    txt=np_text[0:2]

    if txt=="TW":
        print("s")
        v1=np_text[2:p1]
        np_text="TN"+v1
    
    x=0
    print(txt)
    cd=code.split(",")
    for cdd in cd:
        if txt==cdd or txt=="TW":
            x+=1
    print(p1)
    print(x)
    print(np_text)
    if p1>=9 and p1<=10 and x>0:
        st="1"
        mycursor.execute("SELECT count(*) FROM register where vno=%s",(np_text,))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            uu="1"
            mycursor.execute("SELECT * FROM register where vno=%s",(np_text,))
            rw = mycursor.fetchone()
            vid=rw[0]
        #p2=np_text.split(" ")
        
      
    else:
        st="2"


    return render_template('web/process4.html',msg=msg,st=st,fn=fn,np_text=np_text,uu=uu,vid=vid)


@app.route('/send_alert', methods=['GET', 'POST'])
def send_alert():
    msg=""
    uname=""
    fn=request.args.get("fn")
    cimg=""
    np_text=""
    st=""
    fid=""
    alert_type=""
    vid=request.args.get("vid")
    fine=0
    pdate=""
    message=""
    mess=""
    s1=""
    sdata=[]

    ff=open("static/traffic.txt","r")
    uname=ff.read()
    ff.close()

    ff=open("bc.txt","r")
    bc=ff.read()
    ff.close()

    mycursor=mydb.cursor()

    mycursor.execute("SELECT * FROM register where id=%s",(vid,))
    rs = mycursor.fetchone()

    name=rs[1]
    mobile=rs[6]
    vno=rs[2]
    
    if request.method=='POST':
        alert_type=request.form['alert_type']
        location=request.form['location']
        pdate=request.form['pdate']

        if alert_type=="1":
            fine=request.form['fine']
            pdate=request.form['pdate']
            mess="V.No:"+vno+", No Parking Fine Rs. "+str(fine)
        if alert_type=="2":
            message=request.form['message']
            mess="V.No: "+vno+", "+message

        mycursor.execute("SELECT max(id)+1 FROM detection")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO detection(id,vno,name,fine,tc,location,alert_type,message,pdate) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
        val = (maxid,vno,name,fine,uname,location,alert_type,message,pdate)
        mycursor.execute(sql, val)
        mydb.commit()
        fid=str(maxid)
        msg="ok"

    mycursor.execute("SELECT count(*) FROM detection where vno=%s order by id desc",(vno,))
    snt = mycursor.fetchone()[0]
    if snt>0:
        s1="1"
        mycursor.execute("SELECT * FROM detection where vno=%s order by id desc",(vno,))
        sdata = mycursor.fetchall()  
    

    return render_template('web/send_alert.html',msg=msg,st=st,vid=vid,rs=rs,fn=fn,mess=mess,mobile=mobile,sdata=sdata,s1=s1,fid=fid,alert_type=alert_type,bc=bc,vno=vno,fine=fine)


@app.route('/view_detect', methods=['GET', 'POST'])
def view_detect():
    msg=""
    uname=""
    vno=""
    s1=""
    sdata=[]

    ff=open("static/traffic.txt","r")
    uname=ff.read()
    ff.close()

    mycursor=mydb.cursor()

    if request.method=='POST':
        s1="1"
        vno=request.form['vno']
        mycursor.execute("SELECT * FROM detection where vno=%s order by id desc",(vno,))
        sdata = mycursor.fetchall()
        
    else:
        s1="1"
        mycursor.execute("SELECT * FROM detection where tc=%s order by id desc",(uname,))
        sdata = mycursor.fetchall()

    return render_template('web/view_detect.html',msg=msg,sdata=sdata,s1=s1)

def CNN():
    #Lets start by loading the Cifar10 data
    (X, y), (X_test, y_test) = cifar10.load_data()

    #Keep in mind the images are in RGB
    #So we can normalise the data by diving by 255
    #The data is in integers therefore we need to convert them to float first
    X, X_test = X.astype('float32')/255.0, X_test.astype('float32')/255.0

    #Then we convert the y values into one-hot vectors
    #The cifar10 has only 10 classes, thats is why we specify a one-hot
    #vector of width/class 10
    y, y_test = u.to_categorical(y, 10), u.to_categorical(y_test, 10)

    #Now we can go ahead and create our Convolution model
    model = Sequential()
    #We want to output 32 features maps. The kernel size is going to be
    #3x3 and we specify our input shape to be 32x32 with 3 channels
    #Padding=same means we want the same dimensional output as input
    #activation specifies the activation function
    model.add(Conv2D(32, (3, 3), input_shape=(32, 32, 3), padding='same',
                     activation='relu'))
    #20% of the nodes are set to 0
    model.add(Dropout(0.2))
    #now we add another convolution layer, again with a 3x3 kernel
    #This time our padding=valid this means that the output dimension can
    #take any form
    model.add(Conv2D(32, (3, 3), activation='relu', padding='valid'))
    #maxpool with a kernet of 2x2
    model.add(MaxPooling2D(pool_size=(2, 2)))
    #In a convolution NN, we neet to flatten our data before we can
    #input it into the ouput/dense layer
    model.add(Flatten())
    #Dense layer with 512 hidden units
    model.add(Dense(512, activation='relu'))
    #this time we set 30% of the nodes to 0 to minimize overfitting
    model.add(Dropout(0.3))
    #Finally the output dense layer with 10 hidden units corresponding to
    #our 10 classe
    model.add(Dense(10, activation='softmax'))
    #Few simple configurations
    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(momentum=0.5, decay=0.0004), metrics=['accuracy'])
    #Run the algorithm!
    model.fit(X, y, validation_data=(X_test, y_test), epochs=25,
              batch_size=512)
    #Save the weights to use for later
    model.save_weights("cifar10.hdf5")
    #Finally print the accuracy of our model!
    print("Accuracy: &2.f%%" %(model.evaluate(X_test, y_test)[1]*100))
    
##YOLOv8 - for Real Time Predictions
class YoloDetector:
    def __init__(self, weights_name='yolov8n_state_dict.pt', config_name='yolov8n.yaml', device='cuda:0', min_face=100, target_size=None, frontal=False):
           
            self._class_path = pathlib.Path(__file__).parent.absolute()#os.path.dirname(inspect.getfile(self.__class__))
            self.device = device
            self.target_size = target_size
            self.min_face = min_face
            self.frontal = frontal
            if self.frontal:
                print('Currently unavailable')
                # self.anti_profile = joblib.load(os.path.join(self._class_path, 'models/anti_profile/anti_profile_xgb_new.pkl'))
            self.detector = self.init_detector(weights_name,config_name)

    def init_detector(self,weights_name,config_name):
        print(self.device)
        model_path = os.path.join(self._class_path,'weights/',weights_name)
        print(model_path)
        config_path = os.path.join(self._class_path,'models/',config_name)
        state_dict = torch.load(model_path)
        detector = Model(cfg=config_path)
        detector.load_state_dict(state_dict)
        detector = detector.to(self.device).float().eval()
        for m in detector.modules():
            if type(m) in [nn.Hardswish, nn.LeakyReLU, nn.ReLU, nn.ReLU6, nn.SiLU]:
                m.inplace = True  # pytorch 1.7.0 compatibility
            elif type(m) is Conv:
                m._non_persistent_buffers_set = set()  # pytorch 1.6.0 compatibility
        return detector
    
    def _preprocess(self,imgs):
        """
            Preprocessing image before passing through the network. Resize and conversion to torch tensor.
        """
        pp_imgs = []
        for img in imgs:
            h0, w0 = img.shape[:2]  # orig hw
            if self.target_size:
                r = self.target_size / min(h0, w0)  # resize image to img_size
                if r < 1:  
                    img = cv2.resize(img, (int(w0 * r), int(h0 * r)), interpolation=cv2.INTER_LINEAR)

            imgsz = check_img_size(max(img.shape[:2]), s=self.detector.stride.max())  # check img_size
            img = letterbox(img, new_shape=imgsz)[0]
            pp_imgs.append(img)
        pp_imgs = np.array(pp_imgs)
        pp_imgs = pp_imgs.transpose(0, 3, 1, 2)
        pp_imgs = torch.from_numpy(pp_imgs).to(self.device)
        pp_imgs = pp_imgs.float()  # uint8 to fp16/32
        pp_imgs /= 255.0  # 0 - 255 to 0.0 - 1.0
        return pp_imgs
        
    def _postprocess(self, imgs, origimgs, pred, conf_thres, iou_thres):
        """
            Postprocessing of raw pytorch model output.
            Returns:
                bboxes: list of arrays with 4 coordinates of bounding boxes with format x1,y1,x2,y2.
                points: list of arrays with coordinates of 5 facial keypoints (eyes, nose, lips corners).
        """
        bboxes = [[] for i in range(len(origimgs))]
        landmarks = [[] for i in range(len(origimgs))]
        
        pred = non_max_suppression_face(pred, conf_thres, iou_thres)
        
        for i in range(len(origimgs)):
            img_shape = origimgs[i].shape
            h,w = img_shape[:2]
            gn = torch.tensor(img_shape)[[1, 0, 1, 0]]  # normalization gain whwh
            gn_lks = torch.tensor(img_shape)[[1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]  # normalization gain landmarks
            det = pred[i].cpu()
            scaled_bboxes = scale_coords(imgs[i].shape[1:], det[:, :4], img_shape).round()
            scaled_cords = scale_coords_landmarks(imgs[i].shape[1:], det[:, 5:15], img_shape).round()

            for j in range(det.size()[0]):
                box = (det[j, :4].view(1, 4) / gn).view(-1).tolist()
                box = list(map(int,[box[0]*w,box[1]*h,box[2]*w,box[3]*h]))
                if box[3] - box[1] < self.min_face:
                    continue
                lm = (det[j, 5:15].view(1, 10) / gn_lks).view(-1).tolist()
                lm = list(map(int,[i*w if j%2==0 else i*h for j,i in enumerate(lm)]))
                lm = [lm[i:i+2] for i in range(0,len(lm),2)]
                bboxes[i].append(box)
                landmarks[i].append(lm)
        return bboxes, landmarks

    def get_frontal_predict(self, box, points):
        '''
            Make a decision whether face is frontal by keypoints.
            Returns:
                True if face is frontal, False otherwise.
        '''
        cur_points = points.astype('int')
        x1, y1, x2, y2 = box[0:4]
        w = x2-x1
        h = y2-y1
        diag = sqrt(w**2+h**2)
        dist = scipy.spatial.distance.pdist(cur_points)/diag
        predict = self.anti_profile.predict(dist.reshape(1, -1))[0]
        if predict == 0:
            return True
        else:
            return False
    def align(self, img, points):
        '''
            Align faces, found on images.
            Params:
                img: Single image, used in predict method.
                points: list of keypoints, produced in predict method.
            Returns:
                crops: list of croped and aligned faces of shape (112,112,3).
        '''
        crops = [align_faces(img,landmark=np.array(i)) for i in points]
        return crops

    def predict(self, imgs, conf_thres = 0.3, iou_thres = 0.5):
        '''
            Get bbox coordinates and keypoints of faces on original image.
            Params:
                imgs: image or list of images to detect faces on
                conf_thres: confidence threshold for each prediction
                iou_thres: threshold for NMS (filtering of intersecting bboxes)
            Returns:
                bboxes: list of arrays with 4 coordinates of bounding boxes with format x1,y1,x2,y2.
                points: list of arrays with coordinates of 5 facial keypoints (eyes, nose, lips corners).
        '''
        one_by_one = False
        # Pass input images through face detector
        if type(imgs) != list:
            images = [imgs]
        else:
            images = imgs
            one_by_one = False
            shapes = {arr.shape for arr in images}
            if len(shapes) != 1:
                one_by_one = True
                warnings.warn(f"Can't use batch predict due to different shapes of input images. Using one by one strategy.")
        origimgs = copy.deepcopy(images)
        
        
        if one_by_one:
            images = [self._preprocess([img]) for img in images]
            bboxes = [[] for i in range(len(origimgs))]
            points = [[] for i in range(len(origimgs))]
            for num, img in enumerate(images):
                with torch.inference_mode(): # change this with torch.no_grad() for pytorch <1.8 compatibility
                    single_pred = self.detector(img)[0]
                    print(single_pred.shape)
                bb, pt = self._postprocess(img, [origimgs[num]], single_pred, conf_thres, iou_thres)
                #print(bb)
                bboxes[num] = bb[0]
                points[num] = pt[0]
        else:
            images = self._preprocess(images)
            with torch.inference_mode(): # change this with torch.no_grad() for pytorch <1.8 compatibility
                pred = self.detector(images)[0]
            bboxes, points = self._postprocess(images, origimgs, pred, conf_thres, iou_thres)

        return bboxes, points


@app.route('/vo_home', methods=['GET', 'POST'])
def vo_home():
    msg=""
    uname=""
    photo=""
    st=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']

    mycursor=mydb.cursor()
    mycursor.execute("SELECT * FROM register where uname=%s",(uname,))
    rs = mycursor.fetchone()

    return render_template('web/vo_home.html',msg=msg,rs=rs)

@app.route('/view_fine', methods=['GET', 'POST'])
def view_fine():
    msg=""
    uname=""
    photo=""
    st=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']

    mycursor=mydb.cursor()
    mycursor.execute("SELECT * FROM register where uname=%s",(uname,))
    rs = mycursor.fetchone()
    vno=rs[2]

    mycursor.execute("SELECT * FROM detection where vno=%s",(vno,))
    sdata=mycursor.fetchall()

    return render_template('web/view_fine.html',msg=msg,rs=rs,sdata=sdata)

@app.route('/vo_pay', methods=['GET', 'POST'])
def vo_pay():
    msg=""
    uname=""
    photo=""
    st=""
    fid=request.args.get("fid")
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']

    mycursor=mydb.cursor()
    mycursor.execute("SELECT * FROM register where uname=%s",(uname,))
    rs = mycursor.fetchone()
    vno=rs[2]

    if request.method=='POST':
        
        card=request.form['card']
        mycursor.execute("update detection set pay_st=1 where id=%s",(fid,))
        mydb.commit()
        
        msg="success"

    mycursor.execute("SELECT * FROM detection where id=%s",(fid,))
    sdata=mycursor.fetchone()

    return render_template('web/vo_pay.html',msg=msg,rs=rs,sdata=sdata)

@app.route('/vo_page', methods=['GET', 'POST'])
def vo_page():
    msg=""

    mycursor=mydb.cursor()

    url2="http://localhost/trace/data.txt"
    ur = urlopen(url2)#open url
    data1 = ur.read().decode('utf-8')
    vv=data1.split(',')

    for fid in vv:
    
        mycursor.execute("update detection set pay_st=1 where id=%s",(fid,))
        mydb.commit()
        

    return render_template('web/vo_page.html',msg=msg)


@app.route('/detection', methods=['GET', 'POST'])
def detection():
    msg=""
    st=""
    data2=""
    uname=""
    mobile=""
    mess=""
    email=""
    mess1=""
    if 'username' in session:
        uname = session['username']

    mycursor=mydb.cursor()
    

    ff=open("check.txt","w")
    ff.write("")
    ff.close()
    f4=open("file.txt","r")
    fn=f4.read()
    f4.close()


    photo=fn
    f1=open("file.txt","w")
    f1.write(photo)
    f1.close()

    mycursor.execute("SELECT max(id)+1 FROM detection")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
        
    sql = "INSERT INTO detection(id,vno,fine,camera,tc) VALUES (%s, %s, %s, %s, %s)"
    val = (maxid,'','500',photo,uname)
    mycursor.execute(sql, val)
    mydb.commit()
        
    
    return render_template('detection.html',msg=msg,data2=data2,st=st,fn=fn,mobile=mobile,mess=mess,mess1=mess1,email=email)



@app.route('/page', methods=['GET', 'POST'])
def page():
    msg=""
    st=""
    data2=""
    uname=""
    mobile=""
    mess=""
    email=""
    mess1=""
    mycursor=mydb.cursor()
    mycursor.execute("SELECT * FROM register limit 0,1")
    data2 = mycursor.fetchone()
    fn=data2[3]
    

    #mycursor.execute("SELECT * FROM detection order by id desc limit 0,1")
    #data = mycursor.fetchone()
    #vid=data[0]
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    #fa=data[5]
    Actual_image = cv2.imread("static/upload/"+fn)
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

    print("Number Plate:")
    print(mytext)
    stext=mytext.strip()
    vv='%'+stext+'%'
    
    vv="1"
    mycursor.execute("SELECT count(*) FROM register where id=%s",(vv,))
    cn = mycursor.fetchone()[0]

    if cn>0:
        #st="1"
        mycursor.execute("SELECT * FROM register where id=%s",(vv,))
        data2 = mycursor.fetchone()
        mobile=data2[6]
        vno=data2[2]
        name=data2[1]
        mess="No parking Detected, Fine Rs.500"

        mycursor.execute("SELECT * FROM admin")
        dd1 = mycursor.fetchone()
        email=dd1[7]
        mess1="Detected Vehicle No. "+vno+", Name:"+name

        
        mycursor.execute("update detection set vno=%s,name=%s where id=%s",(vno,name,vv))
        mydb.commit()


    ff=open("check.txt","r")
    vf=ff.read()
    ff.close()

    if vf=="1":
        st="1"

    return render_template('page.html',msg=msg,data2=data2,st=st,fn=fn,mobile=mobile,mess=mess,mess1=mess1,email=email)


@app.route('/view_detect1', methods=['GET', 'POST'])
def view_detect1():
    msg=""
    st=""
    tc=""

  
    
    mycursor=mydb.cursor()
    data=[]
    cdata=[]
    mycursor.execute('SELECT * FROM traffic_control')
    tdata = mycursor.fetchall()

    

    if request.method=='POST':
        
        tc=request.form['tc']
        
       
        if tc=="":
            a="1"
        else:
            
            mycursor.execute('SELECT count(*) FROM detection where tc=%s order by id desc',(tc,))
            cnt = mycursor.fetchone()[0]
            if cnt>0:
                mycursor.execute('SELECT * FROM detection d,register r where d.vno=r.vno && d.tc=%s order by d.id desc',(tc,))
                data = mycursor.fetchall()
                st="1"
            else:
                st="2"

            
            
            
            
    
    return render_template('view_detect1.html',msg=msg,data=data,tdata=tdata,st=st,tc=tc)

@app.route('/view', methods=['GET', 'POST'])
def view():
    msg=""
    mycursor=mydb.cursor()
    vno=request.args.get("vno")

    mycursor.execute('SELECT * FROM detection where vno=%s',(vno,))
    data = mycursor.fetchall()

    mycursor.execute('SELECT * FROM register where vno=%s',(vno,))
    data2 = mycursor.fetchone()
    
   
    return render_template('view.html',msg=msg,data=data,data2=data2)

####
def gen3(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    
@app.route('/video_feed3')
def video_feed3():
    return Response(gen3(VideoCamera3()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

####
def gen2(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    
@app.route('/video_feed2')
def video_feed2():
    return Response(gen2(VideoCamera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

###
def gen(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
