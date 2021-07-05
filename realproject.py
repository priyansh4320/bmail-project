import speech_recognition as sr
import pyttsx3
from email.mime.multipart import MIMEMultipart
from  email.mime.text import MIMEText
import smtplib
import random
from future.moves import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as sqlc
from PIL import Image,ImageTk
import imaplib
import email
import traceback
from email.header import decode_header
import webbrowser
import os
import time
#===================tts and stt========================
engine=pyttsx3.init()
r=sr.Recognizer()
m=sr.Microphone()

#===================database connection===============
mydb = sqlc.connect(host="localhost", user="root", passwd="tiger", database="co3rd", autocommit="true")
mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE IF NOT EXISTS co3rd")
#mycursor.execute("CREATE TABLE IF NOT EXISTS userinfo(useername VARCHAR(20)  PRIMARY KEY, password VARCHAR(20), email VARCHAR(300) PRIMARY KEY, phone INT(11) UNIQUE KEY, fullname VARCHAR(300))")

#=================================loginform==================================
class loginform:
    def __init__(self, root):
        #=====================================root=====================================
        self.root = root
        self.root.geometry('1350x700+100+50')
        self.root.configure(background= "orange")
        self.root.title("Bmail - login / Sign-in")

        global im
        im = Image.open("E:\\pythonprojects\\bmail\\images\\6.jfif")
        im = im.resize((730, 700), Image.ANTIALIAS)
        global im1
        im1 = ImageTk.PhotoImage(im)
        imlab = Label(self.root, image=im1)
        imlab.pack(side="right")

        frame = tk.Frame(master=self.root, height=600, width=500, bg="white")
        frame.place(x=50, y=50)
        frame.pack_propagate(False)

        label1 = tk.Label(master=frame, text="login / Sign-in", fg="white", bg="orange",
                          font=("Verdana", 20, " bold"), width=50, anchor="w").pack(anchor="n")

        self.userl = tk.Label(text="username:", master=frame, font=("Verdana, Bold", 11))
        self.userl.place(x=10, y=150)
        self.userE = tk.Text(master=frame, font=("Verdana, Bold", 11), bg="white", fg="grey", width=55,height=3)
        self.userE.place(x=10, y=180)
        self.userE.bind("<Enter>", lambda event, arg="enter your username here": self.speaker(event, arg))
        self.userE.bind("<Button-1>", lambda event, widget=self.userE: self.stt(event, widget))
        self.userE.bind("<Return>",self.focus)

        passl = tk.Label(text="password:", master=frame, font=("Verdana, Bold", 11)).place(x=10, y=270)
        self.passE = tk.Text(master=frame, font=("Verdana, Bold", 11), bg="white", fg="grey", width=55,height=3)
        self.passE.place(x=10, y=300)
        self.passE.bind("<Enter>",lambda event,arg="enter your password here":self.speaker(event,arg))
        self.passE.bind("<Button-1>", lambda event, widget=self.passE: self.stt2(event, widget))


        self.loginb = tk.Button(master=frame,text="login/ signin", bg="orange", fg="white", relief="solid", font=("Verdana", 11),
                                width=20, height=5,command=self.login_func)
        self.loginb.place(x=10, y=370)
        self.loginb.bind("<Enter>",lambda event,arg="press to login":self.speaker(event,arg))


        self.registerb = tk.Button(master=frame, text="register", bg="orange", fg="white", relief="solid",
                                font=("Verdana", 11),
                                width=20, height=5,command=self.registerform)
        self.registerb.place(x=230, y=370)
        self.registerb.bind("<Enter>",lambda event,arg="press to register":self.speaker(event,arg))

    #====================login function
    def login_func(self):
        self.user = self.userE.get("1.0","end-1c")
        self.passw = self.passE.get("1.0","end-1c")
        try:
            mycursor.execute("SELECT * FROM co3rd.userinfo WHERE useername = %s AND password= %s", ((self.user), (self.passw)))
            result = mycursor.fetchone()
            self.resmail=str(result[2])
            if self.user=="" and self.passw=="":
                messagebox.showerror("Error", "Enter all the credentials", parent=self.root)
            if self.user =="" or self.passw=="":
                messagebox.showerror("Error", "missing username or password", parent=self.root)
            if result==None:
                messagebox.showerror("Error", "incorrect credentials", parent=self.root)
            if self.user==result[0] and self.passw==result[1]:
                self.dashboard()
        except Exception as e:
            print(e)
    #======================dashboard==================================================
    def dashboard(self):
        self.root = tk.Toplevel()
        self.root.geometry("1350x700+100+50")
        self.root.resizable(False, False)
        self.root.title("bmail-dashboard")
        self.root.configure(background="orange")

        dframe = tk.Frame(self.root, width=488, height=700, bg="white")
        dframe.place(x=0, y=0)
        dframe.pack_propagate(False)

        global im
        im = Image.open("E:\\pythonprojects\\bmail\\images\\4.jpg")
        im = im.resize((500, 700), Image.ANTIALIAS)
        global im1
        im1 = ImageTk.PhotoImage(im)
        ilabel = tk.Label(master=dframe, image=im1, height=700, width=500)
        ilabel.pack()

        dlabel = tk.Label(self.root, text="Dashboard", bg="orange", width=45, font=("verdana", 20, "bold"), fg="white",
                          anchor="w", padx=1)
        dlabel.pack(side="top", anchor="e")
        dlabel = tk.Label(self.root, text=self.user, bg="orange", width=45, font=("verdana", 20, "bold"), fg="white",
                          anchor="w", padx=1,pady=1)
        dlabel.pack( anchor="e")

        bcompose = tk.Button(self.root, text="compose mail", width=35, height=14, font=("verdana", 11), bg="white", command=self.compose_mail)
        bcompose.place(x=550, y=350)
        bcompose.bind("<Enter>",lambda event,arg="PRESS TO compose email.":self.speaker(event,arg))

        binbox = tk.Button(self.root, text="go to inbox", width=35, height=14, font=("verdana", 11), bg="white", command= self.inbox)
        binbox.place(x=950, y=350)
        binbox.bind("<Enter>",lambda event,arg="press to go to INbox":self.speaker(event, arg))

    #========================================compose mail============================================
    def compose_mail(self):
        self.root = Toplevel()
        self.root.title("Bmail-Compose Mail form")
        self.root.geometry("1350x700+100+50")
        self.root.resizable(False, False)
        self.root.configure(bg="orange")

        global im
        im = Image.open("E:\\pythonprojects\\bmail\\images\\4.jpg")
        im = im.resize((450, 700), Image.ANTIALIAS)
        global im1
        im1 = ImageTk.PhotoImage(im)
        ilabel = tk.Label(self.root, image=im1)
        ilabel.pack(side="left")

        cframe = Frame(self.root, width=900)
        cframe.pack(fill="y", side="right")
        cframe.pack_propagate(False)

        clabel = Label(cframe, text="Compose Mail Here...", fg="white", bg="orange", anchor="sw",
                       font=("Verdana", 20, "bold"), height=4, pady=1)
        clabel.pack(side="top", fill="x")

        lto = Label(cframe, text="TO:")
        lto.place(x=20, y=200)
        self.tto = Text(cframe, width=90, height=3,
                        relief="flat")  # must be flat, groove, raised, ridge, solid, or sunken
        self.tto.place(x=20, y=225)
        self.tto.bind("<Enter>",lambda event,arg="enter recipient mail id here":self.speaker(event,arg))
        self.tto.bind("<Button-1>", lambda event, widget=self.tto: self.stt2(event, widget))

        lsub = Label(cframe, text="Subject:")
        lsub.place(x=20, y=300)
        self.tsub = Text(cframe, width=90, height=3,
                         relief="flat")
        self.tsub.place(x=20, y=325)
        self.tsub.bind("<Enter>",lambda event,arg="enter mail subject here":self.speaker(event,arg))
        self.tsub.bind("<Button-1>", lambda event, widget=self.tsub: self.stt3(event, widget))

        lmessage = Label(cframe, text="Mail Text:")
        lmessage.place(x=20, y=400)
        self.tmessage = Text(cframe, width=90, height=10,
                             relief="flat")
        self.tmessage.place(x=20, y=425)
        self.tmessage.bind("<Enter>",lambda event,arg="Enter mail text here":self.speaker(event,arg))
        self.tmessage.bind("<Button-1>", lambda event, widget=self.tmessage: self.stt3(event, widget))

        self.sendb = Button(cframe, text="Send", width=20, height=37, relief="solid", bg="orange", fg="white",command=self.send)
        self.sendb.place(x=750, y=135)
        self.sendb.bind("<Enter>",lambda event,arg="press to send mail":self.speaker(event,arg))

        back = Button(clabel,text="Back",height=4,width=20,relief="solid",command=self.dashboard)
        back.place(x=750,y=5)
        back.bind("<Enter>", lambda event, arg="press to go back": self.speaker(event, arg))

    #=============================send mail function
    def send(self):
        try:
            to = self.tto.get("1.0", "end-1c") + "@gmail.com"
            acfrom = self.resmail
            subject = self.tsub.get("1.0", "end-1c")
            message = self.tmessage.get("1.0", "end-1c")
            pas = self.passw
            # create message===============================================================
            msg = MIMEMultipart()
            msg['To'] = to
            msg['From'] = acfrom
            msg['Subject'] = subject
            msg.attach(MIMEText(message, "plain"))

            # now send the mail=============================================================
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(acfrom, pas)
            server.sendmail(acfrom, to, msg.as_string())
            server.quit()

        except Exception as e:
            print(e)
    #======================================registerform======================================
    def registerform(self):
        self.root = tk.Toplevel()
        self.root.title("Bmail-Registeration form")
        self.root.geometry("1350x700+100+50")
        self.root.resizable(False, False)
        self.root.configure(bg="orange")

        rframe = Frame(self.root, width=900)
        rframe.pack(fill="y", side="right")
        rframe.pack_propagate(False)

        rlabel = Label(rframe, text="Register / Signup", fg="white", bg="orange", anchor="sw",
                       font=("Verdana", 20, "bold"), height=4, pady=1)
        rlabel.pack(side="top", fill="x")

        sep = ttk.Separator(rframe, orient="horizontal")
        sep.pack(fill="x", pady=1)

        # column1==========
        lname = Label(rframe, text="Enter Full Name:")
        lname.place(x=20, y=200)
        self.tname = Text(rframe, width=50, height=3,
                          relief="flat")  # must be flat, groove, raised, ridge, solid, or sunken
        self.tname.place(x=20, y=225)
        self.tname.bind("<Enter>",lambda event,arg="Enter Full Name here":self.speaker(event,arg))
        self.tname.bind("<Button-1>", lambda event, widget=self.tname: self.stt3(event, widget))

        lphone = Label(rframe, text="Enter Phone Number:")
        lphone.place(x=20, y=300)
        self.tphone = Text(rframe, width=50, height=3, relief="flat")
        self.tphone.place(x=20, y=325)
        self.tphone.bind("<Enter>",lambda event,arg="enter your phone number here":self.speaker(event,arg))
        self.tphone.bind("<Button-1>", lambda event, widget=self.tphone: self.stt2(event, widget))

        lemail = Label(rframe, text="Enter Your Email:")
        lemail.place(x=20, y=400)
        self.temail = Text(rframe, width=50, height=3, relief="flat")
        self.temail.place(x=20, y=425)
        self.temail.bind("<Enter>",lambda event,arg="enter your email id here":self.speaker(event,arg))
        self.temail.bind("<Button-1>", lambda event, widget=self.temail: self.stt2(event, widget))

        lotp = Label(rframe, text="Enter OTP:")
        lotp.place(x=20, y=500)
        self.totp = Text(rframe, width=50, height=3, relief="flat")
        self.totp.place(x=20, y=525)
        self.totp.bind("<Enter>",lambda event,arg="enter o t p here":self.speaker(event,arg))
        self.totp.bind("<Button-1>", lambda event, widget=self.totp: self.stt2(event, widget))

        botp = Button(rframe, text="Send OTP", width=20, height=3, relief="flat", bg="orange", fg="white",command=self.sending)
        botp.place(x=20, y=600)
        botp.bind("<Enter>",lambda event,arg="press to get o t p":self.speaker(event,arg))

        botp1 = Button(rframe, text="Verify OTP", width=20, height=3, relief="flat", bg="orange", fg="white",command=self.verify)
        botp1.place(x=200, y=600)
        botp1.bind("<Enter>",lambda event,arg="press to verify o t p":self.speaker(event,arg))

        self.errorl = Label(rframe, width=50)
        self.errorl.place(x=20, y=670)

        # column2============
        lruser = Label(rframe, text="Set Username:")
        lruser.place(x=450, y=200)
        self.truser = Text(rframe, width=50, height=3, relief="flat", state="disable")
        self.truser.place(x=450, y=225)
        self.truser.bind("<Enter>",lambda event,arg="set user name here":self.speaker(event,arg))
        self.truser.bind("<Button-1>", lambda event, widget=self.truser: self.stt2(event, widget))

        lsetpass = Label(rframe, text="Set Password:")
        lsetpass.place(x=450, y=300)
        self.tsetpass = Text(rframe, width=50, height=3, relief="flat", state="disable")
        self.tsetpass.place(x=450, y=325)
        self.tsetpass.bind("<Enter>", lambda event, arg="set password here": self.speaker(event, arg))
        self.tsetpass.bind("<Button-1>", lambda event, widget=self.tsetpass: self.stt2(event, widget))

        lconpass = Label(rframe, text="Confirm Password:")
        lconpass.place(x=450, y=400)
        self.tconpass = Text(rframe, width=50, height=3, relief="flat", state="disable")
        self.tconpass.bind("<Button-3>",self.checkp)
        self.tconpass.place(x=450, y=425)
        self.tconpass.bind("<Enter>",lambda event,arg="enter password here and then press enter to confirm password":self.speaker(event,arg))
        self.tconpass.bind("<Button-1>", lambda event, widget=self.tconpass: self.stt2(event, widget))

        self.lerror = Label(rframe, width=50)
        self.lerror.place(x=450, y=485)

        bregister = Button(rframe, text="REGISTER", font=("arial", 9, "bold"), width=56, height=8, relief="solid",
                           bg="orange", fg="white",command=self.register)
        bregister.place(x=450, y=525)
        bregister.bind("<Enter>",lambda event,arg="press to register":self.speaker(event,arg))

        back = Button(rlabel, text="Back", height=4, width=20, relief="solid")
        back.place(x=750, y=5)
        back.bind("<Button-1>",lambda event,root=self.root:self.back(event,root))
        back.bind("<Enter>", lambda event, arg="press to go back": self.speaker(event, arg))
    def back(self,event,root):
        root=Toplevel()
        self.__init__(root)
    # ===================================otp sending functions=============================
    r_no = random.randrange(1111, 9999)
    global otp
    otp = r_no

    def sending(self):
        try:
            sender = "sender@gmail.com"
            passw = "password"
            reciever = self.temail.get("1.0","end-1c")+"@gmail.com"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender,passw)
            msg = "welcome to Bmail , your otp is"+str(otp)
            server.sendmail(sender, reciever, msg)
            server.quit()
        except Exception as e:
            print(e)

    def verify(self):
        try:
            no = int(self.totp.get("1.0", "end-1c"))
            print(otp)
            if no == otp:
                self.errorl.configure(text="verified")
                engine.say("o t p has been verfied, now u can set username")
                #self.errorl.place(x=20,y=670)
            else:
                self.errorl.configure(text="wrong otp")
            if self.errorl.cget("text") == "verified":
                self.truser.configure(state="normal")
                self.tsetpass.configure(state="normal")
                self.tconpass.configure(state="normal")

        except Exception as e:
            print(e)

