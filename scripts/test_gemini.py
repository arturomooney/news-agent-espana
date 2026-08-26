import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")
respuesta = model.generate_content("Respondé únicamente con la palabra: FUNCIONA")

print(respuesta.text)
