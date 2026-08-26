import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

respuesta = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Respondé únicamente con la palabra: FUNCIONA"
)

print(respuesta.text)
