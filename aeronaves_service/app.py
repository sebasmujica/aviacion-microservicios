from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from auth import verificar_autorizacion
from funciones import buscar_aeronave

load_dotenv()

PORT = int(os.getenv("PORT","5001"))
SERVICE_TOKEN = os.getenv("SERVICE_TOKEN")

#Datos predeterminados para usar antes de maipular una DB
aeronaves = [
    {"id":1, "modelo":"Cessna 172", "capacidad": 4},
    {"id":2, "modelo":"Boeing 737", "capacidad": 180}
]


app = Flask(__name__)

app.before_request(verificar_autorizacion)

@app.get("/")
def home():
    return "<h1>Servicio de Aeronaves activo </h1>"

@app.get("/health")
def status():
    return jsonify({
        "service": "aeronaves",
        "status": "ok"
    })

#Envia todas las aeronaves enlistadas
@app.get("/aeronaves")
def listar_aeronaves():
    return jsonify(aeronaves)

#Devuelve la aeronave seleccionada por id
@app.get("/aeronaves/<int:aid>")
def obtener_aeronave(aid:int):

    a = buscar_aeronave(aeronaves,aid)
    if not a:
        return jsonify({"error":"not found"}),404
    else:
        return jsonify(a)

#Crea una aeronave nueva
@app.post("/aeronaves")
def crear_aeronave():

    data = request.get_json(force=True, silent=True) or {}
    modelo = (data.get("modelo") or "").strip()
    capacidad = data.get("capacidad") or 0 # El 0 evita problemas con el type hint

    if not modelo:
        return jsonify({"error":"modelo requerido"}),400
    
    try:
        capacidad = int(capacidad)
        if capacidad <= 0:
            raise ValueError()
    except Exception:
        return jsonify({"error":"capacidad invalida"}), 400

    nuevo_id = max([a["id"] for a in aeronaves] + [0]) + 1 # crea una lista con los ids, agarra el mayor y le suma 1   [0] -----> para que la lista no quede vacia
    nueva_aeronave = {"id": nuevo_id, "modelo": modelo, "capacidad": capacidad}
    aeronaves.append(nueva_aeronave)
    return jsonify(nueva_aeronave), 201

#Para actualizar aeronaves
@app.put("/aeronaves/<int:aid>")
def actualizar_aeronave(aid):

    a = buscar_aeronave(aeronaves,aid)
    if not a:
        return jsonify({"error":"not_found"}), 404
    
    data = request.get_json(force=True,silent=True) or {}

    if "modelo" in data:
        modelo = (data.get("modelo") or "").strip()
        a["modelo"] = modelo
    else:
        return jsonify({"error":"modelo_invalido"}), 400
    
    if "capacidad" in data:
        try:
            cap = int(data.get("capacidad") or 0)
            if cap <= 0:
                raise ValueError()
        except Exception:
            return jsonify({"error":"capacidad-invalida"}), 400
        a["capacidad"] = cap
    
    return jsonify(a)

#Para eliminar aeronaves
@app.delete("/aeronaves/<int:aid>")
def eliminar_aeronave(aid):
    global aeronaves
    existe = buscar_aeronave(aeronaves,aid)

    if not existe:
        return jsonify({"error":"not_found"}), 404
    aeronaves = [a for a in aeronaves if a["id"] != aid] # reestructuracion de la lista de aeronaves evitando el id deseado
    return "aeronave eliminada",201


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
