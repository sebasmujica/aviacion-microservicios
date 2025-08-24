from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from funciones import buscar_reserva

load_dotenv()

PORT = int(os.getenv("PORT","5003"))
DB = "reservas.db"

reservas = [
    {"id": 1, "vuelo_id": 1, "pasajero": "Ana Gomez", "asiento": "12A"},
    {"id": 2, "vuelo_id": 2, "pasajero": "Luis Perez", "asiento": "7C"},
]

app = Flask(__name__)

@app.get("/")
def home():
    return "<h1>Servicio de Reservas activo </h1>"

@app.get("/health")
def status():
    return jsonify({
        "service": "reservas",
        "status": "ok"
    })

@app.get("/reservas")
def listar_reservas():
    return jsonify(reservas)

@app.get("/reservas/<int:r_id>")
def obtener_reserva(r_id):
    reserva = buscar_reserva(reservas, r_id)
    if not reserva:
        return jsonify({"error":"not_found"}),404
    return jsonify(reserva)


@app.post("/reservas")
def crear_reserva():
    data = request.get_json(force=True,silent=True) or {}

    vuelo_id = data.get("vuelo_id")
    pasajero =(data.get("pasajero") or "").strip()
    asiento = (data.get("asiento") or "").strip()

    if not pasajero or not asiento:
        return jsonify({"error":"campos requeridos"}),400

    try:
        vuelo_id = int(data["vuelo_id"])
        if vuelo_id <= 0 :
            raise ValueError()
    except Exception:
        return jsonify({"error":"vuelo_id invalido"}),400

    nuevo_id = max([reserva["id"] for reserva in reservas]+ [0]) +1
    reserva = {"id":nuevo_id,"vuelo_id":vuelo_id,"pasajero":pasajero,"asiento":asiento}
    reservas.append(reserva)
    return jsonify(reserva),201

@app.put("/reservas/<int:r_id>")
def modificar_reserva(r_id):
    reserva = buscar_reserva(reservas,r_id)
    if not reserva:
        return jsonify({"error":"not_found"}),404

    data = request.get_json(force=True,silent=True) or {}
    if "pasajero" in data: reserva["pasajero"] = (data.get("pasajero") or "").strip()
    if "asiento" in data: reserva["asiento"] = (data.get("asiento") or "").strip()
    if "vuelo_id" in data:
        try:
            reserva_id = int(data["vuelo_id"])
            if reserva_id <= 0:
                raise ValueError()
            reserva["vuelo_id"] = reserva_id
        except Exception:
            return jsonify({"error":"vuelo_id invalido"}), 400
    return jsonify(reserva)


@app.delete("/reservas/<int:r_id>")
def eliminar_reserva(r_id:int):
    global reservas

    existe = buscar_reserva(reservas, r_id)

    if not existe:
        return jsonify({"error":"not_found"}), 404

    reservas = [reserva for reserva in reservas if reserva["id"]!= r_id]

    return "reserva eliminada", 201


if __name__  == "__main__":
    app.run(port=PORT,debug=True)
