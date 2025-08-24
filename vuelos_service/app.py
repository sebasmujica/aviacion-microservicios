from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from funciones import buscar_vuelo, init_db, agregar_a_db, consultar_a_db, consultar_id_aeronaves
from auth import verificar_autorizacion

load_dotenv()

PORT = int(os.getenv("PORT", "5002"))
DB = "vuelos.db"

sql_script = '''
        CREATE TABLE IF NOT EXISTS  vuelos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origen TEXT NO NULL,
        destino TEXT NO NULL,
        fecha TEXT NO NULL,
        aeronave_id INTEGER NO NULL
        )
'''
init_db(DB,sql_script)

app = Flask(__name__)

app.before_request(verificar_autorizacion)

@app.get("/")
def home():
    return "<h1>Servicio de Vuelos activo </h1>"

@app.get("/health")
def status():
    return jsonify({
        "service": "vuelos",
        "status": "ok"
    })

#Obtener la lista de todos los vuelos
@app.get("/vuelos")
def listar_vuelos():
    sql = "SELECT * FROM vuelos"
    vuelos = consultar_a_db(DB,sql)
    return jsonify(vuelos)

#Obtener un vuelo en específico mediante el ID
@app.get("/vuelos/<int:v_id>")
def obtener_vuelo(v_id:int):
    sql = "SELECT * FROM vuelos WHERE id = ?"
    vuelo = consultar_a_db(DB,sql,(v_id,))
    if not vuelo:
        return jsonify({"error":"not_found"}),404
    else:
        return jsonify(vuelo)

@app.post("/vuelos")
def crear_vuelo():

    data = request.get_json(force= True, silent=True) or {}
    origen = (data.get("origen") or "").strip()
    destino = (data.get("destino") or "").strip()
    fecha = (data.get("fecha") or "").strip()
    aeronave_id = data["aeronave_id"]

    if not origen or not destino or not fecha or not aeronave_id:
        return jsonify({"error":"campos requeridos"}),400

    a_id = consultar_id_aeronaves(aeronave_id)
    if a_id is None:
        return jsonify({"error": "Aeronave no encontrada o servicio no disponible"}), 404

    nuevo_id = agregar_a_db(DB,origen, destino, fecha, a_id)

    vuelo = {"id": nuevo_id, "origen":origen, "destino": destino, "fecha":fecha, "aeronave_id":a_id}

    return jsonify(vuelo), 201

@app.put("/vuelos/<int:v_id>")
def modificar_vuelo(v_id:int):
    sql = "SELECT * FROM vuelos WHERE id = ?"
    sql_update = "UPDATE vuelos SET origen= ?, destino = ?, fecha= ?, aeronave_id= ? WHERE id = ?"
    vuelo = consultar_a_db(DB,sql,(v_id,))

    if not vuelo:
        return jsonify({"error": "not_found"}),404
    
    data = request.get_json(force=True, silent=False) or {}
    origen = (data.get("origen") or "").strip()
    destino = (data.get("destino") or "").strip()
    fecha = (data.get("fecha") or "").strip()
    aeronave_id = data["aeronave_id"]

    if not origen or not destino or not fecha or not aeronave_id:
        return jsonify({"error":"campos requeridos"}),400

    a_id = consultar_id_aeronaves(aeronave_id)
    if a_id is None:
        return jsonify({"error": "Aeronave no encontrada o servicio no disponible"}), 404

    consultar_a_db(DB,sql_update,(origen,destino,fecha,a_id,v_id))
    vuelo = consultar_a_db(DB,sql,(v_id,))


    return jsonify(vuelo)


@app.delete("/vuelos/<int:v_id>")
def eliminar_vuelo(v_id:int):

    sql = "SELECT * FROM vuelos WHERE id = ?"
    existe =  consultar_a_db(DB,sql,(v_id,))
    sql_delete = "DELETE FROM vuelos WHERE id = ?"

    if not existe:
        return jsonify({"error":"not_found"}), 404

    consultar_a_db(DB,sql_delete,(v_id,))

    return "vuelo eliminado", 201


if __name__  == "__main__":
    app.run(port=PORT,debug=True)