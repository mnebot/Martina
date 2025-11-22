#!/usr/bin/env python3

#Licensed under the MIT 

#Autor: Marçal Nebot - https://github.com/mnebot/Martina 

#Utilitza el projecte AIY de Google	 per a donar ordres a la Martina en català https://aiyprojects.withgoogle.com

#Utilitza el sintetitzador de veu Festival i la veu Ona de Festcat http://festcat.talp.cat/

#Es comunica amb el robot mitjançant les llibreries de robotical.io martypy https://robotical.io/

#També es comunica amb altres coses com llums o la tele, fa fotos, envia correus ... https://trello.com/b/3mHrU0Km

# reconeix objectes i persones utilitzant la llibreria cv2 i face_recognition
   
#"""


import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import cv2
import datetime
import decimal
import face_recognition
import json
import martypy
import math
import numpy as np
import os
import picamera
import requests
import smtplib
import yaml
from pathlib import Path


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from martypy import Marty
from PIL import Image
from pylgtv import WebOsClient


class Martina:

    # Load configuration file if present
    def _load_config(self, path='config.yml'):
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return yaml.safe_load(f) or {}
            elif os.path.exists('config.example.yml'):
                with open('config.example.yml', 'r') as f:
                    return yaml.safe_load(f) or {}
        except Exception as e:
            print('Error carregant configuració:', e)
        return {}
              
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
        elif 'hola' in accio:
            self.reconeixPersona(accio)
        elif 'recita' in accio:
            self.recita()
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
            quit()
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
##           imatge = Image.open(nomImatge)
 #          imatgeInvertida = imatge.rotate(180)
  #         nomImatge = 'imatge_' + str(datetime.datetime.now()) + '_rotate.jpg'
   #        imatgeInvertida.save('/home/pi/' + nomImatge)
                    
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

    def recita(self):
        print("Entra a recita")
        try:
           self.mymarty.eyes(20,500)
           self.mymarty.arms(0,127,200) #puja el braç dret a 90 graus amb mig segon
                       
           os.system(" echo 'QUAN SOMRIUS de Josep Tio' | festival --language catalan --tts")
           os.system(" echo 'Es Nadal al meu cor, quan somrius content de veurem, quan quan la nit es fa més pres, t abraces al meu cos.' | festival --language catalan --tts")
           os.system(" echo 'I les llums de colors, m il·luminen nit i dia, les encens amb el somriure, quan em partes amb el cor.' | festival --language catalan --tts")
            
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
           
    # Si reconeix l'objectte s'hi acosta i el xuta
    def xutaObjecte(self, accio):
        
        # identifica objecte a xutar (cotxe o pilota)
        objecte = "cotxe";
        if('pilota' in accio):
            objecte = "pilota"
            
        # Detecta l'objecte
        
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
                    break
                
        # Realitza tracking de l'objecte
        # mentre s'hi acosta mira si ja pot xutar
        # xuta
        #self.mymarty.kick('right')


    # Si reconeix la persona li diu hola i el nom
    def reconeixPersona(self, accio):
        print("Entra a Hola (reconeix persona)")
        try:        
            
            # Initialize some variables
            face_locations = []
            face_encodings = []
            output = np.empty((240, 320, 3), dtype=np.uint8)

            print("Capturing image.")
            self.camera.capture(output, format="rgb")

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(output)
            print("Found {} faces in image.".format(len(face_locations)))
            face_encodings = face_recognition.face_encodings(output, face_locations)
            print(face_encodings)

            hatrobatalgu = False
            # Loop over each face found in the frame to see if it's someone we know.
            print("Per a cada cara trobada mira si hi reconeix algú")
            for face_encoding in face_encodings:
                print(face_encoding)
                
                # See if the face is a match for the known face(s)
                matchmarcal = face_recognition.compare_faces([self.marcal_face_encoding], face_encoding)
                matcharnau = face_recognition.compare_faces([self.arnau_face_encoding], face_encoding)
                matchmariona = face_recognition.compare_faces([self.mariona_face_encoding], face_encoding)
                matchmontse = face_recognition.compare_faces([self.montse_face_encoding], face_encoding)
                if matchmarcal[0]:
                    print("He trobat la cara del Marçal")
                    os.system(" echo 'Hola Marsal!' | festival --language catalan --tts")
                    hatrobatalgu = True
                if matcharnau[0]:
                    print("He trobat la cara de l'Arnau")
                    os.system(" echo 'Hola Arnau!' | festival --language catalan --tts")
                    hatrobatalgu = True
                if matchmariona[0]:
                    print("He trobat la cara de la Mariona")
                    os.system(" echo 'Hola Mariona!' | festival --language catalan --tts")
                    hatrobatalgu = True
                if matchmontse[0]:
                    print("He trobat la cara de la Montse")
                    os.system(" echo 'Hola Montse!' | festival --language catalan --tts")
                    hatrobatalgu = True

            if hatrobatalgu is False:
                print("No he reconegut cap cara")
                os.system(" echo 'Qui ha dit hola?' | festival --language catalan --tts")
                    
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
        # Read SMTP configuration from config (or env var for password)
        smtp_cfg = self.config.get('smtp', {}) if hasattr(self, 'config') else {}
        fromaddr = smtp_cfg.get('user', 'martina3794@gmail.com')
        smtp_host = smtp_cfg.get('host', 'smtp.gmail.com')
        smtp_port = smtp_cfg.get('port', 587)
        smtp_password = os.environ.get('SMTP_PASSWORD') or smtp_cfg.get('password')

        toaddr = to

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = assumpte

        body = missatge
        msg.attach(MIMEText(body, 'plain'))

        filename = fitxer
        try:
            with open(filename, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={Path(filename).name}")
            msg.attach(part)

            print("Envia foto: abans de crear el servidor")
            server = smtplib.SMTP(smtp_host, smtp_port)
            print("Envia foto: servidor creat i connectat")
            server.starttls()
            print("Envia foto: tls configurat")
            if smtp_password:
                server.login(fromaddr, smtp_password)
                print("Envia foto: loggejat")
            else:
                print("Envia foto: No SMTP password configured; attempting send without auth")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            print("Envia foto: mail enviat")
        finally:
            try:
                server.quit()
            except Exception:
                pass
           
           
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
        self.recognizer.expect_phrase('hola')
        self.recognizer.expect_phrase('recita')

        # Inicialitza el gravador de veu per a què el reconeixedor pugi començar a
        # reconèixer comandes de veu
        aiy.audio.get_recorder().start()
        print('Reconeixedor de veu inicialitzat')

    def inicialitzaHue(self):
        hue_cfg = self.config.get('hue', {}) if hasattr(self, 'config') else {}
        ipHue = hue_cfg.get('ip', '192.168.0.10')
        nomUsuari = hue_cfg.get('user', 'juCDLs2nNnys46uLoWngh26Vt4v6dm8DpS03CJ0g')
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


    def inicialitzaCares(self):
            # Carregant cares conegudes (això s'hauria de posar a l'inici)
            marcal_image = face_recognition.load_image_file("/home/pi/AIY-projects-python/src/imatges/marcal.jpg")
            arnau_image = face_recognition.load_image_file("/home/pi/AIY-projects-python/src/imatges/arnau.jpg")
            mariona_image = face_recognition.load_image_file("/home/pi/AIY-projects-python/src/imatges/mariona.jpg")
            montse_image = face_recognition.load_image_file("/home/pi/AIY-projects-python/src/imatges/montse.jpg")
            self.marcal_face_encoding = face_recognition.face_encodings(marcal_image)[0]
            self.arnau_face_encoding = face_recognition.face_encodings(arnau_image)[0]
            self.mariona_face_encoding = face_recognition.face_encodings(mariona_image)[0]
            self.montse_face_encoding = face_recognition.face_encodings(montse_image)[0]
            print('Cares inicialitzades')
       
    # Inicialitza la Martina: el reconeixedor de veu, el Marty the robot, la càmera, etc ...
    def __init__(self):
        # Load configuration
        self.config = self._load_config()

        # inicialitza el reconeixedor de veu i comença a escoltar
        aiy.i18n.set_language_code('ca-ES')
        self.recognizer = aiy.cloudspeech.get_recognizer()
        self.inicialitzaRecognizer()
        
        # inicialitza robot
        self.initResetMarty()
        
        # inicialitza la càmera
        self.camera = picamera.PiCamera()
        # redueix la resolució
        self.camera.resolution = (320, 240)
        print('Càmera inicialitzada')
        
        # inicialitza llums
        self.inicialitzaHue()
        
        # inicialitza la tele LG
        tv_ip = self.config.get('tv', {}).get('ip', '192.168.0.16')
        self.webos_client = WebOsClient(tv_ip)
        print('TV inicialitzada')
        
        # inicialitza model per a reconèixer objectes
        self.inicialitzaModelImatges()

        # inicialitza cares conegudes
        self.inicialitzaCares()

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
