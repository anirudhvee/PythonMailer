#!/usr/local/bin/python3
from colorama import init
from colorama import Fore
from termcolor import colored
from base64 import b64encode
from base64 import b64decode
import cv2
import face_recognition
from time import sleep,time
import sys
import smtplib
import os
from stdiomask import getpass
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import pickle
from datetime import datetime
from random import choice
import speech_recognition as speech
from re import search
from tqdm import trange
from shutil import make_archive,copyfile
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

init()
#lambda functions
encrypt = lambda x: b64encode(x.encode('utf-32')).hex()

decrypt = lambda x: b64decode(bytes.fromhex(x)).decode('utf-32')

parse = lambda x: x.replace('\ ',' ').replace('\~','~')

take_pic = lambda x,y : cv2.imwrite(y,x.read()[-1]) if x.read()[0] else False

if os.name == "nt":
    cam_check = lambda : [a for a in [cv2.VideoCapture(0,cv2.CAP_DSHOW)] if a.read()[0]]
else:
    cam_check = lambda : [a for a in [cv2.VideoCapture(0)] if a.read()[0]]#cv2.CAP_DSHOW does not work for mac


class mailbox:#mailbox object


    def __init__(self,user,pwd):#initialise driver and user and pwd vars

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument('--disable-extensions')
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        self.driver=webdriver.Chrome(options=options,executable_path=ChromeDriverManager().install())
        self.user = user
        self.pwd = pwd


    def gmail(self):#open gmail inbox


        EMAILFIELD = (By.ID, 'identifierId')
        PASSWORDFIELD = (By.NAME, 'password')
        NEXTBUTTON1 = (By.ID, 'identifierNext')
        NEXTBUTTON2 = (By.ID, 'passwordNext')
        CONTINUE = (By.ID, 'confirm-submit')
        self.driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent')
        self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[2]/div[2]/button[1]').click()
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(self.user)
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(NEXTBUTTON1)).click()
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(self.pwd)
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(NEXTBUTTON2)).click()
        sleep(6)
        self.driver.get('https://mail.google.com/mail/u/0/#inbox')
        self.driver.execute_script('alert("LOG OUT NOT REQUIRED AS COOKIES ARE NOT STORED");')
        '''if WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(CONTINUE)):
            mypath = 'QuickMail/'
            f = open(mypath+'log.log','a+')
            f.write('\n[*] ACCOUNT '+self.user+' OPENED TO VIEW ' + '\nAT ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            f.close()
            sleep(2)
            self.driver.get('https://mail.google.com/mail/u/0/#inbox')
            self.driver.execute_script('alert("LOG OUT NOT REQUIRED AS COOKIES ARE NOT STORED");')'''



    def yahoo(self):#open yahoo inbox


        self.driver.get('https://login.yahoo.com')
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.phone-no"))).send_keys(self.user)
        self.driver.find_element_by_css_selector("input.orko-button-primary.orko-button#login-signin").click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#login-passwd"))).send_keys(self.pwd)
        self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.pure-button.puree-button-primary.puree-spinner-button"))))
        mypath = 'QuickMail/'
        f = open(mypath+'log.log','a+')
        f.write('\n[*] ACCOUNT '+self.user+' OPENED TO VIEW ' + '\nAT ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        f.close()
        self.driver.execute_script('alert("LOG OUT NOT REQUIRED AS COOKIES ARE NOT STORED");')


    def outlook(self):#open outlook/hotmail inbox


        EMAILFIELD = (By.ID, "i0116")
        PASSWORDFIELD = (By.ID, "i0118")
        NEXTBUTTON = (By.ID, "idSIButton9")
        self.driver.get('https://login.live.com')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(self.user)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(self.pwd)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
        sleep(2)
        mypath = 'QuickMail/'
        f = open(mypath+'log.log','a+')
        f.write('\n[*] ACCOUNT '+self.user+' OPENED TO VIEW ' + '\nAT ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        f.close()
        self.driver.get('https://outlook.live.com/mail/0/inbox')
        self.driver.execute_script('alert("LOG OUT NOT REQUIRED AS COOKIES ARE NOT STORED");')


    def apple(self):#open apple mail inbox


        self.driver.get('https://www.icloud.com/mail')
        delay = 10
        WebDriverWait(self.driver, delay).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'auth-frame')))
        username = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, 'account_name_text_field')))
        username.send_keys(self.user)
        username.send_keys(Keys.ENTER)
        password = WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.ID, 'password_text_field')))
        password.send_keys(self.pwd)
        password.send_keys(Keys.ENTER)
        mypath = 'QuickMail/'
        f = open(mypath+'log.log','a+')
        f.write('\n[*] ACCOUNT '+self.user+' OPENED TO VIEW ' + '\nAT ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        f.close()
        self.driver.execute_script('alert("LOG OUT NOT REQUIRED AS COOKIES ARE NOT STORED");')


    def rediff(self):#open rediffmail inbox


        self.driver.get('https://mail.rediff.com/cgi-bin/login.cgi')
        self.driver.find_element_by_id('login1').send_keys(self.user)
        self.driver.find_element_by_id('password').send_keys(self.pwd)
        self.driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[2]/form/div[1]/div[2]/div[2]/div[2]/input[2]').click()
        mypath = 'QuickMail/'
        f = open(mypath+'log.log','a+')
        f.write('\n[*] ACCOUNT '+self.user+' OPENED TO VIEW ' + '\nAT ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        f.close()
        self.driver.execute_script('alert("LOG OUT NOT REQUIRED AS COOKIES ARE NOT STORED");')


def setup():#setup to be done for the first time


    d={'gmail':('smtp.gmail.com',587),
       'outlook':('smtp.office365.com',587),
       'yahoo':('smtp.mail.yahoo.com',587),#app specific
       'icloud':('smtp.mail.me.com',587),#app specific
       'rediffmail':('smtp.rediffmailpro.com',587),
       'rediff':('smtp.rediffmail.com',25)}


    def load():#fancy loading animation (of sorts)


        load_str = "starting the setup ..."
        ls_len = len(load_str)
        animation = "|_/-\_|"
        anicount = 0
        counttime = 0
        i = 0
        while (counttime != 100):
            sleep(0.05)
            load_str_list = list(load_str)
            x = ord(load_str_list[i])
            y = 0
            if x != 32 and x != 46:
                if x>90:
                    y = x-32
                else:
                    y = x + 32
                load_str_list[i]= chr(y)
            res =''
            for j in range(ls_len):
                res = res + load_str_list[j]
            sys.stdout.write("\r"+res + animation[anicount])
            sys.stdout.flush()
            load_str = res
            anicount = (anicount + 1)% 4
            i =(i + 1)% ls_len
            counttime = counttime + 1
        if os.name =="nt":
            os.system("cls")
        else:
            os.system("clear")
    try:
        load()
        print(colored('''


       ____  _    _ _____ _____ _  ____  __          _____ _
      / __ \| |  | |_   _/ ____| |/ /  \/  |   /\   |_   _| |
     | |  | | |  | | | || |    | ' /| \  / |  /  \    | | | |
     | |  | | |  | | | || |    |  < | |\/| | / /\ \   | | | |
     | |__| | |__| |_| || |____| . \| |  | |/ ____ \ _| |_| |____
      \___\_\\\____/|_____\_____|_|\_\_|  |_/_/    \_\_____|______|

        A COMPUTER SCIENCE PROJECT BY V. ANIRUDH AND NISHANT OF CLASS 12 E


        ''', 'green', attrs=['bold']))#fancy ascii art
        mypath = 'QuickMail/'
        os.umask(0)
        z=1
        signer=''
        present = []
        if not os.path.isdir(mypath):
            os.makedirs(mypath, 0o777)#create folder if doesnt exist
            open(mypath+'temp_mail.txt','w+')#create mail typing file
        if not os.path.isdir(mypath+'/faces'):
            os.makedirs(mypath+'/faces',0o777)#create folder for face rec
        if not os.path.isdir(mypath+'/faces/2'):
            os.makedirs(mypath+'/faces/2',0o777)
        if not os.path.isdir(mypath+'/faces/1'):
            os.makedirs(mypath+'/faces/1',0o777)
        while 1:
            try:
                open(r'QuickMail/cred.log').read()#check if mail id setup is complete
            except FileNotFoundError:
                add_address('')
            inp1 = colored('\n[*] DO YOU WANT TO ADD ANOTHER ACCOUNT (Y/N) ','green',attrs=['bold'])
            try:
                abcd2 = input(inp1).upper()
            except:
                pri3 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                print(pri3)
                continue
            if abcd2=='N':
                break
            elif abcd2 == 'Y':
                continue
            else:
                pri4 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                print(pri4)
        check = cam_check()
        security = ''
        if check:#for setting a security option
            while 1:
                try:
                    inp2 = colored('\n[*] SELECT METHOD TO SECURE QUICK MAIL\n'+'1)FACE ID\n'+'2)PASSWORD\n','green',attrs=['bold'])
                    a = input(inp2)
                except:
                    pri5 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                    print(pri5)
                    continue
                if a not in '12':
                    pri6 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                    print(pri6)
                else:
                    a = int(a)
                    if a == 1:
                        pri7 = colored('\n[*] STARTING FACE RECOGNITION ENGINE ', 'green',attrs=['bold'])
                        print(pri7)
                        if face(check[0]):
                            pri8 = colored('\n[*] FACE ID SET','green',attrs=['bold'])
                            print(pri8)
                            security = 'face|_/-\_|'
                            while 1:
                                inp10 = colored("\n[*] ENTER BACKUP PASSWORD FOR SERVICE ",'green',attrs=['bold'])
                                inp11 = colored("\n[*] RE-ENTER BACKUP PASSWORD ",'green',attrs=['bold'])
                                secure1 = getpass(prompt=inp10)
                                secure2 = getpass(prompt=inp11)
                                if secure1 ==  secure2:
                                    pri9 = colored('\n[*] PASSWORD SET','green',attrs=['bold'])
                                    print(pri9)
                                    break
                                else:
                                    pri10 =colored('\n[*] PASSWORDS DO NOT MATCH','red',attrs=['bold'])
                                    print(pri10)
                            security += secure1
                    if a == 2:
                        while 1:
                            inp3 = colored("\n[*] ENTER PASSWORD FOR SERVICE ",'green',attrs=['bold'])
                            inp4 = colored("\n[*] RE-ENTER PASSWORD ",'green',attrs=['bold'])
                            secure1 = getpass(prompt=inp3)
                            secure2 = getpass(prompt=inp4)
                            if secure1 ==  secure2:
                                pri11 = colored('\n[*] PASSWORD SET', 'green',attrs=['bold'])
                                print(pri11)
                                break
                            else:
                                pri12 = colored('\n[*] PASSWORDS DO NOT MATCH', 'red',attrs=['bold'])
                                print(pri12)
                        security = secure1
                    break
        else:
            while 1:
                if 1:
                    a = int(a)
                    if a == 1:
                        while 1:
                            inp3 = colored("\n[*] ENTER PASSWORD FOR SERVICE ",'green',attrs=['bold'])
                            inp4 = colored("\n[*] RE-ENTER PASSWORD ",'green',attrs=['bold'])
                            secure1 = getpass(prompt=inp3)
                            secure2 = getpass(prompt=inp4)
                            if secure1 ==  secure2:
                                pri13 = colored('\n[*] PASSWORD SET', 'green',attrs=['bold'])
                                print(pri13)
                                break
                            else:
                                pri14 = colored('\n[*] PASSWORDS DO NOT MATCH', 'red',attrs=['bold'])
                                print(pri14)
                        security = secure1
                    break
        while 1:
            try:
                inp5 = colored('\n[*] ENTER A RECOVERY MAIL ID ','green',attrs=['bold'])
                mail = input(inp5)
            except:
                pri15 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                print(pri15)
                continue
            a = mail.split('@')
            pri16 = colored('\n[*] SENDING OTP TO '+mail[0]+'*'*(len(a[0])-2)+a[0][-1]+'@'+a[1], 'green',attrs=['bold'])
            print(pri16)
            req_otp = otp()
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'CONFIRM RECOVERY MAIL ADDRESS'
            msg['From'] = 'quick.mail.noreply@gmail.com'
            ab = 'ENTER THIS OTP IN QUICK MAIL TO CONFIRM RECOVERY MAIL ADDRESS: '+req_otp
            ac = MIMEText(ab, 'html')
            msg.attach(ac)
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.login('quick.mail.noreply@gmail.com','anirudhnfs01')
            a = time()
            server.sendmail('quick.mail.noreply@gmail.com', mail, msg.as_string())
            server.quit()
            tries = 5
            while tries>0:
                inp6 = colored('\n[*] ENTER OTP SENT TO YOUR RECOVERY MAIL WITHIN 30 SECONDS ','green',attrs=['bold'])
                ad = input(inp6)
                if time()-a > 30:
                    pri17 = colored('\n[*] TIME UP', 'red',attrs=['bold'])
                    print(pri17)
                    break
                if ad == req_otp:
                    tries = 0
                    continue
                else:
                    pri18 = colored('\n[*] INCORRECT OTP. TRIES LEFT: '+str(tries),'red',attrs=['bold'])
                    print(pri18)
                tries -= 1
            if tries:
                pri19 = colored('\n[*] OUT OF TRIES.','red',attrs=['bold'])
                print(pri19)
            elif not tries:
                break
        ab = open(mypath+'/lock.log','w+')
        ab.write(encrypt(encrypt(security))+'\n'+encrypt(encrypt(mail)))
        ab.close()
    except KeyboardInterrupt:
        pri20 = colored('\n[*] YOU HAVE QUIT THE SETUP ','red',attrs=['bold'])
        print(pri20)


def change1(mail,mypath):#change stored credentials for the smtp


    file = open(mypath+'cred.log','r')
    f = open(mypath+'log.log','a+')
    entered = file.read()
    file.close()
    e=entered.split('\n\n\n')
    fa=[]
    for a in e:
        fa.append(a.split('\n'))
    fa.pop(-1)
    new_app = ''
    pri21 = colored('\n[*] STORED PASSWORD IS INCORRECT FOR '+mail,'red',attrs=['bold'])
    print(pri21)
    for a in range(len(fa)):
        if decrypt(decrypt(fa[a][1])) == mail:
            if mail.split('@')[-1].split('.')[0] in ('yahoo','apple'):
                inpoutofblue = colored("\n[*] ENTER NEW APP PASSWORD ",'green',attrs=['bold'])
                new_app = getpass(prompt=inpoutofblue)
            else:
                inpoutofblue2 = colored('\n[*] ENTER YOUR NEW PASSWORD ','green',attrs=['bold'])
                pwd = getpass(prompt=inpoutofblue2)
            if not new_app:
                fa[a][2] = encrypt(encrypt(pwd))
            else:
                fa[a][0] = encrypt(encrypt(new_app))
            f.write('\n[*] PASSWORD CHANGED FOR ACCOUNT '+mail)
            break
    file = open(mypath+'cred.log','w+')
    final = ''
    for a in fa:
        s = ''
        for b in a:
            s += b+'\n'
        final += s+'\n\n\n'
    file.write(final)


def change2(mypath):#change stored credentials for inbox


    try:
        while 1:
            file = open(mypath+'cred.log','r')
            f = open(mypath+'log.log','a+')
            entered = file.read()
            file.close()
            e=entered.split('\n\n\n')
            fa=[]
            for a in e:
                fa.append(a.split('\n'))
            fa.pop(-1)
            acc_select = '\n[*] SELECT YOUR ACCOUNT[PRESS CTRL+C TO GO TO MAIN MENU]\n'
            for a in range(len(fa)):
                acc_select+=str(a+1)+')'+decrypt(decrypt(fa[a][1]))+'\n'
            acc_select = colored(acc_select,'green',attrs=['bold'])
            while 1:
                try:
                    acc_choice=int(input(acc_select))
                except Exception as e:
                    pri22 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                    print(pri22)
                    continue
                if acc_choice > len(fa)+1:
                    pri23 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                    print(pri23)
                else:
                    break
            mail = decrypt(decrypt(fa[acc_choice-1][1]))
            for a in range(len(fa)):
                if decrypt(decrypt(fa[a][1])) == mail:
                    while 1:
                        try:
                            inp7 = colored('\n[*] ENTER YOUR NEW PASSWORD ','green',attrs=['bold'])
                            pwd = getpass(prompt=inp7)
                        except Exception as e:
                            pri24 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                            print(pri24)
                            continue
                        break
                    fa[a][2] = encrypt(encrypt(pwd))
                    file = open(mypath+'cred.log','w+')
                    final = ''
                    for a in fa:
                        s = ''
                        for b in a:
                            s += b+'\n'
                        final += s+'\n\n\n'
                    file.write(final)
                    f.write('\n[*] PASSWORD CHANGED FOR ACCOUNT '+mail)
                    break
            while 1:
                try:
                    inp8 = colored('\n[*] DO YOU WANT TO CHANGE PASSWORD FOR ANOTHER ACCOUNT?(Y/N) ','green',attrs=['bold'])
                    asd = input(inp8).upper()
                except Exception as e:
                    pri25 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                    print(pri25)
                    continue
                if asd in 'YN':
                    break
                else:
                    pri26 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                    print(pri26)
            if asd == 'N':
                pri27 = colored('\n[*] PLEASE RELAUNCH QUICK MAIL FOR THE CHANGES TO TAKE EFFECT ', 'red',attrs=['bold'])
                print(pri27)
                break
    except KeyboardInterrupt:
        print()


def face_id(cam):#face id for unlock


    pri28 = colored('\n[*] STARTING FACE RECOGNITION ENGINE ','green',attrs=['bold'])
    print(pri28)
    vid = cam
    known_faces = []
    known_faces.append(pickle.load(open('QuickMail/faces/1/f.pkz','rb')))
    c = 0
    while 1:
        r,image = vid.read()
        if r < 25:
            pri30 = colored('\n[*] PLEASE MOVE TO A WELL LIT PLACE AND TRY AGAIN','red',attrs=['bold'])
            print(pri30)
            continue
        locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, locations)
        try:
            results = face_recognition.compare_faces(known_faces, encodings[0], 10)
        except:
            continue
        c += 1
        if c == 20:
            vid.release()
            return 0
        if True in results:
            vid.release()
            return 1


def face(cap):#face id for setup


    while 1:
        _,face = cap.read()
        cv2.imshow('PRESS s TO START FACE ID', face)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            pri31 = colored('\n[*] PLEASE WAIT','green',attrs=['bold'])
            print(pri31)
            try:
                locations = face_recognition.face_locations(face)
                encodings = face_recognition.face_encodings(face, locations)
                f = open('QuickMail/faces/1/f.pkz','wb')
                pickle.dump(encodings[0], f)
                f.close()
                cap.release()
                return 1
            except Exception as e:
                pri32 = colored('\n[*] PLEASE TRY AGAIN','red',attrs=['bold'])
                print(pri32)


def pword(mail,check):#reset quick mail password


    try:
        security = ''
        if check:
            while 1:
                try:
                    inp9 = colored('\n[*] SELECT METHOD TO SECURE QUICK MAIL\n'+'1)FACE ID\n'+'2)PASSWORD\n','green',attrs=['bold'])
                    a = input(inp9)
                except:
                    pri33 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                    print(pri33)
                    continue
                if a not in '12':
                    pri34 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                    print(pri34)
                    continue
                else:
                    a = int(a)
                    if a == 1:
                        pri35 = colored('\n[*] STARTING FACE RECOGNITION ENGINE FOR FACE ID ','green',attrs=['bold'])
                        print(pri35)
                        if face(check[0]):
                            pri36 = colored('\n[*] FACE ID SET','green',attrs=['bold'])
                            print(pri36)
                            security = 'face|_/-\_|'
                            while 1:
                                inp10 = colored("\n[*] ENTER BACKUP PASSWORD FOR SERVICE ",'green',attrs=['bold'])
                                inp11 = colored("\n[*] RE-ENTER BACKUP PASSWORD ",'green',attrs=['bold'])
                                secure1 = getpass(prompt=inp10)
                                secure2 = getpass(prompt=inp11)
                                if secure1 ==  secure2:
                                    pri37 = colored('\n[*] PASSWORD SET','green',attrs=['bold'])
                                    print(pri37)
                                    break
                                else:
                                    pri38 = colored('\n[*] PASSWORDS DO NOT MATCH','red',attrs=['bold'])
                                    print(pri38)
                            security += secure1
                    if a == 2:
                        while 1:
                            inp10 = colored("\n[*] ENTER PASSWORD FOR SERVICE ",'green',attrs=['bold'])
                            inp11 = colored("\n[*] RE-ENTER PASSWORD ",'green',attrs=['bold'])
                            secure1 = getpass(prompt=inp10)
                            secure2 = getpass(prompt=inp11)
                            if secure1 ==  secure2:
                                pri39 = colored('\n[*] PASSWORD SET','green',attrs=['bold'])
                                print(pri39)
                                break
                            else:
                                pri40 = colored('\n[*] PASSWORDS DO NOT MATCH','red',attrs=['bold'])
                                print(pri40)
                        security = secure1
                    break
        else:
            while 1:
                if 1:
                    while 1:
                        try:
                            inp10 = colored("\n[*] ENTER PASSWORD FOR SERVICE ",'green',attrs=['bold'])
                            inp11 = colored("\n[*] RE-ENTER PASSWORD ",'green',attrs=['bold'])
                            secure1 = getpass(prompt=inp10)
                            secure2 = getpass(prompt=inp11)
                        except:
                            pri41 = colored('\n[*] INVALID PASSWORD','red',attrs=['bold'])
                            print(pri41)
                            continue
                        if secure1 ==  secure2:
                            pri42 = colored('\n[*] PASSWORD SET','green',attrs=['bold'])
                            print(pri42)
                            break
                        else:
                            pri43 = colored('\n[*] PASSWORDS DO NOT MATCH','red',attrs=['bold'])
                            print(pri43)
                    security = secure1
                break
        recovery = mail
        mypath = 'QuickMail'
        af = open(mypath+'/lock.log','w+')
        af.write(encrypt(encrypt(security))+'\n'+encrypt(encrypt(recovery)))
        af.close()
        f = open(mypath+'log.log','a+')
        f.write('\n[*] QUICK MAIL PASSWORD CHANGED AT ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        f.close()
    except KeyboardInterrupt:
        pri44 = colored('\n[*] YOU HAVE QUIT QUICK MAIL','red',attrs=['bold'])
        print(pri44)


def pic(cap):#take a pic using webcam


    f_name = r'QuickMail/faces/2/pic.jpg'
    while 1:
        if take_pic(cap,f_name):
            return f_name


def otp():#returns an otp to reset password


    OTP = ''.join([choice('ABCDEFGHIVWXY0123456789klmnopqrstvwxyz') for n in range(6)])
    return OTP


def reset(mail,cam):#send and receive otp to confirm password reset


    try:
        a = mail.split('@')
        pri45 = colored('\n[*] SENDING OTP TO '+mail[0]+'*'*(len(a[0])-2)+a[0][-1]+'@'+a[1],'green',attrs=['bold'])
        print(pri45)
        req_otp = otp()
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'CHANGE OF PASSWORD'
        msg['From'] = 'quick.mail.noreply@gmail.com'
        ab = 'CHANGE OF PASSWORD REQUESTED FROM YOUR QUICK MAIL APPLICATION. OTP: '+req_otp
        ac = MIMEText(ab, 'html')
        msg.attach(ac)
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login('quick.mail.noreply@gmail.com','anirudhnfs01')
        a = time()
        server.sendmail('quick.mail.noreply@gmail.com', mail, msg.as_string())
        server.quit()
        tries = 5
        while tries>0:
            try:
                inp12 = colored('\n[*] ENTER OTP SENT TO YOUR RECOVERY MAIL WITHIN 30 SECONDS ','green',attrs=['bold'])
                ad = input(inp12)
            except:
                pri46 = colored('\n[*] INVALID OTP','red',attrs=['bold'])
                print(pri46)
            if time()-a > 30:
                pri47 = colored('\n[*] TIME UP','red',attrs=['bold'])
                print(pri47)
                break
            if ad == req_otp:
                pword(mail,cam)
                break
            else:
                pri48 = colored('\n[*] INCORRECT OTP. TRIES LEFT: '+str(tries),'red',attrs=['bold'])
                print(pri48)
            tries -= 1
        if tries == 1:
            pri49 = colored('\n[*] OUT OF TRIES','red',attrs=['bold'])
            print(pri49)
    except KeyboardInterrupt:
        pri50 = colored('\n[*] YOU HAVE QUIT QUICK MAIL','red',attrs=['bold'])
        print(pri50)


def unlock(cam):#unlock quick mail


    try:
        while 1:
            re = open(r'QuickMail/lock.log').read()
            l=[]
            for a in re.split('\n'):
                l.append(decrypt(decrypt(a)))
            l[0] = l[0].split('|_/-\_|')
            if l[0][0] == 'face':
                if cam[0]:
                    return face_id(cam[0])
                else:
                    tries = 5
                    while tries > 0:
                        try:
                            inp13 = colored('\n[*] ENTER YOUR PASSWORD ','green',attrs=['bold'])
                            p = input(inp13)
                        except:
                            pri51 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                            print(pri51)
                            continue
                        if p == l[0][1]:
                            return 1
                        else:
                            pri52 = colored('\n[*] INCORRECT PASSWORD. TRIES LEFT: '+str(tries),'red',attrs=['bold'])
                            print(pri52)
                        tries -= 1
                    pri53 = colored('\n[*] OUT OF TRIES','red',attrs=['bold'])
                    print(pri53)
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = 'SNOOPER ALERT'
                    msg['From'] = 'quick.mail.noreply@gmail.com'
                    ab = 'PASSWORD ENTERED INCORRECTLY MORE THAN 6 TIMES IN YOUR QUICK MAIL AAPLICATION'
                    ac = MIMEText(ab, 'html')
                    msg.attach(ac)
                    server = smtplib.SMTP('smtp.gmail.com',587)
                    server.ehlo()
                    server.starttls()
                    server.login('quick.mail.noreply@gmail.com','anirudhnfs01')
                    server.sendmail('quick.mail.noreply@gmail.com', l[1], msg.as_string())
                    server.quit()
                    return 0
            else:                
                tries = 5
                while tries > 0:
                    try:
                        inp13 = colored('\n[*] ENTER YOUR PASSWORD ','green',attrs=['bold'])
                        p = getpass(prompt=inp13)
                    except Exception as e:
                        pri55 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                        print(pri55)
                        continue
                    if p == l[0][0]:
                        return 1
                    else:
                        pri56 = colored('\n[*] INCORRECT PASSWORD. TRIES LEFT: '+str(tries),'red',attrs=['bold'])
                        print(pri56)
                    tries -= 1
                pri57 = colored('\n[*] OUT OF TRIES','red',attrs=['bold'])
                print(pri57)
                msg = MIMEMultipart('alternative')
                msg['Subject'] = 'SNOOPER ALERT'
                msg['From'] = 'quick.mail.noreply@gmail.com'
                ab = 'PASSWORD ENTERED INCORRECTLY MORE THAN 6 TIMES IN YOUR QUICK MAIL AAPLICATION'
                ac = MIMEText(ab, 'html')
                msg.attach(ac)
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.ehlo()
                server.starttls()
                server.login('quick.mail.noreply@gmail.com','anirudhnfs01')
                if cam[0]:
                    file_ = open(pic(cam[0]),'rb')
                    attacher = MIMEBase('application','octet-stream')
                    attacher.set_payload((file_).read())
                    encoders.encode_base64(attacher)
                    attacher.add_header("Content-Disposition",'attachment; filename ="%s" '%'snooper.jpg')
                    msg.attach(attacher)
                server.sendmail('quick.mail.noreply@gmail.com', l[1], msg.as_string())
                server.quit()
                return 0
    except KeyboardInterrupt:
        reset(l[1],cam)


def body():#get the body of the mail


    key='''
[*] KEY FOR VOICE RECOGNITION [*]

(ACCURACY DEPENDS ON CLARITY OF DICTATION)

DOULE QUOTES     -> "
SINGLE QUOTES    -> '
FULLSTOP         -> .
SLASH            -> /
BACK SLASH       -> \
ASTERISK         -> *
HYPHEN           -> -
OPEN BRACKETS    -> (
CLOSE BRACKETS   -> )
SEMI-COLON       -> ;
COLON            -> :
UNDERSCORE       -> _
COMMA            -> ,
PERCENT          -> %
EXCLAMATION MARK -> !
HASHTAG          -> #
AT               -> @ (APPLICABLE FOR MAIL ID'S ONLY)
AMPERSAND        -> &
DOLLAR(S)        -> $
PLUS             -> +
EQUALS           -> =
NEW LINE         -> (TO ENTER A NEW LINE)
NEW PARAGRAPH    -> (TO START A NEW PARAGRAPH)
NUMBERS
LETTERS
    '''
    recog = speech.Recognizer()
    with speech.Microphone() as src:
        while 1:
            try:
                inp14 = colored('\n[*] DO YOU WANT TO SPEAK THE BODY OF YOUR MAIL?(Y/N) ','green',attrs=['bold'])
                a = input(inp14).upper()
            except:
                pri58 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                print(pri58)
                continue
            if a == 'Y':
                recog.adjust_for_ambient_noise(src)
                while 1:
                    try:
                        try:
                            inp15 = colored('\n[*] PRESS ENTER TO START SPEAKING ','green',attrs=['bold'])
                            input(inp15)
                        except:
                            pass
                        pri59 = colored('\n[*] TRANSCRIBING.....','green',attrs=['bold'])
                        print(pri59)
                        listen = recog.listen(src)
                        text = recog.recognize_google(listen)
                        break
                    except speech.UnknownValueError:
                        pri109 = colored("\n[*] SORRY DIDN'T GET YOU THERE ",'red',attrs=['bold'])
                        print(pri109)
                f = open(r'QuickMail/temp_mail.txt','w+')
                f.write(text)
                f.close()
                pri60 = colored('\n[*] EDIT YOUR BODY IN THE WINDOW WHICH WILL OPEN AND PRESS ENTER KEY AFTER MAKING AND SAVING YOUR DESIRED CHANGES ','red',attrs=['bold'])
                print(pri60)
                if os.name == "nt":
                    os.system(r'notepad.exe QuickMail/temp_mail.txt')
                else:
                    os.system(r'open QuickMail/temp_mail.txt')
                try:
                    input()
                except:
                    pass
                body = open(r'QuickMail/temp_mail.txt').read()
                open(r'QuickMail/temp_mail.txt','w+').close()
                return body
            elif a == 'N':
                inp16 = colored('\n[*] ENTER THE BODY OF YOUR MAIL IN THE WINDOW OPENING NOW AND PRESS ENTER ONCE DONE','green',attrs=['bold'])
                print(inp16)
                if os.name == "nt":
                    os.system(r'notepad.exe QuickMail/temp_mail.txt')
                else:
                    os.system(r'open QuickMail/temp_mail.txt')
                input()
                body = open('QuickMail/temp_mail.txt','r').read()
                open('QuickMail/temp_mail.txt','w+').close()
                return body
            else:
                pri62 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                print(pri62)
    return body


def add_address(email):#add an account to quick mail


    d={'gmail':('smtp.gmail.com',587),
       'outlook':('smtp.office365.com',587),
       'yahoo':('smtp.mail.yahoo.com',587),
       'icloud':('smtp.mail.me.com',587),
       'rediffmail':('smtp.rediffmailpro.com',587),
       'rediff':('smtp.rediffmail.com',25)}
    z = 1
    while z:
        try:
            mypath = 'QuickMail/'
            signer=''
            while 1:
                app_pwd = ''
                print('\n\n\n\n\n')
                pri63 = colored('!!!GRANT ACCESS TO THIRD PARTY APPS FROM YOUR SECURITY SETTINGS ON YOUR EMAIL ACCOUNT IF PRESENT!!!','red',attrs=['bold'])
                print(pri63)
                print('\n\n\n')
                provider = '[*] SELECT YOUR MAIL PROVIDER \n'
                c = 1
                for a in d:
                    provider += str(c)+')'+a.upper()+'\n'
                    c += 1
                provider = colored(provider,'green',attrs=['bold'])
                while 1:
                    try:
                        selected = int(input(provider))
                    except:
                        pri64 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                        print(pri64)
                        continue
                    if selected > c-1:
                        pri65 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                        print(pri65)
                    else:
                        break
                while 1:
                    try:
                        inp17 = colored("\n[*] ENTER YOUR EMAIL ADDRESS ",'green',attrs=['bold'])
                        from_address = str(input(inp17))
                    except:
                        pri66 = colored('\n[*] INVALID MAIL ID','red',attrs=['bold'])
                        print(pri66)
                        continue
                    break
                if 1:
                    inner = 1
                    for a in d:
                        if inner == selected:
                            smtp_server=d[a][0]
                            smtp_port=d[a][1]
                            while 1:
                                if a in ('icloud','yahoo'):
                                    while 1:
                                        try:
                                            inp18 = colored('\n[*] ENTER AN APP SPECIFIC PASSWORD TO SEND EMAILS ','green',attrs=['bold'])
                                            inp19 = colored('\n[*] ENTER YOUR PASSWORD TO VIEW YOUR EMAILS ','green',attrs=['bold'])
                                            app_pwd = getpass(prompt=inp18)
                                            password = getpass(prompt=inp19)
                                        except:
                                            pri67 = colored('\n[*] INVALID PASSWORD(S)','red',attrs=['bold'])
                                            print(pri67)
                                            continue
                                        break
                                else:
                                    while 1:
                                        try:
                                            inp20 = colored('\n[*] DO YOU WANT TO USE AN APP SPECIFIC PASSWORD?(Y/N) ','green',attrs=['bold'])
                                            abcd = input(inp20).upper()
                                        except:
                                            pri68 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                                            print(pri68)
                                            continue
                                        if abcd == 'N':
                                            while 1:
                                                try:
                                                    inp21 = colored('\n[*] ENTER YOUR PASSWORD TO VIEW YOUR EMAILS ','green',attrs=['bold'])
                                                    password = getpass(prompt=inp21)
                                                except:
                                                    pri69 = colored('\n[*] INVALID PASSWORD','red',attrs=['bold'])
                                                    print(pri69)
                                                    continue
                                                break
                                            break
                                        elif abcd == 'Y':
                                            while 1:
                                                try:
                                                    inp22 = colored('\n[*] ENTER AN APP SPECIFIC PASSWORD TO SEND EMAILS ','green',attrs=['bold'])
                                                    inp23 = colored('\n[*] ENTER YOUR PASSWORD TO VIEW YOUR EMAILS ','green',attrs=['bold'])
                                                    app_pwd = getpass(prompt=inp22)
                                                    password = getpass(prompt=inp23)
                                                except:
                                                    pri70 = colored('\n[*] INVALID PASSWORD(S)','red',attrs=['bold'])
                                                    print(pri70)
                                                    continue
                                                break
                                            break
                                        else:
                                            pri71 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                                            print(pri71)
                                try:
                                    server = smtplib.SMTP(smtp_server, smtp_port)
                                    server.ehlo()
                                    server.starttls()
                                    if app_pwd == '':
                                        server.login(from_address,password)
                                    else:
                                        server.login(from_address,app_pwd)
                                    server.quit()
                                    break
                                except Exception as e:
                                    pri72 = colored('\n[*] INVALID APP/ACCOUNT PASSWORD','red',attrs=['bold'])
                                    print(pri72,end='\n')
                                    pri73 = colored('\n!!!GRANT ACCESS TO THIRD PARTY APPS FROM YOUR SECURITY SETTINGS ON YOUR EMAIL ACCOUNT IF PRESENT!!!','red',attrs=['bold'])
                                    print(pri73)
                            break
                        inner += 1
                while 1:
                    try:
                        inp24 = colored('\n[*] WOULD YOU LIKE TO SIGN YOUR EMAILS?(Y/N) ','green',attrs=['bold'])
                        abcd1 = input(inp24).upper()
                    except:
                        pri74 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                        print(pri74)
                        continue
                    if abcd1 == 'Y':
                        while 1:
                            try:
                                inp25 = colored('\n[*] ENTER THE SIGNATURE WHICH YOU WANT TO INCLUDE OR ENTER THE FULL PATH TO A TEXT FILE CONTAINING YOUR SIGNATURE','green',attrs=['bold'])
                                signe = str(input(inp25))
                            except:
                                pri75 = colored('\n[*] INVALID PATH OR TEXT','red',attrs=['bold'])
                                print(pri75)
                                continue
                            break
                        try:
                            signer = open(signe).read()
                        except:
                            signer = signe
                        break
                    elif abcd1 == 'N':
                        signer = ''
                        break
                    else:
                        pri76 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                        print(pri76)
                file = open(mypath+'cred.log','a+')
                pword = encrypt(encrypt(password))
                if app_pwd:
                    app_pwd = encrypt(encrypt(app_pwd))
                file.write(app_pwd+'\n'+encrypt(encrypt(from_address))+'\n'+pword+'\n'+encrypt(encrypt(signer))+'\n'+encrypt(encrypt(smtp_server))+'\n'+encrypt(encrypt(str(smtp_port)))+'\n\n\n')
                file.flush()
                z = 0
                return
        except KeyboardInterrupt:
            pri77 = colored('\n[*] YOU HAVE QUIT QUICK MAIL','red',attrs=['bold'])
            print(pri77)


def val(list):#validate entered email using regex


    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    invalid = []
    for a in list:
        if not search(regex,a):
            pri78 = colored('\n[*] EMAIL ID '+a+' IS INVALID','red',attrs=['bold'])
            print(pri78)
            invalid.append(a)
    if invalid:
        return 0
    return 1


def main1():#sending mails

    try:
        counter = 0
        mypath = 'QuickMail/'
        if not os.path.isdir(mypath) or len(os.listdir(mypath)) == 0 or open(mypath+'cred.log','r').read() == '':
            setup()
        else:
            looper = 1
            while looper:
                acc_select='\n[*] SELECT YOUR ACCOUNT\n'
                file = open(mypath+'cred.log','r')
                f = open(mypath+'log.log','a+')
                entered = file.read()
                e=entered.split('\n\n\n')
                fa=[]
                for a in e:
                    fa.append(a.split('\n'))
                fa.pop(-1)
                for a in range(len(fa)):
                    acc_select+=str(a+1)+')'+decrypt(decrypt(fa[a][1]))+'\n'
                acc_select += str(len(fa)+1)+')'+'ADD AN ACCOUNT'+'\n'
                acc_select += str(len(fa)+2)+')'+'QUIT'+'\n'
                acc_select = colored(acc_select,'green',attrs=['bold'])
                while 1:
                    try:
                        acc_choice = int(input(acc_select))
                    except:
                        pri79 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                        print(pri79)
                        continue
                    if acc_choice > len(fa)+2:
                        pri80 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                        print(pri80)
                    else:
                        break
                if acc_choice == len(fa)+1:
                    add_address('')
                    continue
                elif acc_choice == len(fa)+2:
                    return 1
                if fa[acc_choice-1][0] != '':
                    password = decrypt(decrypt(fa[acc_choice-1][0]))
                else:
                    password = decrypt(decrypt(fa[acc_choice-1][2]))
                from_address=decrypt(decrypt(fa[acc_choice-1][1]))
                signer=decrypt(decrypt(fa[acc_choice-1][3]))
                smtp_server=decrypt(decrypt(fa[acc_choice-1][4]))
                smtp_port=decrypt(decrypt(fa[acc_choice-1][5]))
                try:
                    server = smtplib.SMTP(smtp_server,int(smtp_port))
                    server.ehlo()
                    server.starttls()
                    server.login(from_address,password)
                    server.quit()
                except:
                    change1(from_address,mypath)
                while 1:
                    try:
                        inp26 = colored("\n[*] ENTER RECIPIENT ADDRESS(SEPERATE WITH COMMAS IF MANY) OR ENTER THE FULL PATH TO A .csv FILE CONTAINING THE RECIPIENT ADDRESSES ",'green',attrs=['bold'])
                        to_address = str(input(inp26))
                    except:
                        pri81 = colored('\n[*] INVALID ADDRESS OR PATH','red',attrs=['bold'])
                        print(pri81)
                        continue
                    break
                if os.path.isfile(to_address):
                    to_a = open(to_address)
                    to_address = ''
                    for a in to_a.read().split('\n'):
                        to_address += a+','
                tolist=to_address.split(',')
                if not val(tolist):
                    return 1
                msg = MIMEMultipart('alternative')
                while 1:
                    try:
                        inp27 = colored("\n[*] ENTER SUBJECT ",'green',attrs=['bold'])
                        msg['Subject'] = str(input(inp27))
                    except:
                        pri82 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                        print(pri82)
                        continue
                    break
                msg['From'] = from_address
                while 1:
                    try:
                        inp28 = colored("\n[*] DO YOU WANT TO INCLUDE ATTACHMENTS(Y/N) ",'green',attrs=['bold'])
                        choice = str(input(inp28))
                    except:
                        pri83 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                        print(pri83)
                        continue
                    break
                z=1
                if choice.upper() == 'Y':
                    file_list = []
                    file_lists = []
                    file_sizes = 0
                    while 1:
                        try:
                            inp29 = colored("\n[*] ENTER THE LOCATION OF THE FILE OR DRAG AND DROP IT INTO THIS WINDOW ",'green',attrs=['bold'])
                            interim_name = str(input(inp29))
                            if interim_name[-1] == ' ':
                                interim_name = interim_name[:-1]
                            if os.name != "nt":
                                interim_name = parse(interim_name)
                            file_list.append(interim_name)
                        except EOFError:
                            pri84 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                            print(pri84)
                            continue
                        for a in range(len(file_list)):
                            try:
                                file_sizes += os.stat(file_list[a]).st_size / (1024*1024)
                                file_lists.append(file_list[a])
                            except FileNotFoundError:
                                pri85 = colored('\n[*] '+file_list[a]+' NOT FOUND ON COMPUTER', 'red',attrs=['bold'])
                                print(pri85)
                                break
                            except OSError:
                                pri110 = colored("\n[*] INCORRECT FILENAME OR FILEPATH "+file_list[a], 'red',attrs=['bold'])
                                print(pri110)
                                break
                        while 1:
                            try:
                                inp30 = colored('\n[*] WOULD YOU LIKE TO INCLUDE ANY OTHER ATTACHMENTS?(Y/N) ','green',attrs=['bold'])
                                temp = str(input(inp30)).upper()
                            except:
                                pri86 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                                print(pri86)
                                continue
                            if temp in 'YN':
                                break
                            else:
                                pri87 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                                print(pri87)
                        if temp == 'N':
                            break
                    for file_name in file_lists:
                        if file_sizes <= 25 and os.path.splitext(file_name)[1] not in ('.ade','.adp','.apk','.appx','.appxbundle','.bat','.cab','.chm','.cmd','.com','.cpl','.dll','.dmg','.exe','.hta','.ins','.isp','.iso','.jar','.js','.jse','.lib','.lnk','.mde','.msc','.msi','.msix','.msixbundle','.msp','.mst','.nsh','.pif','.ps1','.scr','.sct','.shb','.sys','.vb','.vbe','.vbs','.vxd','.wsc','.wsf','.wsh'):
                            pri88 = colored('\n[*] OPENING THE FILE '+os.path.splitext(file_name)[0]+os.path.splitext(file_name)[1], 'green',attrs=['bold'])
                            print(pri88)
                            counter = 0
                            file_ = open(file_name,'rb')
                            attacher = MIMEBase('application','octet-stream')
                            attacher.set_payload((file_).read())
                            encoders.encode_base64(attacher)
                            attacher.add_header("Content-Disposition",'attachment; filename ="%s" '%os.path.basename(file_name))
                            msg.attach(attacher)
                            pri89 = colored('\n[*] ATTACHING THE FILE ','green',attrs=['bold'])
                            print(pri89)
                            file_.close()
                            f.write('[*] INCLUDED ATTACHMENT '+file_name+'\n')
                        else:
                            pri90 = colored('\n[*] CHOSEN FILE(S) ARE LARGER THAN THE ALLOWED LIMIT BY YOUR SERVICE PROVIDER OR WILL BE BLOCKED BY YOUR EMAIL SERVICE PROVIDER. ATTACHING FILE(S) AS .zip FILE', 'red',attrs=['bold'])
                            print(pri90)
                            if 1:
                                pri91 = colored('\n[*] CREATING .zip FOLDER','green',attrs=['bold'])
                                print(pri91)
                                filezz = ''
                                for file_names in file_list:
                                    filezz += file_names
                                    os.mkdir(mypath+'/filestemp')
                                    copyfile(file_names,mypath+'/filestemp/'+os.path.splitext(file_name)[0]+os.path.splitext(file_name)[1])
                                make_archive(mypath+'/files','zip',mypath+'/filestemp')
                                file_namez = mypath+'/files.zip'
                                f.write('[*] CREATED ZIP FILE CONTAINING SELECTED FILES '+filezz+'\n')
                                if os.stat(file_namez).st_size / (1024*1024) <= 25:
                                    file_ = open(file_namez,'rb')
                                    attacher = MIMEBase('application','octet-stream')
                                    attacher.set_payload((file_).read())
                                    encoders.encode_base64(attacher)
                                    attacher.add_header("Content-Disposition",'attachment; filename ="%s" '%os.path.basename(file_namez))
                                    msg.attach(attacher)
                                    pri92 = colored('\n[*] ATTACHING THE .zip FILE','green',attrs=['bold'])
                                    print(pri92)
                                    file_.close()
                                    counter = 1
                                    f.write('[*] INCLUDED ATTACHMENT '+file_namez+'\n')
                                    break
                                else:
                                    pri93 = colored('\n[*] ZIP FILE LARGER THAN THE LIMIT PROVIDED BY YOUR SERVICE PROVIDER','red',attrs=['bold'])
                                    print(pri93)
                                    os.remove(file_namez)
                                    while 1:
                                        try:
                                            inp31 = colored('\n[*] DO YOU WANT TO SEND THE MAIL WITHOUT THE ATTACHMENT(S)?(Y/N) ','green',attrs=['bold'])
                                            temp = input(inp31).upper()
                                        except:
                                            pri94 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                                            print(pri94)
                                            continue
                                        if temp=='Y':
                                            z=0
                                            break
                                        elif temp == 'N':
                                            z = 1
                                            break
                                        else:
                                            pri95 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                                            print(pri95)
                                    if z == 0:
                                        break
                if z:
                    bodyof = body()
                    if not counter:
                        html = """\
                        """ + bodyof + '<br><br><br><i>' + signer +'</i>'
                    elif counter:
                        html = """\
                        """ + bodyof + '<br><br><b>PS: PLEASE UNZIP THE FOLDER TO VIEW THE FILES</b>'+'<br><br><br><i>' + signer + '</i>'
                    part1 = MIMEText(html, 'html')
                    msg.attach(part1)
                    try:
                        print('\n\n\n')
                        pri96 = colored('[*] STARTING THE SERVER','green',attrs=['bold'])
                        print(pri96)
                        server = smtplib.SMTP(smtp_server,int(smtp_port))
                        server.ehlo()
                        server.starttls()
                        server.login(from_address,password)
                        f.write('\n\n[*] LOGIN ATTEMPT AT '+ datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        pri97 = colored('\n[*] LOGGING IN','green',attrs=['bold'])
                        print(pri97)
                        pri98 = colored('\n[*] SENDING MAIL(S)','green',attrs=['bold'])
                        print(pri98)
                        print('\n\n')
                        for toadd in trange(len(tolist),bar_format="%s{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.GREEN,Fore.GREEN)):
                            toaddress = tolist[toadd]
                            msg['To'] = toaddress
                            server.sendmail(from_address, toaddress, msg.as_string())
                            f.write('\n[*] MAIL SENT ' + 'TO ' + toaddress + '\nAT ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        server.quit()
                        pri99 = colored('\n[*] MAIL(S) SENT','green',attrs=['bold'])
                        print(pri99)
                    except TimeoutError:
                        pri111 = colored("\n[*] COULD NOT CONNECT TO SERVER. TRY AGAIN SOMETIME LATER ",'red',attrs=['bold'])
                        print(pri111)
                        f.write('\n[*] CONNECTION TO SERVER FAILED AT '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        f.write('\n[*] SERVICE QUIT AT '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        f.close()
                        break
                    except:
                        pri112 = colored("\n[*] AN UNEXPECTED ERROR OCCURED WHILE SENDING YOUR EMAIL",'red',attrs=['bold'])
                        print(pri112)
                        f.write('\n[*] ERROR WHILE SENDING EMAIL AT '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        f.write('\n[*] SERVICE QUIT AT '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        f.close()
                        break
                    while 1:
                        inp34 = colored('\n[*] DO YOU WANT TO SEND ANOTHER MAIL?(Y/N) ','green',attrs=['bold'])
                        temp = input(inp34).upper()
                        if temp=='N':
                            pri100 = colored('\n[*] THANK YOU FOR USING QUICK MAIL :)','green',attrs=['bold'])
                            print(pri100)
                            f.write('\n[*] SERVICE QUIT AT '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                            f.close()
                            looper = 0
                            break
                        elif temp=='Y':
                            break
                        else:
                            pri101 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                            print(pri101)
    except KeyboardInterrupt:
        pri102 = colored('\n\n[*] YOU HAVE STOPPED QUICK MAIL','red',attrs=['bold'])
        print(pri102)
        try:
            inp33 = colored("[*] PRESS ENTER TO QUIT ",'red',attrs=['bold'])
            input(inp33)
        except:
            pass


def main2():#driver to open mailboxes


    try:
        counter = 0
        mypath = 'QuickMail/'
        if not os.path.isdir(mypath) or len(os.listdir(mypath)) == 0 or open(mypath+'cred.log','r').read() == '':
            setup()
        else:
            while 1:
                acc_select='\n[*] SELECT YOUR ACCOUNT [PRESS CTRL+C TO CHANGE YOUR STORED PASSWORDS]\n'
                file = open(mypath+'cred.log','r')
                f = open(mypath+'log.log','a+')
                entered = file.read()
                e=entered.split('\n\n\n')
                fa=[]
                for a in e:
                    fa.append(a.split('\n'))
                fa.pop(-1)
                for a in range(len(fa)):
                    acc_select+=str(a+1)+')'+decrypt(decrypt(fa[a][1]))+'\n'
                acc_select += str(len(fa)+1)+')'+'ADD AN ACCOUNT'+'\n'
                acc_select += str(len(fa)+2)+')'+'QUIT'+'\n'
                acc_select = colored(acc_select,'green',attrs=['bold'])
                while 1:
                    try:
                        acc_choice = int(input(acc_select))
                    except Exception as e:
                        pri103 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                        print(pri103)
                        continue
                    if acc_choice <= len(fa)+2:
                        break
                    else:
                        pri104 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                        print(pri104)
                if acc_choice == len(fa)+1:
                    add_address('')
                    continue
                elif acc_choice == len(fa)+2:
                    f.write('\n[*] SERVICE QUIT AT '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    return 1
                password = decrypt(decrypt(fa[acc_choice-1][2]))
                from_address=decrypt(decrypt(fa[acc_choice-1][1]))
                smtp_server=decrypt(decrypt(fa[acc_choice-1][4]))
                box = mailbox(user=from_address,pwd=password)
                try:
                    if 'yahoo' in smtp_server:
                        box.yahoo()
                    elif 'hotmail' in smtp_server or 'outlook' in smtp_server:
                        box.outlook()
                    elif 'mail.me' in smtp_server:
                        box.apple()
                    elif 'rediff' in smtp_server:
                        box.rediff()
                    else:
                        box.gmail()
                except Exception as e:
                    print(e)
                    if e != KeyboardInterrupt and e != TypeError:
                        f.write('\n[*] UNEXPECTED ERROR OCCURED WHILE ATTEMPTING TO LOGIN TO '+from_address+' AT '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        pri105 = colored('\n[*] UNEXPECTED ERROR OCCURED WHILE OPENING YOUR MAILING CLIENT. TRY AGAIN AFTER SOME TIME','red',attrs=['bold'])
                        print(pri105)
                f.close()
    except KeyboardInterrupt:
        change2('QuickMail/')


def encrypt_new(data):#encrypt data


    var1 = data.encode('utf-32')
    var2 = b64encode(var1)
    var3 = var2.hex()
    if var3 != data:
        return var3
    else:
        error_msg = '\n\n'+'[*] ERROR OCCURED WHILE ENCRYPTING USER CREDENTIALS'
        error_var = colored(error_msg,'white','on_red')
        return error_var


def decrypt_new(data):#decrypt data


    var1 = bytes.fromhex(data)
    var2 = b64decode(var1)
    var3 = var2.decode('utf-32')
    if var3 != data:
        return var3
    else:
        error_msg = '\n\n'+'[*] ERROR OCCURED WHILE DECRYPTING USER CREDENTIALS'
        error_var = colored(error_msg,'white','on_red')
        return error_var


def parse_new(data):#parse data


    var1 = data.split('\ ')
    var2 = ' '.join(var1)
    check1 = 0
    for a in var1:
        for b in var2:
            if a != b:
                check1 += 1
                continue
            else:
                break
    var3 = var2.split('\~')
    var4 = '~'.join(var3)
    check2 = 0
    for a in var1:
        for b in var2:
            if a != b:
                check2 += 1
                continue
            else:
                break
    if check1 == 0:
        if check2 == 0:
            return var4
    else:
        if check1 > 0:
            if check2 > 0:
                error_msg = '\n\n'+'[*] ERROR OCCURED WHILE PARSING DATA'
                error_var = colored(error_msg,'white','on_red')
                return error_var


def main():#driver function


    try:
        print(colored('''


       ____  _    _ _____ _____ _  ____  __          _____ _
      / __ \| |  | |_   _/ ____| |/ /  \/  |   /\   |_   _| |
     | |  | | |  | | | || |    | ' /| \  / |  /  \    | | | |
     | |  | | |  | | | || |    |  < | |\/| | / /\ \   | | | |
     | |__| | |__| |_| || |____| . \| |  | |/ ____ \ _| |_| |____
      \___\_\\\____/|_____\_____|_|\_\_|  |_/_/    \_\_____|______|

        A COMPUTER SCIENCE PROJECT BY V. ANIRUDH AND NISHANT OF CLASS 12 E


        ''', 'green', attrs=['bold']))#fancy ascii art
        try:
            if not open(r'QuickMail/lock.log').read():#check if initial setup is complete
                setup()#open initial setup
        except:
            setup()
        check = cam_check()#check for presence of webcam
        if not check:
            check = [0]
        if unlock(check):#unlock quick mail
            mypath = 'QuickMail/'
            f = open(mypath+'log.log','a+')
            f.write('\n[*] QUICK MAIL UNLOCKED AT ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            f.close()
            #unlocked(check)#send a picture of unlocker to backup email
            while 1:
                choices = colored('\n[*] SELECT YOUR CHOICE[PRESS CTRL+C TO QUIT]\n'+'1)SEND A MAIL\n'+'2)OPEN MAILBOX\n3)QUIT\n','green',attrs=['bold'])
                try:
                    ab = int(input(choices))
                except Exception as e:
                    pri106 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                    print(pri106)
                    continue
                if ab not in (1,2,3):
                    pri107 = colored('\n[*] INVALID CHOICE', 'red',attrs=['bold'])
                    print(pri107)
                else:
                    if ab == 1:
                        if main1():#sending mails
                            continue
                    elif ab == 2:
                        if main2():#opening inbox
                            continue
                    else:
                        pri108 = colored('\n[*] THANK YOU FOR USING QUICK MAIL :)','green',attrs=['bold'])
                        print(pri108)
                        return
        else:
            pri2 = colored('\n[*] ACCESS DENIED','red',attrs=['bold'])
            print(pri2)
    except KeyboardInterrupt:
        pri1 = colored('\n[*] YOU HAVE QUIT QUICK MAIL','red',attrs=['bold'])
        print(pri1)


if __name__ == '__main__':

    main()
    cv2.destroyAllWindows()
