from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql.json import JSONB

db = SQLAlchemy()
class Model(db.Model):
    __tablename__ = 'modeles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    project_name = db.Column(db.String(255))
    description = db.Column(db.Text)
    architecture_name = db.Column(db.String(255))
    architecture_version = db.Column(db.String(50))
    architecture_description = db.Column(db.Text)
    total_params = db.Column(db.Integer)
    model_size = db.Column(db.String(50))
    batch_size = db.Column(db.Integer)
    learning_rate = db.Column(db.Float)
    task_nature = db.Column(db.String(50))
    __table_args__ = (
        CheckConstraint(task_nature.in_(['classification binaire', 'classification multi-class','régression']), name='check_task_nature'),
    )
    analyses = db.relationship('AnalysesModeles', backref='model', lazy=True)
class Projet(db.Model):
    __tablename__ = 'projets'

    id_project = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    last_updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    name_project = db.Column(db.String, nullable=False)
    description_project = db.Column(db.Text)
    created_by = db.Column(db.String, nullable=False)
    type_project = db.Column(db.String, nullable=False)

    __table_args__ = (
        db.CheckConstraint(type_project.in_(["Classification", "Régression", "Visualisation"]), name='check_type_project'),
    )
    # Define a one-to-many relationship with Analyses
    analyses = db.relationship('Analyses', backref='projet')


class Analyses(db.Model):
    __tablename__ = 'analyses'

    id_analysis = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_project = db.Column(db.Integer, db.ForeignKey('projets.id_project'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    last_updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    name_analysis = db.Column(db.String, nullable=False)
    description_analysis = db.Column(db.Text)
    created_by = db.Column(db.String, nullable=False)
    datasets = db.relationship('AnalysesDatasets', backref='analyse', lazy=True)
    modeles = db.relationship('AnalysesModeles', backref='analyse', lazy=True)

class Datasets(db.Model):
    __tablename__ = 'datasets'

    id_dataset = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=db.func.current_timestamp(), nullable=False)
    name_dataset = db.Column(db.String(), nullable=False)
    description_dataset = db.Column(db.Text, default=None)
    type_dataset = db.Column(db.String(), nullable=False)
    leads_name = db.Column(db.Text, nullable=False,default="")
    study_name = db.Column(db.String(), nullable=False,default="")
    study_details = db.Column(db.String(), default=None)
    source_name = db.Column(db.String(), nullable=False,default="")
    source_details = db.Column(db.String(), default=None)

    __table_args__ = (
        db.CheckConstraint(type_dataset.in_(["search_results", "standard"]), name='check_type_dataset'),
    )
    analyses = db.relationship('AnalysesDatasets', backref='dataset', lazy=True)


class AnalysesDatasets(db.Model):
    __tablename__ = 'analyses_datasets'

    id_dataset_analysis = db.Column(db.Integer, primary_key=True)
    id_dataset = db.Column(db.Integer, db.ForeignKey('datasets.id_dataset'))
    id_analysis = db.Column(db.Integer, db.ForeignKey('analyses.id_analysis'))

    # dataset = db.relationship('Datasets', back_populates='analyses_datasets', primaryjoin=iddataset == Datasets.iddataset)
    # analyse = db.relationship('Analyses', back_populates='datasets', primaryjoin=idAnalysis == Analyses.idAnalysis)
class AnalysesModeles(db.Model):
    __tablename__ = 'analyses_modeles'

    id_model_analysis = db.Column(db.Integer, primary_key=True)
    id_model = db.Column(db.Integer, db.ForeignKey('modeles.id'))
    id_analysis = db.Column(db.Integer, db.ForeignKey('analyses.id_analysis'))

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=func.current_timestamp(), nullable=False)
    last_updated_at = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id_dataset'), nullable=False)
    patient_original_id = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    birth_date = db.Column(db.String)
    height = db.Column(db.String)
    weight = db.Column(db.String)
    sex = db.Column(db.String)
    race = db.Column(db.String)
    observation = db.Column(db.Text)

    def __repr__(self):
        return f"<Patient(id={self.id}, created_at={self.created_at}, last_updated_at={self.last_updated_at}, dataset_id={self.dataset_id}, " \
               f"patient_original_id={self.patient_original_id}, age={self.age}, birth_date={self.birth_date}, " \
               f"height={self.height}, weight={self.weight}, sex={self.sex}, race={self.race}, observation={self.observation})>"
