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
import os
import picamera

from martypy import Marty

#os.system(" echo 'text a parlar' | festival --language catalan --tts")
def main():
    
    # inicialitza el reconeixedor de veu i comença a escoltar
    aiy.i18n.set_language_code('ca-ES')
    recognizer = aiy.cloudspeech.get_recognizer()
    inicialitzaRecognizer(recognizer)
    
    # inicialitza robot
    mymarty = Marty('socket://192.168.0.20') # Change IP accordingly
    mymarty.hello()  # Move to zero positions and wink True
    
    
    camera = picamera.PiCamera()

    #Saluda
    os.system(" echo 'Hola ja estic llesta!' | festival --language catalan --tts")
    
    # Mentre no escolti adéu processa el què escolta
    while True:

        # Escolta i reconeix a text el que s'escolta després de dir "Martina"        
        print('Escoltant-te...')
        text = recognizer.recognize()
        
        # si no escolta res, mostra el missatge pertinent
        # si reconeix, mostra el què s'ha dit
        # si reconeix una acció, l'executa
        if not text:
            print ('no sento res')
        else:
            
            print('Has dit "', text, '"')
            
            if 'fes una foto' in text:
                foto(camera,mymarty)
            elif 'camina' in text:
                camina(mymarty)
            elif 'balla' in text:
                balla(mymarty)
            elif 'guapa' in text:
                guapa(mymarty)
            elif 'adéu' in text:
                print('Adéu')
                os.system(" echo 'Fins aviat!' | festival --language catalan --tts")
                break
            



def inicialitzaRecognizer(recognizer):
    
    recognizer.expect_hotword('Martina')
    
    recognizer.expect_phrase('fes una foto')
    recognizer.expect_phrase('camina')
    recognizer.expect_phrase('balla')
    recognizer.expect_phrase('guapa')
    recognizer.expect_phrase('Adéu')
    
    aiy.audio.get_recorder().start()


def foto(camera,mymarty):
    print("Entra a foto")
    try:
       os.system(" echo 'Lluiiiiiiiiiis' | festival --language catalan --tts")
       mymarty.eyes(60,move_time=500)
       camera.capture('/home/pi/image.jpg')
       mymarty.eyes(20,move_time=500)

    except Exception as e:
       print("Unexpected error: ", str(e))
        
    
def camina(mymarty):
    print("Entra a camina")
    try:
         mymarty.walk(num_steps=2, start_foot='auto', turn=20, step_length=30, move_time=2000)
    except Exception as e:
       print("Unexpected error: ", str(e))


def balla(mymarty):
    print("Entra a balla")
    try:
       mymarty.circle_dance()
    except Exception as e:
       print("Unexpected error: ", str(e))
        
def guapa(mymarty):
    print("Entra a guapa")
    try:
       mymarty.eyes(20,500)
       mymarty.lean('left', 50, 2000)
                   
       os.system(" echo 'Ai quina vergonya' | festival --language catalan --tts")
        
       mymarty.hello()
    except Exception as e:
       print("Unexpected error: ", str(e))
        


if __name__ == '__main__':
    main()