#!/usr/bin/env python3

#Licensed under the MIT 

#Autor: Marçal Nebot - https://github.com/mnebot/Martina 

#Utilitza el projecte AIY de Google	 per a donar ordres a la Martina en català https://aiyprojects.withgoogle.com

#Utilitza el sintetitzador de veu Festival i la veu Ona de Festcat http://festcat.talp.cat/

#Es comunica amb el robot mitjançant les llibreries de robotical.io martypy https://robotical.io/

#També es comunica amb altres coses com llums o la tele, fa fotos, envia correus ... https://trello.com/b/3mHrU0Km
   
#"""


import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import cv2
import datetime
import decimal
import json
import martypy
import math
import os
import picamera
import requests
import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from martypy import Marty
from PIL import Image
from pylgtv import WebOsClient


class Martina:
              
    # Identifica i executa l'acció
    def executaAccio(self,accio):
        print('Has dit "', accio, '"')
        if 'fes una foto' in accio:
            self.foto()
        elif 'camina' in accio:
            self.camina(accio)
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
        elif 'obre la tele' in accio:
            self.obreTV()
        elif 'tanca la tele' in accio:
            self.tancaTV()
        elif 'netflix' in accio:
            self.netflix()
        elif 'posa dibuixos' in accio:
            self.dibuixos()
        elif 'adéu' in accio:
            self.adeu()
        elif 'xuta' in accio:
            self.xutaObjecte(accio)
        else:
            print('Acció no identificada')



    # ACCIONS
    
    def dibuixos(self):
        try:
            print(self.webos_client.get_channels())
            self.webos_client.set_channel(4)
        except Exception as e:
            print("Unexpected error posant dibuixos")
  
    def netflix(self):
        try:
            self.webos_client.launch_app('netflix')

        except Exception as e:
            print("Unexpected error obrint netflix: ", str(e))
        
    def obreTV(self):
        try:
            self.webos_client.request("system/turnOn")

        except Exception as e:
            print("Unexpected error obre TV: ", str(e))

    
    
    def tancaTV(self):
        try:
            self.webos_client.power_off()

        except Exception as e:
            print("Unexpected error tancant TV: ", str(e))
        

    def adeu(self):
        print("Entra a adéu")
        try:    
            os.system(" echo 'Fins aviat!' | festival --language catalan --tts")
            self.mymarty.hello()
        except Exception as e:
           print("Unexpected error dient Adéu: ", str(e))
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
           
           

        
    def camina(self,accio):
        
        # per defecte camina endavant 10 centímetres
        centimetres = 10
        llargadaPassos = 45 # en milímetres teoricament a l'api de martypi
        correccioPassos = .35 # basat amb proves realitzades
        nombrePassos = 1
        direccio = 1
        gir = 0 
        
        try:
            if 'enrere' in accio:
                direccio = -1
                
            llargadaPassosReal = decimal.Decimal(llargadaPassos) * decimal.Decimal(correccioPassos)
            nombrePassos =  self.calculaPassos(accio,llargadaPassosReal)
            
            logngitudPassos = int(direccio * llargadaPassosReal)

            self.mymarty.walk(num_steps=nombrePassos,
                              start_foot='auto',
                              turn=gir,
                              step_length=logngitudPassos,
                              move_time=1200)
            
            # al final es posa recte
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
    
    # calcula el nombre de passos en funció del centímtres que li diuen
    # i la llargada del passos (en milimetres)
    def calculaPassos(self,accio,llargadaPassos):
        
        passos = 0
        
        centimetres =  [int(s) for s in accio.split() if s.isdigit()]
                
        if len(centimetres) == 0:
            centimetres = [10]
        
        passos = math.floor(decimal.Decimal(centimetres[0]) / (llargadaPassos / decimal.Decimal(10)))
        
        print(passos)
                
        return passos
    
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
        
    # Si reconeix l'objectte s'hi acosta i el xuta
    def xutaObjecte(self, accio):
        
        # identifica objecte a xutar (cotxe o pilota)
        objecte = "cotxe";
        if('pilota' in accio):
            objecte = "pilota"
            
        # Realitza intents fins que pot xutar l'objecte (un màxim de 7 vegades)
        maxim = 7
        intents = 0
        
        # caputura imatge i cerca objectes
        # reconèixer objectes
        nomImatge = '/home/pi/image_' + str(datetime.datetime.now()) + '.jpg'
        self.camera.capture(nomImatge)
        image = cv2.imread(nomImatge)

        # inicia intent
        # estic prou aprop? sí -> xuta ; no -> acostat
        image_height, image_width, _ = image.shape

        self.model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
        output = self.model.forward()


        for detection in output[0, 0, :, :]:
            confidence = detection[2]
            if confidence > .5:
                class_id = detection[1]
                class_name = self.id_class_name(class_id)
                if(objecte == class_name):
                    print(str(str(class_id) + " " + str(detection[2])  + " " + class_name))
                    box_x = detection[3] * image_width
                    box_y = detection[4] * image_height
                    box_width = detection[5] * image_width
                    box_height = detection[6] * image_height
                    cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)
                    cv2.putText(image,class_name ,(int(box_x), int(box_y+.05*image_height)),cv2.FONT_HERSHEY_SIMPLEX,(.005*image_width),(0, 0, 255))
                    cv2.imshow('image', image)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
        # si existeix s'hi acosta
        # xuta
        #self.mymarty.kick('right')
        
        
           
           
    # MÈTODES INICIALITZADORS

    # Inicialitza el Marty: realitza la connexió via socket y fes que es posi dret
    def initResetMarty(self):
        marty = martypy.SocketClient.discover(timeout=10)[0]
        ipmarty = str(marty)[3:15]
        self.mymarty = Marty('socket://' + ipmarty)
        self.mymarty.hello()  # Move to zero positions and wink True
        print('Marty inicialitzat')

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
        self.recognizer.expect_phrase('obre la tele')
        self.recognizer.expect_phrase('tanca la tele')
        self.recognizer.expect_phrase('netflix')
        self.recognizer.expect_phrase('posa dibuixos')
        self.recognizer.expect_phrase('adéu')
        self.recognizer.expect_phrase('xuta la pilota')
        self.recognizer.expect_phrase('xuta el cotxe')

        # Inicialitza el gravador de veu per a què el reconeixedor pugi començar a
        # reconèixer comandes de veu
        aiy.audio.get_recorder().start()
        print('Reconeixedor de veu inicialitzat')

    def inicialitzaHue(self):
        ipHue = '192.168.0.10'
        nomUsuari = 'juCDLs2nNnys46uLoWngh26Vt4v6dm8DpS03CJ0g'
        self.urlLamparaLavabo = 'http://' + ipHue + '/api/' + nomUsuari + '/lights/3/state'
        print('Hue inicialitzat')
        
    # Pretrained classes in the model
    classNames = {0: 'background',
              1: 'person', 2: 'bicycle', 3: 'cotxe', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
              37: 'pilota', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}


    def id_class_name(self,class_id):
        for key, value in self.classNames.items():
            if class_id == key:
                return value
            
    def inicialitzaModelImatges(self):
        # Loading model
        self.model = cv2.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                      'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')
        print('Model inicialitzat')
        
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
        print('Càmera inicialitzada')
        
        # inicialitza llums
        self.inicialitzaHue()
        
        # inicialitza la tele LG
        self.webos_client = WebOsClient('192.168.0.16')
        print('TV inicialitzada')
        
        # inicialitza model per a reconèixer objectes
        self.inicialitzaModelImatges()

        #Saluda
        print('Martina inicialitzada')
        os.system(" echo 'Hola ja estic llesta!' | festival --language catalan --tts")
                

# Acció principal, identifica i executa ordres fins que li dius adéu a partir
# d'una paraula disparadora que és "Martina".
#
# Li pots dir:
#    - Martina [balla, fes una foto, guapa, camina, Adéu, etc ]
#

#Crea una instància de Martina
martina = Martina()

# Escolta i quan es digui "Matina [acció]" executa l'acció, i així anar fent
while True:
    # Escolta i reconeix a text el que s'escolta després de dir "Martina"        
    martina.executaAccio(martina.recognize())
