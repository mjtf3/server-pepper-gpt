# -*- coding: utf-8 -*-
import requests

def call_AI_model(model, ip, port):

    # El endpoint al que queremos llamar
    url = "http://" + ip + ":" + port + "/procesar_recibir_respuesta"

    print("Llamando al modelo AI en:", url)

    try:
        # Hacemos la petición GET
        response = requests.get(url)

        # Verificamos si la petición fue exitosa (código de estado 200)
        response.raise_for_status()  # Lanza una excepción para errores HTTP (4xx o 5xx)

        # Convertimos la respuesta a formato JSON
        data = response.text
        if isinstance(data, unicode):
            data = data.encode('utf-8')

    
        # Imprimimos los datos obtenidos
        print("Petición exitosa!")
        print("Datos recibidos:")
        print(data)

        return data

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
    parser.add_argument('--port', type=str, default='5000', required=False, help='Port of the remote server')
    args = parser.parse_args()

    print("IP del servidor:", args.IP)
    print("Puerto del servidor:", args.port)

    # Llamar a la función con la IP del servidor
    call_AI_model("test_model", args.IP, args.port)