#!/usr/bin/env python3

import wave
import sys
import json
import time
from vosk import Model, KaldiRecognizer, SetLogLevel

# You can set log level to -1 to disable debug messages
SetLogLevel(-1)

def transcribir_audio(archivo_audio):
    wf = wave.open(archivo_audio, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("El archivo de audio debe ser en formato WAV mono PCM.")
        sys.exit(1)

    start = time.perf_counter()    # ← marca inicio

    model = Model(lang="es") # Small model
    # model = Model(model_name="vosk-model-es-0.42") # Large model

    # Puedes inicializar el modelo por nombre o con una ruta de carpeta
    # model = Model("models/en")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    rec.SetPartialWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            #print(rec.Result())
            pass
        else:
            #print(rec.PartialResult())
            pass

    final_json = json.loads(rec.FinalResult())

    end = time.perf_counter()      # ← marca fin
    print(f"Tiempo transcurrido: {end - start:.3f} segundos")

    print("Creo que has dicho: ",final_json["text"])
    return final_json["text"]


if __name__ == "__main__":
    transcribir_audio(sys.argv[1]) if len(sys.argv) > 1 else "test.wav"