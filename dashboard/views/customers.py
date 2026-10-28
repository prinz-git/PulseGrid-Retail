"""PulseGrid - Retail — Customer Intelligence."""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from views.design import C, LAYOUT, kpi_card, page_header, section_title

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")

SEG_COLORS = {
    "Champions":           "#38BDF8",  # vibrant sky
    "Loyal":               "#818CF8",  # indigo
    "Potential Loyalists": "#34D399",  # emerald
    "Need Attention":      "#FBBF24",  # amber
    "At Risk":             "#FB923C",  # orange
    "Dormant":             "#64748B",  # muted slate
}

RISK_COLORS = {
    "High Risk":   C["red"],
    "Medium Risk": C["amber"],
    "Low Risk":    C["green"],
}


def render():
    page_header(
        "2",
        "Customer Intelligence",
        "RFM segmentation, behavioral clustering, and churn risk profiling.",
    )

    segments = pd.read_csv(os.path.join(DATA_DIR, "customer_segments.csv"))
    churn_path = os.path.join(DATA_DIR, "customer_churn.csv")
    churn = pd.read_csv(churn_path) if os.path.exists(churn_path) else None

    total     = len(segments)
    avg_mon   = segments["monetary"].mean()
    avg_freq  = segments["frequency"].mean()
    avg_rec   = segments["recency"].mean()
    high_risk = len(churn[churn["churn_risk"] == "High Risk"]) if churn is not None else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Total Customers",     f"{total:,}",           "Unique buyer accounts")
    kpi_card(c2, "Avg Lifetime Value",  f"£{avg_mon:,.0f}",     "Monetary value (RFM)")
    kpi_card(c3, "Avg Order Frequency", f"{avg_freq:.1f}",      "Orders per customer")
    kpi_card(c4, "Avg Recency",         f"{avg_rec:.0f} days",  "Days since last purchase")
    kpi_card(c5, "High-Risk Churners",  f"{high_risk:,}",       "Action needed",
             value_color=C["red"])

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Segmentation & RFM distribution ───────────────────────────────────────
    l, r = st.columns(2)

    with l:
        section_title("Customer Segments — RFM Score-Based (6 Tiers)")
        seg_counts = segments["kmeans_label"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Customers"]
        fig = go.Figure(go.Pie(
            labels=seg_counts["Segment"],
            values=seg_counts["Customers"],
            hole=0.55,
            marker=dict(
                colors=[SEG_COLORS.get(s, "#64748B") for s in seg_counts["Segment"]],
                line=dict(color="#1E293B", width=2.5),
            ),
            textfont=dict(color="#F8FAFC", size=11),
            hovertemplate="<b>%{label}</b><br>%{value:,} accounts (%{percent})<extra></extra>",
        ))
        fig.update_layout(**{
            **LAYOUT,
            "height": 360,
            "showlegend": True,
            "legend": dict(
                font=dict(color="#E2E8F0", size=11),
                orientation="v",
                x=1.02,
                y=0.5,
            ),
        })
        st.plotly_chart(fig, use_container_width=True)

    with r:
        section_title("RFM Score Distribution (Scale 3–15)")
        fig2 = go.Figure(go.Histogram(
            x=segments["rfm_score"],
            nbinsx=13,
            marker=dict(color="#0284C7", line=dict(color="#1E293B", width=1.5)),
            hovertemplate="Score: %{x}<br>Customers: %{y}<extra></extra>",
        ))
        fig2.update_layout(**{
            **LAYOUT,
            "height": 360,
            "xaxis_title": "RFM Score",
            "yaxis_title": "Number of Accounts",
        })
        st.plotly_chart(fig2, use_container_width=True)

    # ── RFM scatter ───────────────────────────────────────────────────────────
    section_title("RFM Value Mapping — Recency vs. Monetary (Bubble = Order Frequency)")
    fig3 = px.scatter(
        segments,
        x="recency",
        y="monetary",
        color="kmeans_label",
        size="frequency",
        size_max=16,
        opacity=0.75,
        color_discrete_map=SEG_COLORS,
        labels={
            "recency": "Recency (Days since last purchase)",
            "monetary": "Monetary Value (£)",
            "kmeans_label": "Segment",
            "frequency": "Orders",
        },
    )
    fig3.update_traces(marker=dict(line=dict(width=0.5, color="#0F172A")))
    fig3.update_layout(**{
        **LAYOUT,
        "height": 420,
        "legend": dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            font=dict(color="#E2E8F0", size=11),
        ),
    })
    st.plotly_chart(fig3, use_container_width=True)

    # ── Segment table ─────────────────────────────────────────────────────────
    section_title("Segment Profile Summary")
    summary = segments.groupby("kmeans_label").agg(
        Customers=("Customer ID", "count"),
        Avg_Recency=("recency", "mean"),
        Avg_Orders=("frequency", "mean"),
        Avg_Spend=("monetary", "mean"),
        Avg_RFM=("rfm_score", "mean"),
    ).round(1).sort_values("Avg_Spend", ascending=False)
    summary.index.name = "Segment"
    summary.columns = ["Customers", "Avg Recency (days)", "Avg Orders", "Avg Spend (£)", "Avg RFM Score"]
    st.dataframe(summary, use_container_width=True)

    # ── Export button ─────────────────────────────────────────────────────────
    st.download_button(
        label="Export Segment Data (CSV)",
        data=segments.to_csv(index=False),
        file_name="pulsegrid_retail_customer_segments_export.csv",
        mime="text/csv",
    )

    # ── Churn analysis ────────────────────────────────────────────────────────
    if churn is not None:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        section_title("Churn Risk Intelligence")

        cl, cr = st.columns(2)
        with cl:
            risk_counts = churn["churn_risk"].value_counts().reset_index()
            risk_counts.columns = ["Risk Level", "Customers"]
            fig4 = go.Figure(go.Bar(
                x=risk_counts["Risk Level"],
                y=risk_counts["Customers"],
                marker_color=[RISK_COLORS.get(r, "#64748B") for r in risk_counts["Risk Level"]],
                marker_line=dict(color="#1E293B", width=1),
                text=risk_counts["Customers"].apply(lambda v: f"{v:,}"),
                textposition="outside",
                textfont=dict(color="#F8FAFC", size=12),
            ))
            fig4.update_layout(**{
                **LAYOUT,
                "height": 320,
                "showlegend": False,
                "yaxis_title": "Customers",
                "title": "Accounts by Risk Tier",
            })
            st.plotly_chart(fig4, use_container_width=True)

        with cr:
            fig5 = go.Figure(go.Histogram(
                x=churn["churn_probability"],
                nbinsx=30,
                marker=dict(color=C["red"], line=dict(color="#1E293B", width=1)),
                hovertemplate="Probability: %{x:.2f}<br>Customers: %{y}<extra></extra>",
            ))
            fig5.update_layout(**{
                **LAYOUT,
                "height": 320,
                "xaxis_title": "Churn Probability",
                "yaxis_title": "Customers",
                "title": "Churn Probability Distribution",
            })
            st.plotly_chart(fig5, use_container_width=True)

        section_title("Top 15 Highest-Risk Accounts (Urgent Retention Required)")
        top_risk = (
            churn[churn["churn_risk"] == "High Risk"]
            .nlargest(15, "churn_probability")
            [["Customer ID", "recency", "frequency", "monetary", "churn_probability", "churn_risk"]]
            .reset_index(drop=True)
        )
        top_risk.columns = [
            "Customer ID",
            "Recency (days)",
            "Orders",
            "Spend (£)",
            "Churn Probability",
            "Risk Level",
        ]
        st.dataframe(top_risk, use_container_width=True)

        st.download_button(
            label="Export Churn Data (CSV)",
            data=churn.to_csv(index=False),
            file_name="pulsegrid_retail_churn_analysis_export.csv",
            mime="text/csv",
        )
