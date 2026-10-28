#!/usr/bin/env bash
# Re-execute the PulseGrid - Retail notebook workflow sequentially.
# Usage: bash rerun_all.sh

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTEBOOKS_DIR="${PROJECT_ROOT}/notebooks"
TIMEOUT=900  # 15 min per notebook
FAILED=0

NOTEBOOKS=(
  "00_data_ingestion.ipynb"
  "01_eda_exploration.ipynb"
  "02_data_cleaning_feature_engineering.ipynb"
  "03_customer_segmentation.ipynb"
  "04_timeseries_preparation.ipynb"
  "05_prophet_forecasting.ipynb"
  "06_lstm_forecasting.ipynb"
  "07_mlflow_experiment_tracking.ipynb"
  "08_hybrid_ensemble.ipynb"
  "09_churn_prediction.ipynb"
  "10_inventory_optimization.ipynb"
  "11_optuna_tuning.ipynb"
  "12_drift_detection.ipynb"
  "13_model_refinement.ipynb"
  "14_mlflow_week2.ipynb"
)

for nb in "${NOTEBOOKS[@]}"; do
  echo ""
  echo "=========================================="
  echo "  RUNNING: $nb"
  echo "=========================================="
  if jupyter nbconvert --to notebook --execute --inplace \
    "${NOTEBOOKS_DIR}/${nb}" \
    --ExecutePreprocessor.timeout=${TIMEOUT} 2>&1; then
    echo "  SUCCESS: $nb"
  else
    echo "  FAILED: $nb — continuing to next..."
    FAILED=1
  fi
done

echo ""
echo "=========================================="
echo "  ALL NOTEBOOKS COMPLETE"
echo "=========================================="
exit "${FAILED}"
