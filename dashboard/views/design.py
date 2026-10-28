"""PulseGrid - Retail — Shared design tokens and dark executive theme components."""

# ── Color palette (matching executive dark HTML theme) ────────────────────────
C = {
    # Brand Accents
    "sky":         "#38BDF8",   # bright sky blue
    "navy":        "#0284C7",   # brand sky-600
    "blue":        "#38BDF8",   # links, highlights
    "indigo":      "#6366F1",   # indigo accent
    "teal":        "#0284C7",   # chart primary series

    # Semantic Status
    "green":       "#10B981",   # positive / maintain / success
    "amber":       "#F59E0B",   # warning / medium risk
    "red":         "#EF4444",   # danger / stockout / high risk

    # High Contrast Text (Dark Mode)
    "text_h":      "#F8FAFC",   # headings: bright white
    "text_b":      "#E2E8F0",   # body text: slate-200
    "text_sub":    "#94A3B8",   # sub-labels: slate-400
    "text_hint":   "#64748B",   # hints / captions: slate-500

    # Backgrounds & Surfaces
    "bg_page":     "#0F172A",   # darkbg: slate-900
    "bg_card":     "#1E293B",   # darkcard: slate-800
    "border":      "#334155",   # darkborder: slate-700
    "border_subtle": "rgba(51, 65, 85, 0.6)",
    "bg_subtle":   "rgba(15, 23, 42, 0.6)",
}

# ── Plotly Dark Chart Template ────────────────────────────────────────────────
LAYOUT = dict(
    template="plotly_dark",
    font=dict(
        family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
        size=12,
        color="#CBD5E1",
    ),
    title_font=dict(size=14, color="#F8FAFC", family="Inter, sans-serif"),
    margin=dict(l=14, r=14, t=44, b=14),
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    hoverlabel=dict(
        bgcolor="#0F172A",
        font_color="#F8FAFC",
        font_size=12,
        bordercolor="#334155",
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor="rgba(51, 65, 85, 0.4)",
        gridwidth=1,
        linecolor="#334155",
        tickfont=dict(color="#94A3B8", size=11),
        title_font=dict(color="#E2E8F0", size=12, family="Inter"),
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="rgba(51, 65, 85, 0.4)",
        gridwidth=1,
        linecolor="#334155",
        tickfont=dict(color="#94A3B8", size=11),
        title_font=dict(color="#E2E8F0", size=12, family="Inter"),
    ),
    legend=dict(
        font=dict(color="#CBD5E1", size=11),
        bgcolor="rgba(15, 23, 42, 0.75)",
        bordercolor="#334155",
        borderwidth=1,
    ),
)


# ── Reusable Dark Executive KPI Card ──────────────────────────────────────────
def kpi_card(col, label, value, sub="", value_color=None):
    """Render an executive KPI card in the given Streamlit column."""
    import streamlit as st
    v_color = value_color or "#FFFFFF"
    col.markdown(f"""
    <div style="
      background:#1E293B;
      border:1px solid rgba(51, 65, 85, 0.6);
      border-radius:16px;
      padding:20px 18px;
      position:relative;
      overflow:hidden;
      box-shadow:0 4px 12px rgba(0, 0, 0, 0.25);
      transition: all 0.2s ease;
      height: 100%;
    ">
      <div style="
        position:absolute;
        top:-16px;
        right:-16px;
        width:70px;
        height:70px;
        background:radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, rgba(56, 189, 248, 0) 70%);
        border-radius:50%;
        pointer-events:none;
      "></div>
      <div style="
        font-size:0.72rem;
        font-weight:700;
        color:#94A3B8;
        text-transform:uppercase;
        letter-spacing:0.08em;
        margin-bottom:8px;
      ">{label}</div>
      <div style="
        font-size:1.85rem;
        font-weight:800;
        color:{v_color};
        line-height:1.15;
        letter-spacing:-0.02em;
        margin-bottom:6px;
      ">{value}</div>
      <div style="
        font-size:0.78rem;
        color:#38BDF8;
        font-weight:500;
        display:flex;
        align-items:center;
        gap:4px;
      ">{sub}</div>
    </div>""", unsafe_allow_html=True)


def page_header(module_num, title, subtitle):
    """Render the top dark executive banner for each page."""
    import streamlit as st
    st.markdown(f"""
    <div style="
      background:linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
      border:1px solid #334155;
      border-radius:16px;
      padding:24px 28px;
      margin-bottom:24px;
      box-shadow:0 4px 20px rgba(0, 0, 0, 0.35);
      display:flex;
      justify-content:space-between;
      align-items:center;
      flex-wrap:wrap;
      gap:16px;
    ">
      <div style="display:flex; align-items:center; gap:16px;">
        <div style="
          width:44px;
          height:44px;
          border-radius:12px;
          background:linear-gradient(135deg, #0284C7 0%, #6366F1 100%);
          display:flex;
          align-items:center;
          justify-content:center;
          color:#FFFFFF;
          font-size:1.25rem;
          font-weight:800;
          box-shadow:0 4px 12px rgba(2, 132, 199, 0.35);
        ">
          ⚡
        </div>
        <div>
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <span style="
              color:#FFFFFF;
              font-size:1.45rem;
              font-weight:800;
              letter-spacing:-0.01em;
            ">{title}</span>
            <span style="
              background:rgba(56, 189, 248, 0.12);
              color:#38BDF8;
              font-size:0.68rem;
              font-weight:700;
              padding:3px 10px;
              border-radius:999px;
              border:1px solid rgba(56, 189, 248, 0.25);
              text-transform:uppercase;
              letter-spacing:0.05em;
            ">PulseGrid - Retail • Module {module_num} of 5</span>
          </div>
          <div style="
            color:#94A3B8;
            font-size:0.84rem;
            font-weight:400;
          ">{subtitle}</div>
        </div>
      </div>
      <div style="
        display:flex;
        align-items:center;
        gap:8px;
        background:rgba(15, 23, 42, 0.6);
        border:1px solid #334155;
        border-radius:10px;
        padding:8px 14px;
        font-size:0.75rem;
        color:#CBD5E1;
      ">
        <span style="width:8px; height:8px; border-radius:50%; background:#10B981; box-shadow:0 0 8px #10B981; display:inline-block;"></span>
        <span>Platform Status: <strong style="color:#F8FAFC;">Active Intelligence</strong></span>
      </div>
    </div>""", unsafe_allow_html=True)


def section_title(text):
    """Render a section subheading with uniform high-contrast styling."""
    import streamlit as st
    st.markdown(f"""
    <div style="
      font-size:1.02rem;
      font-weight:700;
      color:#F8FAFC;
      margin:18px 0 14px 0;
      padding-bottom:8px;
      border-bottom:1px solid #334155;
      letter-spacing:-0.01em;
      display:flex;
      align-items:center;
      gap:8px;
    ">
      <span style="width:4px; height:16px; background:#0284C7; border-radius:2px; display:inline-block;"></span>
      <span>{text}</span>
    </div>""", unsafe_allow_html=True)
