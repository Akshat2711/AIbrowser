#take my pic not not working
import requests
from customtkinter import*
from bs4 import BeautifulSoup
from tkinter import*
from PIL import ImageTk,Image
import mysql.connector as mycon
from datetime import date
import time
from gtts import gTTS
import openai
from apikey import *
import os
from smtplib import *
import urllib.request
import speech_recognition as sr
import webbrowser
import cv2
import numpy as np
import pyautogui
from random import*
import datetime
import pywhatkit as pwk
import wikipedia
from pytube import YouTube  
language = 'en'#language of output
openai.api_key =""
#theme txt color
f=open("theme_colortext_save.txt","r")
uitext_color=f.read()
f.close()
#theme fg color
f=open("theme_colorfg_save.txt","r")
uifg_color=f.read()
f.close()
#theme border color
f=open("theme_colorbc_save.txt","r")
uiborder_color=f.read()
f.close()
#ui theme default
uitheme="dark"
##bg_prev_img#####
f=open("bgimage_save","r")
back_image=f.read()
f.close()
###########


con=mycon.connect(host="localhost",user="root",database="searchhistory",password="")
cur=con.cursor()

set_appearance_mode(uitheme)#####for appearence of window
#called when result direct on google
def query():
    global result
    result=wikipedia.page(res).content
    msg1.delete("0.0", "end")
    msg1.insert("0.0",result+"\n\n\n")
    but4.place(x=700,y=745)
    but6.place(x=520,y=745)


   

def window1():
    global win1
    global count
    win1=CTk()
    win1.title("main window")
    win1.geometry("1920x1080-10-7")
    #image background
    b_img=ImageTk.PhotoImage(Image.open(back_image))
    canvas=Canvas(win1,width=5000,height=2000,highlightthickness=0)
    canvas.create_image(0,0,anchor='nw',image=b_img)
    canvas.pack()



#history being sent  to database
#sent to while loop
    def sgoogle():
        global res
        global date
#date code
        date = date.today()
        res=str(txt1.get())
#current time code
        ###################
        ###############
        t = time.localtime()
        gm=open("getmailforhis.txt","r")
        fm=gm.read()
        gm.close()
        current_time = time.strftime("%H:%M:%S", t)
        cur.execute("insert into history() values('{}','{}','{}','{}');".format(res,date,current_time,fm))
        con.commit()
        whileloop()
    def his():
        win_his=CTk()
        win_his.config()
        win_his.title("History")
        win_his.geometry("1920x1080-10-7")

# to delete history
        def delete_his():
            gm=open("getmailforhis.txt","r")
            fm=gm.read()
            gm.close()
            cur.execute("delete from history where email='{}'".format(fm))
            con.commit()
            lbl_confirm.configure(text="REOPEN TO SEE CHANGES!")
        textbox = CTkTextbox(win_his, height=850, width=760,font=("Helvitica",25))#textbox in which history written
        but_his=CTkButton(win_his,text="DELETE HISTORY",font=("Helvitica",18),command=delete_his,fg_color=uiborder_color,text_color=uitext_color).place(x=695,y=700)
        lbl_confirm=CTkLabel(win_his,text=" ",font=("Helvitica",15))
        lbl_confirm.place(x=620,y=675)
        gm=open("getmailforhis.txt","r")
        fm=gm.read()
        gm.close()
        cur.execute("select * from history where email='{}'".format(fm))
        h=cur.fetchall()
        print(h)

        
        
        for h1 in h:#########################
            textbox.insert("0.0",">>>Query-["+h1[0]+"]\n      Date-["+h1[1]+"]\n      Time-["+h1[2]+"]\n")
        textbox.place(x=400, y=10)
        win_his.mainloop()
