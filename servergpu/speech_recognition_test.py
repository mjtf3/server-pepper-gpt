import speech_recognition as sr
import sys

def transcribe_audio_file(file_path: str, language: str = "es-ES") -> str:
    """
    Transcribe el contenido de un archivo de audio usando Google Web Speech API.

    :param file_path: Ruta al archivo de audio (wav, aiff, flac).
    :param language: Código de idioma (por defecto "es-ES").
    :return: Texto transcrito o mensaje de error.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        return "Error: No se pudo entender el audio."
    except sr.RequestError as e:
        return f"Error al conectar con el servicio de reconocimiento: {e}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python speech_recognition_test.py <ruta_al_archivo_audio>")
        sys.exit(1)

    ruta_audio = sys.argv[1]
    resultado = transcribe_audio_file(ruta_audio)
    print("Transcripción:", resultado)