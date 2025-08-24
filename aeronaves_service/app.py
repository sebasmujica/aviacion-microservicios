from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from auth import verificar_autorizacion
from funciones import buscar_aeronave, init_db, agregar_a_db, consultar_a_db

load_dotenv()

PORT = int(os.getenv("PORT","5001"))
DB = "aeronaves.db"

sql_script = '''
        CREATE TABLE IF NOT EXISTS  aeronaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        modelo TEXT NO NULL,
        capacidad INTEGER NO NULL
        )
'''

init_db(DB,sql_script)

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
    sql = "SELECT * FROM aeronaves"
    aeronaves = consultar_a_db(DB,sql)
    return jsonify(aeronaves)

#Devuelve la aeronave seleccionada por id
@app.get("/aeronaves/<int:aid>")
def obtener_aeronave(aid:int):
    sql = "SELECT * FROM aeronaves WHERE id = ?"

    a = consultar_a_db(DB,sql,(aid,))

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

    nuevo_id = agregar_a_db(DB,modelo,capacidad)
    nueva_aeronave = {"id": nuevo_id, "modelo": modelo, "capacidad": capacidad}

    return jsonify(nueva_aeronave), 201

#Para actualizar aeronaves
@app.put("/aeronaves/<int:aid>")
def actualizar_aeronave(aid):

    sql = "SELECT * FROM aeronaves WHERE id = ?"
    sql_update = "UPDATE aeronaves SET modelo= ?, capacidad = ? WHERE id = ?"

    a = consultar_a_db(DB,sql,(aid,))

    if not a:
        return jsonify({"error":"not_found"}), 404
    
    data = request.get_json(force=True,silent=True) or {}

    if "modelo" in data:
        modelo = (data.get("modelo") or "").strip()

    else:
        return jsonify({"error":"modelo_invalido"}), 400
    
    if "capacidad" in data:
        try:
            cap = int(data.get("capacidad") or 0)
            if cap <= 0:
                raise ValueError()
        except Exception:
            return jsonify({"error":"capacidad-invalida"}), 400
    else:
        return jsonify({"error":"capacidad-invalida"}), 400

    _ = consultar_a_db(DB,sql_update,(modelo,cap,aid))
    a = consultar_a_db(DB,sql,(aid,))
    
    return jsonify(a)

#Para eliminar aeronaves
@app.delete("/aeronaves/<int:aid>")
def eliminar_aeronave(aid):

    sql = "SELECT * FROM aeronaves WHERE id = ?"
    existe =  consultar_a_db(DB,sql,(aid,))
    sql_delete = "DELETE FROM aeronaves WHERE id = ?"

    if not existe:
        return jsonify({"error":"not_found"}), 404
    consultar_a_db(DB,sql_delete,(aid,)) 
    return "aeronave eliminada",201


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
