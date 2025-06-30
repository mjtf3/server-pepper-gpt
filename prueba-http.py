# -*- coding: utf-8 -*-
import requests

def call_AI_model(model, ip):

    # El endpoint al que queremos llamar
    url = "http://" + ip + "/procesar_recibir_respuesta"

    try:
        # Hacemos la petición GET
        response = requests.get(url)

        # Verificamos si la petición fue exitosa (código de estado 200)
        response.raise_for_status()  # Lanza una excepción para errores HTTP (4xx o 5xx)

        # Convertimos la respuesta a formato JSON
        data = response.text
    
        # Imprimimos los datos obtenidos
        print("Petición exitosa!")
        print("Datos recibidos:")
        print(data)

    except requests.exceptions.HTTPError as errh:
        print("Error HTTP: {}".format(errh))
    except requests.exceptions.ConnectionError as errc:
        print("Error de Conexión: {}".format(errc))
    except requests.exceptions.Timeout as errt:
        print("Error de Timeout: {}".format(errt))
    except requests.exceptions.RequestException as err:
        print("Algo salió mal: {}".format(err))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Call an AI model via HTTP.")
    parser.add_argument('--IP', type=str, required=True, help='IP address of the remote server')
    args = parser.parse_args()

    # Llamar a la función con la IP del servidor
    call_AI_model("test_model", args.IP)