##  comandos utilizados

# Readme
Los archivos de la carpeta pepper se han de guardar y ejecutar en el robot Pepper y los archivos de la carpeta servergpu se han de guardar y ejecutar en el servidor externo que corresponda.

# crear env
mkdir myproject
cd myproject
python3 -m venv .venv

# usar env
conda activate pepper-py310
. .venv/bin/activate

# instalar dependencias (con el env activado)
pip install Flask
pip install python-dotenv
pip install google-genai
pip install SpeechRecognition

# o
pip install -r requirements.txt

# ejecutar aplicacion
flask --app hello run
# (si la aplicacion se llama app.py o wsgi.py)
flask run
# para todos los ip
flask run --host=0.0.0.0




# 30/06
me he quedado intentando ejecutar flask en el pepper

# 08/07
- [] poner el servidor en el pepper para poder realizar las llamadas al script desde la web
- [x] poner la api key de gemini en un entorno en condiciones 







# 18/05
- [x] que se puedan cambiar de providers de ia
- [] haer documentacion para todoc
- [x] realizar distintos prompts del sistema para la ia y que al iniciar se puedan elegir que personalidad se quiere
    - personalidades:
        - neutro
        - cuidador para ancionos
        - cuidador para niños
        - profesor para estudiantes de secundaria
- [] arregla el tema de los argumentos en ai_pepper_script.py