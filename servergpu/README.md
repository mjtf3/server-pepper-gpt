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

# Sistema de AI Modular para Pepper

Este sistema refactorizado permite usar múltiples providers de IA (Gemini, OpenAI, etc.) y personalidades configurables para el robot Pepper.

## 🚀 Características

-   **Múltiples Providers**: Soporte para Gemini, OpenAI y fácil adición de nuevos providers
-   **Personalidades Configurables**: System prompts personalizables via archivo JSON
-   **Arquitectura Modular**: Código no duplicado, fácil mantenimiento
-   **API REST**: Endpoints claros y documentados
-   **Validación de Parámetros**: Manejo robusto de errores

## 📁 Estructura del Proyecto

```
servergpu/
├── app.py                      # Servidor Flask principal
├── server_recognition.py       # Procesamiento de audio y lógica principal
├── personality_manager.py      # Gestor de personalidades
├── personalities.json          # Configuración de personalidades
├── providers/
│   ├── __init__.py            # Factory de providers
│   ├── base_provider.py       # Clase base abstracta
│   ├── gemini_provider.py     # Implementación de Gemini
│   └── openai_provider.py     # Template para OpenAI (ejemplo)
├── gemini.py                  # (Archivo legacy - puede eliminarse)
└── requirements.txt
```

## 🔧 Instalación

1. Instalar dependencias:

```bash
pip install flask speech_recognition google-genai
```

2. Configurar variables de entorno:

```bash
export GEMINI_API_KEY="tu_api_key_de_gemini"
export OPENAI_API_KEY="tu_api_key_de_openai"  # Cuando lo implementes
```

3. Ejecutar el servidor:

```bash
python app.py
```

## 📖 Uso

### Endpoint Principal

```
GET /procesar_recibir_respuesta?provider=gemini&personalidad=1&modelo=gemini-2.5-flash-lite-preview-06-17
```

**Parámetros:**

-   `provider` (requerido): Nombre del provider (`gemini`, `openai`)
-   `personalidad` (opcional): ID de personalidad (1-5, default: 1)
-   `modelo` (opcional): Modelo específico del provider
-   `archivo` (opcional): Archivo de audio (default: test.wav)

### Endpoints Informativos

-   `GET /providers` - Lista providers disponibles y sus modelos
-   `GET /personalidades` - Lista personalidades disponibles
-   `GET /info` - Información completa del sistema

### Ejemplos de Uso

```bash
# Usar Gemini con personalidad amigable
curl "http://localhost:5000/procesar_recibir_respuesta?provider=gemini&personalidad=1"

# Usar personalidad profesional
curl "http://localhost:5000/procesar_recibir_respuesta?provider=gemini&personalidad=2"

# Ver providers disponibles
curl "http://localhost:5000/providers"

# Ver personalidades disponibles
curl "http://localhost:5000/personalidades"
```

## 🎭 Personalidades Disponibles

1. **Pepper Amigable**: Asistente amigable y conciso
2. **Pepper Profesional**: Tono formal y empresarial
3. **Pepper Educativo**: Explicaciones didácticas para estudiantes
4. **Pepper Entretenimiento**: Divertido y con humor
5. **Pepper Recepcionista**: Cortés y útil para recepción

## 🔌 Agregar Nuevos Providers

1. Crear clase heredando de `BaseProvider`:

```python
# providers/mi_provider.py
from .base_provider import BaseProvider

class MiProvider(BaseProvider):
    def generate_response(self, prompt: str, system_prompt: str = "", **kwargs) -> str:
        # Tu implementación aquí
        pass

    def get_available_models(self) -> list:
        return ["modelo1", "modelo2"]
```

2. Registrar en `providers/__init__.py`:

```python
from .mi_provider import MiProvider

providers = {
    'gemini': GeminiProvider,
    'mi_provider': MiProvider,  # Agregar aquí
}
```

## 🎨 Agregar Nuevas Personalidades

Editar `personalities.json`:

```json
{
    "6": {
        "name": "Mi Nueva Personalidad",
        "system_prompt": "Tu system prompt personalizado aquí..."
    }
}
```

O usar el PersonalityManager programáticamente:

```python
from personality_manager import PersonalityManager

pm = PersonalityManager()
pm.add_personality("6", "Mi Personalidad", "System prompt aquí")
```

## 🛠️ Desarrollo

### Estructura de Clases

```
BaseProvider (Abstracta)
├── generate_response()     # Método principal
├── get_available_models()  # Lista de modelos
├── clean_response()        # Limpieza de texto
└── validate_config()       # Validación

PersonalityManager
├── get_system_prompt()     # Obtener prompt
├── get_personality()       # Obtener configuración
└── add_personality()       # Agregar nueva
```

### Testing

```bash
# Test del servidor
python app.py

# Test de providers específicos
python -c "from providers import get_provider; p = get_provider('gemini'); print(p.get_available_models())"
```

## 🔍 Troubleshooting

### Error: Provider no disponible

-   Verificar que el provider esté registrado en `providers/__init__.py`
-   Verificar que las dependencias estén instaladas

### Error: API Key

-   Verificar variables de entorno
-   Verificar permisos de la API key

### Error: Personalidad no encontrada

-   Verificar que el ID exista en `personalities.json`
-   El sistema usa personalidad "1" por defecto si no encuentra la solicitada

## 🚀 Próximos Pasos

1. Implementar OpenAI provider completo
2. Agregar más personalidades
3. Implementar cache de respuestas
4. Agregar logging estructurado
5. Implementar rate limiting
6. Agregar tests unitarios

## 📝 Notas

-   El archivo `gemini.py` original puede eliminarse después de verificar que todo funciona
-   Los acentos se eliminan automáticamente para compatibilidad con text-to-speech
-   El sistema es retrocompatible con el uso anterior
