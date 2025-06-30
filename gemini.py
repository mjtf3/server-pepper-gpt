# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate(modelChosen ="gemini-2.5-flash-lite-preview-06-17", input = "Why is the sky blue?"):
    client = genai.Client(
        #api_key=os.environ.get("GEMINI_API_KEY"),
        api_key="AIzaSyAji8v9h1fzseYKrE5uoCxw4v1sBMxSt78",
    )
    response = client.models.generate_content(
        model=modelChosen, contents=input
    )
    # print(response.text)
    return response

if __name__ == "__main__":
    generate()
