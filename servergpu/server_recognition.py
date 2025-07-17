import speech_recognition as sr
from gemini import generate

'''
Programa que procesa un archivo de audio, lo convierte a texto y llama a un modelo de IA para generar una respuesta.
'''

def procesar_archivo(modelo, archivo):

    num_of_words = 10  # Number of words to limit the response
    language_code = 'es-ES'  # Language code for Spanish
    
    print('Translating...')
    recognizer = sr.Recognizer()
    with sr.AudioFile(archivo) as source:
        audio = recognizer.record(source)
    
    
    try:
        print("I think you asked: ")
        translation = recognizer.recognize_google(audio, language=language_code)
        print(translation)
    except sr.UnknownValueError:
        print("Error: No se pudo entender el audio.")
        message_error = "No pude entenderte, lo siento"
        return message_error
    except sr.RequestError as e:
        print("Error al conectar con el servicio de reconocimiento: {0}".format(e))
        message_error = "Error al procesar la solicitud de reconocimiento de voz"
        return message_error

    prompt = "Por favor, responde a la siguiente pregunta con una sola opción: "
    text_question = prompt + " '" + translation + "?' "
    print(text_question)

    return llamar_modelo_AI(modelo, text_question)



def llamar_modelo_AI(modelo, pregunta):
    # response = call_AI_model(modelo, pregunta) #hacer llamada al modelo AI, creo que se deberia de hacer aqui de hecho
    response = generate(modelChosen=modelo, input=pregunta)

    print("GPT response: ", response.text)

    response = response.text     
    result = response.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'ny')
    #result = response.strip()

    if result == '':
        print("Respuesta vacía")
        response = "Puedes repetir la pregunta"

    print(result)
    return result