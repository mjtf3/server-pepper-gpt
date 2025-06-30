from flask import Flask
from server_recognition import procesar_archivo as procesar_archivo_local

app = Flask(__name__)

@app.route("/procesar_recibir_respuesta", methods=["GET"])
def llamada():
    modelo = "gemini-2.5-flash-lite-preview-06-17"
    archivo = "test.wav"
    respuesta = procesar_archivo_local(modelo, archivo)
    return respuesta