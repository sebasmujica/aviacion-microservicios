import sqlite3

def buscar_aeronave(aeronaves,aircraft_id:int):
    return next((aircraft for aircraft in aeronaves if aircraft["id"]== aircraft_id), None)


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

def agregar_a_db(db,modelo,capacidad):

    conn = get_conn(db)
    cur = conn.cursor()

    cur.execute("INSERT INTO aeronaves (modelo, capacidad) VALUES (?,?) ", (modelo,capacidad) )
    id_aeronave = cur.lastrowid

    conn.commit()
    conn.close()

    return id_aeronave

def consultar_a_db(db,sql, params = ()):

    conn = get_conn(db)
    cur = conn.cursor()

    cur.execute(sql, params)
    rows = cur.fetchall()

    datos= [dict(row) for row in rows]

    conn.commit()
    conn.close()

    return datos