#settings
    def settings():
         def apply_theme_sett():
              a=ent1.get()
              global back_image
              win1.destroy()
              back_image=a
              f=open("bgimage_save","w")
              f.write(a)
              f.close()
              window1()
         win_settings=CTk()
         win_settings.geometry("600x600")
         win_settings.title("SETTINGS")
         def switch_event():
            global uitheme
            uitheme=switch_var.get()
            set_appearance_mode(uitheme)
         def uibordercolor(choice):
            f=open("theme_colorbc_save.txt","w")
            f.write(choice)
            f.close()
            global uiborder_color
            win1.destroy()
            win_settings.destroy()
            uiborder_color=choice
            window1()
         def uitextcolor(choice):
            f=open("theme_colortxt_save.txt","w")
            f.write(choice)
            f.close()
            global uitext_color
            win1.destroy()
            win_settings.destroy()
            uitext_color=choice
            window1()
         def uifgcolor(choice):
            f=open("theme_colorfg_save.txt","w")
            f.write(choice)
            f.close()
            global uifg_color
            win1.destroy()
            win_settings.destroy()
            uifg_color=choice
            window1()

         list1=[uiborder_color,"purple","green","red","blue","black","white"]
         list2=[uitext_color,"purple","green","red","blue","black","white"]
         list3=[uifg_color,"purple","green","red","blue","black","white"]
         switch_var =StringVar(value="dark")
         switch =CTkSwitch(win_settings,text="",border_color=uiborder_color, command=switch_event,variable=switch_var, onvalue="light", offvalue="dark").place(x=110,y=302)
         but_sett1=CTkButton(win_settings,font=("Helvitica",14),text="LOG OUT",width=10,fg_color=uiborder_color,text_color=uitext_color,command=logout).place(x=10,y=10)
         lbl_sett1=CTkLabel(win_settings,text="THEME:",font=("Roberto",20),width=30,corner_radius=10,fg_color="transparent",text_color=uiborder_color).place(x=8,y=300)
         but_sett2=CTkButton(win_settings,text="HISTORY",font=("Helvitica",20),command=his,width=580,fg_color=uiborder_color,text_color=uitext_color).place(x=10,y=565)
         but_sett3=CTkButton(win_settings,text="APPLY",font=("Helvitica",20),command=apply_theme_sett,width=580,fg_color=uiborder_color,text_color=uitext_color).place(x=10,y=515)
         optionmenu1 = CTkOptionMenu(win_settings, values=list1,fg_color=uiborder_color,command=uibordercolor).place(x=10,y=200)
         optionmenu2 = CTkOptionMenu(win_settings, values=list2,fg_color=uiborder_color,command=uitextcolor).place(x=10,y=150)
         optionmenu3 = CTkOptionMenu(win_settings, values=list3,fg_color=uiborder_color,command=uifgcolor).place(x=10,y=100)
         ent1=CTkEntry(win_settings,width=242,font=("Helvitica",18),fg_color=uiborder_color,text_color=uitext_color,placeholder_text="ENTER PATH OF BG IMG...",corner_radius=10)
         ent1.place(x=10,y=430)
         win_settings.mainloop()
    global msg1
#to open google visible when query 2 fnc runs
    def opengoogle():
        q=txt1.get()
        webbrowser.open('https://google.com/'+'search?q='+q)
    def logout():
        win1.destroy()
        login()
    def wiki_summary():
        msg1.delete("0.0", "end")
        first_choice=wikipedia.search(txt1.get())[0]
        msg1.insert("0.0",wikipedia.summary(first_choice))
#to get answers using chatgpt
    def ai_search():
        global date
        ques=txt2.get()
#history save
        date = date.today()
        #current time code
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        gm=open("getmailforhis.txt","r")
        fm=gm.read()
        gm.close()
        cur.execute("insert into history(query, date, time, email) values('{}','{}','{}','{}');".format(ques+"(SIDEBAR)",date,current_time,fm))
        con.commit()

