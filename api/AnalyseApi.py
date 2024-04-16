
from flask import jsonify, request
from datetime import datetime
from models.datasets import db,Analyses, Datasets, AnalysesDatasets 
import json


def health():
    return jsonify({"status": "up"})



def addAnalyse():
    data = request.json

    # Extraction des données depuis la requête
    id_project = data.get('id_project')
    name_analysis = data.get('name_analysis')
    description_analysis = data.get('description_analysis')
    created_by = data.get('created_by')

    # Validation des données nécessaires
    if not all([id_project, name_analysis, created_by]):
        return jsonify({"error": "Veuillez fournir toutes les données requises"}), 400

    # Création de la nouvelle Analyse
    new_analysis = Analyses(id_project=id_project, name_analysis=name_analysis,
                           description_analysis=description_analysis, created_by=created_by)

    # Ajout à la session de la base de données
    db.session.add(new_analysis)

    try:
        # Commit de la transaction
        db.session.commit()
        return jsonify({"message": "Analyse ajoutée avec succès"}), 201
    except Exception as e:
        # En cas d'erreur, rollback et renvoi d'un message d'erreur
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



def getAllAnalyses():
    # Récupérer toutes les analyses depuis la base de données
    all_analyses = Analyses.query.all()

    # Créer la liste des analyses pour les renvoyer au client
    serialized_analyses = [{
            "id_analysis": analysis.id_analysis,
            "id_project": analysis.id_project,
            "created_at": analysis.created_at,
            "last_updated_at": analysis.last_updated_at,
            "name_analysis": analysis.name_analysis,
            "description_analysis": analysis.description_analysis,
            "created_by": analysis.created_by
        } for analysis in all_analyses]

    return jsonify(serialized_analyses)


def deleteAnalyseById(id):
    print(id)
    analyse = Analyses.query.filter_by(id_analysis=id).first()  # on recupere l'analyse a supprimer
    if analyse:
        db.session.delete(analyse)
        db.session.commit()
        return jsonify({"message": "Analyse deleted with success"}), 201
    else: 
        return jsonify({"error": "Analyse not found"}), 404
   

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
