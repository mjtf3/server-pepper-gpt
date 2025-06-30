##  comandos utilizados

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
