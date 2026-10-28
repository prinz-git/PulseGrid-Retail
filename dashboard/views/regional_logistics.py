"""PulseGrid - Retail — Regional Logistics & Supply Chain Dashboard view."""

import os
import json
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

from views.design import C, page_header

# Use the canonical, processed dashboard dataset.
DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "processed",
    "pulsegrid_retail_enhanced_dataset.csv",
)


@st.cache_data
def load_clean_dataset():
    df = pd.read_csv(DATA_PATH)

    def clean_curr(val):
        if pd.isna(val):
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)
        return float(str(val).replace("₹", "").replace(",", "").strip())

    records = []
    for _, r in df.iterrows():
        s = clean_curr(r["Sum of Total Sales"])
        c = clean_curr(r["Sum of Estimated Cost"])
        p = clean_curr(r["Sum of Estimated Profit"])
        stock = str(r["Stock Suggetion"]).strip()
        if stock == "Maintain Stock":
            stock = "Maintain Stock Level"
        elif stock == "Reduce Stock":
            stock = "Reduce Stock Level"

        churn = str(r["Churn Risk"]).strip()
        if churn.upper() == "LOW RISK":
            churn = "Low Risk"
        elif churn.upper() == "MEDIUM RISK":
            churn = "Medium Risk"
        elif churn.upper() == "HIGH RISK":
            churn = "High Risk"

        records.append({
            "invoice": int(r["Sum of Invoice Number"]),
            "country": str(r["Country"]).strip(),
            "region": str(r["Geographic Region"]).strip(),
            "quantity": int(r["Sum of Quantity"]),
            "sales": round(s, 2),
            "cost": round(c, 2),
            "profit": round(p, 2),
            "volumeCategory": str(r["Order Volume Category"]).strip(),
            "stockAction": stock,
            "churnRisk": churn,
            "actionPriority": str(r["Action Priority"]).strip(),
            "customerSegment": str(r.get("Customer Segment", "")).strip(),
            "recency": int(r.get("Sum of Recency", 0))
        })
    return records


