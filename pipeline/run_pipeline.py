import os
import uuid
import json
import pandas as pd
import requests
from datetime import datetime

API = os.getenv("METADATA_API_URL", "http://api:5000")
DATA_FILE = "OpenFoodFacts.csv"
DATASET_NAME = "openfoodfacts_dataset"

EXAMPLES_DIR = "/examples"
os.makedirs(EXAMPLES_DIR, exist_ok=True)

print("[PIPELINE] Loading CSV...")
df = pd.read_csv(DATA_FILE, sep="\t", on_bad_lines="skip", low_memory=False)
print(f"[PIPELINE] Rows={len(df)} Columns={len(df.columns)}")

schema = [{"name": c, "type": "string"} for c in df.columns]

payload = {
    "name": DATASET_NAME,
    "uri": f"file://{DATA_FILE}",
    "description": "Ingested via pipeline",
    "schema": schema
}

print("[PIPELINE] Registering dataset...")
r = requests.post(f"{API}/datasets", json=payload)
r.raise_for_status()
dataset_id = r.json()["dataset_id"]

# ---------------- RUN ----------------
run_id = str(uuid.uuid4())
requests.post(f"{API}/runs", json={
    "id": run_id,
    "job_name": "openfoodfacts_ingest",
    "status": "START"
})

# ---------------- OPENLINEAGE EVENT 1 ----------------
event_1 = {
    "eventType": "COMPLETE",
    "eventTime": datetime.utcnow().isoformat(),
    "job": {"name": "openfoodfacts_ingest"},
    "run": {"id": run_id},
    "inputs": [{"name": dataset_id}],
    "outputs": [{"name": dataset_id}]
}

with open(f"{EXAMPLES_DIR}/openlineage_event_1.json", "w") as f:
    json.dump(event_1, f, indent=2)

requests.post(f"{API}/openlineage/events", json=event_1)

# ---------------- OPENLINEAGE EVENT 2 ----------------
event_2 = {
    "eventType": "COMPLETE",
    "eventTime": datetime.utcnow().isoformat(),
    "job": {"name": "openfoodfacts_validation"},
    "run": {"id": str(uuid.uuid4())},
    "inputs": [{"name": dataset_id}],
    "outputs": [{"name": dataset_id}]
}

with open(f"{EXAMPLES_DIR}/openlineage_event_2.json", "w") as f:
    json.dump(event_2, f, indent=2)

requests.post(f"{API}/openlineage/events", json=event_2)

print("[PIPELINE] OpenLineage events written to /examples")
print("[PIPELINE] DONE")