#to get ques answers through sidebar

        if "temperature" in ques:
            user_query="temp of"+ques.split()[-1]
            URL = "https://www.google.co.in/search?q=" + user_query
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find(class_='wob_t q8U8x').get_text()
            msg3.insert("0.0",">>>"+result+"℃\n")
        elif "todays news" in ques  or "headlines" in ques:
                        url = 'https://www.bbc.com/news'
                        response = requests.get(url) 
                        soup = BeautifulSoup(response.text, 'html.parser') 
                        headlines = soup.find('body').find_all('h3') 
                        news_line=""
                        for x in headlines: 
                            print(x.text.strip())
                            news_line+=x.text.strip()
                        msg3.insert("0.0",">>>"+news_line+"\n")
        elif "current time" in ques:
                        nowt2= datetime.datetime.now()
                        current_time1=str(nowt2.time())
                        final_time="currently it's "+current_time1[:5]
                        msg3.insert("0.0",">>>"+final_time+"\n")
        elif "create image" in ques:
                        msg3.insert("0.0",">>>just a sec.....\n")
                        response = openai.Image.create(prompt=ques,n=1,size="256x256")
                        out=response["data"][0]["url"]
                        url = str(out)
                        urllib.request.urlretrieve(url, "vaiimg.png")
                        img = Image.open(r"vaiimg.png")
                        img.show()
        elif "play" in ques:
                        msg3.insert("0.0",">>>playing.."+ques[4:]+"\n")
                        pwk.playonyt(ques.split()[1:])
        elif "download" in ques:
            msg3.insert("0.0",">>>ok,just a sec...\n")
            SAVE_PATH = "D:\ytdownloadsxpython" #location where to be saved 
            all_files=os.listdir('D:\ytdownloadsxpython')
            file_no=0
            file_name="ytvideo.mp4"
            for i in all_files:
                if i==file_name:
                    file_no+=1
                    file_name="ytvideo"+str(file_no)+".mp4"
            # link of the video to be downloaded  
            link=ques.split()[1:][0]
            try:  
                # object creation using YouTube 
                # which was imported in the beginning  
                yt = YouTube(link)  
            except:  
                msg3.insert("0.0",">>>connection error\n")
            
            # filters out all the files with "mp4" extension and progressive streams  
            mp4files = yt.streams.filter(file_extension='mp4', progressive=True)  
            
            # get the highest resolution progressive stream  
            d_video = mp4files.get_highest_resolution()  
            
            # print resolution of the stream  
            msg3.insert("0.0",">>>downloaded,vid res("+d_video.resolution+") video_location("+SAVE_PATH+") \nfile_name("+file_name+")\n")
            
            try:  
                # downloading the video with the specified filename  
                d_video.download(SAVE_PATH, filename=file_name)  
            except:  
                 msg3.insert("0.0",">>>some error\n")
                
        elif "sgmail" in ques:
             msg3.insert("0.0",">>>use chat-gpt for mail or write on your own(y/n)\n")
             time.sleep(5)
             if ques=='y':
                  msg3.insert("0.0",">>>topic of your mail\n")
                  time.sleep(6)
                  output = openai.ChatCompletion.create(model="gpt-3.5-turbo",  messages=[{"role": "user", "content":"write email to"+ques.split()[-1]+"topic:"+ques}])
                  email_gpt=(output['choices'][0]['message']['content'])
                  msg3.insert("0.0",">>>"+email_gpt+"\n")  
        elif "take screenshot" in ques:
                        msg3.insert("0.0",">>>ok...\n")
                        time.sleep(3)
                        image = pyautogui.screenshot()
                        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                        all_files=os.listdir('.')
                        file_no=0
                        file_name="screenshot.jpg"
                        for i in all_files:
                            if i==file_name:
                                file_no+=1
                                file_name="screenshot"+str(file_no)+".jpg"
                        cv2.imwrite(file_name, image)
        elif "take my pic" in ques:
            all_files=os.listdir('.')
            # Capture the video frame 
            # by frame
            file_no=0
            file_name="mypic.jpg"
            for i in all_files:
                if i==file_name:
                    file_no+=1
                    file_name="mypic"+str(file_no)+".jpg"
            vid = cv2.VideoCapture(0) 
            while True: 
                ret, frame = vid.read() 
                cv2.imshow("Hold 't' to take pic", frame) 
  
                if cv2.waitKey(1) & 0xFF == ord('t'): 
                    cv2.imwrite(file_name, frame)
                    msg3.insert("0.0",">>>Taken\n")
                    break
# After the loop release the cap object 
            vid.release() 
# Destroy all the windows 
            cv2.destroyAllWindows() 
                    
      
            

        else:
                        output = openai.chat.completions.create(
                        model="gpt-3.5-turbo", 
                        messages=[{"role": "user", "content":ques}])
                        answer=(output.choices[0].message.content)
                        msg3.insert("0.0",">>>"+answer+"\n")     

