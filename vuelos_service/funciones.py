import sqlite3
from dotenv import load_dotenv
import requests,os

load_dotenv()

AERONAVES_URL = os.getenv("AERONAVES_URL", "http://localhost:5001")

#TODO Eliminar
def buscar_vuelo(vuelos,vuelo_id:int):
    return next((vuelo for vuelo in vuelos if vuelo["id"]== vuelo_id), None)

def get_conn(db):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db,sql_script):

    conn = get_conn(db)
    cur = conn.cursor()

    cur.execute(sql_script)

    conn.commit()
    conn.close()

def agregar_a_db(db,origen,destino,fecha,a_id):

    conn = get_conn(db)
    cur = conn.cursor()

    cur.execute("INSERT INTO vuelos (origen, destino, fecha, aeronave_id) VALUES (?,?,?,?) ", (origen,destino,fecha,a_id) )
    id_vuelo = cur.lastrowid

    conn.commit()
    conn.close()

    return id_vuelo

def consultar_a_db(db,sql, params = ()):

    conn = get_conn(db)
    cur = conn.cursor()

    cur.execute(sql, params)
    rows = cur.fetchall()

    datos= [dict(row) for row in rows]

    conn.commit()
    conn.close()

    return datos

def consultar_id_aeronaves(aid):

    URL = f"{AERONAVES_URL}/aeronaves/{aid}"

    try:
        r = requests.get(URL,timeout=10)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        data = r.json()
    except requests.RequestException:
        return None
    print(data)
    return data[0].get("id")