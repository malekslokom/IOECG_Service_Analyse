import requests
import json
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
