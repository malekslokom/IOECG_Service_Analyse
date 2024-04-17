from flask import Flask, jsonify,request
from flask_cors import CORS
import json

from consul import register_service_with_consul,SERVICE_PORT

from models.datasets import db

from config.config import Config
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)


from api.AnalyseApi import health, addAnalyse, getAllAnalyses, deleteAnalyseById, \
                            getAnalyseById, filter_data
app.route('/api/analyses/health') (health)

app.route('/api/analyses/new',methods=["POST"])(addAnalyse)
app.route('/api/analyses/allAnalyse', methods=['GET'])(getAllAnalyses)
app.route('/api/analyses/delete/<int:id>',methods=["DELETE"])(deleteAnalyseById)
 
app.route('/api/analyses/<int:id>',methods=["GET"]) (getAnalyseById)   #fonction peut etre inutile car utilise les données statiques
app.route('/api/analyses/filter', methods=['GET']) (filter_data)    #fonction à revoir, données statiques


from api.AnalyseDatasetApi import getAllDatasetsTest, get_datasets_for_analysis, add_datasets_to_analysis,delete_dataset_from_analysis
from api.AnalyseSearchDatasetApi import get_patient_filters,get_datasets_filters,get_filters_data,getAllDatasetEcgs
from api.AnalyseModelApi import add_models_to_analysis,delete_model_from_analysis,get_models_for_analysis

app.route('/api/analyses/all', methods=['GET'])(getAllDatasetsTest)
app.route('/api/analyses/<int:id>/datasets', methods=['GET'])(get_datasets_for_analysis)
app.route('/api/analyses/<int:id>/datasets', methods=['POST'])(add_datasets_to_analysis)
app.route('/api/analyses/<int:id>/datasets/<int:id_dataset>', methods=['DELETE'])(delete_dataset_from_analysis)


app.route('/api/analyses/datasetSearch/patientFilters', methods=['GET'])(get_patient_filters)
app.route('/api/analyses/datasetSearch/datasetFilters', methods=['GET'])(get_datasets_filters)
app.route('/api/analyses/datasetSearch/filter', methods=['POST'])(get_filters_data)
app.route('/api/analyses/allTest',methods=["GET"])(getAllDatasetEcgs)


app.route('/api/analyses/<int:id>/models/<int:id_model>', methods=['DELETE'])(delete_model_from_analysis)
app.route('/api/analyses/<int:id>/models', methods=['GET'])(get_models_for_analysis)
app.route('/api/analyses/<int:id>/models', methods=['POST'])(add_models_to_analysis)
from api.AnalyseExperienceApi import get_experiences_for_analysis, getAllExperiences, createExperience, getExperienceById,\
                                    update_experience_status

app.route('/api/analyses/experiences/all/', methods=['GET'])(getAllExperiences)
app.route('/api/analyses/<int:id_analyse>/experiences', methods=['GET'])(get_experiences_for_analysis)
app.route('/api/analyses/experiences/<int:id_experience>', methods=['GET'])(getExperienceById)
app.route('/api/analyses/<int:id_analyse>/experiences', methods=['POST'])(createExperience)
app.route('/api/analyses/experiences/<int:id_experience>/update-status', methods=['PUT'])(update_experience_status)


if __name__ == "__main__":
   
    register_service_with_consul()
    app.run(debug=True, port=SERVICE_PORT, host='0.0.0.0')  # Utilisez '0.0.0.0' pour rendre votre service accessible à partir d'autres machines sur le réseau
