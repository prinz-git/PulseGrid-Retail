"""PulseGrid - Retail — Demand Forecasting."""

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from views.design import C, LAYOUT, kpi_card, page_header, section_title

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def render():
    page_header(
        "3",
        "Demand Forecasting",
        "Hybrid Prophet + LSTM ensemble — 4-week forward revenue outlook with confidence bands.",
    )

    prophet_ready = pd.read_csv(os.path.join(DATA_DIR, "prophet_ready.csv"), parse_dates=["ds"])
    forecast_30d  = pd.read_csv(os.path.join(DATA_DIR, "prophet_forecast_30d.csv"), parse_dates=["ds"])
    ensemble      = pd.read_csv(os.path.join(DATA_DIR, "ensemble_predictions.csv"), parse_dates=["ds"])
    comparison    = pd.read_csv(os.path.join(DATA_DIR, "model_comparison.csv"))

    best_row  = comparison.iloc[0]
    avg_fc    = forecast_30d["yhat"].mean()
    max_fc    = forecast_30d["yhat"].max()
    fc_range  = max_fc - forecast_30d["yhat"].min()

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Best Model",            best_row["Model"],              "Lowest test MAPE")
    kpi_card(c2, "Best MAPE",             f"{best_row['MAPE (%)']:.2f}%", "Mean Absolute % Error",
             value_color=C["green"])
    kpi_card(c3, "Weekly Avg Forecast",   f"£{avg_fc:,.0f}",              "Average weekly revenue")
    kpi_card(c4, "Peak Week Projected",   f"£{max_fc:,.0f}",              "Highest projected week")
    kpi_card(c5, "Forecast Swing Range",  f"£{fc_range:,.0f}",            "Peak minus trough",
             value_color=C["sky"])

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Historical + 30-day forecast ──────────────────────────────────────────
    section_title("Historical Weekly Revenue + 4-Week Forward Forecast")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=prophet_ready["ds"], y=prophet_ready["y"],
        mode="lines", name="Historical Revenue",
        line=dict(color="#64748B", width=1.2),
    ))
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_30d["ds"], forecast_30d["ds"][::-1]]),
        y=pd.concat([forecast_30d["yhat_upper"], forecast_30d["yhat_lower"][::-1]]),
        fill="toself", fillcolor="rgba(16, 185, 129, 0.12)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Confidence Band (80%)",
    ))
    fig.add_trace(go.Scatter(
        x=forecast_30d["ds"], y=forecast_30d["yhat"],
        mode="lines+markers", name="4-Week Forecast",
        line=dict(color=C["green"], width=2.5),
        marker=dict(size=6, color=C["green"]),
    ))
    fig.update_layout(**{
        **LAYOUT,
        "height": 400,
        "xaxis_title": "Date",
        "yaxis_title": "Revenue (£)",
        "legend": dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#E2E8F0", size=11),
        ),
    })
    st.plotly_chart(fig, use_container_width=True)

    # ── Model comparison charts ───────────────────────────────────────────────
    l, r = st.columns([1.3, 0.7])

    with l:
        section_title("Test Set Evaluation: Models vs. Actual Weekly Revenue")
        fig2 = go.Figure()
        if "actual" in ensemble.columns:
            fig2.add_trace(go.Scatter(
                x=ensemble["ds"], y=ensemble["actual"],
                mode="lines+markers", name="Actual",
                line=dict(color="#38BDF8", width=2.5),
                marker=dict(size=4),
            ))
        model_traces = [
            ("prophet_predicted", "Prophet",          C["amber"], "dash"),
            ("lstm_predicted",    "LSTM",              C["red"],   "dot"),
            ("optimal_blend",     "Hybrid Ensemble",   C["green"], "solid"),
        ]
        for col, label, color, dash in model_traces:
            if col in ensemble.columns:
                fig2.add_trace(go.Scatter(
                    x=ensemble["ds"], y=ensemble[col],
                    mode="lines", name=label,
                    line=dict(color=color, width=2, dash=dash),
                ))
        fig2.update_layout(**{
            **LAYOUT,
            "height": 360,
            "xaxis_title": "Date",
            "yaxis_title": "Revenue (£)",
            "legend": dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                font=dict(color="#E2E8F0", size=11),
            ),
        })
        st.plotly_chart(fig2, use_container_width=True)

    with r:
        section_title("Model Ranking by MAPE")
        cmp = comparison.sort_values("MAPE (%)")
        bar_cols = [C["green"] if i == 0 else "#334155" for i in range(len(cmp))]
        fig3 = go.Figure(go.Bar(
            y=cmp["Model"], x=cmp["MAPE (%)"],
            orientation="h",
            marker_color=bar_cols,
            marker_line=dict(color="#1E293B", width=1),
            text=cmp["MAPE (%)"].apply(lambda v: f"{v:.2f}%"),
            textposition="outside",
            textfont=dict(color="#F8FAFC", size=11),
        ))
        fig3.update_layout(**{
            **LAYOUT,
            "height": 360,
            "xaxis_title": "MAPE (%)",
            "showlegend": False,
            "yaxis": dict(
                categoryorder="total ascending",
                tickfont=dict(color="#E2E8F0", size=11),
            ),
        })
        st.plotly_chart(fig3, use_container_width=True)

    # ── What-If Scenario Analysis ─────────────────────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    section_title("Executive What-If Scenario Simulator")
    st.markdown(
        "<p style='color:#94A3B8;font-size:13px;margin-bottom:16px;'>"
        "Dynamically adjust growth vectors and seasonality factors to simulate macro-economic shocks on the forward outlook.</p>",
        unsafe_allow_html=True,
    )

    wl, wr = st.columns(2)
    with wl:
        growth_pct = st.slider(
            "Revenue growth / decline (%)",
            -30,
            50,
            0,
            key="wi_growth",
            help="Simulate overall demand shifts (e.g. +20% for marketing promotions)",
        )
    with wr:
        seasonal_pct = st.slider(
            "Seasonal swing adjustment (%)",
            -20,
            40,
            0,
            key="wi_seasonal",
            help="Simulate seasonal surges (e.g. +30% for Q4 holiday peak)",
        )

    combined_factor = 1 + (growth_pct / 100) + (seasonal_pct / 100)
    fc_whatif = forecast_30d.copy()
    fc_whatif["yhat_adjusted"] = fc_whatif["yhat"] * combined_factor
    fc_whatif["yhat_upper_adj"] = fc_whatif["yhat_upper"] * combined_factor
    fc_whatif["yhat_lower_adj"] = fc_whatif["yhat_lower"] * combined_factor

    fig_wi = go.Figure()
    fig_wi.add_trace(go.Scatter(
        x=fc_whatif["ds"], y=fc_whatif["yhat"],
        mode="lines", name="Base Forecast",
        line=dict(color="#64748B", width=2, dash="dash"),
    ))
    fig_wi.add_trace(go.Scatter(
        x=pd.concat([fc_whatif["ds"], fc_whatif["ds"][::-1]]),
        y=pd.concat([fc_whatif["yhat_upper_adj"], fc_whatif["yhat_lower_adj"][::-1]]),
        fill="toself", fillcolor="rgba(16, 185, 129, 0.12)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Adjusted Confidence Band",
    ))
    fig_wi.add_trace(go.Scatter(
        x=fc_whatif["ds"], y=fc_whatif["yhat_adjusted"],
        mode="lines+markers", name=f"Adjusted Forecast ({combined_factor:.0%})",
        line=dict(color=C["green"], width=2.5),
        marker=dict(size=5, color=C["green"]),
    ))
    fig_wi.update_layout(**{
        **LAYOUT,
        "height": 350,
        "xaxis_title": "Date",
        "yaxis_title": "Revenue (£)",
        "legend": dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            font=dict(color="#E2E8F0", size=11),
        ),
    })
    st.plotly_chart(fig_wi, use_container_width=True)

    # ── Scenario KPIs ────
    wi1, wi2, wi3 = st.columns(3)
    adj_total = fc_whatif["yhat_adjusted"].sum()
    base_total = forecast_30d["yhat"].sum()
    delta = adj_total - base_total
    kpi_card(wi1, "Adjusted 30-Day Total", f"£{adj_total:,.0f}", "Scenario gross projection")
    kpi_card(wi2, "Base 30-Day Baseline",  f"£{base_total:,.0f}", "Baseline model forecast")
    kpi_card(wi3, "Simulated Financial Impact", f"{'+'if delta>=0 else ''}£{delta:,.0f}",
             f"{'Net Gain' if delta >= 0 else 'Net Contraction'} vs baseline",
             value_color=C["green"] if delta >= 0 else C["red"])

    # ── Tables ────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    section_title("Model Architecture Performance Comparison")
    display = comparison.copy()
    display["MAPE (%)"] = display["MAPE (%)"].apply(lambda v: f"{v:.2f}%")
    display["MAE"]  = display["MAE"].apply(lambda v: f"£{v:,.0f}")
    display["RMSE"] = display["RMSE"].apply(lambda v: f"£{v:,.0f}")
    st.dataframe(display, use_container_width=True, hide_index=True)

    section_title("4-Week Forecast Granular Schedule")
    fc_display = forecast_30d[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
    fc_display["ds"] = fc_display["ds"].dt.strftime("%d %b %Y")
    fc_display.columns = ["Date", "Forecast (£)", "Lower Bound (£)", "Upper Bound (£)"]
    for col in ["Forecast (£)", "Lower Bound (£)", "Upper Bound (£)"]:
        fc_display[col] = fc_display[col].apply(lambda v: f"£{v:,.0f}")
    st.dataframe(fc_display, use_container_width=True, hide_index=True, height=280)

    # ── Export buttons ────────────────────────────────────────────────────────
    ex1, ex2 = st.columns(2)
    with ex1:
        st.download_button(
            label="Export Forward Forecast (CSV)",
            data=forecast_30d.to_csv(index=False),
            file_name="pulsegrid_retail_forecast_30d_export.csv",
            mime="text/csv",
        )
    with ex2:
        st.download_button(
            label="Export Model Performance (CSV)",
            data=comparison.to_csv(index=False),
            file_name="pulsegrid_retail_model_comparison_export.csv",
            mime="text/csv",
        )
