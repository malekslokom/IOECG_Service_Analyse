
import json
from datetime import datetime
from flask import jsonify, request
from models.datasets import db,Model,AnalysesModeles
from sqlalchemy import func
            
def get_models_for_analysis(id):
    print(id)
    try:
        models = Model.query.join(AnalysesModeles, AnalysesModeles.id_model == Model.id) \
                                  .filter(AnalysesModeles.id_analysis == id) \
                                  .all()
        serialized_datasets=[]
        for model in models:
            serialized_datasets.append({
                "id": model.id,
                "name": model.name,
                "author": model.author,
                "project_name": model.project_name,
                "description": model.description,
                "architecture_name": model.architecture_name,
                "architecture_version": model.architecture_version,
                "architecture_description": model.architecture_description,
                "total_params": model.total_params,
                "model_size": model.model_size,
                'batch_size': model.batch_size,
                'learning_rate': model.learning_rate,
                'task_nature': model.task_nature
            })
        return jsonify(serialized_datasets)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def add_models_to_analysis(id):
    db.session.flush()
    try:
        new_models_data = request.json
        print(new_models_data)
        # Ajouter les nouvelles datasets à l'analyse dans la base de données
        for model_data in new_models_data:
            iddmodel = model_data['id']
            # Check if the association already exists
            existing_association = AnalysesModeles.query.filter_by(id_analysis=id, id_model=iddmodel).first()
            if not existing_association:
                # If association doesn't exist, add it
                new_association = AnalysesModeles(id_analysis=id, id_model=iddmodel)
                print(new_association)
                db.session.add(new_association)
        
        db.session.commit()
        return get_models_for_analysis(id)
    except Exception as e:
        db.session.rollback()  
        print("Error: ", str(e))
        return jsonify({"error": str(e)}), 500 
    
def delete_model_from_analysis(id, id_model):
    try:
        analysis_model = AnalysesModeles.query \
            .filter_by(id_analysis=id, id_model=id_model) \
            .first()

        if not analysis_model:
            return jsonify({'error': 'Analysis model association not found'}), 404

        db.session.delete(analysis_model)
        db.session.commit()

        return jsonify({'message': 'Model deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
def delete_models_for_analysis(id_analysis):
    print(id_analysis)
    try:
        # Récupérer tous les enregistrements de AnalysesModeles où id_analysis est égal à l'ID passé
        analysis_models = AnalysesModeles.query.filter_by(id_analysis=id_analysis).all()

        if analysis_models:
            for model in analysis_models:
                db.session.delete(model)  # Supprimer chaque enregistrement trouvé
            db.session.commit()
            return jsonify({"message": "All models for the analysis deleted with success"}), 201
        else:
            return jsonify({"error": "No models found for this analysis"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500