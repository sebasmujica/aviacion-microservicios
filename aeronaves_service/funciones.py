


def buscar_aeronave(aeronaves,aircraft_id:int):
    return next((aircraft for aircraft in aeronaves if aircraft["id"]== aircraft_id), None)