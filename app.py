from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Configuration de service
SERVICE_NAME = "analyses"
SERVICE_PORT = 5002
CONSUL_AGENT_URL = "http://localhost:8500/v1/agent/service/register"

# Fonction pour enregistrer le service auprès de Consul
def register_service_with_consul():
    service_info = {
        "name": SERVICE_NAME,
        "tags": ["analyses", "flask"],
        "port": SERVICE_PORT,
        "check": {
            "http": f"http://127.0.0.1:{SERVICE_PORT}/api/{SERVICE_NAME}/health",
            "interval": "10s"
        }
    }

    try:
        response = requests.put(CONSUL_AGENT_URL, data=json.dumps(service_info))
        if response.status_code == 200:
            print("Service enregistré avec succès dans Consul.")
        else:
            print("Erreur lors de l'enregistrement du service dans Consul:", response.text)
    except Exception as e:
        print("Erreur lors de la communication avec Consul:", str(e))

@app.route('/api/analyses/health')
def health():
    return jsonify({"status": "up"})

@app.route('/api/analyses/')
def getAll():
    print("here")
    data = [
        {"nom": "Analyse 1","dateCreation": "01/01/24", "auteur": "Andy", "description": "Description 1"},
        { "nom": "Analyse 2","dateCreation": "01/01/24", "auteur": "Andy", "description": "Description 2"},
        { "nom": "Analyse 3","dateCreation": "01/01/24", "auteur": "Andy", "description": "Description 3"},
        { "nom": "Analyse 4","dateCreation": "01/01/24", "auteur": "Andy", "description": "Description 4"}

    ]
    return jsonify(data)

if __name__ == "__main__":
    register_service_with_consul()
    app.run(debug=True, port=SERVICE_PORT, host='0.0.0.0')  # Utilisez '0.0.0.0' pour rendre votre service accessible à partir d'autres machines sur le réseau
