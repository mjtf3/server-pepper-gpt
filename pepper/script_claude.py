#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para que Pepper reaccione a respuestas SI/NO
Requiere Python 2.7 y NAOqi SDK
"""

from naoqi import ALProxy
import time

# Clave de ALMemory para marcar vocab inicializado
VOCAB_FLAG = "MyApp/VocabInitialized"


def main():
    # Configuración del robot
    ROBOT_IP = "localhost"  # Cambia por la IP de tu robot
    ROBOT_PORT = 9559

    try:
        # Crear proxies para los servicios necesarios
        tts = ALProxy("ALTextToSpeech", ROBOT_IP, ROBOT_PORT)
        asr = ALProxy("ALSpeechRecognition", ROBOT_IP, ROBOT_PORT)
        memory = ALProxy("ALMemory", ROBOT_IP, ROBOT_PORT)

        # Configurar el reconocimiento de voz
        asr.setLanguage("Spanish")  # o "English" según prefieras

        try:
            asr.unsubscribe("MiApp_ASR")
        except RuntimeError:
            pass

        # SOLO la primera vez: definir y cargar el vocabulario
        try:
            already = memory.getData(VOCAB_FLAG)
        except Exception:
            already = False

        if not already:
            # Pausar ASR para cambiar vocabulario
            asr.pause(True)

            # Definir vocabulario
            vocabulary = ["si", "no", "yes"]
            asr.setVocabulary(vocabulary, False)

            # Reanudar ASR
            asr.pause(False)

            # Marcar en ALMemory que ya lo inicializamos
            memory.insertData(VOCAB_FLAG, True)



        # Hacer una pregunta al usuario
        tts.say("¿Tienes alguna otra pregunta?")

        # limpiamos memorio
        memory.insertData("WordRecognized", ["", 0.0])

        # Iniciar reconocimiento de voz
        asr.subscribe("Test_ASR")

        print("Robot esperando respuesta... Di 'sí' o 'no'")

        # Esperar respuesta del usuario
        recognized = False
        start_time = time.time()
        timeout = 10  # 10 segundos de timeout

        time.sleep(0.5)  # Esperar un segundo antes de empezar a escuchar

        responseType = None

        while not recognized and (time.time() - start_time) < timeout:
            # Verificar si hay una palabra reconocida
            word_recognized = memory.getData("WordRecognized")
            if word_recognized and len(word_recognized) > 1:
                recognized_word = word_recognized[0]
                confidence = word_recognized[1]

                if confidence > 0.5:  # Umbral de confianza
                    print("Palabra reconocida: {}".format(recognized_word))
                    responseType = process_response(recognized_word, tts)
                    recognized = True
                    break

            time.sleep(0.1)

        if not recognized:
            tts.say("No pude escuchar tu respuesta. Intenta de nuevo.")

        # Detener reconocimiento
        asr.unsubscribe("Test_ASR")
        
        return responseType

    except Exception as e:
        print("Error conectando al robot: {}".format(e))
        print("Asegúrate de que:")
        print("1. El robot esté encendido")
        print("2. La IP sea correcta")
        print("3. Estés en la misma red")

        # Detener el reconocimiento
        if 'asr' in locals():
            try:
                asr.unsubscribe("Test_ASR")
            except RuntimeError:
                pass
        return None


def process_response(word, tts):
    """
    Procesa la respuesta del usuario y hace que el robot reaccione
    """
    word_lower = word.lower()

    if word_lower in [u"si", u"yes"]:
        # Reacción positiva
        # tts.say("¡Excelente! Me alegra saber que te gusta programar.")
        # tts.say("La programación es muy divertida y útil.")
        print("Usuario respondió SÍ - Reacción positiva")
        return True

    elif word_lower in [u"no"]:
        # Reacción negativa
        tts.say("Entiendo. Ha sido un placer.")
        tts.say("No dudes en volver a consultarme.")
        print("Usuario respondió NO - Reacción comprensiva")
        return False

    else:
        # Respuesta no reconocida
        tts.say("No estoy seguro de tu respuesta. Puedes decir sí o no.")
        print("Respuesta no reconocida")
        return None


if __name__ == "__main__":
    result = main()
    print("Resultado:", result)