####################################
####################################
        

    global but4,but6
    txt1=CTkEntry(win1,width=680,font=("Helvitica",30),fg_color=uifg_color,text_color=uitext_color,placeholder_text="SEARCH WIKIPEDIA",corner_radius=10)
    txt1.place(x=300,y=10)
    txt2=CTkEntry(win1,width=242,font=("Helvitica",30),fg_color=uifg_color,text_color=uitext_color,placeholder_text="ASK STRAIN...",corner_radius=10)
    txt2.place(x=1220,y=745)
    but1=CTkButton(win1,text="search",font=("Helvitica",30),command=sgoogle,width=12,corner_radius=10,fg_color=uiborder_color,text_color=uitext_color).place(x=987,y=10)
#button 2,3 removed from here to settings
    msg1=CTkTextbox(win1,font=("Helvitica",20),width=800,height=690,corner_radius=10,fg_color=uifg_color,text_color=uitext_color,border_width=7,border_color=uiborder_color)
    msg1.place(x=300,y=95)
    but4=CTkButton(win1,font=("Helvitica",14),text="OPEN IN BROWSER",command=opengoogle,fg_color=uifg_color,text_color=uitext_color)
    #####################
    but6=CTkButton(win1,font=("Helvitica",14),text="GENERATE SUMMARY",command=wiki_summary,fg_color=uifg_color,text_color=uitext_color)
    #to diplay welcome message
    f=open("himsgfile(code1).txt","r")
    namehello=f.read()
    f.close()
    #to get temp of location
    user_query="temperature of chennai"
    URL = "https://www.google.co.in/search?q=" + user_query

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_='wob_t q8U8x').get_text()
    #######################
    #news lines for day
    url = 'https://www.bbc.com/news'
    response = requests.get(url) 
    soup = BeautifulSoup(response.text, 'html.parser') 
    headlines = soup.find('body').find_all('h3')
    hlno="TODAY'S HEADLINE\n\n"
    for x in headlines: 
        hlno+=x.text.strip()+"\n"
    ###################
    lbl3=CTkLabel(win1,text="WELCOME "+namehello,font=("Roberto",25),width=30,corner_radius=10,fg_color=uiborder_color,text_color=uitext_color).place(x=10,y=10)
    lbl4=CTkLabel(win1,text=result+"°CELCIUS",font=("Roberto",35),width=30,corner_radius=10,fg_color=uiborder_color,text_color=uitext_color).place(x=11,y=45)
    msg3=CTkTextbox(win1,font=("Helvitica",20),width=300,height=640,fg_color=uifg_color,text_color=uitext_color,border_width=7,border_color=uiborder_color)
    msg3.place(x=1225,y=95)
    but7=CTkButton(win1,width=5,font=("Helvitica",35),corner_radius=20,text="↩",command=ai_search,fg_color=uiborder_color,text_color=uitext_color).place(x=1476,y=741)
    but8=CTkButton(win1,width=5,font=("Helvitica",35),command=settings,corner_radius=20,text="⨁",fg_color=uiborder_color,text_color=uitext_color).place(x=1465,y=10)
    msg2=CTkTextbox(win1,font=("Helvitica",20),width=231,height=690,fg_color=uifg_color,text_color=uitext_color,border_width=7,border_color=uiborder_color)
    msg2.place(x=10,y=95)
    msg2.insert("0.0",hlno)
    win1.mainloop()
#called when result no direct on google
def query2(res2):
    global result
    first_choice=wikipedia.search(res2)[0]
    result = wikipedia.page(first_choice).content
    msg1.delete("0.0", "end")
    msg1.insert("0.0",result+"\n\n\n")
    but4.place(x=600,y=745)
    but6.place(x=400,y=745)
#deciding whether result directly on google or not
def whileloop():
    while True:
        try:
            query()
        except Exception:
            query2(res)
        break
