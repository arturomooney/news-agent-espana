
import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

mensaje = """
🎉 ¡Hola!

Este es el primer mensaje enviado automáticamente por tu News Agent España.

Si recibís este mensaje, GitHub ya puede hablar con Telegram.
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": mensaje
    }
)

print("Mensaje enviado.")
