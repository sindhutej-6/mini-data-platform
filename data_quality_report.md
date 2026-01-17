# Data Quality Report
##  Implemented Data Quality Rules

### 1. Not Null Check
- **Purpose:** Ensure critical columns do not contain `NULL` values.  
- **Description:** Columns that are mandatory for analysis (e.g., `order_id`, `customer_id`) are checked for missing values.  
- **Result Interpretation:**  
  - `true` → No NULLs found  
  - `false` → NULL values detected (requires investigation)

### 2. Row Count Check
- **Purpose:** Ensure the dataset contains the expected number of rows.  
- **Description:** Compares observed row count against expected row count defined in pipeline metadata.  
- **Result Interpretation:**  
  - `true` → Observed row count matches expectation  
  - `false` → Mismatch detected (investigate upstream/downstream causes)

---
##  Sample Results

| Dataset       | Check Name       | Success | Observed Value | Success % | Notes                       |
|---------------|-----------------|---------|----------------|-----------|-----------------------------|
| sales_orders  | not_null_check  | true    | 100%           | 100       | All critical columns valid |
| sales_orders  | row_count_check | true    | 100%           | 100       | Row count matches expected |

> **Tip:** If a check fails, review dataset schema, pipeline logs, and upstream data sources.

---

##  Conclusion
All implemented data quality checks passed successfully during this pipeline run.  
The dataset is considered valid for downstream processing and analysis.

---

##  Recommendations / Next Steps
- Maintain automated DQ checks for all new datasets.  
- Log detailed error messages for any failed checks.  
- Consider adding additional rules such as:
  - Unique key check  
  - Referential integrity check  
  - Value range / type validation
