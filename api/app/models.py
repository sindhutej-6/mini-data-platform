import uuid
from app import db

class Dataset(db.Model):
    __tablename__ = "datasets"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String, nullable=False)
    uri = db.Column(db.String)
    description = db.Column(db.String)


class Column(db.Model):
    __tablename__ = "columns"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = db.Column(db.String, db.ForeignKey("datasets.id"))
    name = db.Column(db.String)
    data_type = db.Column(db.String)


class Run(db.Model):
    __tablename__ = "runs"

    id = db.Column(db.String, primary_key=True)
    job_name = db.Column(db.String)
    status = db.Column(db.String)


class LineageEdge(db.Model):
    __tablename__ = "lineage_edges"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_dataset_id = db.Column(db.String)
    target_dataset_id = db.Column(db.String)
    run_id = db.Column(db.String)


class DataQualityResult(db.Model):
    __tablename__ = "dq_results"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = db.Column(db.String)
    run_id = db.Column(db.String)
    check_name = db.Column(db.String)
    success = db.Column(db.Boolean)
    observed_value = db.Column(db.String)
    success_percentage = db.Column(db.Float)
