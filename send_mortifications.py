import json
import random
import requests
import os  # Para leer variables de entorno

# Obtener credenciales desde GitHub Secrets
PHONE_NUMBERS = [
    os.getenv("WHATSAPP_NUMBER"),  # Primer número
    os.getenv("WHATSAPP_NUMBER_2")  # Segundo número
]
API_KEY = os.getenv("CALLMEBOT_APIKEY")

# Cargar las mortificaciones desde el JSON
with open("mortificaciones.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Mortificaciones constantes
MORTIFICACIONES_FIJAS = [
    "Ayunar los viernes.",
    "Orar el Rosario todos los días."
]

# Seleccionar 3 mortificaciones aleatorias
mortificaciones_aleatorias = []
categorias = list(data["mortificaciones"])
random.shuffle(categorias)

for categoria in categorias:
    acciones = categoria["acciones"]
    if acciones:
        mortificacion = random.choice(acciones)
        if mortificacion not in MORTIFICACIONES_FIJAS:
            mortificaciones_aleatorias.append(mortificacion)
    if len(mortificaciones_aleatorias) == 3:
        break

# Crear el mensaje final
mensaje = "Mortificaciones del día:\n\n"
mensaje += f"1️⃣ {MORTIFICACIONES_FIJAS[0]}\n"
mensaje += f"2️⃣ {MORTIFICACIONES_FIJAS[1]}\n"
mensaje += f"3️⃣ {mortificaciones_aleatorias[0]}\n"
mensaje += f"4️⃣ {mortificaciones_aleatorias[1]}\n"
mensaje += f"5️⃣ {mortificaciones_aleatorias[2]}\n"

# Enviar el mensaje a cada número
for phone in PHONE_NUMBERS:
    if phone:  # Verificar que la variable de entorno no está vacía
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={mensaje}&apikey={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            print(f"✅ Mensaje enviado a {phone}")
        else:
            print(f"❌ Error al enviar el mensaje a {phone}: {response.status_code}")
