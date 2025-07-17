#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para que Pepper reaccione a respuestas SI/NO
Requiere Python 2.7 y NAOqi SDK
"""

from naoqi import ALProxy
import time

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

        # Pausamos el motor de reconocimiento antes de cambiar vocabulario
        asr.pause(True)

        # Definir vocabulario más amplio para reconocimiento
        vocabulary = ["si", "sí", "no", "yes", "yep", "nope", "vale", "okay"]
        asr.setVocabulary(vocabulary, False)

        # Reanudo el motor de reconocimiento
        asr.pause(False)

        # Hacer una pregunta al usuario
        tts.say("¿Tienes alguna otra pregunta?")

        # Iniciar reconocimiento de voz
        asr.subscribe("Test_ASR")

        print("Robot esperando respuesta... Di 'sí' o 'no'")

        # Limpiar datos anteriores de memoria
        memory.insertData("WordRecognized", [])

        # Esperar respuesta del usuario
        recognized = False
        start_time = time.time()
        timeout = 15  # Aumentado a 15 segundos

        time.sleep(1.0)  # Esperar un poco más antes de empezar a escuchar

        responseType = None

        while not recognized and (time.time() - start_time) < timeout:
            # Verificar si hay una palabra reconocida
            word_recognized = memory.getData("WordRecognized")
            if word_recognized and len(word_recognized) > 1:
                recognized_word = word_recognized[0]
                confidence = word_recognized[1]

                print("Palabra detectada: '{}' con confianza: {:.2f}".format(recognized_word, confidence))

                if confidence > 0.5:  # Umbral de confianza más estricto
                    print("Palabra reconocida con suficiente confianza: {}".format(recognized_word))
                    responseType = process_response(recognized_word, tts)
                    recognized = True
                    # Limpiar memoria después del reconocimiento
                    memory.insertData("WordRecognized", [])
                    break
                else:
                    print("Confianza insuficiente ({:.2f}), continuando...".format(confidence))
                    # Limpiar para evitar re-procesamiento
                    memory.insertData("WordRecognized", [])

            time.sleep(0.1)

        if not recognized:
            tts.say("No pude escuchar tu respuesta claramente. Intenta hablar más claro.")

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
            asr.unsubscribe("Test_ASR")
        return None


def process_response(word, tts):
    """
    Procesa la respuesta del usuario y hace que el robot reaccione
    """
    word_lower = word.lower()

    if word_lower in [u"si", u"sí", u"yes", u"yep", u"vale", u"okay"]:
        # Reacción positiva
        # tts.say("¡Excelente! Me alegra saber que te gusta programar.")
        # tts.say("La programación es muy divertida y útil.")
        print("Usuario respondió SÍ - Reacción positiva")
        return True

    elif word_lower in [u"no", u"nope"]:
        # Reacción negativa
        tts.say("Entiendo. Ha sido un placer.")
        tts.say("No dudes en volver a consultarme.")
        print("Usuario respondió NO - Reacción comprensiva")
        return False

    else:
        # Respuesta no reconocida
        tts.say("No estoy seguro de tu respuesta. Puedes decir sí o no.")
        print("Respuesta no reconocida: '{}'".format(word_lower))
        return None


if __name__ == "__main__":
    result = main()
    print("Resultado:", result)
