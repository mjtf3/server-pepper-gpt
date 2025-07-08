# Instrucciones para ejecutar el código del servidor

## Crear y configurar venv (entorno de python)

Crear entorno
```bash
python3 -m venv .venv
```

Usar entorno
```bash
. .venv/bin/activate
```

## Instalar dependencias necesarias

Hay que instalar las dependencias del archivo requirements.txt
```bash
pip install -r requirements.txt
```

## Configurar la api key de gemini como una variable de entorno (válido para gemini 2.5)
### Linux / macOS (Bash)

Verifica si existe ~/.bashrc
```bash
ls ~/.bashrc
```

Si no existe, créalo y ábrelo:

```bash
touch ~/.bashrc
open ~/.bashrc   # macOS (o usa tu editor, e.g., nano ~/.bashrc)
```

Agrega esta linea en el archivo .bashrc:

```bash
export GEMINI_API_KEY="<YOUR_API_KEY_HERE>"
```

Aplica los cambios:

```bash
source ~/.bashrc
```