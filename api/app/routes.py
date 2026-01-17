from flask import Blueprint, request, jsonify
from app import db
from app.models import Dataset, Column, Run, LineageEdge, DataQualityResult
from uuid import UUID

bp = Blueprint("api", __name__)

# -------------------- HEALTH --------------------
@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# -------------------- DATASETS --------------------
@bp.route("/datasets", methods=["POST"])
def create_dataset():
    data = request.get_json()

    dataset = Dataset(
        name=data["name"],
        uri=data.get("uri"),
        description=data.get("description")
    )
    db.session.add(dataset)
    db.session.commit()

    for col in data.get("schema", []):
        db.session.add(Column(
            dataset_id=dataset.id,
            name=col["name"],
            data_type=col["type"]
        ))

    db.session.commit()
    return jsonify({"dataset_id": str(dataset.id)}), 201


@bp.route("/datasets", methods=["GET"])
def list_datasets():
    datasets = Dataset.query.all()
    return jsonify([
        {
            "id": str(d.id),
            "name": d.name,
            "uri": d.uri,
            "description": d.description
        } for d in datasets
    ])


@bp.route("/datasets/<dataset_id>", methods=["GET"])
def get_dataset(dataset_id):
    try:
        UUID(dataset_id)
    except Exception:
        return jsonify({"error": "Invalid dataset_id"}), 400

    dataset = Dataset.query.get_or_404(dataset_id)
    columns = Column.query.filter_by(dataset_id=dataset_id).all()

    return jsonify({
        "id": dataset.id,
        "name": dataset.name,
        "schema": [
            {"name": c.name, "type": c.data_type}
            for c in columns
        ]
    })



# -------------------- SEARCH --------------------
@bp.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "")
    datasets = Dataset.query.filter(Dataset.name.ilike(f"%{q}%")).all()
    return jsonify([
        {"id": str(d.id), "name": d.name}
        for d in datasets
    ])


# -------------------- RUNS --------------------
@bp.route("/runs", methods=["POST"])
def create_run():
    data = request.get_json()

    run = Run(
        id=data["id"],
        job_name=data["job_name"],
        status=data["status"]
    )
    db.session.add(run)
    db.session.commit()

    return jsonify({"run_id": str(run.id)}), 201


# -------------------- DATA QUALITY --------------------
@bp.route("/runs/<uuid:run_id>/dq_results", methods=["POST"])
def save_dq(run_id):
    data = request.get_json()

    # validate dataset_id
    try:
        UUID(data["dataset_id"])
    except Exception:
        return jsonify({"error": "dataset_id must be UUID"}), 400

    dq = DataQualityResult(
        dataset_id=data["dataset_id"],   # STRING
        run_id=str(run_id),               # 🔴 FORCE STRING
        check_name=data["check_name"],
        success=data["success"],
        observed_value=data["observed_value"],
        success_percentage=data.get("success_percentage")
    )
    db.session.add(dq)
    db.session.commit()

    return jsonify({"status": "saved"}), 201


@bp.route("/runs/<uuid:run_id>/dq_results", methods=["GET"])
def get_dq_results(run_id):
    results = DataQualityResult.query.filter(
        DataQualityResult.run_id == str(run_id)  # 🔴 STRING compare
    ).all()

    return jsonify([
        {
            "check_name": r.check_name,
            "success": r.success,
            "observed_value": r.observed_value,
            "success_percentage": r.success_percentage
        } for r in results
    ])


# -------------------- OPENLINEAGE --------------------
@bp.route("/openlineage/events", methods=["POST"])
def openlineage_event():
    e = request.get_json()
    run_id = e["run"]["id"]

    for i in e.get("inputs", []):
        for o in e.get("outputs", []):
            try:
                UUID(i["name"])
                UUID(o["name"])
            except Exception:
                continue

            db.session.add(LineageEdge(
                source_dataset_id=i["name"],  # STRING
                target_dataset_id=o["name"],  # STRING
                run_id=run_id                 # STRING
            ))

    db.session.commit()
    return jsonify({"status": "lineage stored"}), 201


@bp.route("/datasets/<uuid:dataset_id>/lineage", methods=["GET"])
def dataset_lineage(dataset_id):
    dataset_id_str = str(dataset_id)

    edges = LineageEdge.query.filter(
        (LineageEdge.source_dataset_id == dataset_id_str) |
        (LineageEdge.target_dataset_id == dataset_id_str)
    ).all()

    return jsonify([
        {
            "source": e.source_dataset_id,
            "target": e.target_dataset_id,
            "run_id": e.run_id
        } for e in edges
    ])
