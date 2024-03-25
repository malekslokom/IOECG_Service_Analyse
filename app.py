from flask import Flask, jsonify,request
from flask_cors import CORS
import json
from consul import register_service_with_consul,SERVICE_PORT
from datetime import datetime
from models.analyses import db
from config.config import Config
from models.analyses import Analyses, Datasets, AnalysesDatasets 

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

@app.route('/api/analyses/health')
def health():
    return jsonify({"status": "up"})

@app.route('/api/analyses/')
def getAll():
    with open('analyseStaticData.json') as f: 
        data = json.load(f)
    return jsonify(data)

@app.route('/api/analyses/<int:id>',methods=["GET"])
def getAnalyseById(id):
    print(id)
    with open('analyseStaticData.json') as f: 
        analyses = json.load(f)
        analyse=[item for item in analyses if item["id"] ==id]
    if analyses:
        return jsonify(analyse[0])
    else:
        return jsonify({"error": "Analyse not found"}), 404

def convert_date(date_str):
    """Converts a date string from DD-MM-YYYY to a datetime object."""
    return datetime.strptime(date_str, "%d-%m-%Y")

@app.route('/api/analyses/filter', methods=['GET'])
def filter_data():
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    search_term = request.args.get('search_term', '').lower()
    # Convert the start and end dates from DD-MM-YYYY to datetime objects
    start_date = convert_date(start_date_str) if start_date_str else None
    end_date = convert_date(end_date_str) if end_date_str else None

    with open('analyseStaticData.json') as f:
        data = json.load(f)
        filtered_data = []
        for item in data:
            item_date = convert_date(item['dateCreation'])
            if ((not start_date or item_date >= start_date) and
                (not end_date or item_date <= end_date) and
                (not search_term or search_term in item['nom'].lower() or search_term in item['type'].lower())):
                filtered_data.append(item)

        if filtered_data:
            return jsonify(filtered_data)
        else:
            return jsonify({"error": "No analyse found matching the criteria"}), 404

            
@app.route('/api/analyses/all', methods=['GET'])
def getAlla():
    # Récupérer tous les modèles depuis la base de données
    datasets = Datasets.query.all()
    # Créer une liste des données des modèles pour les renvoyer au client
    serialized_datasets = [{
            "iddataset": dataset.iddataset,
            "created_at": dataset.created_at,
            "nameDataset": dataset.namedataset,
            "descriptionDataset": dataset.descriptiondataset,
            "typeDataset": dataset.typedataset,
            "leads_name": dataset.leads_name,
            "study_name": dataset.study_name,
            "study_details": dataset.study_details,
            "source_name": dataset.source_name,
            "source_details": dataset.source_details
        } for dataset in datasets]
    return jsonify(serialized_datasets)

@app.route('/api/analyses/<int:id>/datasets', methods=['GET'])
def get_datasets_for_analysis(id):
    try:
        # Fetch the datasets associated with the analysis
        datasets = Datasets.query.join(AnalysesDatasets, AnalysesDatasets.iddataset == Datasets.iddataset) \
                                  .filter(AnalysesDatasets.idanalysis == id) \
                                  .all()

        # Serialize datasets to JSON format
        serialized_datasets = [{
            "idDataset": dataset.iddataset,
            "created_at": dataset.created_at,
            "nameDataset": dataset.namedataset,
            "descriptionDataset": dataset.descriptiondataset,
            "typeDataset": dataset.typedataset,
            "leads_name": dataset.leads_name,
            "study_name": dataset.study_name,
            "study_details": dataset.study_details,
            "source_name": dataset.source_name,
            "source_details": dataset.source_details
        } for dataset in datasets]

        return jsonify(serialized_datasets), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyses/<int:id>/datasets', methods=['POST'])
def add_datasets_to_analysis(id):
    try:
        # Récupérer les données de la nouvelle dataset depuis la requête
        new_datasets_data = request.json
        print(new_datasets_data)
        # Ajouter les nouvelles datasets à l'analyse dans la base de données
        for dataset_data in new_datasets_data:
            print("dataset_data " + str(dataset_data))  # Convertir en chaîne de caractères
            # Extract the iddataset from the dataset_data
            iddataset = dataset_data['iddataset']
            print("iddataset " + str(iddataset))  
            # Insérer l'association dans la table 'AnalysesDatasets'
            new_association = AnalysesDatasets(idanalysis=id, iddataset=iddataset)
            print(new_association)
            db.session.add(new_association)
        
        # Commit des changements dans la base de données
        db.session.commit()

        # Rafraîchir les données des datasets de l'analyse après l'ajout des nouvelles datasets
        updated_datasets = Datasets.query.join(AnalysesDatasets, AnalysesDatasets.iddataset == Datasets.iddataset) \
                                  .filter(AnalysesDatasets.idanalysis == id) \
                                  .all()

        # Serialize datasets to JSON format
        serialized_datasets = [{
            "idDataset": dataset.iddataset,
            "created_at": dataset.created_at,
            "nameDataset": dataset.namedataset,
            "descriptionDataset": dataset.descriptiondataset,
            "typeDataset": dataset.typedataset,
            "leads_name": dataset.leads_name,
            "study_name": dataset.study_name,
            "study_details": dataset.study_details,
            "source_name": dataset.source_name,
            "source_details": dataset.source_details
        } for dataset in updated_datasets]

        return jsonify(serialized_datasets), 200
    except Exception as e:
        db.session.rollback()  # Rollback en cas d'erreur pour annuler les changements
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    register_service_with_consul()
    app.run(debug=True, port=SERVICE_PORT, host='0.0.0.0')  # Utilisez '0.0.0.0' pour rendre votre service accessible à partir d'autres machines sur le réseau
