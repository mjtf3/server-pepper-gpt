#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from naoqi import ALProxy
import time
import uuid

class PepperListener(object):
    def __init__(self, robot_ip, robot_port=9559):
        # Proxies a ALMemory y ALSpeechRecognition
        self.memory = ALProxy("ALMemory", robot_ip, robot_port)
        self.asr    = ALProxy("ALSpeechRecognition", robot_ip, robot_port)
        self.ultima_palabra = None
        
        # Generar un identificador único para esta instancia
        self.subscriber_id = "PepperListener_" + str(uuid.uuid4())[:8]
        
        # Pausamos el motor de reconocimiento antes de cambiar vocabulario
        self.asr.pause(True)

        # Defino un vocabulario sencillo
        vocab = ["sí", "no"]
        self.asr.setVocabulary(vocab, False)

        # Reanudo el motor de reconocimiento
        self.asr.pause(False)

        # Suscribo el recognizer
        self.asr.subscribe("MiApp_ASR")

        # Crear un callback usando ALMemory directamente
        self.memory.insertData("WordRecognized", [])
        
        # Suscribirse al evento usando el nombre del archivo actual
        self.memory.subscribeToEvent(
            "WordRecognized",
            __name__,
            "on_word_recognized"
        )

    def on_word_recognized(self, event_name, value, message):
        """
        Callback para WordRecognized.
        value es una lista [palabra_reconocida, confianza]
        """
        if value and len(value) >= 2:
            palabra, confianza = value[0], value[1]
            if confianza > 0.4:
                print("¡He reconocido '%s' con confianza %.2f!" %
                      (palabra, confianza))
                self.ultima_palabra = palabra

    def run(self, tiempo_segundos=5):
        """Mantengo el programa vivo para escuchar eventos"""
        print("Escuchando durante %d seg…" % tiempo_segundos)
        time.sleep(tiempo_segundos)

        # Al terminar, limpio suscripciones de ASR y ALMemory
        try:
            self.asr.unsubscribe("MiApp_ASR")
        except RuntimeError as e:
            print("Error al desuscribir ASR:", e)

        try:
            self.memory.unsubscribeToEvent("WordRecognized", __name__)
        except RuntimeError as e:
            print("Error al desuscribir evento:", e)

if __name__ == "__main__":
    IP = "127.0.0.1"   # cambia por la IP de tu Pepper
    PL = PepperListener(IP)
    PL.run(20)
    print("Variable última_palabra =", PL.ultima_palabra)
