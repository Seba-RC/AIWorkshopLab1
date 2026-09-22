# Lab 1 · Local data

Six role-specific CSVs and lab01_manifest_v1.json contain the required data. Train copies preserve the Thursday snapshot bytes. Calibration/test are season-filtered extracts from newly captured Jolpica responses. The manifest records hashes, URLs and pagination receipts. Read train first; test files remain locally accessible but must not be inspected before freezing decisions.

Key: season + round + driver_id. Qualifying position is the qualifying classification. Results position is the final numeric classification, used only to construct the target; position_text/status preserve additional context. Empty Q1/Q2/Q3 fields are source missingness. grid, points, laps and status from results are not approved predictors. A missing qualifying row remains a missing value after a left join; it is not a reason to drop a result.

Coverage means records available from the source, not a verified complete list of pre-race entrants. Snapshots are historical records retrieved later, not timestamped historical information sets. Sprint results and 2026 classroom predictions are excluded.

Source documentation: https://github.com/jolpica/jolpica-f1/blob/main/docs/endpoints/results.md
