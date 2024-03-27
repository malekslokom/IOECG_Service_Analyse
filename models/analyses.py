from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
db = SQLAlchemy()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Projet(db.Model):
    __tablename__ = 'projets'

    idProject = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    last_updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    nameProject = db.Column(db.String, nullable=False)
    descriptionProject = db.Column(db.Text)
    created_by = db.Column(db.String, nullable=False)
    typeProject = db.Column(db.String, nullable=False)

    __table_args__ = (
        db.CheckConstraint(typeProject.in_(["Classification", "Régression", "Visualisation"]), name='check_type_project'),
    )
    # Define a one-to-many relationship with Analyses
    analyses = db.relationship('Analyses', backref='projet')


class Analyses(db.Model):
    __tablename__ = 'analyses'

    id_analysis = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_project = db.Column(db.Integer, db.ForeignKey('projets.idProject'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    last_updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    name_analysis = db.Column(db.String, nullable=False)
    description_analysis = db.Column(db.Text)
    created_by = db.Column(db.String, nullable=False)
    datasets = db.relationship('AnalysesDatasets', backref='analyse', lazy=True)


class Datasets(db.Model):
    __tablename__ = 'datasets'

    id_dataset = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=db.func.current_timestamp(), nullable=False)
    name_dataset = db.Column(db.String(), nullable=False)
    description_dataset = db.Column(db.Text, default=None)
    type_dataset = db.Column(db.String(), nullable=False)
    leads_name = db.Column(db.Text, nullable=False)
    study_name = db.Column(db.String(), nullable=False)
    study_details = db.Column(db.String(), default=None)
    source_name = db.Column(db.String(), nullable=False)
    source_details = db.Column(db.String(), default=None)

    __table_args__ = (
        db.CheckConstraint(type_dataset.in_(["search_results", "standard"]), name='check_type_dataset'),
    )
    analyses = db.relationship('AnalysesDatasets', backref='dataset', lazy=True)


class AnalysesDatasets(db.Model):
    __tablename__ = 'analyses_datasets'

    id_dataset_analysis = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_dataset = db.Column(db.Integer, db.ForeignKey('datasets.id_dataset'))
    id_analysis = db.Column(db.Integer, db.ForeignKey('analyses.id_analysis'))

    # dataset = db.relationship('Datasets', back_populates='analyses_datasets', primaryjoin=iddataset == Datasets.iddataset)
    # analyse = db.relationship('Analyses', back_populates='datasets', primaryjoin=idAnalysis == Analyses.idAnalysis)

