"""PulseGrid - Retail — Inventory Optimization."""

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from views.design import C, LAYOUT, kpi_card, page_header, section_title

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def render():
    page_header(
        "4",
        "Inventory Optimization",
        "EOQ modeling, safety stock buffers, reorder triggers, and historical stockout simulations.",
    )

    metrics = pd.read_csv(os.path.join(DATA_DIR, "inventory_metrics.csv"))
    sim     = pd.read_csv(os.path.join(DATA_DIR, "inventory_simulation.csv"), parse_dates=["Date"])
    daily   = pd.read_csv(os.path.join(DATA_DIR, "daily_sales_features.csv"), parse_dates=["Date"])

    md = dict(zip(metrics["Metric"], metrics["Value"]))

    # Parse ROP for reference line
    try:
        rop_num = int(str(md.get("Reorder Point (95%)", "0"))
                      .replace(",", "").replace(" units", "").strip())
    except (ValueError, AttributeError):
        rop_num = 0

    stockout_str = str(md.get("Stockout Days", "0")).replace(" days", "").strip()
    stockout_color = C["red"] if stockout_str not in ["0", ""] else C["green"]

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpi_card(c1, "Economic Order Qty",   md.get("EOQ", "N/A"),                  "Optimal batch size")
    kpi_card(c2, "Safety Stock (95%)",   md.get("Safety Stock (95%)", "N/A"),   "Buffer cushion")
    kpi_card(c3, "Reorder Point (95%)",  md.get("Reorder Point (95%)", "N/A"), "Replenish threshold")
    kpi_card(c4, "Lead Time SLA",        md.get("Lead Time", "N/A"),             "Days to receive")
    kpi_card(c5, "Fill Rate Achieved",   md.get("Fill Rate", "N/A"),             "Target service level",
             value_color=C["green"])
    kpi_card(c6, "Stockout Incidents",   md.get("Stockout Days", "0"),           "Days depleted",
             value_color=stockout_color)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Stock level simulation ─────────────────────────────────────────────────
    section_title("Inventory Level Simulation (Historical Trajectory)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sim["Date"], y=sim["stock_level"],
        mode="lines", name="Stock Level",
        line=dict(color=C["sky"], width=2),
        fill="tozeroy", fillcolor="rgba(2, 132, 199, 0.08)",
    ))
    reorders = sim[sim["ordered"] > 0]
    if len(reorders) > 0:
        fig.add_trace(go.Scatter(
            x=reorders["Date"], y=reorders["stock_level"],
            mode="markers", name="Reorder Triggered",
            marker=dict(color=C["amber"], size=10, symbol="triangle-up",
                        line=dict(color="#1E293B", width=1.5)),
        ))
    stockout_days_sim = sim[sim["stockout"] > 0]
    if len(stockout_days_sim) > 0:
        fig.add_trace(go.Scatter(
            x=stockout_days_sim["Date"], y=[0] * len(stockout_days_sim),
            mode="markers", name="Stockout Event",
            marker=dict(color=C["red"], size=11, symbol="x",
                        line=dict(color=C["red"], width=2)),
        ))
    if rop_num > 0:
        fig.add_hline(
            y=rop_num, line_dash="dash", line_color=C["red"], line_width=1.5,
            annotation_text=f"Reorder Point: {rop_num:,} units",
            annotation_position="top right",
            annotation_font=dict(color=C["red"], size=12),
        )
    fig.update_layout(**{
        **LAYOUT,
        "height": 400,
        "xaxis_title": "Date",
        "yaxis_title": "Units in Stock",
        "legend": dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            font=dict(color="#E2E8F0", size=11),
        ),
    })
    st.plotly_chart(fig, use_container_width=True)

    # ── Two column charts ─────────────────────────────────────────────────────
    l, r = st.columns(2)

    with l:
        section_title("Daily Demand Frequency Distribution")
        mean_qty = daily["total_quantity"].mean()
        std_qty  = daily["total_quantity"].std()
        fig2 = go.Figure(go.Histogram(
            x=daily["total_quantity"], nbinsx=40,
            marker=dict(color="#0284C7", line=dict(color="#1E293B", width=1)),
            hovertemplate="Units: %{x}<br>Days: %{y}<extra></extra>",
        ))
        fig2.add_vline(x=mean_qty, line_dash="dash", line_color=C["amber"], line_width=2,
                       annotation_text=f"Mean: {mean_qty:,.0f}",
                       annotation_font=dict(color=C["amber"], size=11))
        fig2.add_vline(x=mean_qty + std_qty, line_dash="dot", line_color="#94A3B8",
                       annotation_text=f"+1σ: {mean_qty+std_qty:,.0f}",
                       annotation_font=dict(color="#CBD5E1", size=11))
        fig2.update_layout(**{
            **LAYOUT,
            "height": 330,
            "xaxis_title": "Daily Units Sold",
            "yaxis_title": "Number of Days",
        })
        st.plotly_chart(fig2, use_container_width=True)

    with r:
        section_title("Replenishment Trigger Log")
        orders = sim[sim["ordered"] > 0][["Date", "ordered", "stock_level"]].copy()
        if len(orders) > 0:
            orders.columns = ["Date", "Order Quantity", "Stock at Trigger"]
            orders["Date"] = orders["Date"].dt.strftime("%d %b %Y")
            orders["Order Quantity"]  = orders["Order Quantity"].apply(lambda v: f"{v:,.0f} units")
            orders["Stock at Trigger"] = orders["Stock at Trigger"].apply(lambda v: f"{v:,.0f}")
            st.dataframe(orders.reset_index(drop=True), use_container_width=True, height=290)
        else:
            st.info("No reorder events were triggered in the simulation period.")

    # ── Parameters table ──────────────────────────────────────────────────────
    section_title("Optimization Engine Parameters Reference")
    st.dataframe(metrics, use_container_width=True, hide_index=True)

    # ── Export ────────────────────────────────────────────────────────────────
    ex1, ex2 = st.columns(2)
    with ex1:
        st.download_button(
            label="Export Simulation Logs (CSV)",
            data=sim.to_csv(index=False),
            file_name="pulsegrid_retail_inventory_simulation_export.csv",
            mime="text/csv",
        )
    with ex2:
        st.download_button(
            label="Export Optimization Metrics (CSV)",
            data=metrics.to_csv(index=False),
            file_name="pulsegrid_retail_inventory_metrics_export.csv",
            mime="text/csv",
        )
