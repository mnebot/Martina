#!/usr/bin/env python3

#Licensed under the MIT 

#Autor: Marçal Nebot - https://github.com/mnebot/Martina 

#Utilitza el projecte AIY de Google	 per a donar ordres a 
#la Martina en català.

#Utilitza el sintetitzador de veu Festival i la veu Ona de Fescat.

#Es comunica amb el robot mitjançant les llibreries de robotical.io martypy
   
#"""


import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import datetime
import json
import martypy
import os
import picamera
import requests
import smtplib

from email.mime.multipart import MIMEMultipart
#from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from martypy import Marty
from PIL import Image


class Martina:
              
    # Identifica i executa l'acció
    def executaAccio(self,accio):
        print('Has dit "', accio, '"')
        if 'fes una foto' in accio:
            self.foto()
        elif 'camina' in accio:
            self.camina()
        elif 'balla' in accio:
            self.balla()
        elif 'guapa' in accio:
            self.guapa()
        elif 'agafa les claus' in accio:
            self.agafaClaus()
        elif 'obre la llum' in accio:
            self.obreLlum()
        elif 'tanca la llum' in accio:
            self.tancaLlum()            
        elif 'adéu' in accio:
            self.adeu()
        else:
            print('Acció no identificada')



    # ACCIONS

    def adeu(self):
        print("Entra a adéu")
        try:    
            os.system(" echo 'Fins aviat!' | festival --language catalan --tts")
            self.mymarty.hello()
        except Exception as e:
           print("Unexpected error: ", str(e))
           self.initResetMarty()
        
    def agafaClaus(self):
        print("Entra a agafa les claus")
        try:
            self.mymarty.arms(0,127,200) #puja el braç dret a 90 graus amb mig segon
        except Exception as e:
           print("Unexpected error: ", str(e))
           self.initResetMarty()
           
    def deixaClaus(self):
        print("Entra a deixa les claus")
        try:
            self.mymarty.arms(0,0,100) #baixa els braços en 1 sengo
        except Exception as e:
           print("Unexpected error: ", str(e))
           self.initResetMarty()
           
    def foto(self):
        print("Entra a foto")
        try:
           # diu Lluís
           os.system(" echo 'Lluiiiiiiiiiis' | festival --language catalan --tts")
           
           # mou els ulls per a indicar que fa la foto i fa la foto
           self.mymarty.eyes(60,move_time=500)
           nomImatge = '/home/pi/image_' + str(datetime.datetime.now()) + '.jpg'
           self.camera.capture(nomImatge)
           self.mymarty.eyes(20,move_time=500)
           
           # transforma la foto
           imatge = Image.open(nomImatge)
           imatgeInvertida = imatge.rotate(180)
           nomImatge = 'imatge_' + str(datetime.datetime.now()) + '_rotate.jpg'
           imatgeInvertida.save('/home/pi/' + nomImatge)
           
           # Envia la foto per correu
           self.enviaCorreu('mnebot@gmail.com',
                            'Foto de la Martina',
                            'La Martina t''envia aquesta foto!',
                            nomImatge)
           # es posa recte
           self.mymarty.hello()
        except Exception as e:
           print("Unexpected error: ", str(e))
           self.initResetMarty()
           
           
        
        
    def camina(self):
        print("Entra a camina")
        try:
            self.mymarty.walk(num_steps=3, start_foot='auto', turn=20, step_length=40, move_time=1600)
            self.mymarty.hello()
        except Exception as e:
            print("Unexpected error: ", str(e))
            self.initResetMarty()

    def balla(self):
        print("Entra a balla")
        try:
           self.mymarty.circle_dance(side='right',move_time=5000)
           self.mymarty.hello()
        except Exception as e:
           print("Unexpected error: ", str(e))
           self.initResetMarty()
            
    def guapa(self):
        print("Entra a guapa")
        try:
           self.mymarty.eyes(20,500)
           self.mymarty.lean('left', 50, 2000)
                       
           os.system(" echo 'Ai quina vergonya' | festival --language catalan --tts")
            
           self.mymarty.hello()
        except Exception as e:
           print("Unexpected error: ", str(e))
           self.initResetMarty()
           
    def obreLlum(self):
        print("Entra a obre la llum")
        try:
            data_on = {"on":True, "sat":254, "bri":254,"hue":5000}
            r = requests.put(self.urlLamparaLavabo, json.dumps(data_on), timeout=5)
        except Exception as e:
           print("Unexpected error: ", str(e))
           self.initResetMarty()

    def tancaLlum(self):
        print("Entra a tanca la llum")
        try:
            data_off = {"on":False}
            r = requests.put(self.urlLamparaLavabo, json.dumps(data_off), timeout=5)
        except Exception as e:
           print("Unexpected error: ", str(e))
           self.initResetMarty()

    # MÈTODES ACCESSORIS
  
    # Reconeix el que dius 
    def recognize(self):
        return self.recognizer.recognize()
    
    # Envia un correu amb un document adjunt
    def enviaCorreu(self, to, assumpte, missatge, fitxer):
        
        fromaddr = "martina3794@gmail.com"
        toaddr = to
         
        msg = MIMEMultipart()
         
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = assumpte
         
        body = missatge
         
        msg.attach(MIMEText(body, 'plain'))
         
        filename = fitxer
        attachment = open("/home/pi/"+filename, "rb")
         
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
         
        msg.attach(part)
         
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "Martina37$")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
           
           
    # MÈTODES INICIALITZADORS

    # Inicialitza el Marty: realitza la connexió via socket y fes que es posi dret
    def initResetMarty(self):
        marty = martypy.SocketClient.discover(timeout=10)[0]
        ipmarty = str(marty)[3:15]
        self.mymarty = Marty('socket://' + ipmarty)
        self.mymarty.hello()  # Move to zero positions and wink True

    # Defineix l'activador (hotword) com a Martina conegui
    def inicialitzaRecognizer(self):
        # Defineix activador
        self.recognizer.expect_hotword('Martina')

        # Defineix les accions 
        self.recognizer.expect_phrase('fes una foto')
        self.recognizer.expect_phrase('camina')
        self.recognizer.expect_phrase('balla')
        self.recognizer.expect_phrase('guapa')
        self.recognizer.expect_phrase('agafa les claus')
        self.recognizer.expect_phrase('obre la llum')
        self.recognizer.expect_phrase('tanca la llum')
        self.recognizer.expect_phrase('adéu')

        # Inicialitza el gravador de veu per a què el reconeixedor pugi començar a
        # reconèixer comandes de veu
        aiy.audio.get_recorder().start()


    def inicialitzaHue(self):
        ipHue = '192.168.0.10'
        nomUsuari = 'juCDLs2nNnys46uLoWngh26Vt4v6dm8DpS03CJ0g'
        self.urlLamparaLavabo = 'http://' + ipHue + '/api/' + nomUsuari + '/lights/3/state'
        
    # Inicialitza la Martina: el reconeixedor de veu, el Marty the robot, la càmera, etc ...
    def __init__(self):
        
        # inicialitza el reconeixedor de veu i comença a escoltar
        aiy.i18n.set_language_code('ca-ES')
        self.recognizer = aiy.cloudspeech.get_recognizer()
        self.inicialitzaRecognizer()
        
        # inicialitza robot
        self.initResetMarty()
        
        # inicialitza la càmera
        self.camera = picamera.PiCamera()
        
        # inicialitza llums
        self.inicialitzaHue()

        #Saluda
        os.system(" echo 'Hola ja estic llesta!' | festival --language catalan --tts")
                

# Acció principal, identifica i executa ordres fins que li dius adéu a partir
# d'una paraula disparadora que és "Martina".
#
# Li pots dir:
#    - Martina [balla, fes una foto, guapa, camina, Adéu]
#

#Crea una instància de Martina
martina = Martina()

# Escolta i quan es digui "Matina [acció]" executa l'acció, i així anar fent
while True:
    # Escolta i reconeix a text el que s'escolta després de dir "Martina"        
    martina.executaAccio(martina.recognize())
