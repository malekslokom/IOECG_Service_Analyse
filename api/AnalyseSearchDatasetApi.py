import json
from datetime import datetime
from flask import jsonify, request
from models.datasets import db,Analyses, Datasets, AnalysesDatasets,Patient,Ecg,EcgLead
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def get_patient_filters():
    
    patients = Patient.query.with_entities(Patient.age).distinct()  
    age_filters = [patient.age for patient in patients]
    height_filters = [patient.height for patient in Patient.query.with_entities(Patient.height).distinct()]
    weight_filters = [patient.weight for patient in Patient.query.with_entities(Patient.weight).distinct()]
    sex_filters = [patient.sex for patient in Patient.query.with_entities(Patient.sex).distinct()]
    return jsonify({'age': age_filters, 'height': height_filters, 'weight': weight_filters, 'sex': sex_filters})

def get_datasets_filters():
    name_dataset_filters = [dataset.name_dataset for dataset in Datasets.query.with_entities(Datasets.name_dataset).distinct()]
    source_name_filters = [dataset.source_name for dataset in Datasets.query.with_entities(Datasets.source_name).distinct()]
    study_name_filters = [dataset.study_name for dataset in Datasets.query.with_entities(Datasets.study_name).distinct()]
    return jsonify({'name_dataset': name_dataset_filters,  'source_name': source_name_filters, 'study_name': study_name_filters})

from sqlalchemy import and_

def get_filters_data():
    data = request.json

    age = data.get('age')
    height = data.get('height')
    weight = data.get('weight')
    sex = data.get('sex')
    source_name = data.get('source_name')
    study_name = data.get('study_name')

    try:
        query = db.session.query(Datasets, Patient, Ecg, EcgLead).\
            join(Patient, Datasets.id_dataset == Patient.dataset_id).\
            join(Ecg, Ecg.id_patient == Patient.id).\
            join(EcgLead, Ecg.id_ecg == EcgLead.ecg_id)

        if age:
            query = query.filter(Patient.age == age)
        if height:
            query = query.filter(Patient.height == height)
        if weight:
            query = query.filter(Patient.weight == weight)
        if sex:
            query = query.filter(Patient.sex == sex)
        if source_name:
            query = query.filter(Datasets.source_name == source_name)
        if study_name:
            query = query.filter(Datasets.study_name == study_name)

        results = query.all()

        response_data = []
        for dataset, patient, ecg, ecg_lead in results:
            response_data.append({
            'patient_id': patient.id,
            'age': patient.age,
            'height': patient.height,
            'weight': patient.weight,
            'sex': patient.sex,
            
            # ECG information
            'id_ecg':ecg.id_ecg,
            'recording_started_at': ecg.recording_started_at,
            'recording_ended_at': ecg.recording_ended_at,
            'recording_initial_sampling_rate': ecg.recording_initial_sampling_rate,
            'recording_sampling_rate': ecg.recording_sampling_rate,
            'recording_duration': ecg.recording_duration,
            'protocol_details': ecg.protocol_details,
            'ecg_filepath': ecg.filepath,
            # ECG lead information
            'lead_i': ecg_lead.lead_i,
            'lead_ii': ecg_lead.lead_ii,
            'lead_iii': ecg_lead.lead_iii,
            'lead_avr': ecg_lead.lead_avr,
            'lead_avf': ecg_lead.lead_avf,
            'lead_avl': ecg_lead.lead_avl,
            'lead_v1': ecg_lead.lead_v1,
            'lead_v2': ecg_lead.lead_v2,
            'lead_v3': ecg_lead.lead_v3,
            'lead_v4': ecg_lead.lead_v4,
            'lead_v5': ecg_lead.lead_v5,
            'lead_v6': ecg_lead.lead_v6,
            'lead_x': ecg_lead.lead_x,
            'lead_y': ecg_lead.lead_y,
            'lead_z': ecg_lead.lead_z,
            'lead_es': ecg_lead.lead_es,
            'lead_as': ecg_lead.lead_as,
            'lead_ai': ecg_lead.lead_ai,
            # dataset lead information
            "id_dataset": dataset.id_dataset,
            "created_at": dataset.created_at,
            "name_dataset": dataset.name_dataset,
            "description_dataset": dataset.description_dataset,
            "type_dataset": dataset.type_dataset,
            "leads_name": dataset.leads_name,
            "study_name": dataset.study_name,
            "study_details": dataset.study_details,
            "source_name": dataset.source_name,
            "source_details": dataset.source_details
        })
        return jsonify({'data': response_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()




def getAllDatasetEcgs():
    response_data_list = []

    query = db.session.query(Datasets, Patient, Ecg, EcgLead).\
            join(Patient, Datasets.id_dataset == Patient.dataset_id).\
            join(Ecg, Ecg.id_patient == Patient.id).\
            join(EcgLead, Ecg.id_ecg == EcgLead.ecg_id)

    results = query.all()
    print("???")
    print(results)
    for dataset, patient, ecg, ecg_lead in results:
        response_data = {
            'patient_id': patient.id,
            'age': patient.age,
            'height': patient.height,
            'weight': patient.weight,
            'sex': patient.sex,
            # dataset lead information
            "id_dataset": dataset.id_dataset,
            "created_at": dataset.created_at,
            "nameDataset": dataset.name_dataset,
            "descriptionDataset": dataset.description_dataset,
            "typeDataset": dataset.type_dataset,
            "leads_name": dataset.leads_name,
            "study_name": dataset.study_name,
            "study_details": dataset.study_details,
            "source_name": dataset.source_name,
            "source_details": dataset.source_details,
            # ECG information
            'id_ecg': ecg.id_ecg,
            'recording_started_at': ecg.recording_started_at,
            'recording_ended_at': ecg.recording_ended_at,
            'recording_initial_sampling_rate': ecg.recording_initial_sampling_rate,
            'recording_sampling_rate': ecg.recording_sampling_rate,
            'recording_duration': ecg.recording_duration,
            'protocol_details': ecg.protocol_details,
            'ecg_filepath': ecg.filepath,
            # ECG lead information
            'lead_i': ecg_lead.lead_i,
            'lead_ii': ecg_lead.lead_ii,
            'lead_iii': ecg_lead.lead_iii,
            'lead_avr': ecg_lead.lead_avr,
            'lead_avf': ecg_lead.lead_avf,
            'lead_avl': ecg_lead.lead_avl,
            'lead_v1': ecg_lead.lead_v1,
            'lead_v2': ecg_lead.lead_v2,
            'lead_v3': ecg_lead.lead_v3,
            'lead_v4': ecg_lead.lead_v4,
            'lead_v5': ecg_lead.lead_v5,
            'lead_v6': ecg_lead.lead_v6,
            'lead_x': ecg_lead.lead_x,
            'lead_y': ecg_lead.lead_y,
            'lead_z': ecg_lead.lead_z,
            'lead_es': ecg_lead.lead_es,
            'lead_as': ecg_lead.lead_as,
            'lead_ai': ecg_lead.lead_ai,
        }
        response_data_list.append(response_data)

    return response_data_list

