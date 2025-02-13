import json
import random
import requests
import os
import datetime

# Obtener credenciales desde GitHub Secrets
PHONE_NUMBER = "573058180027"
API_KEY = "5298266"

# Definir mortificaciones fijas por día de la semana
MORTIFICACIONES_FIJAS = {
    "Monday": ["No tomar café", "Hacer 10 minutos de oración en silencio"],
    "Tuesday": ["No comer dulces", "Leer un capítulo de la Biblia"],
    "Wednesday": ["No usar redes sociales por una hora", "Hacer un acto de caridad"],
    "Thursday": ["Tomar agua en lugar de gaseosas", "Evitar quejarse todo el día"],
    "Friday": ["Hacer ayuno parcial", "Rezar el Viacrucis"],
    "Saturday": ["Hacer una visita al Santísimo", "No ver televisión"],
}

# Obtener el día de la semana actual
hoy = datetime.datetime.now().strftime("%A")

# Si es domingo, no se envía nada
if hoy == "Sunday":
    print("Hoy es domingo, no se envían mortificaciones.")
    exit()

# Cargar las mortificaciones desde el JSON
with open("mortificaciones.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Seleccionar 3 mortificaciones aleatorias
mortificaciones_aleatorias = []
categorias = list(data["mortificaciones"])
random.shuffle(categorias)

for categoria in categorias:
    acciones = categoria["acciones"]
    if acciones:
        mortificacion = random.choice(acciones)
        if mortificacion not in MORTIFICACIONES_FIJAS[hoy]:  # Evita duplicados
            mortificaciones_aleatorias.append(mortificacion)
    if len(mortificaciones_aleatorias) == 3:
        break

# Crear el mensaje final
mensaje = f"Mortificaciones del {hoy}:\n\n"
mensaje += f"1️⃣ {MORTIFICACIONES_FIJAS[hoy][0]}\n"
mensaje += f"2️⃣ {MORTIFICACIONES_FIJAS[hoy][1]}\n"
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