#=============password check================

    def checkp(self, event):
        try:
            if self.tsetpass.get("1.0", "end-1c") != "" and self.tconpass.get("1.0", "end-1c") != "":
                if self.tsetpass.get("1.0", "end-1c") == self.tconpass.get("1.0", "end-1c"):
                    self.lerror.configure(text="password confirmed")
                else:
                    self.lerror.configure(text="not confirmed")
        except Exception as e:
            print(e)

#================register function=================

    def register(self):
        try:
            if self.lerror.cget("text")=="password confirmed":
                fname= self.tname.get("1.0","end-1c")
                passw= self.tconpass.get("1.0","end-1c")
                mails =self.temail.get("1.0","end-1c") + "@gmail.com"
                phno=self.tphone.get("1.0","end-1c")
                user =self.truser.get("1.0","end-1c")
                mycursor.execute("SELECT * FROM co3rd.userinfo")
                result = mycursor.fetchone()
                #print(result,len(phno))
                mycursor.execute("INSERT INTO co3rd.userinfo VALUES(%s,%s,%s,%s,%s)",((user),(passw),(mails),(phno),(fname)))
                mydb.commit()


            else:

                print("not registered ",str(self.tphone.get("1.0", "end-1c")))

        except Exception as e:
            print(e)

    #===============================inbox============================
    def inbox(self):
        self.root = tk.Toplevel()
        self.root.title("INBOX form")
        self.root.geometry("1350x700+100+50")
        self.root.resizable(False, False)
        self.root.configure(bg="orange")

        inframe = Frame(self.root, width=900)
        inframe.pack(fill="y", side="right")
        inframe.pack_propagate(False)

        rlabel = Label(inframe, text="INBOX", fg="white", bg="orange", anchor="sw",
                       font=("Verdana", 20, "bold"), height=4, pady=1)
        rlabel.pack(side="top", fill="x")

        sep = ttk.Separator(inframe, orient="horizontal")
        sep.pack(fill="x", pady=1)

        self.inuser = Label(inframe, text="",height=27,width=100,anchor="nw",bg="yellow")
        self.inuser.place(x=20, y=200)
        self.inuser.bind("<Enter>",lambda event,arg="press to read mails":self.speaker(event,arg))
        self.inuser.bind("<Button-1>",self.readmail)

        self.refresh = Button(inframe, text="refresh", width=20, height=37, relief="solid", bg="orange", fg="white")
        self.refresh.place(x=750, y=135)
        self.refresh.bind("<Enter>",lambda event,arg="press to refresh":self.speaker(event,arg))
        self.refresh.bind("<Button-1>",self.read_email_from_gmail)

        back = Button(rlabel, text="Back", height=4, width=20, relief="solid",command=self.dashboard)
        back.place(x=750, y=5)
        back.bind("<Enter>", lambda event, arg="press to go back": self.speaker(event, arg))

    def readmail(self,event):
        speak=self.inuser.cget("text")
        engine.say(speak)
        engine.runAndWait()
