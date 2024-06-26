import json
from datetime import datetime
from flask import jsonify, request
from models.datasets import Rapport, db,Analyses, Datasets, AnalysesDatasets, AnalysesModeles, DatasetsECG, Experiences


def getAllExperiences():
    experiences = Experiences.query.all()
    # Créer une liste des données des experiences pour les renvoyer au client
    serialized_experiences = [{
        "id_experience": experience.id_experience,
        'id_analysis_experience': experience.id_analysis_experience, 
        "name_experience": experience.name_experience,
        "models": experience.models,
        "datasets": experience.datasets,
        "nom_machine": experience.nom_machine,
        "nb_gpu": experience.nb_gpu,
        "nb_processeurs": experience.nb_processeurs,
        "heure_lancement": str(experience.heure_lancement),
        "heure_fin_prevu": str(experience.heure_fin_prevu),
        "statut": experience.statut
        } for experience in experiences]
    return jsonify(serialized_experiences)
            

def get_experiences_for_analysis(id_analyse):
    experiences = Experiences.query.filter_by(id_analysis_experience=id_analyse).all()  

    # Convertir les résultats en une liste JSON
    serialized_experiences = [{'id_experience': exp.id_experience, 
                        'id_analysis_experience': exp.id_analysis_experience, 
                        'name_experience': exp.name_experience,
                        "models": exp.models,
                        "datasets": exp.datasets,
                        "nom_machine": exp.nom_machine,
                        "nb_gpu": exp.nb_gpu,
                        "nb_processeurs": exp.nb_processeurs,
                        "heure_lancement":  str(exp.heure_lancement),
                        "heure_fin_prevu": str(exp.heure_fin_prevu),
                        "statut": exp.statut} 
                         for exp in experiences]
    return jsonify(serialized_experiences)

def delete_experiences_for_analysis(id_analysis):
    print(id_analysis)
    try:
        # Récupérer toutes les expériences où id_analysis_experience est égal à l'ID passé
        analysis_experiences = Experiences.query.filter_by(id_analysis_experience=id_analysis).all()

        if analysis_experiences:
            for experience in analysis_experiences:
                # Avant de supprimer l'expérience, supprimer tous les rapports associés
                associated_reports = Rapport.query.filter_by(id_experience_rapport=experience.id_experience).all()
                for report in associated_reports:
                    db.session.delete(report)  # Supprimer chaque rapport trouvé

                db.session.delete(experience)  # Supprimer l'expérience après avoir supprimé les rapports

            db.session.commit()
            return jsonify({"message": "All experiences and their associated reports for the analysis deleted with success"}), 201
        else:
            return jsonify({"error": "No experiences found for this analysis"}), 404
    except Exception as e:
        # Erreur, annuler les modifications et renvoyer un message d'erreur
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def getExperienceById(id_experience):
    experience = Experiences.query.filter_by(id_experience=id_experience).first()

    if experience:
        experience_data = {
            "id_experience": experience.id_experience,
            "id_analysis_experience" : experience.id_analysis_experience,
            "name_experience": experience.name_experience,
            "models": experience.models,
            "datasets": experience.datasets,
            "nom_machine": experience.nom_machine,
            "nb_gpu": experience.nb_gpu,
            "nb_processeurs": experience.nb_processeurs,
            "heure_lancement": str(experience.heure_lancement),
            "heure_fin_prevu": str(experience.heure_fin_prevu),
            "statut": experience.statut,
            "resultat_prediction": experience.resultat_prediction
    }
        return jsonify(experience_data)
    else:
        return jsonify({"error": "Experience not found"}), 404



def createExperience(id_analyse):
    data = request.json  
    
    print(id_analyse)

    id_analysis_experience = data.get('id_analysis_experience')
    name_experience = data.get('name_experience')
    models = data.get("models")
    datasets = data.get("datasets")
    nom_machine = data.get("nom_machine")
    nb_gpu = data.get("nb_gpu")
    nb_processeurs = data.get("nb_processeurs")
    heure_lancement = data.get("heure_lancement")
    heure_fin_prevu = data.get("heure_fin_prevu")
    resultat_prediction=data.get("resultat_prediction")
    statut = data.get("statut")
    
    print(models)
    print(datasets)
    # Convertir les chaînes de caractères en listes d'entiers
    # models = str(data.get("models")).replace('{{', '{').replace('}}', '}')  # Correction ici
    # datasets = str(data.get("datasets")).replace('{{', '{').replace('}}', '}')  # Correction ici

    

    print(data)

    # Création de la nouvelle experience
    new_experience = Experiences(id_analysis_experience=id_analysis_experience,name_experience=name_experience,models=models,
                                 datasets=datasets,nom_machine=nom_machine,nb_gpu=nb_gpu,
                                  nb_processeurs=nb_processeurs, heure_lancement=heure_lancement,
                                  heure_fin_prevu=heure_fin_prevu, statut=statut,resultat_prediction=resultat_prediction )   
    # Ajouter dans la bdd
    db.session.add(new_experience)
    try:
        # Valider et enregistrer les modifications dans la bdd
        db.session.commit()

        #Transmission de l'id_experience pour l'affichage immédiat des infos de l'experience
        id_experience = new_experience.id_experience

        return jsonify({"message": "Experience créé avec succès", "id_experience": id_experience}), 201
    except Exception as e:
        # Erreur, annuler les modifications et renvoyer un message d'erreur
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

def update_experience_status(id_experience):
    experience = Experiences.query.get(id_experience)
    if not experience:
        return jsonify({"error": "Experience non trouvée"}), 404
    
    data = request.json
    new_status = data.get("statut")
    if new_status is None:
        return jsonify({"error": "Champ 'statut' vide"}), 400
    
    experience.statut = new_status
    try:
        db.session.commit()
        return jsonify({"message": "Mise à jour du statut réussi"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
def update_experience_resultat(id_experience):
    experience = Experiences.query.get(id_experience)
    if not experience:
        return jsonify({"error": "Experience non trouvée"}), 404
    
    data = request.json
    new_resultat = data.get("resultat_prediction")
    if new_resultat is None:
        return jsonify({"error": "Champ 'resultat_prediction' vide"}), 400
    
    experience.resultat_prediction= new_resultat
    try:
        db.session.commit()
        return jsonify({"message": "Mise à jour du resultat_prediction réussi"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    


def deleteExperienceById(id_experience):
    print(id_experience)
    experience = Experiences.query.filter_by(id_experience=id_experience).first()  # on recupere l'experience à supprimer
    if experience:
        db.session.delete(experience)
        db.session.commit()
        return jsonify({"message": "Experience deleted with success"}), 201
    else: 
        return jsonify({"error": "Experience not found"}), 404