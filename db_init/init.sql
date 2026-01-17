CREATE TABLE IF NOT EXISTS datasets (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    uri VARCHAR,
    description VARCHAR
);

CREATE TABLE IF NOT EXISTS columns (
    id VARCHAR PRIMARY KEY,
    dataset_id VARCHAR,
    name VARCHAR,
    data_type VARCHAR
);

CREATE TABLE IF NOT EXISTS runs (
    id VARCHAR PRIMARY KEY,
    job_name VARCHAR,
    status VARCHAR
);

CREATE TABLE IF NOT EXISTS lineage_edges (
    id VARCHAR PRIMARY KEY,
    source_dataset_id VARCHAR,
    target_dataset_id VARCHAR,
    run_id VARCHAR
);

CREATE TABLE IF NOT EXISTS data_quality_results (
    id VARCHAR PRIMARY KEY,
    dataset_id VARCHAR,
    check_name VARCHAR,
    success BOOLEAN,
    observed_value VARCHAR,
    success_percentage FLOAT
);
