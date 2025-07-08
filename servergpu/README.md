# Como configurar la api key de gemini como una variable de entorno (válido para gemini 2.5)
## Linux / macOS (Bash)

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