def seeuserhistories():
    def nowords():
        no_words=CTk()
        no_words.title("history window")
        no_words.geometry("1920x1080-10-7")
        ent1= CTkEntry(no_words, width=900, font=("Helvitica", 28),fg_color=uifg_color,text_color=uitext_color,placeholder_text="enter word of which data to be taken out")
        ent1.place(x=335,y=10)
        no_bt1 = CTkButton(no_words, text="ENTER", font=("Helvitica", 28),fg_color=uiborder_color,text_color=uitext_color)
        no_bt1.place(x=1094,y=10) 


        
        no_words.mainloop()
    def histbtn():
        b=ent1.get()
        txt2.delete("0.0", "end")
        cur.execute("select name from logininf where email='{}'".format(b))
        d=cur.fetchall()
        cur.execute("select * from history where email='{}'".format(b))
        a=cur.fetchall()
        for i in a:
            c=">>>query:"+i[0]+"\n"+"date:"+i[1]+"\ntime:"+i[2]+"\n"
            txt2.insert("0.0",c)
        txt2.insert("0.0",d[0][0]+" HISTORY\n")
            
        
    userhistories=CTk()
    userhistories.title("history window")
    userhistories.geometry("1920x1080-10-7")
    txt1 = CTkTextbox(userhistories, width=500, height=600)
    txt1.place(x=200, y=100)
    txt2 = CTkTextbox(userhistories, width=500, height=600)
    txt2.place(x=840, y=100)
    txt2.insert("0.0", "                                                             USER HISTORY:")
    cur.execute("select * from logininf")
    inf=cur.fetchall()
    for i in inf:
        txt1.insert("0.0","name:"+i[0]+"\n"+"email:"+i[1]+"\n"+"password:"+i[2]+"\n"+"####################################"+"\n")
    ent1= CTkEntry(userhistories, width=900, font=("Helvitica", 28),fg_color=uifg_color,text_color=uitext_color,placeholder_text="see user history by entering email of user here")
    hisbt1 = CTkButton(userhistories, text="ENTER", font=("Helvitica", 28),command=histbtn)
    hisbt1.place(x=1094,y=10)
    bt2=CTkButton(userhistories,text="No. of times words searched by user",width=18,font=("Helvitica",29),command=nowords,fg_color=uiborder_color,text_color=uitext_color)
    bt2.place(x=500,y=700)
    ent1.place(x=335,y=10)
    userhistories.mainloop()




    
    
    
def adminwindow():
    winadmin=CTk()
    winadmin.title("admin window")
    winadmin.geometry("1920x1080-10-7")
    b_img=ImageTk.PhotoImage(Image.open(back_image))
    canvas=Canvas(winadmin,width=5000,height=2000,highlightthickness=0)
    canvas.create_image(0,0,anchor='nw',image=b_img)
    canvas.pack()
    bt1=CTkButton(winadmin,text="USER INFORMTION",width=18,font=("Helvitica",50),command=seeuserhistories,fg_color=uiborder_color,text_color=uitext_color)
    bt1.place(x=500,y=300)
    winadmin.mainloop()
