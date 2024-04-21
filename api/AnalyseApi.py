
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

    print(data)
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
    all_analyses = Analyses.query.order_by(Analyses.created_at.desc()).all()
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
    analyse = Analyses.query.filter_by(id_analysis=id).first()
    print(id)

    if analyse:

        analyse_data = {
            "id_analysis": analyse.id_analysis,
            "id_project": analyse.id_project,
            "created_at": analyse.created_at,
            "last_updated_at": analyse.last_updated_at,
            "name_analysis": analyse.name_analysis,
            "description_analysis": analyse.description_analysis,
            "created_by": analyse.created_by
        }
        return jsonify(analyse_data)
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

    query = Analyses.query
    if start_date:
        query = query.filter(Analyses.created_at >= start_date)
    if end_date:
        query = query.filter(Analyses.created_at <= end_date)
    if search_term:
        query = query.filter((Analyses.name_analysis.ilike(f'%{search_term}%')) |
                             (Analyses.description_analysis.ilike(f'%{search_term}%')) |
                             (Analyses.created_by.ilike(f'%{search_term}%')) )

    # Exécution de la requête et récupération des résultats
    filtered_analysis = query.all()

    if filtered_analysis:
        # Convertir les résultats en une liste de dictionnaires
        analyse_data=[{
            "id_analysis":analyse.id_analysis,
            "id_project":analyse.id_project,
            "created_at":analyse.created_at,
            "name_analysis":analyse.name_analysis,
            "description_analysis":analyse.description_analysis,
            "created_by":analyse.created_by        
        } for analyse in filtered_analysis]
        return jsonify(analyse_data)
        
    else:
        return jsonify({"error": "No analyse found matching the criteria"}), 404