def render():
    page_header(
        "5",
        "Regional Logistics & Supply Chain",
        "Interactive executive intelligence on regional expansion, logistics stock actions, wholesale volume tiers, and churn risk."
    )

    records = load_clean_dataset()
    data_json = json.dumps(records)

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>PulseGrid - Retail - Executive Regional Expansion & Logistics Dashboard</title>
      <!-- Tailwind CSS -->
      <script src="https://cdn.tailwindcss.com"></script>
      <!-- Inter Font -->
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
      <!-- Chart.js -->
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <!-- FontAwesome Icons -->
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

      <script>
        tailwind.config = {{
          darkMode: 'class',
          theme: {{
            extend: {{
              fontFamily: {{
                sans: ['Inter', 'sans-serif'],
              }},
              colors: {{
                brand: {{
                  50: '#f0f9ff',
                  100: '#e0f2fe',
                  500: '#0284c7',
                  600: '#0284c7',
                  700: '#0369a1',
                  900: '#0c4a6e',
                }},
                darkbg: '#0f172a',
                darkcard: '#1e293b',
                darkborder: '#334155'
              }}
            }}
          }}
        }}
      </script>
      <style>
        body {{
          font-family: 'Inter', sans-serif;
          transition: background-color 0.3s ease, color 0.3s ease;
        }}
        ::-webkit-scrollbar {{
          width: 6px;
          height: 6px;
        }}
        ::-webkit-scrollbar-track {{
          background: rgba(15, 23, 42, 0.6);
        }}
        ::-webkit-scrollbar-thumb {{
          background: #475569;
          border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
          background: #64748b;
        }}
      </style>
    </head>
    <body class="bg-darkbg text-slate-100 min-h-screen flex flex-col antialiased">

      <!-- TOP HEADER -->
      <header class="sticky top-0 z-40 bg-slate-900/90 light:bg-white/90 backdrop-blur-md border-b border-slate-800 light:border-slate-200 px-4 sm:px-6 py-3 transition-colors duration-200">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <!-- Title & Subtitle -->
          <div class="flex items-center space-x-3 w-full sm:w-auto justify-between sm:justify-start">
            <div class="flex items-center space-x-3">
              <div class="h-10 w-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-sky-500/20">
                <i class="fa-solid fa-globe text-xl"></i>
              </div>
              <div>
                <h1 class="text-lg font-bold tracking-tight text-white light:text-slate-900 flex items-center gap-2">
                  PulseGrid - Retail Analytics
                  <span class="text-xs px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-400 light:bg-sky-100 light:text-sky-700 font-semibold border border-sky-500/20">Executive</span>
                </h1>
                <p class="text-xs text-slate-400 light:text-slate-500">Regional Expansion & Supply Chain Logistics Dashboard</p>
              </div>
            </div>

            <!-- Mobile Theme Switcher Toggle -->
            <button id="themeToggleMobile" class="sm:hidden text-slate-400 hover:text-white p-2 rounded-lg bg-slate-800 light:bg-slate-100">
              <i class="fa-solid fa-moon dark:hidden"></i>
              <i class="fa-solid fa-sun hidden dark:block text-amber-400"></i>
            </button>
          </div>

          <!-- Header Quick Actions & Theme Toggle -->
          <div class="flex items-center space-x-3 w-full sm:w-auto justify-end">
            <div class="hidden md:flex items-center text-xs text-slate-400 bg-slate-800/60 light:bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-700/50 light:border-slate-200">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse mr-2"></span>
              Dataset Status: <strong class="text-slate-200 light:text-slate-700 ml-1">Live Enriched ({len(records):,} Recs)</strong>
            </div>

            <button id="themeToggle" class="hidden sm:flex items-center space-x-2 text-xs font-medium text-slate-300 light:text-slate-600 hover:text-white light:hover:text-slate-900 p-2 sm:px-3 sm:py-2 rounded-lg bg-slate-800 light:bg-slate-100 border border-slate-700 light:border-slate-200 transition">
              <i class="fa-solid fa-moon dark:hidden"></i>
              <i class="fa-solid fa-sun hidden dark:block text-amber-400"></i>
              <span class="hidden md:inline" id="themeText">Dark Mode</span>
            </button>

            <button id="toggleInsightsBtn" class="flex items-center space-x-2 text-xs font-semibold text-white bg-sky-600 hover:bg-sky-500 px-3 py-2 rounded-lg transition shadow-md shadow-sky-600/20">
              <i class="fa-solid fa-lightbulb"></i>
              <span>Strategic Insights</span>
            </button>
          </div>
        </div>
      </header>

      <!-- CONTROLS & FILTER BAR -->
      <section class="bg-slate-900/40 light:bg-slate-50 border-b border-slate-800/80 light:border-slate-200 px-4 sm:px-6 py-4">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 flex-1">

            <!-- Region Filter -->
            <div class="flex flex-col">
              <label class="text-[11px] font-semibold uppercase tracking-wider text-slate-400 light:text-slate-600 mb-1 flex items-center gap-1.5">
                <i class="fa-solid fa-earth-americas text-sky-400"></i> Geographic Region
              </label>
              <select id="regionFilter" class="bg-slate-800 light:bg-white text-slate-200 light:text-slate-800 text-sm rounded-lg border border-slate-700 light:border-slate-300 px-3 py-2 focus:ring-2 focus:ring-sky-500 outline-none transition cursor-pointer">
                <option value="ALL">All Regions (Global)</option>
                <option value="Northern Europe">Northern Europe</option>
                <option value="Western Europe">Western Europe</option>
                <option value="Asia-Pacific">Asia-Pacific</option>
                <option value="Southern Europe">Southern Europe</option>
                <option value="Americas">Americas</option>
                <option value="Middle East">Middle East</option>
                <option value="Eastern Europe">Eastern Europe</option>
                <option value="Africa">Africa</option>
              </select>
            </div>

            <!-- Order Volume Filter -->
            <div class="flex flex-col">
              <label class="text-[11px] font-semibold uppercase tracking-wider text-slate-400 light:text-slate-600 mb-1 flex items-center gap-1.5">
                <i class="fa-solid fa-boxes-stacked text-indigo-400"></i> Order Volume Category
              </label>
              <select id="volumeFilter" class="bg-slate-800 light:bg-white text-slate-200 light:text-slate-800 text-sm rounded-lg border border-slate-700 light:border-slate-300 px-3 py-2 focus:ring-2 focus:ring-sky-500 outline-none transition cursor-pointer">
                <option value="ALL">All Volume Tiers</option>
                <option value="Small Order (1-5 units)">Small Order (1–5 units)</option>
                <option value="Medium Order (6-24 units)">Medium Order (6–24 units)</option>
                <option value="Bulk Order (25-99 units)">Bulk Order (25–99 units)</option>
                <option value="Wholesale (100+ units)">Wholesale (100+ units)</option>
              </select>
            </div>

            <!-- Stock Action Filter -->
            <div class="flex flex-col">
              <label class="text-[11px] font-semibold uppercase tracking-wider text-slate-400 light:text-slate-600 mb-1 flex items-center gap-1.5">
                <i class="fa-solid fa-warehouse text-emerald-400"></i> Stock Recommendation
              </label>
              <select id="stockFilter" class="bg-slate-800 light:bg-white text-slate-200 light:text-slate-800 text-sm rounded-lg border border-slate-700 light:border-slate-300 px-3 py-2 focus:ring-2 focus:ring-sky-500 outline-none transition cursor-pointer">
                <option value="ALL">All Stock Actions</option>
                <option value="Maintain Stock Level">Maintain Stock Level</option>
                <option value="Reduce Stock Level">Reduce Stock Level</option>
              </select>
            </div>

          </div>

          <!-- Action buttons & reset -->
          <div class="flex items-end space-x-2">
            <button id="resetFiltersBtn" class="w-full sm:w-auto flex items-center justify-center space-x-2 text-xs font-semibold text-slate-300 light:text-slate-700 hover:bg-slate-800 light:hover:bg-slate-200 px-4 py-2.5 rounded-lg border border-slate-700 light:border-slate-300 transition">
              <i class="fa-solid fa-arrows-rotate"></i>
              <span>Reset Filters</span>
            </button>
          </div>
        </div>
      </section>

      <!-- MAIN DASHBOARD CONTENT -->
      <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 space-y-6">

        <!-- TOP KPI SUMMARY CARDS -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

          <!-- KPI 1: Total Gross Revenue -->
          <div class="bg-slate-800/80 light:bg-white p-5 rounded-2xl border border-slate-700/60 light:border-slate-200 shadow-sm relative overflow-hidden group">
            <div class="absolute -right-3 -bottom-3 w-20 h-20 bg-sky-500/10 rounded-full blur-xl group-hover:bg-sky-500/20 transition"></div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold uppercase tracking-wider text-slate-400 light:text-slate-500">Gross Sales Revenue</span>
              <div class="p-2.5 bg-sky-500/10 text-sky-400 rounded-xl">
                <i class="fa-solid fa-indian-rupee-sign text-base"></i>
              </div>
            </div>
            <div class="text-2xl font-extrabold text-white light:text-slate-900 tracking-tight" id="kpiGrossRevenue">₹0</div>
            <div class="mt-2 flex items-center text-xs text-emerald-400 light:text-emerald-600 font-medium">
              <i class="fa-solid fa-arrow-trend-up mr-1"></i>
              <span id="kpiRevenueSub">0 Transacted Invoices</span>
            </div>
          </div>

          <!-- KPI 2: Top Regional Market -->
          <div class="bg-slate-800/80 light:bg-white p-5 rounded-2xl border border-slate-700/60 light:border-slate-200 shadow-sm relative overflow-hidden group">
            <div class="absolute -right-3 -bottom-3 w-20 h-20 bg-indigo-500/10 rounded-full blur-xl group-hover:bg-indigo-500/20 transition"></div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold uppercase tracking-wider text-slate-400 light:text-slate-500">Top Market Region</span>
              <div class="p-2.5 bg-indigo-500/10 text-indigo-400 rounded-xl">
                <i class="fa-solid fa-crown text-base"></i>
              </div>
            </div>
            <div class="text-2xl font-extrabold text-white light:text-slate-900 tracking-tight" id="kpiTopRegion">Northern Europe</div>
            <div class="mt-2 flex items-center justify-between text-xs text-indigo-400 light:text-indigo-600 font-medium">
              <span><i class="fa-solid fa-chart-pie mr-1"></i> <span id="kpiTopRegionShare">0%</span> of Global Revenue</span>
            </div>
          </div>

          <!-- KPI 3: Wholesale Volume Revenue Share -->
          <div class="bg-slate-800/80 light:bg-white p-5 rounded-2xl border border-slate-700/60 light:border-slate-200 shadow-sm relative overflow-hidden group">
            <div class="absolute -right-3 -bottom-3 w-20 h-20 bg-emerald-500/10 rounded-full blur-xl group-hover:bg-emerald-500/20 transition"></div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold uppercase tracking-wider text-slate-400 light:text-slate-500">Wholesale Tier Volume</span>
              <div class="p-2.5 bg-emerald-500/10 text-emerald-400 rounded-xl">
                <i class="fa-solid fa-truck-ramp-box text-base"></i>
              </div>
            </div>
            <div class="text-2xl font-extrabold text-white light:text-slate-900 tracking-tight" id="kpiWholesaleCount">0 Orders</div>
            <div class="mt-2 flex items-center text-xs text-emerald-400 light:text-emerald-600 font-medium">
              <i class="fa-solid fa-sack-dollar mr-1"></i>
              <span id="kpiWholesaleRevenue">₹0 (0% Sales Share)</span>
            </div>
          </div>

          <!-- KPI 4: Stock Action Ratio -->
          <div class="bg-slate-800/80 light:bg-white p-5 rounded-2xl border border-slate-700/60 light:border-slate-200 shadow-sm relative overflow-hidden group">
            <div class="absolute -right-3 -bottom-3 w-20 h-20 bg-amber-500/10 rounded-full blur-xl group-hover:bg-amber-500/20 transition"></div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold uppercase tracking-wider text-slate-400 light:text-slate-500">Stock Action Ratio</span>
              <div class="p-2.5 bg-amber-500/10 text-amber-400 rounded-xl">
                <i class="fa-solid fa-boxes-packing text-base"></i>
              </div>
            </div>
            <div class="text-2xl font-extrabold text-white light:text-slate-900 tracking-tight" id="kpiStockRatio">0% Maintain</div>
            <div class="mt-2 flex items-center text-xs text-amber-400 light:text-amber-600 font-medium">
              <i class="fa-solid fa-triangle-exclamation mr-1"></i>
              <span id="kpiStockSub">0% Stock Reduction Target</span>
            </div>
          </div>

        </div>

        <!-- CHARTS GRID (2x2 Layout) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

          <!-- Chart 1: Regional Sales & Profit Contribution -->
          <div class="bg-slate-800/80 light:bg-white p-5 rounded-2xl border border-slate-700/60 light:border-slate-200 shadow-sm flex flex-col">
            <div class="flex items-center justify-between mb-4">
              <div>
                <h3 class="text-base font-bold text-white light:text-slate-900">Regional Sales & Profit Matrix</h3>
                <p class="text-xs text-slate-400 light:text-slate-500">Total gross revenue vs estimated net profit contribution by geographic zone</p>
              </div>
              <span class="text-xs font-semibold px-2.5 py-1 rounded-md bg-slate-700/60 text-slate-300 light:bg-slate-100 light:text-slate-700">Zone Breakdown</span>
            </div>
            <div class="relative flex-1 min-h-[280px]">
              <canvas id="regionalRevenueChart"></canvas>
            </div>
          </div>

          <!-- Chart 2: Order Volume Category Distribution -->
          <div class="bg-slate-800/80 light:bg-white p-5 rounded-2xl border border-slate-700/60 light:border-slate-200 shadow-sm flex flex-col">
            <div class="flex items-center justify-between mb-4">
              <div>
                <h3 class="text-base font-bold text-white light:text-slate-900">Order Volume Tier Breakdown</h3>
                <p class="text-xs text-slate-400 light:text-slate-500">Distribution of order volume categories across transactions</p>
              </div>
              <span class="text-xs font-semibold px-2.5 py-1 rounded-md bg-slate-700/60 text-slate-300 light:bg-slate-100 light:text-slate-700">Volume Shares</span>
            </div>
            <div class="relative flex-1 min-h-[280px] flex items-center justify-center">
              <canvas id="volumeCategoryChart"></canvas>
            </div>
          </div>

          <!-- Chart 3: Logistics & Stock Recommendation Matrix -->
          <div class="bg-slate-800/80 light:bg-white p-5 rounded-2xl border border-slate-700/60 light:border-slate-200 shadow-sm flex flex-col">
            <div class="flex items-center justify-between mb-4">
              <div>
                <h3 class="text-base font-bold text-white light:text-slate-900">Logistics & Stock Recommendation Matrix</h3>
                <p class="text-xs text-slate-400 light:text-slate-500">Count of orders recommended for stock level maintenance vs reduction by region</p>
              </div>
              <span class="text-xs font-semibold px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-400 light:bg-emerald-50 light:text-emerald-700">Inventory Health</span>
            </div>
            <div class="relative flex-1 min-h-[280px]">
              <canvas id="stockMatrixChart"></canvas>
            </div>
          </div>

          <!-- Chart 4: Order Quantity vs Sales Correlation Bubble Chart -->
          <div class="bg-slate-800/80 light:bg-white p-5 rounded-2xl border border-slate-700/60 light:border-slate-200 shadow-sm flex flex-col">
            <div class="flex items-center justify-between mb-4">
              <div>
                <h3 class="text-base font-bold text-white light:text-slate-900">Order Quantity vs Sales Value Correlation</h3>
                <p class="text-xs text-slate-400 light:text-slate-500">Mapping transaction volume density against financial yield per region</p>
              </div>
              <span class="text-xs font-semibold px-2.5 py-1 rounded-md bg-sky-500/10 text-sky-400 light:bg-sky-50 light:text-sky-700">Correlation Bubble</span>
            </div>
            <div class="relative flex-1 min-h-[280px]">
              <canvas id="correlationBubbleChart"></canvas>
            </div>
          </div>

        </div>

        <!-- DATA TABLE SECTION: Regional & Logistics Breakdown -->
        <div class="bg-slate-800/80 light:bg-white rounded-2xl border border-slate-700/60 light:border-slate-200 shadow-sm overflow-hidden">

          <!-- Table Header & Controls -->
          <div class="p-5 border-b border-slate-700/60 light:border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h3 class="text-base font-bold text-white light:text-slate-900 flex items-center gap-2">
                <i class="fa-solid fa-table-list text-sky-400"></i>
                Regional Logistics & Country Performance Table
              </h3>
              <p class="text-xs text-slate-400 light:text-slate-500">Granular view of country performance metrics, churn risk, and operational logistics</p>
            </div>

            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
              <!-- Table Search -->
              <div class="relative min-w-[240px]">
                <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                <input type="text" id="tableSearchInput" placeholder="Search country, region..." class="w-full bg-slate-900/80 light:bg-slate-50 text-slate-200 light:text-slate-800 text-xs rounded-lg border border-slate-700 light:border-slate-300 pl-9 pr-3 py-2 focus:ring-2 focus:ring-sky-500 outline-none transition">
              </div>

              <!-- Quick Export / Filter Pill -->
              <div class="text-xs text-slate-400 light:text-slate-600 self-center font-medium">
                Showing <strong id="visibleRowCount" class="text-sky-400 light:text-sky-600">0</strong> Countries
              </div>
            </div>
          </div>

          <!-- Scrollable Table -->
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs">
              <thead>
                <tr class="bg-slate-900/60 light:bg-slate-100 text-slate-300 light:text-slate-700 border-b border-slate-700/60 light:border-slate-200 font-semibold uppercase tracking-wider">
                  <th class="py-3 px-4 cursor-pointer hover:text-white" onclick="sortTable(0)">Country <i class="fa-solid fa-sort text-[10px] ml-1 opacity-60"></i></th>
                  <th class="py-3 px-4 cursor-pointer hover:text-white" onclick="sortTable(1)">Geographic Zone <i class="fa-solid fa-sort text-[10px] ml-1 opacity-60"></i></th>
                  <th class="py-3 px-4 text-center cursor-pointer hover:text-white" onclick="sortTable(2)">Total Invoices <i class="fa-solid fa-sort text-[10px] ml-1 opacity-60"></i></th>
                  <th class="py-3 px-4 text-right cursor-pointer hover:text-white" onclick="sortTable(3)">Total Sales (₹) <i class="fa-solid fa-sort text-[10px] ml-1 opacity-60"></i></th>
                  <th class="py-3 px-4 text-right cursor-pointer hover:text-white" onclick="sortTable(4)">Avg Basket (₹) <i class="fa-solid fa-sort text-[10px] ml-1 opacity-60"></i></th>
                  <th class="py-3 px-4 text-center">Primary Volume Tier</th>
                  <th class="py-3 px-4 text-center">Stock Recommendation</th>
                  <th class="py-3 px-4 text-center">Churn Risk Profile</th>
                </tr>
              </thead>
              <tbody id="logisticsTableBody" class="divide-y divide-slate-700/40 light:divide-slate-200 text-slate-300 light:text-slate-700">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>

        </div>

      </main>

      <!-- STRATEGIC INSIGHTS DRAWER / SIDEBAR -->
      <div id="insightsDrawer" class="fixed inset-y-0 right-0 w-full max-w-md bg-slate-900 light:bg-white shadow-2xl z-50 transform translate-x-full transition-transform duration-300 border-l border-slate-800 light:border-slate-200 flex flex-col">

        <!-- Drawer Header -->
        <div class="p-5 border-b border-slate-800 light:border-slate-200 flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <div class="p-2 bg-amber-500/10 text-amber-400 rounded-lg">
              <i class="fa-solid fa-lightbulb text-base"></i>
            </div>
            <h3 class="text-base font-bold text-white light:text-slate-900">Logistics & Strategy Insights</h3>
          </div>
          <button id="closeInsightsBtn" class="text-slate-400 hover:text-white light:hover:text-slate-900 text-lg p-1">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>

        <!-- Drawer Content -->
        <div class="p-5 overflow-y-auto flex-1 space-y-5 text-xs text-slate-300 light:text-slate-600">

          <!-- Insight 1 -->
          <div class="p-4 rounded-xl bg-slate-800/80 light:bg-slate-50 border border-slate-700/60 light:border-slate-200 space-y-2">
            <div class="flex items-center space-x-2 text-sky-400 font-semibold">
              <i class="fa-solid fa-warehouse"></i>
              <span>Northern Europe Fulfillment Hub</span>
            </div>
            <p class="leading-relaxed">
              Northern Europe represents <strong>92.7% of gross revenue (₹202,495)</strong> across 3,474 invoices. Establishing a dedicated regional cross-docking center in the UK/EIRE corridor will reduce lead-time variability and lower cross-border parcel freight overhead.
            </p>
          </div>

          <!-- Insight 2 -->
          <div class="p-4 rounded-xl bg-slate-800/80 light:bg-slate-50 border border-slate-700/60 light:border-slate-200 space-y-2">
            <div class="flex items-center space-x-2 text-emerald-400 font-semibold">
              <i class="fa-solid fa-truck-fast"></i>
              <span>Wholesale Tier Margin Optimization</span>
            </div>
            <p class="leading-relaxed">
              Exactly <strong>70 wholesale orders (100+ units)</strong> account for <strong>₹113,878 (52.1% of global gross sales)</strong>. Deploying tailored account-manager dispatch protocols and bulk shipping SLAs protects over half of business revenue.
            </p>
          </div>

          <!-- Insight 3 -->
          <div class="p-4 rounded-xl bg-slate-800/80 light:bg-slate-50 border border-slate-700/60 light:border-slate-200 space-y-2">
            <div class="flex items-center space-x-2 text-amber-400 font-semibold">
              <i class="fa-solid fa-boxes-packing"></i>
              <span>Stock Rationalization & Capital Relief</span>
            </div>
            <p class="leading-relaxed">
              Across secondary markets, inventory models recommend <strong>Reduce Stock Level</strong> on low-turnover SKUs. Reallocating slow-moving inventory releases working capital into fast-moving bulk stock.
            </p>
          </div>

          <!-- Insight 4 -->
          <div class="p-4 rounded-xl bg-slate-800/80 light:bg-slate-50 border border-slate-700/60 light:border-slate-200 space-y-2">
            <div class="flex items-center space-x-2 text-indigo-400 font-semibold">
              <i class="fa-solid fa-shield-halved"></i>
              <span>Urgent Retention Campaign</span>
            </div>
            <p class="leading-relaxed">
              <strong>182 accounts</strong> are flagged under <strong>High Priority (Urgent Retention)</strong>. Automated CRM triggers and personalized win-back discount vouchers should target these high-churn accounts before invoice lapses become permanent attrition.
            </p>
          </div>

        </div>

        <!-- Drawer Footer -->
        <div class="p-4 border-t border-slate-800 light:border-slate-200 bg-slate-900/50 light:bg-slate-50 text-center">
          <button onclick="window.print()" class="w-full py-2 bg-slate-800 light:bg-slate-200 hover:bg-slate-700 light:hover:bg-slate-300 text-white light:text-slate-800 rounded-lg text-xs font-semibold transition">
            <i class="fa-solid fa-file-pdf mr-1.5"></i> Export Executive Summary PDF
          </button>
        </div>
      </div>

      <!-- BACKDROP FOR DRAWER -->
      <div id="drawerBackdrop" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 hidden transition-opacity"></div>

      <!-- FOOTER -->
      <footer class="bg-slate-900 light:bg-slate-100 border-t border-slate-800 light:border-slate-200 py-4 px-6 text-center text-xs text-slate-500 light:text-slate-600">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <div>PulseGrid - Retail Analytics Platform &copy; 2026. All rights reserved.</div>
          <div class="flex items-center space-x-4">
            <span class="hover:text-slate-300 cursor-pointer">Logistics Policy</span>
            <span>&bull;</span>
            <span class="hover:text-slate-300 cursor-pointer">API Integration</span>
            <span>&bull;</span>
            <span class="hover:text-slate-300 cursor-pointer">Support</span>
          </div>
        </div>
      </footer>

      <!-- SCRIPT LOGIC -->
      <script>
        const dataset = {data_json};

        // GLOBAL CHART REFERENCES
        let chartRegionalRevenue = null;
        let chartVolumeCategory = null;
        let chartStockMatrix = null;
        let chartCorrelationBubble = null;

        window.onload = function() {{
          setupThemeToggle();
          setupInsightsDrawer();
          setupFilterListeners();
          renderDashboard();
        }};

        function getFilteredData() {{
          const regionVal = document.getElementById('regionFilter').value;
          const volumeVal = document.getElementById('volumeFilter').value;
          const stockVal = document.getElementById('stockFilter').value;
          const searchVal = document.getElementById('tableSearchInput').value.toLowerCase().trim();

          return dataset.filter(item => {{
            const matchesRegion = (regionVal === "ALL" || item.region === regionVal);
            const matchesVolume = (volumeVal === "ALL" || item.volumeCategory === volumeVal);
            const matchesStock = (stockVal === "ALL" || item.stockAction === stockVal);
            const matchesSearch = !searchVal ||
              item.country.toLowerCase().includes(searchVal) ||
              item.region.toLowerCase().includes(searchVal);

            return matchesRegion && matchesVolume && matchesStock && matchesSearch;
          }});
        }}

        function renderDashboard() {{
          const filtered = getFilteredData();
          updateKPIs(filtered);
          renderRegionalRevenueChart(filtered);
          renderVolumeCategoryChart(filtered);
          renderStockMatrixChart(filtered);
          renderCorrelationBubbleChart(filtered);
          renderTable(filtered);
        }}

        function updateKPIs(data) {{
          const totalSales = data.reduce((sum, d) => sum + d.sales, 0);
          const totalOrders = data.length;

          // KPI 1: Gross Revenue
          document.getElementById('kpiGrossRevenue').textContent = `₹${{Math.round(totalSales).toLocaleString('en-IN')}}`;
          document.getElementById('kpiRevenueSub').textContent = `${{totalOrders.toLocaleString()}} Transacted Invoices`;

          // KPI 2: Top Regional Market
          const regionSalesMap = {{}};
          data.forEach(d => {{
            regionSalesMap[d.region] = (regionSalesMap[d.region] || 0) + d.sales;
          }});

          let topRegion = "N/A";
          let topRegionSales = 0;
          Object.entries(regionSalesMap).forEach(([reg, sales]) => {{
            if (sales > topRegionSales) {{
              topRegionSales = sales;
              topRegion = reg;
            }}
          }});

          const topShare = totalSales > 0 ? ((topRegionSales / totalSales) * 100).toFixed(1) : 0;
          document.getElementById('kpiTopRegion').textContent = topRegion;
          document.getElementById('kpiTopRegionShare').textContent = `${{topShare}}%`;

          // KPI 3: Wholesale Volume Tier
          const wholesaleOrders = data.filter(d => d.volumeCategory === "Wholesale (100+ units)");
          const wholesaleCount = wholesaleOrders.length;
          const wholesaleSales = wholesaleOrders.reduce((sum, d) => sum + d.sales, 0);
          const wholesaleShare = totalSales > 0 ? ((wholesaleSales / totalSales) * 100).toFixed(1) : 0;

          document.getElementById('kpiWholesaleCount').textContent = `${{wholesaleCount}} Orders`;
          document.getElementById('kpiWholesaleRevenue').textContent = `₹${{Math.round(wholesaleSales).toLocaleString('en-IN')}} (${{wholesaleShare}}% Sales Share)`;

          // KPI 4: Stock Action Ratio
          const maintainCount = data.filter(d => d.stockAction === "Maintain Stock Level").length;
          const reduceCount = data.filter(d => d.stockAction === "Reduce Stock Level").length;
          const maintainRatio = totalOrders > 0 ? ((maintainCount / totalOrders) * 100).toFixed(1) : 0;
          const reduceRatio = totalOrders > 0 ? ((reduceCount / totalOrders) * 100).toFixed(1) : 0;

          document.getElementById('kpiStockRatio').textContent = `${{maintainRatio}}% Maintain`;
          document.getElementById('kpiStockSub').textContent = `${{reduceRatio}}% Stock Reduction Target`;
        }}

        function renderRegionalRevenueChart(data) {{
          const ctx = document.getElementById('regionalRevenueChart').getContext('2d');
          if (chartRegionalRevenue) chartRegionalRevenue.destroy();

          const regionMap = {{}};
          data.forEach(d => {{
            if (!regionMap[d.region]) {{
              regionMap[d.region] = {{ sales: 0, profit: 0 }};
            }}
            regionMap[d.region].sales += d.sales;
            regionMap[d.region].profit += d.profit;
          }});

          const labels = Object.keys(regionMap).sort((a,b) => regionMap[b].sales - regionMap[a].sales);
          const salesData = labels.map(l => Math.round(regionMap[l].sales));
          const profitData = labels.map(l => Math.round(regionMap[l].profit));

          chartRegionalRevenue = new Chart(ctx, {{
            type: 'bar',
            data: {{
              labels: labels,
              datasets: [
                {{
                  label: 'Gross Sales (₹)',
                  data: salesData,
                  backgroundColor: '#0284c7',
                  borderRadius: 6
                }},
                {{
                  label: 'Net Profit (₹)',
                  data: profitData,
                  backgroundColor: '#10b981',
                  borderRadius: 6
                }}
              ]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              indexAxis: 'y',
              plugins: {{
                legend: {{ labels: {{ color: getTextColor(), font: {{ family: 'Inter', size: 11 }} }} }},
                tooltip: {{
                  callbacks: {{
                    label: (ctx) => `${{ctx.dataset.label}}: ₹${{ctx.raw.toLocaleString('en-IN')}}`
                  }}
                }}
              }},
              scales: {{
                x: {{
                  grid: {{ color: getGridColor() }},
                  ticks: {{ color: getTextColor(), font: {{ family: 'Inter', size: 10 }} }}
                }},
                y: {{
                  grid: {{ display: false }},
                  ticks: {{ color: getTextColor(), font: {{ family: 'Inter', size: 11 }} }}
                }}
              }}
            }}
          }});
        }}

        function renderVolumeCategoryChart(data) {{
          const ctx = document.getElementById('volumeCategoryChart').getContext('2d');
          if (chartVolumeCategory) chartVolumeCategory.destroy();

          const volMap = {{
            "Small Order (1-5 units)": 0,
            "Medium Order (6-24 units)": 0,
            "Bulk Order (25-99 units)": 0,
            "Wholesale (100+ units)": 0
          }};

          data.forEach(d => {{
            if (volMap[d.volumeCategory] !== undefined) {{
              volMap[d.volumeCategory]++;
            }}
          }});

          chartVolumeCategory = new Chart(ctx, {{
            type: 'doughnut',
            data: {{
              labels: Object.keys(volMap),
              datasets: [{{
                data: Object.values(volMap),
                backgroundColor: ['#10b981', '#0284c7', '#8b5cf6', '#f59e0b'],
                borderWidth: 2,
                borderColor: getCardBgColor()
              }}]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{
                  position: 'bottom',
                  labels: {{ color: getTextColor(), font: {{ family: 'Inter', size: 11 }}, boxWidth: 12 }}
                }},
                tooltip: {{
                  callbacks: {{
                    label: (ctx) => `${{ctx.label}}: ${{ctx.raw.toLocaleString()}} Orders`
                  }}
                }}
              }},
              cutout: '65%'
            }}
          }});
        }}

        function renderStockMatrixChart(data) {{
          const ctx = document.getElementById('stockMatrixChart').getContext('2d');
          if (chartStockMatrix) chartStockMatrix.destroy();

          const matrixMap = {{}};
          data.forEach(d => {{
            if (!matrixMap[d.region]) {{
              matrixMap[d.region] = {{ maintain: 0, reduce: 0 }};
            }}
            if (d.stockAction === "Maintain Stock Level") matrixMap[d.region].maintain++;
            else matrixMap[d.region].reduce++;
          }});

          const labels = Object.keys(matrixMap);
          const maintainData = labels.map(l => matrixMap[l].maintain);
          const reduceData = labels.map(l => matrixMap[l].reduce);

          chartStockMatrix = new Chart(ctx, {{
            type: 'bar',
            data: {{
              labels: labels,
              datasets: [
                {{
                  label: 'Maintain Stock',
                  data: maintainData,
                  backgroundColor: '#3b82f6',
                  borderRadius: 4
                }},
                {{
                  label: 'Reduce Stock',
                  data: reduceData,
                  backgroundColor: '#ef4444',
                  borderRadius: 4
                }}
              ]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ labels: {{ color: getTextColor(), font: {{ family: 'Inter', size: 11 }} }} }}
              }},
              scales: {{
                x: {{
                  grid: {{ color: getGridColor() }},
                  ticks: {{ color: getTextColor(), font: {{ family: 'Inter', size: 10 }} }}
                }},
                y: {{
                  grid: {{ color: getGridColor() }},
                  ticks: {{ color: getTextColor(), font: {{ family: 'Inter', size: 10 }} }}
                }}
              }}
            }}
          }});
        }}

        function renderCorrelationBubbleChart(data) {{
          const ctx = document.getElementById('correlationBubbleChart').getContext('2d');
          if (chartCorrelationBubble) chartCorrelationBubble.destroy();

          const bubbleMap = {{}};
          data.forEach(d => {{
            if (!bubbleMap[d.region]) {{
              bubbleMap[d.region] = {{ totalQty: 0, totalSales: 0, count: 0 }};
            }}
            bubbleMap[d.region].totalQty += d.quantity;
            bubbleMap[d.region].totalSales += d.sales;
            bubbleMap[d.region].count += 1;
          }});

          const bubbleData = Object.keys(bubbleMap).map(reg => {{
            const avgQty = bubbleMap[reg].totalQty / bubbleMap[reg].count;
            const avgSales = bubbleMap[reg].totalSales / bubbleMap[reg].count;
            return {{
              x: Math.round(avgQty),
              y: Math.round(avgSales),
              r: Math.min(Math.max(Math.sqrt(bubbleMap[reg].count) * 1.5, 6), 30),
              region: reg
            }};
          }});

          chartCorrelationBubble = new Chart(ctx, {{
            type: 'bubble',
            data: {{
              datasets: [{{
                label: 'Regional Market Profile',
                data: bubbleData,
                backgroundColor: 'rgba(56, 189, 248, 0.6)',
                borderColor: '#0284c7',
                borderWidth: 1.5
              }}]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ display: false }},
                tooltip: {{
                  callbacks: {{
                    label: (ctx) => `${{ctx.raw.region}}: Avg Qty ${{ctx.raw.x}} units | Avg Basket ₹${{ctx.raw.y}}`
                  }}
                }}
              }},
              scales: {{
                x: {{
                  title: {{ display: true, text: 'Average Order Quantity (Units)', color: getTextColor(), font: {{ size: 11 }} }},
                  grid: {{ color: getGridColor() }},
                  ticks: {{ color: getTextColor() }}
                }},
                y: {{
                  title: {{ display: true, text: 'Average Sales Value (₹)', color: getTextColor(), font: {{ size: 11 }} }},
                  grid: {{ color: getGridColor() }},
                  ticks: {{ color: getTextColor() }}
                }}
              }}
            }}
          }});
        }}

        let currentSortColumn = 3;
        let currentSortAsc = false;

        function renderTable(data) {{
          const tbody = document.getElementById('logisticsTableBody');
          tbody.innerHTML = '';

          const countryMap = {{}};
          data.forEach(d => {{
            if (!countryMap[d.country]) {{
              countryMap[d.country] = {{
                country: d.country,
                region: d.region,
                orders: 0,
                sales: 0,
                cost: 0,
                volumeTiers: {{}},
                stockActions: {{}},
                churnRisks: {{}}
              }};
            }}
            countryMap[d.country].orders++;
            countryMap[d.country].sales += d.sales;
            countryMap[d.country].cost += d.cost;
            countryMap[d.country].volumeTiers[d.volumeCategory] = (countryMap[d.country].volumeTiers[d.volumeCategory] || 0) + 1;
            countryMap[d.country].stockActions[d.stockAction] = (countryMap[d.country].stockActions[d.stockAction] || 0) + 1;
            countryMap[d.country].churnRisks[d.churnRisk] = (countryMap[d.country].churnRisks[d.churnRisk] || 0) + 1;
          }});

          let summaryList = Object.values(countryMap).map(c => {{
            const topVol = Object.keys(c.volumeTiers).reduce((a, b) => c.volumeTiers[a] > c.volumeTiers[b] ? a : b, 'Medium Order (6-24 units)');
            const topStock = Object.keys(c.stockActions).reduce((a, b) => c.stockActions[a] > c.stockActions[b] ? a : b, 'Maintain Stock Level');
            const topChurn = Object.keys(c.churnRisks).reduce((a, b) => c.churnRisks[a] > c.churnRisks[b] ? a : b, 'High Risk');

            return {{
              country: c.country,
              region: c.region,
              orders: c.orders,
              sales: c.sales,
              avgBasket: c.sales / c.orders,
              volumeTier: topVol,
              stockAction: topStock,
              churnRisk: topChurn
            }};
          }});

          summaryList.sort((a, b) => {{
            let valA, valB;
            switch(currentSortColumn) {{
              case 0: valA = a.country; valB = b.country; break;
              case 1: valA = a.region; valB = b.region; break;
              case 2: valA = a.orders; valB = b.orders; break;
              case 3: valA = a.sales; valB = b.sales; break;
              case 4: valA = a.avgBasket; valB = b.avgBasket; break;
              default: valA = a.sales; valB = b.sales;
            }}

            if (typeof valA === 'string') {{
              return currentSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }}
            return currentSortAsc ? valA - valB : valB - valA;
          }});

          document.getElementById('visibleRowCount').textContent = summaryList.length;

          if (summaryList.length === 0) {{
            tbody.innerHTML = `
              <tr>
                <td colspan="8" class="text-center py-8 text-slate-400">
                  <i class="fa-solid fa-folder-open text-2xl mb-2 block"></i>
                  No matching regional data found for selected filters.
                </td>
              </tr>
            `;
            return;
          }}

          summaryList.forEach(item => {{
            const tr = document.createElement('tr');
            tr.className = "hover:bg-slate-700/30 light:hover:bg-slate-50/80 transition cursor-pointer";

            const stockBadge = item.stockAction === "Maintain Stock Level"
              ? `<span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 light:bg-emerald-100 light:text-emerald-700 border border-emerald-500/20">Maintain Stock</span>`
              : `<span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-rose-500/10 text-rose-400 light:bg-rose-100 light:text-rose-700 border border-rose-500/20">Reduce Stock</span>`;

            let churnBadge = "";
            if (item.churnRisk === "High Risk") {{
              churnBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-500/10 text-amber-400 light:bg-amber-100 light:text-amber-700">High Risk</span>`;
            }} else if (item.churnRisk === "Medium Risk") {{
              churnBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-sky-500/10 text-sky-400 light:bg-sky-100 light:text-sky-700">Medium Risk</span>`;
            }} else {{
              churnBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-slate-500/10 text-slate-400 light:bg-slate-100 light:text-slate-700">Low Risk</span>`;
            }}

            tr.innerHTML = `
              <td class="py-3 px-4 font-semibold text-white light:text-slate-900">${{item.country}}</td>
              <td class="py-3 px-4 text-slate-300 light:text-slate-600">${{item.region}}</td>
              <td class="py-3 px-4 text-center font-medium">${{item.orders.toLocaleString()}}</td>
              <td class="py-3 px-4 text-right font-bold text-white light:text-slate-900">₹${{Math.round(item.sales).toLocaleString('en-IN')}}</td>
              <td class="py-3 px-4 text-right text-slate-300 light:text-slate-600">₹${{Math.round(item.avgBasket).toLocaleString('en-IN')}}</td>
              <td class="py-3 px-4 text-center text-[11px] text-slate-300 light:text-slate-600">${{item.volumeTier}}</td>
              <td class="py-3 px-4 text-center">${{stockBadge}}</td>
              <td class="py-3 px-4 text-center">${{churnBadge}}</td>
            `;
            tbody.appendChild(tr);
          }});
        }}

        function sortTable(colIndex) {{
          if (currentSortColumn === colIndex) {{
            currentSortAsc = !currentSortAsc;
          }} else {{
            currentSortColumn = colIndex;
            currentSortAsc = true;
          }}
          renderTable(getFilteredData());
        }}

        function setupFilterListeners() {{
          document.getElementById('regionFilter').addEventListener('change', renderDashboard);
          document.getElementById('volumeFilter').addEventListener('change', renderDashboard);
          document.getElementById('stockFilter').addEventListener('change', renderDashboard);
          document.getElementById('tableSearchInput').addEventListener('input', renderDashboard);

          document.getElementById('resetFiltersBtn').addEventListener('click', () => {{
            document.getElementById('regionFilter').value = 'ALL';
            document.getElementById('volumeFilter').value = 'ALL';
            document.getElementById('stockFilter').value = 'ALL';
            document.getElementById('tableSearchInput').value = '';
            renderDashboard();
          }});
        }}

        function setupThemeToggle() {{
          const toggleBtn = document.getElementById('themeToggle');
          const toggleMobile = document.getElementById('themeToggleMobile');
          const themeText = document.getElementById('themeText');

          function switchTheme() {{
            const isDark = document.documentElement.classList.contains('dark');
            if (isDark) {{
              document.documentElement.classList.remove('dark');
              document.documentElement.classList.add('light');
              if (themeText) themeText.textContent = 'Light Mode';
            }} else {{
              document.documentElement.classList.remove('light');
              document.documentElement.classList.add('dark');
              if (themeText) themeText.textContent = 'Dark Mode';
            }}
            renderDashboard();
          }}

          if (toggleBtn) toggleBtn.addEventListener('click', switchTheme);
          if (toggleMobile) toggleMobile.addEventListener('click', switchTheme);
        }}

        function setupInsightsDrawer() {{
          const drawer = document.getElementById('insightsDrawer');
          const backdrop = document.getElementById('drawerBackdrop');
          const openBtn = document.getElementById('toggleInsightsBtn');
          const closeBtn = document.getElementById('closeInsightsBtn');

          function openDrawer() {{
            drawer.classList.remove('translate-x-full');
            backdrop.classList.remove('hidden');
          }}

          function closeDrawer() {{
            drawer.classList.add('translate-x-full');
            backdrop.classList.add('hidden');
          }}

          openBtn.addEventListener('click', openDrawer);
          closeBtn.addEventListener('click', closeDrawer);
          backdrop.addEventListener('click', closeDrawer);
        }}

        function getTextColor() {{
          return document.documentElement.classList.contains('dark') ? '#94a3b8' : '#475569';
        }}
        function getGridColor() {{
          return document.documentElement.classList.contains('dark') ? 'rgba(51, 65, 85, 0.4)' : 'rgba(226, 232, 240, 0.8)';
        }}
        function getCardBgColor() {{
          return document.documentElement.classList.contains('dark') ? '#1e293b' : '#ffffff';
        }}
      </script>
    </body>
    </html>
    """

    components.html(html_code, height=1400, scrolling=True)
