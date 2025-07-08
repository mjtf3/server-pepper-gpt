# To run this code you need to install the following dependencies:
# pip install google-genai

'''
Codigo que genera contenido utilizando el modelo Gemini de Google.
'''
import base64
import os
from google import genai
from google.genai import types


def generate(modelChosen ="gemini-2.5-flash-lite-preview-06-17", input = "Why is the sky blue?"):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
        #api_key="<TU_API_KEY_AQUI>",  # Reemplaza con tu API key de Gemini
    )
    response = client.models.generate_content(
        model=modelChosen, contents=input,
        config=types.GenerateContentConfig(
            system_instruction='Eres un asistente de IA el cual potencia al robot Pepper. \
                                Responde a las preguntas de los usuarios de manera clara y concisa. \
                                En la medida de lo posible, responde en español y que sean alrededor de 10-15 palabras.',
        ),
    )
    # print(response.text)
    return response

if __name__ == "__main__":
    generate()
