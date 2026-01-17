# Mini Data Platform

This project implements a mini metadata data platform similar to DataHub/Amundsen.
It supports dataset registration, schema storage, search, data quality tracking,
and dataset lineage ingestion using OpenLineage-compatible events.

## 🏗 Architecture Diagram

                            +-------------+
                            |   Pipeline  |
                            | (Simulated) |
                            +------+------+ 
                                    |
                                    | OpenLineage Events
                                    v
                        +---------------------+
                        |     Flask API       |
                        |  Metadata Service   |
                        +----------+----------+
                                   |
                                   |
                            +------+------+ 
                            | PostgreSQL  |
                            |  Metadata   |
                            |  Database   |
                            +-------------+

## Components
1. **Metadata API (Flask)**

    The core service that exposes RESTful endpoints for:
    - Registering datasets and schemas.
    - Ingesting OpenLineage-compatible events to track data movement.
    - Storing and retrieving Data Quality (DQ) results.

2. **Metadata Store (PostgreSQL)**

    A relational database used to maintain the state of the platform, including:
    - **Datasets:** Names, URIs, and descriptions.
    - **Schemas:** Column-level metadata and types.
    - **Lineage:** Relationship mapping between upstream and downstream datasets.
    - **Runs:** History of job executions and their quality status.

3. **OpenLineage Integration**

    Standardized ingestion of lineage events. This allows the platform to be "pluggable" with modern orchestrators like Airflow or Dagster.

##  Setup & Execution

### Step 1: Clone Repository
```bash
git clone <repo-url>
cd mini-data-platform
```

### Step 2: Start Services
```bash
docker-compose up --build
```

### Step 3: Verify Health
```bash
curl http://localhost:5000/health
```
Expected:
```json
{"status":"ok"}
```

##  API Documentation

### 1. Datasets
- `GET /datasets` - Returns a list of all registered datasets.
- `POST /datasets` - Registers a new dataset.  
  Payload:
  ```json
  {
    "name": "sales_data",
    "uri": "s3://bucket/sales.csv",
    "schema": [...]
  }
  ```

### 2. Search
- `GET /search?q={query}` - Search for datasets by name or description.

### 3. Lineage
- `POST /openlineage/events` - Ingests a standard OpenLineage JSON event.
- `GET /datasets/{id}/lineage` - Retrieves the upstream and downstream dependencies for a specific dataset.

### 4. Data Quality & Runs
- `POST /runs` - Creates a new pipeline run entry.
- `POST /runs/{run_id}/dq_results` - Logs specific data quality check results (Success/Failure).

## Submission Validation
This repository includes a `submission.yml` file. To run the automated validation suite, ensure the services are up and execute the commands listed in that file.