#===============================speech asistant===================================
    def speaker(self, event, arg):
        engine.say(arg)
        engine.runAndWait()

    def stt(self,event,widget):
        self.passE.delete("1.0", "end")
        with m:
            print("speak now")
            audio = r.listen(m,timeout=10)
        global text
        text = r.recognize_google(audio)
        lst = []
        ra = len(text)
        for i in range(ra):
            lst.append(text[i])
        print(lst)
        b = ""
        lr = len(lst)
        lst2 = []
        for i in range(lr):
            if lst[i] != " ":
                lst2.append(lst[i])
        print(str("".join(lst2)))
        widget.insert("1.0",(str("".join(lst2))).lower())


    def focus(self,event):
        self.userl.focus()

    def stt2(self,event,widget):
        widget.delete("1.0", "end")
        r1 = sr.Recognizer()
        m1 = sr.Microphone()
        with m1 as source:
            print("speak now")
            audio = r1.listen(source,timeout=8)

        text = r1.recognize_google(audio)
        lst = []
        ra = len(text)
        for i in range(ra):
            lst.append(text[i])
        print(lst)
        b = ""
        lr = len(lst)
        lst2 = []
        for i in range(lr):
            if lst[i] != " ":
                lst2.append(lst[i])
        print(str("".join(lst2)))
        widget.insert("1.0",(str("".join(lst2))).lower())

    def stt3(self,event,widget):
        r2 = sr.Recognizer()
        m2 = sr.Microphone()
        with m2 as source:
            widget.delete("1.0", "end")
            print("speak now")
            audio = r2.listen(source, timeout=8)
        text = r2.recognize_google(audio)
        print(text)
        widget.insert("1.0", text)

    def read_email_from_gmail(self,event):
        try:
            username = self.resmail
            password = self.passw

            def clean(text):
                return "".join(c if c.isalnum() else "_" for c in text)

            imap = imaplib.IMAP4_SSL("imap.gmail.com",993)
            imap.login(username, password)

            status, messages = imap.select("INBOX")
            N = 3
            messages = int(messages[0])

            for i in range(messages, messages - N, -1):
                res, msg = imap.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding)
                        From, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(From, bytes):
                            From = From.decode(encoding)
                        print("Subject:", subject)
                        print("From:", From)
                        text1=self.inuser.cget("text")+subject+'\n'+From
                        self.inuser.configure(text=text1)
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    print(body)
                                    text2=self.inuser.cget("text")+'\n'+body
                                    self.inuser.configure(text=text2)
            imap.close()
            imap.logout()


        except Exception as e:
            traceback.print_exc()
            print(str(e))


root=tk.Tk()
obj=loginform(root)
obj.root.mainloop()
