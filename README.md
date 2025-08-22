# ✈️ Aviación – Microservicios

Proyecto en Flask para practicar microservicios con un tema de aviación.

## 📦 Servicios
- **Aeronaves** → registra aeronaves (puerto 5001)
- **Vuelos** → gestiona vuelos (puerto 5002)
- **Reservas** → gestiona reservas (puerto 5003)

## ▶️ Cómo ejecutar
Ejemplo para **Aeronaves**:
```bash
cd aeronaves_service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py

Codigo  Significado
200     OK → lecturas y actualizaciones correctas.
201     Created → creación.
204     No Content → borrado.
400     Bad Request → datos inválidos.
401     Unauthorized → falta/incorrecto token.
404     Not Found → id inexistente.