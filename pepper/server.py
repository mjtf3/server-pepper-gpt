#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import subprocess
import os
import urlparse

SCRIPT_PATH = "/home/nao/pepper-chatbot/ai_pepper_script.py"  # Ruta a tu script

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Manejo de preflight CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # Parseamos la URL para separar path y query string
        parsed = urlparse.urlparse(self.path)
        path = parsed.path

        if path == '/run-script':
            # Ejecutamos el script externo y capturamos su salida
            try:
                # Llama al intérprete python2.7 para ejecutar el script
                output = subprocess.check_output(
                    ['python', SCRIPT_PATH, '--serverIP', '172.18.33.110', '--serverPort', '5000'],
                    stderr=subprocess.STDOUT,
                    cwd=os.path.dirname(SCRIPT_PATH)
                )
                status_code = 200
                body = output
                content_type = 'text/plain'
            except subprocess.CalledProcessError as e:
                status_code = 500
                body = "Error ejecutando el script:\n" + e.output
                content_type = 'text/plain'

            # Enviamos la respuesta HTTP
            self.send_response(status_code)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            # Si la ruta no coincide, devolvemos 404
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write("Not Found: {}".format(path))

if __name__ == '__main__':
    port = 8080
    httpd = HTTPServer(('0.0.0.0', port), RequestHandler)
    print "Servidor escuchando en http://0.0.0.0:{}".format(port)
    httpd.serve_forever()