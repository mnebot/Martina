#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""

Google CloudSpeech recognizer utilitzat per a donar ordres a 
la Martina en català.
 
"""

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
    aiy.audio.get_recorder().start()
    
    # inicialitza robot
    mymarty = Marty('socket://192.168.0.22') # Change IP accordingly
    mymarty.hello()  # Move to zero positions and wink True

    os.system(" echo 'Hola ja estic llesta!' | festival --language catalan --tts")
    
    # Mentre no escolti adéu processa el què escolta
    while True:

        # Escolta i reconeix a text el que s'escolta després de que es premi
        # qualsevol tecla
        
        input('Apreta l''intro per a parlar')
        print('Escoltant-te...')
        text = recognizer.recognize()
        
        
        # si no escolta res, mostra el missatge pertinent
        # si reconeix, mostra el què s'ha dit
        # si reconeix una acció, l'executa
        if not text:
            os.system(" echo 'Ho sento, no t''he sentit.' | festival --language catalan --tts")
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
            elif 'Adéu' in text:
                os.system(" echo 'Fins aviat!' | festival --language catalan --tts")
                break


if __name__ == '__main__':
    main()