def login():
    loginwin=CTk()
    loginwin.title("LOGIN")
    loginwin.geometry("1920x1080-10-7")
    b_img=ImageTk.PhotoImage(Image.open(back_image))
    canvas=Canvas(loginwin,width=5000,height=2000,highlightthickness=0)
    canvas.create_image(0,0,anchor='nw',image=b_img)
    canvas.pack()
    def back_sign_login():
        loginwin.destroy()
        login()
    def signupcmd():
         adminbtn.destroy()
         signinbut.place(x=10000,y=700)###code to remove CTkButton from screen
         signupbut.place(x=10000,y=650)####code to remove CTkButton from screen
         namelogin.place(x=570,y=350)
         gmaillogin.place(x=570,y=400)
         passlogin.place(x=570,y=450)
         otplogin.place(x=570,y=500)
         contbut2.place(x=1307,y=762)
         backbtn.place(x=0,y=762)
         otpbtn.place(x=975,y=348)
        
            
    def signincmd():
         adminbtn.destroy()
         otplogin.place(x=3000,y=500)
         contbut2.place(x=3000,y=700)
         namelogin.place(x=3000,y=350)
         lbl1_login.place(x=3000,y=350)
         otpbtn.place(x=3000,y=100)
         ####################above 6 line code just to remove CTkButton and CTkLabels out of screen
         gmaillogin.place(x=570,y=400)
         passlogin.place(x=570,y=450)
         signinbut.place(x=10000,y=700)
         signupbut.place(x=10000,y=650)
         contbut.place(x=1397,y=762)
         backbtn.place(x=0,y=762)
    
    def getotp():
        global rando
        gm=str(gmaillogin.get())
        na=str(namelogin.get())
        rando=randint(1000,10000)
        send="Hi "+na+",\n"+"OTP for your STRAIN browser is  "+str(rando)
        s_e="cs.pr0j3ct.xii@gmail.com"#sender email
        passwd=""#pass of sender
        server=SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(s_e,passwd)
        server.sendmail(s_e,gm,send)


    def cont_to_signin():
        o=otplogin.get()
        ####################################CTkLabel for account created?
        if str(rando)==o:
            pa=str(passlogin.get())
            na=str(namelogin.get())
            gm=str(gmaillogin.get())
            
            cur.execute("select* from logininf;")
            allinf=cur.fetchall()
            if allinf==[]:
                cur.execute("insert into logininf() values('{}','{}','{}');".format(na,gm,pa))
                con.commit()
                signincmd()
                
            else:
                for i in allinf:
                    if i[1]==gm:
                    
                        lbl1_login.configure(text="account already exist!")
                        lbl1_login.place(x=650,y=290)
                    else:
                        cur.execute("insert into logininf() values('{}','{}','{}');".format(na,gm,pa))
                        con.commit()
                        signincmd()
                            
            
        else:
            lbl1_login.configure(text="otp incorrect")
            lbl1_login.place(x=650,y=290)
        
        
    
        
    def cont_to_main():
        g=gmaillogin.get()
        p=passlogin.get()
        cur.execute("select* from logininf;")
        allinf=cur.fetchall()
        for i in allinf:
            if (g,p)==(i[1],i[2]):
                gm=open("getmailforhis.txt","w")#used to get personalized history for email
                gm.write(str(g))
                gm.close()
                f=open("himsgfile(code1).txt","w")
                f.write(i[0])
                f.close()
                loginwin.destroy()
                window1()
                break
            else:
                lbl1_login.configure(text="TRY AGAIN!")
                lbl1_login.place(x=650,y=305)
    def adminlogin():

        otplogin.place(x=3000, y=500)
        contbut2.place(x=3000, y=700)
        namelogin.place(x=3000, y=350)
        lbl1_login.place(x=3000, y=350)
        otpbtn.place(x=3000, y=100)
        gmaillogin.place(x=3000, y=400)
        passlogin.place(x=3000, y=450)
        signinbut.place(x=3000, y=700)
        signupbut.place(x=3000, y=650)
        contbut.place(x=3000, y=762)
        adminbtn.place(x=3000,y=762)
        ####################above  line code just to remove CTkButton  out of screen
        backbtn.place(x=0, y=762)
        adminup.place(x=640,y=650)
        adminin.place(x=690,y=700)
    def getotpadmin():
        global adminrand
        na=str(namelogin.get())
        adminrand=randint(1000,10000)
        send="Hi Akshat,\n"+na+" want to login as admin if you want allow him share this OTP with him\n"+"OTP:"+str(adminrand)
        s_e="cs.pr0j3ct.xii@gmail.com"#sender email
        r_e="akshatsrivastava206@gmail.com"
        passwd="omtghmrwfehjgcqb"#pass of sender
        server=SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(s_e,passwd)
        server.sendmail(s_e,r_e,send)





    def adminin():
        def toadminwin():
            g = gmaillogin.get()
            p = passlogin.get()
            cur.execute("select* from adminlogin;")
            allinf = cur.fetchall()
            for i in allinf:
                if (g, p) == (i[1], i[2]):
                    f = open("himsgfile(code1).txt", "w")
                    f.write(i[0])
                    f.close()
                    loginwin.destroy()
                    adminwindow()
                    break
                else:
                    lbl1_login.configure(text="TRY AGAIN!")
                    lbl1_login.place(x=650, y=305)

        adminup.place(x=3000, y=650)
        adminin.place(x=3000, y=700)
        gmaillogin.place(x=570, y=400)
        passlogin.place(x=570, y=450)
        cont_but_adminwin = CTkButton(loginwin, text="CONTINUE", font=("Helvitica", 20), command=toadminwin,fg_color=uiborder_color,text_color=uitext_color)
        cont_but_adminwin.place(x=1397,y=762)

    def cont_to_adminsignin():
        o = otplogin.get()
        ####################################CTkLabel for account created?
        if str(adminrand) == o:
            pa = str(passlogin.get())
            na = str(namelogin.get())
            gm = str(gmaillogin.get())

            cur.execute("select* from adminlogin;")
            allinf = cur.fetchall()
            if allinf==[]:
                cur.execute("insert into adminlogin() values('{}','{}','{}');".format(na, gm, pa))
                con.commit()
                otpbtn2.destroy()
                adminlogin()
                   
                
            else:
                for i in allinf:
                    if i[1] == gm:

                        lbl1_login.configure(text="account already exist!")
                        lbl1_login.place(x=650, y=290)
                    else:
                        cur.execute("insert into adminlogin() values('{}','{}','{}');".format(na, gm, pa))
                        con.commit()
                        otpbtn2.destroy()
                        adminlogin()
                   


        else:
            lbl1_login.configure(text="otp incorrect")
            lbl1_login.place(x=650, y=290)


    def adminup():
        global otpbtn2
        adminup.place(x=3000, y=650)
        adminin.place(x=3000, y=700)
        gmaillogin.place(x=570, y=400)
        passlogin.place(x=570, y=450)
        namelogin.place(x=570, y=350)
        otplogin.place(x=570, y=500)
        otpbtn2 = CTkButton(loginwin, text="G\nE\nT\n \nO\nT\nP", width=8, font=("Helvitica", 23), command=getotpadmin,fg_color=uiborder_color,text_color=uitext_color)
        otpbtn2.place(x=975, y=348)
        cont_but_adminsignin = CTkButton(loginwin, text="NEXT", font=("Helvitica", 20), command=cont_to_adminsignin,fg_color=uiborder_color,text_color=uitext_color)
        cont_but_adminsignin.place(x=1397, y=762)
    #login image
    signinbut=CTkButton(loginwin,text="SIGN IN",font=("Helvitica",20),command=signincmd,fg_color=uiborder_color,text_color=uitext_color)
    signinbut.place(x=690,y=700)
    signupbut=CTkButton(loginwin,text="SIGN UP",font=("Helvitica",19),command=signupcmd,fg_color=uiborder_color,text_color=uitext_color)
    signupbut.place(x=690,y=650)
    gmaillogin=CTkEntry(loginwin,width=400,font=("Helvitica",28),fg_color=uifg_color,text_color=uitext_color,placeholder_text="Enter your Email....")
    passlogin=CTkEntry(loginwin,width=400,font=("Helvitica",28),fg_color=uifg_color,text_color=uitext_color,placeholder_text="Enter your Password....")
    namelogin=CTkEntry(loginwin,width=400,font=("Helvitica",28),fg_color=uifg_color,text_color=uitext_color,placeholder_text="Enter your Name....")#remove place on sign up
    otplogin=CTkEntry(loginwin,width=400,font=("Helvitica",28),fg_color=uifg_color,text_color=uitext_color,placeholder_text="Enter your OTP....")
    lbl1_login=CTkLabel(loginwin,text="TRY AGAIN!",font=("Helvitica",27))
    contbut=CTkButton(loginwin,text="CONTINUE",font=("Helvitica",20),command=cont_to_main,fg_color=uiborder_color,text_color=uitext_color)
    contbut2=CTkButton(loginwin,text="CONTINUE TO SIGN IN",font=("Helvitica",20),command=cont_to_signin,fg_color=uiborder_color,text_color=uitext_color)
    backbtn=CTkButton(loginwin,text="BACK",font=("Helvitica",20),command=back_sign_login,fg_color=uiborder_color,text_color=uitext_color)
    otpbtn=CTkButton(loginwin,text="G\nE\nT\n \nO\nT\nP",width=8,font=("Helvitica",23),command=getotp,fg_color=uiborder_color,text_color=uitext_color)
    adminbtn = CTkButton(loginwin, text="ADMIN LOGIN", width=8, font=("Helvitica", 19),command=adminlogin,fg_color=uiborder_color,text_color=uitext_color)
    adminbtn.place(x=690, y=600)
    adminup = CTkButton(loginwin, text="NEW! REGISTER AS ADMIN", font=("Helvitica", 20),command=adminup,fg_color=uiborder_color,text_color=uitext_color)
    adminin = CTkButton(loginwin, text="LOGIN AS ADMIN", font=("Helvitica", 20),command=adminin,fg_color=uiborder_color,text_color=uitext_color)

    
    
    
    loginwin.mainloop()  
login()
#window1()



#use destroy command with unused buttom,adminpage