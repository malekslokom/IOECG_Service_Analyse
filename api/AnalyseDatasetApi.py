import json
from datetime import datetime
from flask import jsonify, request
from models.analyses import db,Analyses, Datasets, AnalysesDatasets,Patient,Ecg ,EcgLead
from sqlalchemy import func
            
def getAllDatasetsTest():
    datasets = Datasets.query.all()
    # Créer une liste des données des modèles pour les renvoyer au client
    serialized_datasets = [{
        "idDataset": dataset.id_dataset,
        "created_at": dataset.created_at,
        "nameDataset": dataset.name_dataset,
        "descriptionDataset": dataset.description_dataset,
        "typeDataset": dataset.type_dataset,
        "leads_name": dataset.leads_name,
        "study_name": dataset.study_name,
        "study_details": dataset.study_details,
        "source_name": dataset.source_name,
        "source_details": dataset.source_details
        } for dataset in datasets]
    return jsonify(serialized_datasets)


def get_datasets_for_analysis(id):
    try:
        datasets = Datasets.query.join(AnalysesDatasets, AnalysesDatasets.id_dataset == Datasets.id_dataset) \
                                  .filter(AnalysesDatasets.id_analysis == id) \
                                  .all()

        serialized_datasets=[]
        for dataset in datasets:
            num_patients = Patient.query.filter_by(dataset_id=dataset.id_dataset).count()
            num_ecgs = Ecg.query.join(EcgLead).filter_by(dataset_id=dataset.id_dataset).count()
            print(num_ecgs)
            serialized_datasets.append({
                "idDataset": dataset.id_dataset,
                "created_at": dataset.created_at,
                "nameDataset": dataset.name_dataset,
                "descriptionDataset": dataset.description_dataset,
                "typeDataset": dataset.type_dataset,
                "leads_name": dataset.leads_name,
                "study_name": dataset.study_name,
                "study_details": dataset.study_details,
                "source_name": dataset.source_name,
                "source_details": dataset.source_details,
                'numPatients': num_patients,
                'numECGs': num_ecgs
            })

        return jsonify(serialized_datasets), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def add_datasets_to_analysis(id):
    try:
        new_datasets_data = request.json
        # Ajouter les nouvelles datasets à l'analyse dans la base de données
        for dataset_data in new_datasets_data:
            iddataset = dataset_data['idDataset']
            new_association = AnalysesDatasets(id_analysis=id, id_dataset=iddataset)
            db.session.add(new_association)
        
        db.session.commit()

        # Rafraîchir les données des datasets de l'analyse après l'ajout des nouvelles datasets
        updated_datasets = Datasets.query.join(AnalysesDatasets, AnalysesDatasets.id_dataset == Datasets.id_dataset) \
                                  .filter(AnalysesDatasets.id_analysis == id) \
                                  .all()

        serialized_datasets = [{
            "idDataset": dataset.id_dataset,
            "created_at": dataset.created_at,
            "nameDataset": dataset.name_dataset,
            "descriptionDataset": dataset.description_dataset,
            "typeDataset": dataset.type_dataset,
            "leads_name": dataset.leads_name,
            "study_name": dataset.study_name,
            "study_details": dataset.study_details,
            "source_name": dataset.source_name,
            "source_details": dataset.source_details
        } for dataset in updated_datasets]

        return jsonify(serialized_datasets), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": str(e)}), 500


def delete_dataset_from_analysis(id, id_dataset):
    try:
        analysis_dataset = AnalysesDatasets.query \
            .filter_by(id_analysis=id, id_dataset=id_dataset) \
            .first()

        if not analysis_dataset:
            return jsonify({'error': 'Analysis dataset association not found'}), 404

        db.session.delete(analysis_dataset)
        db.session.commit()

        return jsonify({'message': 'Dataset deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
