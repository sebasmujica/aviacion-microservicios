import sqlite3
from dotenv import load_dotenv
import requests,os

load_dotenv()

VUELOS_URL = os.getenv("VUELOS_URL","http://localhost:5002")

def buscar_reserva(reservas,reserva_id:int):
    return next((reserva for reserva in reservas if reserva["id"]== reserva_id), None)

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

def agregar_a_db(db,pasajero,asiento,v_id):

    conn = get_conn(db)
    cur = conn.cursor()

    cur.execute("INSERT INTO reservas (pasajero, asiento, vuelo_id) VALUES (?,?,?) ", (pasajero,asiento,v_id) )
    id_reserva = cur.lastrowid

    conn.commit()
    conn.close()

    return id_reserva

def consultar_a_db(db,sql, params = ()):

    conn = get_conn(db)
    cur = conn.cursor()

    cur.execute(sql, params)
    rows = cur.fetchall()

    datos= [dict(row) for row in rows]

    conn.commit()
    conn.close()

    return datos

def consultar_id_vuelo(v_id):

    URL = f"{VUELOS_URL}/vuelos/{v_id}"

    try:
        r = requests.get(URL,timeout=10)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        data = r.json()
    except requests.RequestException:
        return None
    return data[0].get("id")