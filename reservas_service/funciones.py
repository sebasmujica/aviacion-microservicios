


def buscar_reserva(reservas,reserva_id:int):
    return next((reserva for reserva in reservas if reserva["id"]== reserva_id), None)