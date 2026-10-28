# PulseGrid - Retail architecture

## Current system

PulseGrid - Retail is organized as a notebook-led analytics project with a Streamlit presentation layer:

1. **Data acquisition** — `notebooks/00_data_ingestion.ipynb` downloads Online Retail II into `data/raw/`.
2. **Analysis and model development** — `notebooks/01` through `notebooks/14` cover exploration, feature engineering, segmentation, forecasting, churn, inventory, tuning, drift analysis, and MLflow experiments.
3. **Data products** — `data/interim/` holds the cleaned dashboard table. `data/processed/` holds model outputs and the enhanced dashboard table.
4. **Presentation** — `dashboard/app.py` composes the Streamlit dashboard; individual pages live in `dashboard/views/`.
5. **Deployment scaffolding** — `Dockerfile`, `.github/workflows/ci.yml`, and `k8s/deployment.yaml` define container, CI, and Kubernetes entry points.
6. **Analysis outputs** — `reports/report.md` and `reports/figures/` preserve notebook results.

The Power BI package is kept separately in `bi/powerbi/pulsegrid_retail_report_unpacked/`. It is an extracted report directory, not a single `.pbix` file.

## Data boundaries

- The full transaction-level source is not included. Run the ingestion notebook to download it into `data/raw/` before rerunning the modeling notebooks.
- The cleaned and enhanced CSVs supplied with this workspace each contain 3,806 aggregated rows. The enhanced file is the dashboard input; it is distinct from the transaction-level dataset used in the notebook workflow.
- Only the canonical enhanced table is included in the repository; the workspace's byte-identical duplicate is retained outside the publishable project.
- Dashboard pages read precomputed CSVs from `data/processed/`. They do not call a live prediction API or trigger retraining.

## Architecture findings

- `src/churn/`, `src/forecasting/`, `src/ingestion/`, `src/inventory/`, and `src/segmentation/` currently contain package markers, not production implementations. Most analytical logic lives in notebooks.
- The churn target is defined as `recency > 90 days`, while `recency` is also used as an input feature in notebooks 09 and 11. This target leakage explains the reported AUC of 1.0; it does not validate future churn prediction.
- MLflow tracking and drift analysis are represented by notebooks. There is no scheduled monitoring, retraining, or model-serving service in the current code.
- The CI workflow has no project test suite to run; it falls back to import checks before building the Docker image.
- The Streamlit dashboard and deployment files make this a useful end-to-end prototype, but the repository does not yet implement the automated, real-time production platform described in the project brief.

## Recommended next steps

1. Move reusable data cleaning, feature generation, model training, and inference into the domain packages under `src/`.
2. Define churn from a future inactivity window, exclude features that define that target, and add schema checks and unit tests around inputs and predictions.
3. Replace notebook-only execution with a parameterized batch entry point; keep notebooks for exploration and reporting.
4. Add a versioned prediction interface and connect the dashboard to that interface or to a documented batch refresh process.
5. Add scheduled drift checks, model performance monitoring, and a retraining approval path before describing the platform as production-ready.
