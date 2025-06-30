#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from __future__ import print_function
'''

Este script sería para ejecutarlo en el robot Pepper y manda las ordendes de IA a un servidor remoto.

Main script to perform the whole conversation pipeline. This consists of:

1) Speech recognition system: 
    - Input: Human voice recording
    - Output: Text recognixed from the audio

2) Question answering bot:
    - Input: Text recognized from the audio
    - Output: Answer for the question in a given context

3) Text-to-speech generation:
    - Input Answer for the question
    - Output: Audio for the answer
'''
import subprocess
import os 
# import speech_recognition as sr #no compatible with Python 2.7 
import random 
import argparse 
import threading
import time
import sys
import requests
#from paramiko import SSHClient
#from scp import SCPClient
 

def call_python_script(action, args_dict=None):
    '''
    Function used to run a script in another python version. We need this to use Naoqi and work with
    Pepper robot, which only works in Python 2.7 (https://developer.softbankrobotics.com/pepper-naoqi-25/naoqi-developer-guide/getting-started/downloading-installing-softbank-robotics)
    '''
    command = ["python", "pepper_interact.py", "--action", action]
    if args_dict:
        for key, value in args_dict.items():
            command.append("--%s" % key)
            command.append(str(value))
    subprocess.call(command)

def call_AI_model(model, ip, port):

    # El endpoint al que queremos llamar
    url = "http://" + ip + ":" + port + "/procesar_recibir_respuesta"

    print("Llamando al modelo AI en:", url)

    try:
        # Hacemos la petición GET
        response = requests.get(url)

        # Verificamos si la petición fue exitosa (código de estado 200)
        response.raise_for_status()  # Lanza una excepción para errores HTTP (4xx o 5xx)

        # Convertimos la respuesta a formato JSON
        data = response.text
        if isinstance(data, unicode):
            data = data.encode('utf-8')

    
        # Imprimimos los datos obtenidos
        print("Petición exitosa!")
        print("Datos recibidos:")
        print(data)

        return data

    except requests.exceptions.HTTPError as errh:
        print("Error HTTP: {}".format(errh))
    except requests.exceptions.ConnectionError as errc:
        print("Error de Conexión: {}".format(errc))
    except requests.exceptions.Timeout as errt:
        print("Error de Timeout: {}".format(errt))
    except requests.exceptions.RequestException as err:
        print("Algo salió mal: {}".format(err))



def mandarArchivo(archivo, ip):

    print("Mandando archivo al servidor remoto...")
    user = 'pepper'
    
    # Comando SCP
    cmd = [
        'scp', 
        '-o', 'StrictHostKeyChecking=no',  # Evitar verificación de host
        '/home/nao/test.wav',
        '{}@{}:/home/pepper/server-pepper-gpt'.format(user, ip)
    ]
    
    try:
        # Ejecutar comando SCP
        result = subprocess.call(cmd)
        if result == 0:
            print("Archivo transferido exitosamente")
        else:
            print("Error en la transferencia")
    except Exception as e:
        print("Error: {}".format(e))


def countdown(seconds):
    for i in range(seconds, 0, -1):
        sys.stdout.write("⏳ Time left: %2d seconds\r" % i)
        sys.stdout.flush()
        time.sleep(1)
    print("\n⏹️ Time's up!")


def main(args):
    # recognizer = sr.Recognizer()
    os.system('clear')
    
    use_pepper = args.usePepper
    IP = args.IP  
    recording_time = args.recording_time # in seconds
    num_of_words = args.num_of_words  

    sentence = "Toca mi cabeza para hacerme una pregunta"
    text_robot = sentence
    print(sentence)     
    language = 'Spanish' #Spanish, 'en': English
    call_python_script("speak", {"sentence": text_robot, "language": language})
    
    waiting_messages = [["Estoy pensando"], ["Un momento"],["espere un momento"]]
    
    try:
        while True:
            # Wait for pepper to sense touch
            call_python_script("wait_touch", {"language": language})
            # Open microphone and wait for the question            
            if use_pepper:
                print('Pepper is listening to you!')        
                call_python_script("listen", {"listen_time": recording_time})
                print("Pepper has stopped listening.")
                call_python_script("speak", {"sentence": random.choice(waiting_messages)[0], "language": language})
                # Aqui en vez de copiar el archivo, lo procesamos directamente en el robot
                createdFile = '/home/nao/test.wav'

                call_python_script("speak", {"sentence": "ya he terminado de escuchar", "language": language})
                #recording = sr.AudioFile(createdFile)   
                #with recording as source:
                #    audio = recognizer.listen(source)
            else:
                pass
                #with sr.Microphone() as source:
                #    print("🎙️ Listening... You have %d seconds to speak" % recording_time)
                #    
                #    # Start countdown in background
                #    countdown_thread = threading.Thread(target=countdown, args=(recording_time,))
                #    countdown_thread.start()
                #    
                #    start_time = time.time()
                #    # Start listening (in background) and show countdown simultaneously
                #    audio = recognizer.listen(source, phrase_time_limit=recording_time)    
                #    elapsed_time = time.time() - start_time                             
                #    print("⏹️ Stop listening. Recording time was: {:.2f} seconds".format(elapsed_time))
                #call_python_script("speak", {"sentence": random.choice(waiting_messages)[0], "language": language})        

            # try:
            #     print('Translating...')
            #     print("I think you asked: ")
            #     langue_voulue = 'es'
            #     translation = recognizer.recognize_google(audio, language=langue_voulue)
            #     print(translation)
            # except sr.UnknownValueError:
            #     print("Sorry, I didn't understand you")
            #     message_error = "No pude entenderte, lo siento"
            #     call_python_script("speak", {"sentence": message_error, "language": language})
            #     continue 
            # except sr.RequestError as e:
            #     print("Could not request results from Google Speech Recognition service; {0}".format(e))

            print('Ejecutamos funcion para mandar el archivo al servidor')
            mandarArchivo(createdFile, args.serverIP)
            response = call_AI_model(args.model, args.serverIP, args.serverPort)
            print("GPT response: ", response)

            if response == '':
                print("Respuesta vacía")
                response = "Puedes repetir la pregunta"

            print([response])
            call_python_script("speak", {"sentence": response, "language": language})

    except KeyboardInterrupt:
        call_python_script("switch_awareness", {"sentence": "Disable"})

if __name__ == "__main__":  
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_pepper_mic", dest="usePepper", type=bool, default=True, required=False)
    parser.add_argument("--IP", type=str, default="127.0.0.1",
                        help="IP address of the Pepper robot. Por defecto usamos localhost")
    parser.add_argument("--port", type=int, default=9559, required=False)
    parser.add_argument("--recording_time", type=int, default=6, required=False,
                        help="Time in seconds to record the question")
    parser.add_argument("--num_of_words", type=int, default=30, required=False)
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", required=False,
                        help="Model to use for the question answering bot")
    parser.add_argument("--serverIP", type=str, default="192.168.1.221", required=False,
                        help="IP address of the server where the AI model is hosted")
    parser.add_argument("--serverPort", type=str, default="5000", required=False,
                        help="Port of the server where the AI model is hosted")
    
    args = parser.parse_args()

    main(args)