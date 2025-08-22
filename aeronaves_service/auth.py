from flask import Flask,request,jsonify
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_TOKEN = os.getenv("SERVICE_TOKEN")

def token_valido():
    auth = request.headers.get("Authorization", "")
    return auth.startswith("Bearer ") and auth.split(" ",1)[1] == SERVICE_TOKEN


def verificar_autorizacion():
    if request.method in ["POST", "PUT", "DELETE"]:
        if not token_valido():
            return jsonify({"error":"unauthorized"}), 401