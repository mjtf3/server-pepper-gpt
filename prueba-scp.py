# -*- coding: utf-8 -*-

import argparse
import subprocess
import os

def mandarArchivo(archivo, ip):

    print("Mandando archivo al servidor remoto...")
    user = 'pepper'
    
    # Comando SCP
    cmd = [
        'scp', 
        '-o', 'StrictHostKeyChecking=no',  # Evitar verificación de host
        '/home/nao/test.wav',
        '{}@{}:/home/pepper/server-pepper-gpt'.format(user, ip)
    ]
    
    try:
        # Ejecutar comando SCP
        result = subprocess.call(cmd)
        if result == 0:
            print("Archivo transferido exitosamente")
        else:
            print("Error en la transferencia")
    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Transfer a file to a remote server using SCP.")
    parser.add_argument('--IP', type=str, required=True, help='IP address of the remote server')
    args = parser.parse_args()

    # Llamar a la función con el archivo y la IP del servidor
    mandarArchivo("test.wav", args.IP)