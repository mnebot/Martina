#!/usr/bin/env python3

#Licensed under the MIT License

#Utilitza el projecte AIY de Google	 per a donar ordres a 
#la Martina en català.

#Utilitza el sintetitzador de veu Festival i la veu Ona de Fescat.

#Es comunica amb el robot mitjançant les llibreries de robotical.io martypy
 
#"""

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import os
from martypy import Marty

#os.system(" echo 'text a parlar' | festival --language catalan --tts")
def main():
    
    # inicialitza el reconeixedor de veu i comença a escoltar
    aiy.i18n.set_language_code('ca-ES')
    recognizer = aiy.cloudspeech.get_recognizer()
    
    recognizer.expect_hotword('Martina')
    
    recognizer.expect_phrase('fes una foto')
    recognizer.expect_phrase('camina')
    recognizer.expect_phrase('balla')
    recognizer.expect_phrase('guapa')
    recognizer.expect_phrase('Adéu')
    
    aiy.audio.get_recorder().start()
    
    # inicialitza robot
    mymarty = Marty('socket://192.168.0.20') # Change IP accordingly
    mymarty.hello()  # Move to zero positions and wink True

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
                os.system(" echo 'Acció fer la foto' | festival --language catalan --tts")
            elif 'camina' in text:
                mymarty.walk(num_steps=2, start_foot='auto', turn=20, step_length=30, move_time=2000)
            elif 'balla' in text:
                mymarty.circle_dance()
            elif 'guapa' in text:
                mymarty.eyes(20,500)
                mymarty.lean('left', 50, 2000)
                           
                os.system(" echo 'Ai quina vergonya' | festival --language catalan --tts")
                
                mymarty.hello()
            elif 'adéu' in text:
                print('Adéu')
                os.system(" echo 'Fins aviat!' | festival --language catalan --tts")
                break


if __name__ == '__main__':
    main()

