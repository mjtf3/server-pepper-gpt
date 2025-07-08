#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from naoqi import ALProxy
import time

class PepperListener(object):
    def __init__(self, robot_ip, robot_port=9559):
        # Proxy a ALMemory y ALSpeechRecognition
        self.memory = ALProxy("ALMemory", robot_ip, robot_port)
        self.asr    = ALProxy("ALSpeechRecognition", robot_ip, robot_port)
        # Variable que quieres modificar
        self.ultima_palabra = None

        # Defino un vocabulario sencillo
        vocab = ["sí", "no"]
        self.asr.setVocabulary(vocab, False)
        # Suscribo el reconocedor
        self.asr.subscribe("MiApp_ASR")

        # Me suscribo al evento WordRecognized
        # Cuando NAO reconozca una palabra de vocabulario
        self.memory.subscribeToEvent("WordRecognized", "PepperListener", "on_word_recognized")

    def on_word_recognized(self, event_name, value, message):
        """
        Callback para WordRecognized.
        value es una lista [palabra_reconocida, confianza]
        """
        palabra, confianza = value
        # Umbral de confianza (por defecto viene 0.0–1.0)
        if confianza > 0.4:
            print("¡He reconocido '%s' con confianza %.2f!" % (palabra, confianza))
            # Aquí modificas tu variable de Python
            self.ultima_palabra = palabra

    def run(self, tiempo_segundos=5):
        """Mantengo el programa vivo para escuchar eventos"""
        print("Escuchando durante %d seg…" % tiempo_segundos)
        time.sleep(tiempo_segundos)
        # Al terminar, limpia
        self.asr.unsubscribe("MiApp_ASR")
        self.memory.unsubscribeToEvent("WordRecognized", "PepperListener")

if __name__ == "__main__":
    IP   = "127.0.0.1"   # cambia por la IP de tu Pepper
    PL   = PepperListener(IP)
    PL.run(20)
    print("Variable última_palabra =", PL.ultima_palabra)