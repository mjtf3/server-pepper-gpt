'''
Servidor Flask para procesar archivos de audio y recibir respuestas del modelo AI.
Alojado en el servidor externo de Pepper.

REQUISITOS:
- Tener flask
- Tener el archivo server_recognition.py en la misma carpeta que este script
- Tener el archivo gemini.py en la misma carpeta que el archivo server_recognition.py
- Tener la API key de Gemini configurada en el entorno o directamente en el código (no recomendado para producción)
- Tener el archivo de audio test.wav en la misma carpeta que este script
'''

from flask import Flask
from server_recognition import procesar_archivo as procesar_archivo_local

app = Flask(__name__)

@app.route("/procesar_recibir_respuesta", methods=["GET"])
def llamada():
    modelo = "gemini-2.5-flash-lite-preview-06-17"
    archivo = "test.wav"
    respuesta = procesar_archivo_local(modelo, archivo)
    return respuesta