class Ecg(db.Model):
    __tablename__ = 'ecg'

    id_ecg = db.Column(db.Integer, primary_key=True)
    id_patient = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    origine_dataset = db.Column(db.Integer, nullable=True)
    filepath = db.Column(db.String, nullable=False)
    recording_started_at = db.Column(db.TIMESTAMP, nullable=False)
    recording_ended_at = db.Column(db.TIMESTAMP, nullable=False)
    recording_initial_sampling_rate = db.Column(db.Integer, nullable=False)
    recording_sampling_rate = db.Column(db.Integer, nullable=False)
    recording_duration = db.Column(db.Integer, nullable=False)
    protocol_details = db.Column(db.JSON)

class EcgLead(db.Model):
    __tablename__ = 'ecg_leads'

    id = db.Column(db.Integer, primary_key=True)
    ecg_id = db.Column(db.Integer, db.ForeignKey('ecg.id_ecg'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    dataset_id = db.Column(db.Integer, nullable=False)
    lead_i = db.Column(db.ARRAY(db.REAL))
    lead_ii = db.Column(db.ARRAY(db.REAL))
    lead_iii = db.Column(db.ARRAY(db.REAL))
    lead_avr = db.Column(db.ARRAY(db.REAL))
    lead_avf = db.Column(db.ARRAY(db.REAL))
    lead_avl = db.Column(db.ARRAY(db.REAL))
    lead_v1 = db.Column(db.ARRAY(db.REAL))
    lead_v2 = db.Column(db.ARRAY(db.REAL))
    lead_v3 = db.Column(db.ARRAY(db.REAL))
    lead_v4 = db.Column(db.ARRAY(db.REAL))
    lead_v5 = db.Column(db.ARRAY(db.REAL))
    lead_v6 = db.Column(db.ARRAY(db.REAL))
    lead_x = db.Column(db.ARRAY(db.REAL))
    lead_y = db.Column(db.ARRAY(db.REAL))
    lead_z = db.Column(db.ARRAY(db.REAL))
    lead_es = db.Column(db.ARRAY(db.REAL))
    lead_as = db.Column(db.ARRAY(db.REAL))
    lead_ai = db.Column(db.ARRAY(db.REAL))


class DatasetsECG(db.Model):
    __tablename__ = 'datasets_ecg'

    id_dataset = db.Column(db.Integer, db.ForeignKey('datasets.id_dataset'), primary_key=True)
    id_ecg = db.Column(db.Integer, db.ForeignKey('ecg.id_ecg'), primary_key=True)


class Experiences(db.Model):
    __tablename__ = 'experiences'
    id_analysis_experience = db.Column(db.Integer, db.ForeignKey('analyses.id_analysis'))
    id_experience = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_experience = db.Column(db.String)
    models = db.Column(ARRAY(db.Integer), nullable=False)
    datasets = db.Column(ARRAY(db.Integer), nullable=False)
    nom_machine = db.Column(db.String())
    nb_gpu = db.Column(db.Integer)
    nb_processeurs = db.Column(db.Integer)
    heure_lancement = db.Column(db.TIMESTAMP(timezone=True), default=db.func.current_timestamp(), nullable=False)
    heure_fin_prevu = db.Column(db.TIMESTAMP(timezone=True), default=db.func.current_timestamp())
    statut = db.Column(db.String(), nullable=False)
    resultat_prediction  = db.Column(JSONB, default=lambda: {})

    __table_args__ = (
        CheckConstraint(statut.in_(['En cours', 'Terminé']), name='check_statut'),
    )

class Rapport(db.Model):
    __tablename__ = 'rapports'

    id_rapport = db.Column(db.Integer, primary_key=True)
    id_experience_rapport = db.Column(db.Integer, db.ForeignKey('experiences.id_experience'), nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=db.func.current_timestamp(), nullable=False)
    name_rapport = db.Column(db.String(), nullable=False)