import json
import requests

#Prueba practica de ataques de fuerza bruta (usando WireShark)
#para capturar el trafico de estas peticiones como estamos en localhost tenemos que usar la opcion de loopback (localhost)
#y ahi veremos estas peticiones http que estamos haciendo asi como si son autorizadas o no 
#tcp.port == 5000


#python espera algo como: Content-Type: application/json
#cuando usas "json=" requests añade automaticamente ese Content-Type
with open("fuerza.json", "r", encoding="utf-8") as f:
    credenciales = json.load(f)

for payload in credenciales:
    r = requests.post(
        "http://127.0.0.1:5000/api/login",
        json=payload
    )
    print(payload["correo"], r.status_code)
