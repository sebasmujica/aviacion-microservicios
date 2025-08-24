from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from funciones import buscar_reserva, init_db,agregar_a_db,consultar_a_db,consultar_id_vuelo

load_dotenv()

PORT = int(os.getenv("PORT","5003"))
DB = "reservas.db"

sql_script = '''
    CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pasajero TEXT NO NULL,
    asiento TEXT NO NULL,
    vuelo_id INTEGER NO NULL)'''

init_db(DB,sql_script)

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
    sql = "SELECT * FROM reservas"
    reservas = consultar_a_db(DB,sql)
    return jsonify(reservas)

@app.get("/reservas/<int:r_id>")
def obtener_reserva(r_id):
    sql = "SELECT * FROM reservas WHERE id = ?"
    reserva = consultar_a_db(DB,sql,(r_id,))
    if not reserva:
        return jsonify({"error":"not_found"}),404
    return jsonify(reserva)


@app.post("/reservas")
def crear_reserva():

    data = request.get_json(force=True,silent=True) or {}

    
    pasajero =(data.get("pasajero") or "").strip()
    asiento = (data.get("asiento") or "").strip()
    vuelo_id = int(data["vuelo_id"])
    if not pasajero or not asiento or not vuelo_id:
        return jsonify({"error":"campos requeridos"}),400

    v_id = consultar_id_vuelo(vuelo_id)
    if v_id is None:
        return jsonify({"error":"Vuelo no encontrado o servicio no disponible"}), 404

    nuevo_id = agregar_a_db(DB,pasajero,asiento,v_id)
    reserva = {"id":nuevo_id,"vuelo_id":v_id,"pasajero":pasajero,"asiento":asiento}

    return jsonify(reserva),201

@app.put("/reservas/<int:r_id>")
def modificar_reserva(r_id):

    sql = "SELECT * FROM reservas WHERE id = ?"
    sql_update = "UPDATE reservas SET pasajero= ?, asiento = ?, vuelo_id = ? WHERE id = ?"

    reserva = consultar_a_db(DB,sql,(r_id,))
    if not reserva:
        return jsonify({"error":"not_found"}),404

    data = request.get_json(force=True,silent=True) or {}
    pasajero= (data.get("pasajero") or "").strip()
    asiento = (data.get("asiento") or "").strip()
    vuelo_id = data.get("vuelo_id")

    if not pasajero or not asiento or not vuelo_id :
        return jsonify({"error":"campos requeridos"}), 400

    v_id = consultar_id_vuelo(vuelo_id)
    if v_id is None:
        return jsonify({"error":"Vuelo no encontrado o servicio no disponible"}),404

    consultar_a_db(DB,sql_update,(pasajero,asiento,v_id,r_id))
    reserva = consultar_a_db(DB,sql,(r_id,))

    return jsonify(reserva), 200


@app.delete("/reservas/<int:r_id>")
def eliminar_reserva(r_id):

    sql = "SELECT * FROM reservas WHERE id = ?"
    sql_delete = "DELETE FROM reservas WHERE id = ?"

    existe = consultar_a_db(DB,sql,(r_id,))

    if not existe:
        return jsonify({"error":"not_found"}), 404

    consultar_a_db(DB,sql_delete,(r_id,))

    return "reserva eliminada", 204


if __name__  == "__main__":
    app.run(port=PORT,debug=True)
