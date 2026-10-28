# PulseGrid - Retail workflow

## Analytics workflow

1. Download Online Retail II with `notebooks/00_data_ingestion.ipynb` into `data/raw/`.
2. Explore, clean, and engineer features with notebooks `01` and `02`.
3. Build customer segments and prepare time-series inputs with notebooks `03` and `04`.
4. Train and compare Prophet, LSTM, and ensemble forecasts with notebooks `05` through `08`.
5. Develop churn and inventory analyses with notebooks `09` and `10`.
6. Tune models, inspect drift, refine forecasts, and log experiments with notebooks `11` through `14`.
7. Review saved outputs in `data/processed/` and figures in `reports/figures/`.
8. Run the Streamlit interface with `streamlit run dashboard/app.py`.

The numbered notebooks form an analysis sequence. The current workspace also contains processed output files from earlier runs, so the dashboard can display those outputs without rerunning model training.

## Streamlit pages

- Sales summary
- Regional logistics and supply chain
- Customer intelligence
- Demand forecasting
- Inventory optimization

## Power BI workflow

The separate Power BI workflow is documented in [powerbi_dashboards.md](powerbi_dashboards.md). Its extracted report assets are under `bi/powerbi/`.
