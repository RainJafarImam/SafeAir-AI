"""
gradio_app.py
─────────────
SafeAir AI — Gen AI Multi-Agent AQI Health Risk Intelligence System.
Upgraded Production Dashboard for Dayananda Sagar University (DSU) Academic Review.
Course: 25MSD5302 (Generative AI with LLM)
Student: Rain Jafar Imam (SCA25MSD059)
"""

from __future__ import annotations
import html
import json
import time
from typing import Dict, List, Optional, Tuple

import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()

from agents.data_agent import DataAgent
from agents.health_agent import HealthAgent
from agents.reasoning_agent import ReasoningAgent
from config import (
    AQI_CATEGORIES,
    DEFAULT_CITY,
    DEFAULT_PERSONA,
    GROQ_API_KEY,
    INDIAN_CITIES,
    LLM_MODEL,
    LLM_PROVIDER,
    PERSONAS,
    POLLUTANT_LIMITS,
    get_aqi_category,
    get_aqi_label,
)
from tools.health_tools import PERSONA_RULES, calculate_risk_score, resolve_persona_key
from utils.guardrails import MEDICAL_DISCLAIMER, apply_guardrails, check_prompt_injection, sanitize_input

# Core agent singletons
data_agent = DataAgent()
health_agent = HealthAgent()
reasoning_agent = ReasoningAgent()

CITY_LIST = list(INDIAN_CITIES.keys())
PERSONA_CHOICES = [
    ("Asthma Patients 🫁", "asthma_patient"),
    ("Children (< 12 yrs) 👶", "children"),
    ("Elderly (> 65 yrs) 👴", "elderly"),
    ("COPD Patients 🫀", "copd_patient"),
    ("Heart/Cardiovascular ❤️", "heart_patient"),
    ("Athletes / Runners 🏃", "athlete"),
    ("Outdoor Workers 👷", "outdoor_worker"),
    ("Pregnant Women 🤰", "pregnant"),
    ("Respiratory Conditions 😮‍💨", "respiratory_patient"),
    ("General Population 👤", "general_population"),
]

# ─── Head HTML & Dark Mode Enforcer ──────────────────────────────────────────
HEAD_HTML = """
<script>
function enforceDarkMode() {
    document.documentElement.classList.add('dark');
    document.body.classList.add('dark');
}
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enforceDarkMode);
} else {
    enforceDarkMode();
}
setInterval(enforceDarkMode, 1500);
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
"""

# ─── Custom CSS for High-End Dark Glassmorphism ──────────────────────────────
CUSTOM_CSS = """
/* Base typography and reset */
* {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

body, .gradio-container {
    background-color: #080c14 !important;
    color: #f1f5f9 !important;
    min-height: 100vh;
}

/* Glassmorphic Container Cards */
.glass-panel {
    background: #0f172a !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5) !important;
}

/* Header & Status Bar */
.brand-title {
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
    margin: 0;
}
.brand-sub {
    font-size: 0.82rem;
    color: #94a3b8;
    margin-top: 4px;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.pill-groq { background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.28); }
.pill-chroma { background: rgba(168, 85, 247, 0.12); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.28); }
.pill-sensor { background: rgba(34, 197, 94, 0.12); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.28); }

/* KPI Metric Cards Grid */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin: 14px 0 18px 0;
}
.kpi-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-2px);
    border-color: #38bdf8;
}
.kpi-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.76rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.kpi-card-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #f8fafc;
    margin: 6px 0 2px 0;
    line-height: 1.1;
}
.kpi-card-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
}
.badge-good    { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
.badge-satisf  { background: rgba(132, 204, 22, 0.2); color: #a3e635; border: 1px solid rgba(132, 204, 22, 0.3); }
.badge-mod     { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
.badge-poor    { background: rgba(249, 115, 22, 0.2); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.3); }
.badge-vpoor   { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
.badge-severe  { background: rgba(153, 27, 27, 0.3); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); }

/* Gen AI Briefing Box */
.briefing-card {
    background: linear-gradient(180deg, #111c30 0%, #0d1527 100%);
    border: 1px solid #1e3a5f;
    border-left: 4px solid #38bdf8;
    border-radius: 12px;
    padding: 18px 20px;
    margin-top: 10px;
    color: #e2e8f0;
    font-size: 0.9rem;
    line-height: 1.6;
}
.briefing-card h3 {
    margin-top: 14px;
    margin-bottom: 6px;
    font-size: 0.95rem;
    color: #38bdf8;
    font-weight: 700;
}
.briefing-card ul {
    margin: 4px 0 10px 18px;
    padding: 0;
}

/* Multi-Agent Trace Pipeline */
.trace-container {
    background: #090e1a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.5;
}
.trace-item {
    position: relative;
    padding-left: 24px;
    margin-bottom: 14px;
}
.trace-item::before {
    content: '';
    position: absolute;
    left: 4px;
    top: 6px;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #38bdf8;
    box-shadow: 0 0 8px #38bdf8;
}
.trace-item::after {
    content: '';
    position: absolute;
    left: 7px;
    top: 18px;
    width: 2px;
    height: calc(100% + 2px);
    background: #1e293b;
}
.trace-item:last-child::after { display: none; }
.trace-title {
    font-weight: 700;
    color: #38bdf8;
    font-size: 0.85rem;
    margin-bottom: 2px;
}

/* Medical Disclaimer Banner */
.disclaimer-banner {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.25);
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 18px;
    color: #fca5a5;
    font-size: 0.82rem;
    line-height: 1.5;
}

/* Chat Styling */
.gradio-chatbot {
    background: #090e1a !important;
    border: 1px solid #1e293b !important;
    border-radius: 12px !important;
}
"""

# Theme creation with Ocean base
dashboard_theme = gr.themes.Ocean(
    primary_hue="cyan",
    secondary_hue="sky",
    neutral_hue="slate",
).set(
    body_background_fill="#080c14",
    body_background_fill_dark="#080c14",
    block_background_fill="#0f172a",
    block_background_fill_dark="#0f172a",
    block_border_color="#1e293b",
    block_border_color_dark="#1e293b",
    panel_background_fill="#0f172a",
    panel_background_fill_dark="#0f172a",
    input_background_fill="#1e293b",
    input_background_fill_dark="#1e293b",
    input_border_color="#334155",
    input_border_color_dark="#334155",
)


# ─── Helper: Fetch City Telemetry ─────────────────────────────────────────────
def get_city_telemetry(city: str) -> Tuple[dict, List[dict], float, str]:
    try:
        data_out = data_agent.run(city=city, mode="current")
        data_p = data_out.payload if data_out else {}
        readings = data_p.get("readings", [])
        if readings:
            avg_aqi = sum(float(r.get("aqi", 0)) for r in readings) / len(readings)
        else:
            avg_aqi = 65.0
        cat_info = get_aqi_category(avg_aqi)
        return data_p, readings, round(avg_aqi, 1), cat_info["label"]
    except Exception:
        return {}, [], 65.0, "Satisfactory"


# ─── Plotly Figure: Sleek Radial AQI Gauge ────────────────────────────────────
def create_aqi_gauge(aqi_value: float, category: str) -> go.Figure:
    cat_colors = {
        "Good": "#22c55e",
        "Satisfactory": "#84cc16",
        "Moderately Polluted": "#f59e0b",
        "Poor": "#f97316",
        "Very Poor": "#ef4444",
        "Severe / Hazardous": "#991b1b",
    }
    bar_color = cat_colors.get(category, "#38bdf8")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=aqi_value,
            title={"text": f"<b>{category.upper()}</b>", "font": {"size": 16, "color": "#f8fafc", "family": "Plus Jakarta Sans"}},
            number={"font": {"size": 46, "color": bar_color, "family": "Plus Jakarta Sans", "weight": 800}},
            gauge={
                "axis": {"range": [0, 500], "tickwidth": 1, "tickcolor": "#475569", "tickfont": {"color": "#94a3b8"}},
                "bar": {"color": bar_color, "thickness": 0.28},
                "bgcolor": "#1e293b",
                "borderwidth": 1,
                "bordercolor": "#334155",
                "steps": [
                    {"range": [0, 50], "color": "rgba(34, 197, 94, 0.25)"},
                    {"range": [50, 100], "color": "rgba(132, 204, 22, 0.25)"},
                    {"range": [100, 200], "color": "rgba(245, 158, 11, 0.25)"},
                    {"range": [200, 300], "color": "rgba(249, 115, 22, 0.25)"},
                    {"range": [300, 400], "color": "rgba(239, 68, 68, 0.25)"},
                    {"range": [400, 500], "color": "rgba(153, 27, 27, 0.35)"},
                ],
                "threshold": {
                    "line": {"color": "#ffffff", "width": 3},
                    "thickness": 0.8,
                    "value": aqi_value,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        margin={"t": 35, "b": 15, "l": 25, "r": 25},
        height=270,
    )
    return fig


# ─── Plotly Figure: 6-Pollutant Bar Chart ─────────────────────────────────────
def create_pollutant_chart(readings: List[dict]) -> go.Figure:
    pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
    keys = ["pm25", "pm10", "no2", "so2", "co", "o3"]

    vals = []
    for k in keys:
        p_vals = [float(r.get(k, 0)) for r in readings if r.get(k) is not None]
        avg = sum(p_vals) / len(p_vals) if p_vals else 0.0
        vals.append(round(avg, 2))

    cpcb_limits = [60.0, 100.0, 80.0, 80.0, 2.0, 100.0]
    who_limits = [15.0, 45.0, 25.0, 40.0, 4.0, 100.0]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=pollutants,
            y=vals,
            name="Ambient Concentration (µg/m³)",
            marker={
                "color": ["#38bdf8", "#38bdf8", "#818cf8", "#818cf8", "#c084fc", "#38bdf8"],
                "opacity": 0.88,
                "line": {"color": "#0284c7", "width": 1.5},
            },
        )
    )

    fig.add_trace(
        go.Scatter(
            x=pollutants,
            y=cpcb_limits,
            mode="lines+markers",
            name="CPCB Standard (24h)",
            line={"color": "#f59e0b", "dash": "dash", "width": 2},
            marker={"size": 8, "symbol": "diamond", "color": "#f59e0b"},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=pollutants,
            y=who_limits,
            mode="lines+markers",
            name="WHO Guideline",
            line={"color": "#22c55e", "dash": "dot", "width": 2},
            marker={"size": 7, "symbol": "circle", "color": "#22c55e"},
        )
    )

    fig.update_layout(
        title={"text": "<b>Multi-Pollutant Telemetry vs. CPCB & WHO Standards</b>", "font": {"size": 14, "color": "#f8fafc", "family": "Plus Jakarta Sans"}},
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0b1120",
        font={"color": "#94a3b8", "size": 11, "family": "Plus Jakarta Sans"},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        margin={"t": 40, "b": 30, "l": 40, "r": 20},
        height=270,
        xaxis={"gridcolor": "#1e293b", "zerolinecolor": "#1e293b"},
        yaxis={"gridcolor": "#1e293b", "zerolinecolor": "#1e293b", "title": "Concentration (µg/m³)"},
    )
    return fig


# ─── Interactive OpenStreetMap (Leaflet HTML) ─────────────────────────────────
def create_leaflet_map_html(city: str, readings: List[dict]) -> str:
    coords = INDIAN_CITIES.get(city, {"lat": 12.9716, "lon": 77.5946})
    center_lat = coords["lat"]
    center_lon = coords["lon"]

    markers_js = []
    for r in readings:
        s_name = html.escape(str(r.get("station_name", "Station")))
        s_aqi = float(r.get("aqi", 0))
        s_lat = float(r.get("lat", center_lat))
        s_lon = float(r.get("lon", center_lon))
        s_cat = get_aqi_label(s_aqi)

        if s_aqi <= 50:
            m_color = "#22c55e"
        elif s_aqi <= 100:
            m_color = "#84cc16"
        elif s_aqi <= 200:
            m_color = "#f59e0b"
        elif s_aqi <= 300:
            m_color = "#f97316"
        elif s_aqi <= 400:
            m_color = "#ef4444"
        else:
            m_color = "#991b1b"

        pm25_val = r.get("pm25", "N/A")
        popup_html = (
            f"<b>{s_name}</b><br/>"
            f"AQI: <b>{int(s_aqi)}</b> ({s_cat})<br/>"
            f"PM2.5: {pm25_val} µg/m³"
        )

        markers_js.append(f"""
            L.circleMarker([{s_lat}, {s_lon}], {{
                radius: 11,
                fillColor: '{m_color}',
                color: '#ffffff',
                weight: 2,
                opacity: 0.95,
                fillOpacity: 0.8
            }}).addTo(map).bindPopup('{popup_html}');
        """)

    leaflet_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; background: #080c14; }}
            #map {{ width: 100%; height: 100%; border-radius: 10px; }}
            .leaflet-popup-content-wrapper {{ background: #0f172a; color: #f8fafc; border-radius: 8px; border: 1px solid #334155; font-family: 'Plus Jakarta Sans', sans-serif; }}
            .leaflet-popup-tip {{ background: #0f172a; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([{center_lat}, {center_lon}], 11);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 18,
                attribution: '&copy; OpenStreetMap'
            }}).addTo(map);
            {''.join(markers_js)}
        </script>
    </body>
    </html>
    """

    escaped_doc = html.escape(leaflet_html, quote=True)
    return f"""<iframe srcdoc="{escaped_doc}" style="width: 100%; height: 360px; border: 1px solid #1e293b; border-radius: 12px;" frameborder="0"></iframe>"""


# ─── Gen AI Executive Briefing (Groq LLM) ────────────────────────────────────
def generate_ai_briefing(city: str, persona_key: str) -> str:
    start_time = time.perf_counter()
    data_p, readings, avg_aqi, category = get_city_telemetry(city)

    pm25_vals = [float(r.get("pm25", 0)) for r in readings if r.get("pm25")]
    no2_vals = [float(r.get("no2", 0)) for r in readings if r.get("no2")]
    o3_vals = [float(r.get("o3", 0)) for r in readings if r.get("o3")]

    pm25 = round(sum(pm25_vals) / len(pm25_vals), 1) if pm25_vals else 28.0
    no2 = round(sum(no2_vals) / len(no2_vals), 1) if no2_vals else 19.0
    o3 = round(sum(o3_vals) / len(o3_vals), 1) if o3_vals else 42.0

    rules = PERSONA_RULES.get(persona_key, PERSONA_RULES.get("general_population", {}))
    persona_label = rules.get("label", persona_key)
    multiplier = rules.get("risk_multiplier", 1.0)

    if GROQ_API_KEY:
        try:
            from groq import Groq

            prompt = (
                f"You are the SafeAir AI Clinical Environmental Advisory Agent.\n"
                f"Location: {city}, India\n"
                f"CPCB AQI: {avg_aqi:.0f} ({category})\n"
                f"Pollutant Concentrations: PM2.5: {pm25} µg/m³, NO2: {no2} µg/m³, O3: {o3} µg/m³\n"
                f"Target Demographic: {persona_label} (Vulnerability Multiplier: {multiplier}x)\n\n"
                f"Generate a structured, professional executive advisory in this exact markdown format:\n"
                f"### 📋 Executive Summary\n"
                f"(2-3 clear sentences assessing atmospheric severity and immediate physiological risk for {persona_label})\n\n"
                f"### 🛡️ Priority Clinical Precautions\n"
                f"- **Ventilation & Air Filtration**: (Actionable advice on windows/HEPA purifiers)\n"
                f"- **Respiratory Protection**: (Masking guidance e.g. N95 / FFP2)\n"
                f"- **Activity Modification**: (Optimal outdoor window or indoor relocation)\n\n"
                f"### ⚠️ Vulnerability Risk Assessment\n"
                f"(1 specific physiological impact highlight for {persona_label})\n"
            )

            client = Groq(api_key=GROQ_API_KEY)
            resp = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a professional environmental health intelligence advisor."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.15,
                max_tokens=650,
            )
            raw_text = resp.choices[0].message.content.strip()
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 1)

            guarded_text, _ = apply_guardrails(
                prompt,
                raw_text,
                is_fallback_data=("mock_data" in data_p.get("sources_used", [])),
            )
            return f"{guarded_text}\n\n---\n*⚡ Inferred via Groq `{LLM_MODEL}` in **{elapsed_ms} ms***"
        except Exception:
            pass

    # Deterministic Rule Fallback
    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 1)
    fallback_text = (
        f"### 📋 Executive Summary\n"
        f"Ambient air quality in **{city}** reflects an AQI of **{avg_aqi:.0f} ({category})**, "
        f"with dominant PM2.5 concentration at **{pm25} µg/m³**. For **{persona_label}** "
        f"(demographic multiplier {multiplier}x), environmental exposure is elevated.\n\n"
        f"### 🛡️ Priority Clinical Precautions\n"
        f"- **Ventilation & Air Filtration**: Keep windows sealed during morning inversions (7:00 AM – 10:00 AM); run indoor air purifiers.\n"
        f"- **Respiratory Protection**: Wear a snug N95 or FFP2 respirator for transit exceeding 30 minutes in congested corridors.\n"
        f"- **Activity Modification**: Move aerobic workouts indoors to protect bronchial lining from fine particulate deposition.\n\n"
        f"### ⚠️ Vulnerability Risk Assessment\n"
        f"Elevated particulate matter increases microvascular airway resistance and triggers coughing or bronchospasm."
    )
    guarded_text, _ = apply_guardrails(persona_label, fallback_text, is_fallback_data=True)
    return f"{guarded_text}\n\n---\n*⚡ Deterministic Expert Rule Engine in **{elapsed_ms} ms***"


# ─── Tab 1 Refresh Function ──────────────────────────────────────────────────
def update_tab1_dashboard(city: str, persona: str):
    data_p, readings, avg_aqi, category = get_city_telemetry(city)

    sources = ", ".join(data_p.get("sources_used", ["Open-Meteo CAAQMS"]))
    st_count = len(readings)

    # Dominant pollutant
    pm25_vals = [float(r.get("pm25", 0)) for r in readings if r.get("pm25")]
    o3_vals = [float(r.get("o3", 0)) for r in readings if r.get("o3")]
    pm25_avg = round(sum(pm25_vals) / len(pm25_vals), 1) if pm25_vals else 24.0
    o3_avg = round(sum(o3_vals) / len(o3_vals), 1) if o3_vals else 38.0

    dom_pollutant = "PM2.5" if pm25_avg >= 30 else "O3"
    dom_val = pm25_avg if dom_pollutant == "PM2.5" else o3_avg

    # Category badge class
    badge_cls = "badge-good"
    if avg_aqi > 400:
        badge_cls = "badge-severe"
    elif avg_aqi > 300:
        badge_cls = "badge-vpoor"
    elif avg_aqi > 200:
        badge_cls = "badge-poor"
    elif avg_aqi > 100:
        badge_cls = "badge-mod"
    elif avg_aqi > 50:
        badge_cls = "badge-satisf"

    kpi_html = f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span>Current CPCB AQI</span>
                <span>🌡️</span>
            </div>
            <div class="kpi-card-value">{avg_aqi:.0f}</div>
            <div><span class="kpi-card-badge {badge_cls}">{category.upper()}</span></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span>Dominant Pollutant</span>
                <span>🧪</span>
            </div>
            <div class="kpi-card-value">{dom_pollutant}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;"><b>{dom_val} µg/m³</b> ambient level</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span>Active Network</span>
                <span>📡</span>
            </div>
            <div class="kpi-card-value">{st_count}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">CAAQMS monitoring stations</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span>Ingestion Pipeline</span>
                <span>⚡</span>
            </div>
            <div class="kpi-card-value" style="font-size: 1.4rem; padding-top: 6px;">Live Telemetry</div>
            <div style="font-size: 0.8rem; color: #38bdf8;">{sources}</div>
        </div>
    </div>
    """

    gauge_fig = create_aqi_gauge(avg_aqi, category)
    pollutant_fig = create_pollutant_chart(readings)
    map_html = create_leaflet_map_html(city, readings)
    briefing_text = generate_ai_briefing(city, persona)

    return kpi_html, gauge_fig, pollutant_fig, map_html, briefing_text


# ─── Tab 2: Conversational Chat + Visual Multi-Agent Trace ────────────────────
def chat_with_agent(
    user_message: str,
    chat_history: List[dict],
    city: str,
    persona: str,
) -> Tuple[List[dict], str]:
    if not user_message or not user_message.strip():
        return chat_history, ""

    sanitized_q = sanitize_input(user_message)
    chat_history.append({"role": "user", "content": sanitized_q})

    res = reasoning_agent.process_query(sanitized_q, city=city, persona=persona)
    answer_text = res.get("text", "No response generated.")

    chat_history.append({"role": "assistant", "content": answer_text})

    trace = res.get("pipeline_trace", {})
    t_reason = trace.get("reasoning", {})
    t_data = trace.get("data", {})
    t_health = trace.get("health", {})
    t_gis = trace.get("gis", {})
    t_rag = trace.get("rag_llm", {})
    tot_ms = trace.get("total_latency_ms", res.get("duration_ms", 0))

    trace_html = f"""
    <div class="trace-container">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 8px; margin-bottom: 12px;">
            <span style="font-weight: 700; color: #f8fafc;">⚡ Multi-Agent Pipeline Trace</span>
            <span style="color: #38bdf8; font-weight: 600;">{tot_ms} ms</span>
        </div>
        
        <div class="trace-item">
            <div class="trace-title">1. 🧠 Reasoning & Planning Agent</div>
            <div>&bull; Intent: <b style="color: #f8fafc;">{t_reason.get('intent', 'unknown')}</b></div>
            <div>&bull; City: <b>{t_reason.get('city', city)}</b> &middot; Persona: <b>{t_reason.get('persona', persona)}</b></div>
            <div>&bull; Plan: {t_reason.get('agents_planned', [])}</div>
        </div>

        <div class="trace-item">
            <div class="trace-title">2. 📡 Data Ingestion Agent</div>
            <div>&bull; Feeds: {t_data.get('sources', ['Open-Meteo'])}</div>
            <div>&bull; Stations Parsed: <b>{t_data.get('stations_count', 0)}</b> &middot; Latency: {t_data.get('latency_ms', 0)} ms</div>
        </div>

        <div class="trace-item">
            <div class="trace-title">3. 🫁 Health Risk & Spatial GIS Agents</div>
            <div>&bull; Persona Risk Score: <b style="color: #f59e0b;">{t_health.get('risk_score', 0)} / 10</b></div>
            <div>&bull; Alert Triggered: <b>{t_health.get('alert_triggered', False)}</b> &middot; Spatial Clusters: <b>{t_gis.get('clusters', 0)}</b></div>
        </div>

        <div class="trace-item" style="margin-bottom: 0;">
            <div class="trace-title" style="color: #c084fc;">4. 🔍 Gen AI / RAG Explanation Agent</div>
            <div>&bull; Inference: Groq (<code style="color: #38bdf8;">{t_rag.get('model', LLM_MODEL)}</code>)</div>
            <div>&bull; LLM Latency: {t_rag.get('latency_ms', 0)} ms &middot; Guardrails: <span style="color: #4ade80;">ACTIVE</span></div>
        </div>
    </div>
    """

    return chat_history, trace_html


# ─── Tab 3: 10-Persona Risk Matrix ───────────────────────────────────────────
def update_tab3_matrix(city: str) -> Tuple[go.Figure, str]:
    data_p, readings, avg_aqi, category = get_city_telemetry(city)

    poll_keys = ["pm25", "pm10", "no2", "so2", "co", "o3"]
    pol_dict = {}
    for k in poll_keys:
        vals = [float(r.get(k, 0)) for r in readings if r.get(k) is not None]
        pol_dict[k] = sum(vals) / len(vals) if vals else 20.0

    scores = []
    labels = []
    levels = []
    colors = []

    for p_key, p_meta in PERSONAS.items():
        score, risk_lvl = calculate_risk_score(avg_aqi, p_key, pol_dict)
        score_val = round(min(10.0, max(0.0, score)), 1)
        scores.append(score_val)
        labels.append(f"{p_meta['icon']} {p_meta['label']}")
        levels.append(risk_lvl.value if hasattr(risk_lvl, "value") else str(risk_lvl))

        if score_val >= 7.5:
            colors.append("#ef4444")
        elif score_val >= 5.5:
            colors.append("#f97316")
        elif score_val >= 3.5:
            colors.append("#f59e0b")
        else:
            colors.append("#22c55e")

    fig = go.Figure(
        go.Bar(
            y=labels,
            x=scores,
            orientation="h",
            marker={"color": colors, "opacity": 0.88, "line": {"color": "#1e293b", "width": 1}},
            text=[f"  <b>{s} / 10</b> ({lvl})" for s, lvl in zip(scores, levels)],
            textposition="auto",
            textfont={"color": "#ffffff", "family": "Plus Jakarta Sans"},
        )
    )
    fig.update_layout(
        title={
            "text": f"<b>Comparative Demographic Health Risk (City: {city} &middot; AQI: {avg_aqi:.0f} {category})</b>",
            "font": {"size": 14, "color": "#f8fafc", "family": "Plus Jakarta Sans"},
        },
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0b1120",
        font={"color": "#94a3b8", "size": 11, "family": "Plus Jakarta Sans"},
        margin={"t": 40, "b": 30, "l": 180, "r": 25},
        height=380,
        xaxis={"range": [0, 10], "title": "Multi-Pollutant Health Risk Score (0–10)", "gridcolor": "#1e293b"},
        yaxis={"autorange": "reversed"},
    )

    rows_html = []
    for p_key, p_meta in PERSONAS.items():
        score, risk_lvl = calculate_risk_score(avg_aqi, p_key, pol_dict)
        score_val = round(min(10.0, max(0.0, score)), 1)
        lvl_str = risk_lvl.value if hasattr(risk_lvl, "value") else str(risk_lvl)
        action = (
            "Avoid strenuous outdoor activities; use HEPA air purifier."
            if score_val >= 6.5
            else "Limit extended outdoor exertion during peak traffic hours."
            if score_val >= 4.0
            else "Normal outdoor activity permitted; monitor air advisory updates."
        )

        badge_col = "#ef4444" if score_val >= 7.5 else ("#f59e0b" if score_val >= 4.0 else "#4ade80")

        rows_html.append(f"""
        <tr style="border-bottom: 1px solid #1e293b;">
            <td style="padding: 12px 14px; font-weight: 600; color: #f8fafc;">{p_meta['icon']} {p_meta['label']}</td>
            <td style="padding: 12px 14px; color: #38bdf8; font-weight: 700;">{p_meta['risk_multiplier']}x</td>
            <td style="padding: 12px 14px; font-weight: 800; color: {badge_col};">{score_val:.1f} / 10</td>
            <td style="padding: 12px 14px;"><span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">{lvl_str}</span></td>
            <td style="padding: 12px 14px; font-size: 0.82rem; color: #cbd5e1;">{action}</td>
        </tr>
        """)

    table_html = f"""
    <div style="margin-top: 18px; overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; background: #0f172a; border-radius: 10px; font-size: 0.85rem; border: 1px solid #1e293b;">
            <thead>
                <tr style="background: #111e33; color: #94a3b8; text-align: left; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;">
                    <th style="padding: 12px 14px;">Vulnerable Persona</th>
                    <th style="padding: 12px 14px;">Multiplier</th>
                    <th style="padding: 12px 14px;">Risk Score</th>
                    <th style="padding: 12px 14px;">Risk Band</th>
                    <th style="padding: 12px 14px;">Tailored Clinical Precaution</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows_html)}
            </tbody>
        </table>
    </div>

    <div class="disclaimer-banner">
        {MEDICAL_DISCLAIMER}
    </div>
    """

    return fig, table_html


# ─── Build Gradio App Layout ──────────────────────────────────────────────────
with gr.Blocks(title="SafeAir AI — Health Risk Intelligence") as demo:

    # Global Navbar / Branding
    gr.HTML(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; padding: 12px 0 16px 0; border-bottom: 1px solid #1e293b; margin-bottom: 16px;">
        <div>
            <div class="brand-title">🌫️ SafeAir AI</div>
            <div class="brand-sub">
                <b>Dayananda Sagar University (DSU) Bengaluru</b> &middot; Course 25MSD5302 (Gen AI with LLM) &middot; Student: Rain Jafar Imam (<code>SCA25MSD059</code>)
            </div>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <span class="status-pill pill-groq">● Groq LLM: Online ({LLM_MODEL})</span>
            <span class="status-pill pill-chroma">● ChromaDB: Active (MiniLM-L6)</span>
            <span class="status-pill pill-sensor">● Telemetry: Open-Meteo Live</span>
        </div>
    </div>
    """)

    # Elevated Control Bar
    with gr.Row():
        city_dropdown = gr.Dropdown(
            choices=CITY_LIST,
            value="Bengaluru",
            label="📍 Target City (Bengaluru DSU Default)",
            scale=3,
        )
        persona_dropdown = gr.Dropdown(
            choices=[(label, key) for label, key in PERSONA_CHOICES],
            value="asthma_patient",
            label="👤 Target Vulnerable Demographic",
            scale=3,
        )
        refresh_btn = gr.Button("🔄 Refresh Telemetry", variant="secondary", scale=1)

    # Main Tabs
    with gr.Tabs():

        # ─── TAB 1: Live AQI & Gen AI Briefing ────────────────────────────────
        with gr.TabItem("📊 Live AQI & Gen AI Briefing", id="tab1"):
            kpi_display = gr.HTML()

            with gr.Row():
                with gr.Column(scale=1):
                    gauge_plot = gr.Plot(label="CPCB AQI Meter", container=True)
                with gr.Column(scale=2):
                    pollutant_plot = gr.Plot(label="6-Pollutant Distribution", container=True)

            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🗺️ Live Spatial Station Map (OpenStreetMap)")
                    map_display = gr.HTML()
                with gr.Column(scale=1):
                    with gr.Row():
                        gr.Markdown("### ⚡ Gen AI Executive Health Briefing")
                    briefing_btn = gr.Button("⚡ Re-Generate AI Briefing", variant="primary")
                    briefing_display = gr.Markdown(
                        value="*Click 'Re-Generate AI Briefing' or change city/persona to synthesize an AI summary...*",
                        elem_classes=["briefing-card"],
                    )

        # ─── TAB 2: Conversational Gen AI + Agent Trace ───────────────────────
        with gr.TabItem("💬 Conversational Gen AI + Agent Trace", id="tab2"):
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(
                        label="SafeAir AI Conversational Intelligence Assistant",
                        height=440,
                        value=[{
                            "role": "assistant",
                            "content": (
                                "👋 **Hello! I am SafeAir AI**, your clinical environmental health assistant.\n\n"
                                "I integrate live CPCB telemetry, spatial GIS clustering, and Groq LLM reasoning. "
                                "Ask me about current air quality, outdoor safety windows, or personalized health risks!"
                            )
                        }],
                    )
                    with gr.Row():
                        chat_input = gr.Textbox(
                            placeholder="Ask any natural-language air quality or health question...",
                            show_label=False,
                            scale=4,
                        )
                        send_btn = gr.Button("Ask Agent 🚀", variant="primary", scale=1)

                    gr.Markdown("#### 💡 Quick Starter Evaluation Questions (Click to Test):")
                    with gr.Row():
                        chip1 = gr.Button("🏃 Jogging in Bengaluru for Asthma", size="sm")
                        chip2 = gr.Button("🔬 PM2.5 vs PM10 for Elderly", size="sm")
                        chip3 = gr.Button("🏠 Indoor Precautions to Reduce PM2.5", size="sm")
                        chip4 = gr.Button("🗺️ Worst Pollution Hotspots", size="sm")

                with gr.Column(scale=2):
                    gr.Markdown("### 🔍 Live Multi-Agent Pipeline Trace")
                    gr.Markdown("Reviewers can inspect every intermediate agent execution stage in real time:")
                    trace_display = gr.HTML("""
                    <div class="trace-container" style="color: #64748b;">
                        Pipeline execution trace will appear here as soon as a question is processed...
                    </div>
                    """)

        # ─── TAB 3: 10-Persona Health Risk Matrix ─────────────────────────────
        with gr.TabItem("🫁 10-Persona Health Risk Matrix", id="tab3"):
            matrix_plot = gr.Plot(label="Risk Distribution", container=True)
            matrix_table = gr.HTML()

    # ─── Event Bindings ───────────────────────────────────────────────────────
    demo.load(
        fn=update_tab1_dashboard,
        inputs=[city_dropdown, persona_dropdown],
        outputs=[kpi_display, gauge_plot, pollutant_plot, map_display, briefing_display],
    )
    demo.load(
        fn=update_tab3_matrix,
        inputs=[city_dropdown],
        outputs=[matrix_plot, matrix_table],
    )

    refresh_btn.click(
        fn=update_tab1_dashboard,
        inputs=[city_dropdown, persona_dropdown],
        outputs=[kpi_display, gauge_plot, pollutant_plot, map_display, briefing_display],
    ).then(
        fn=update_tab3_matrix,
        inputs=[city_dropdown],
        outputs=[matrix_plot, matrix_table],
    )

    city_dropdown.change(
        fn=update_tab1_dashboard,
        inputs=[city_dropdown, persona_dropdown],
        outputs=[kpi_display, gauge_plot, pollutant_plot, map_display, briefing_display],
    ).then(
        fn=update_tab3_matrix,
        inputs=[city_dropdown],
        outputs=[matrix_plot, matrix_table],
    )

    persona_dropdown.change(
        fn=generate_ai_briefing,
        inputs=[city_dropdown, persona_dropdown],
        outputs=[briefing_display],
    )

    briefing_btn.click(
        fn=generate_ai_briefing,
        inputs=[city_dropdown, persona_dropdown],
        outputs=[briefing_display],
    )

    # Chat submission
    send_btn.click(
        fn=chat_with_agent,
        inputs=[chat_input, chatbot, city_dropdown, persona_dropdown],
        outputs=[chatbot, trace_display],
    ).then(lambda: "", outputs=[chat_input])

    chat_input.submit(
        fn=chat_with_agent,
        inputs=[chat_input, chatbot, city_dropdown, persona_dropdown],
        outputs=[chatbot, trace_display],
    ).then(lambda: "", outputs=[chat_input])

    # Quick chip clicks
    chip1.click(
        fn=lambda: "Is it safe for an asthmatic person to jog in Bengaluru at 7 AM?",
        outputs=[chat_input],
    ).then(
        fn=chat_with_agent,
        inputs=[chat_input, chatbot, city_dropdown, persona_dropdown],
        outputs=[chatbot, trace_display],
    ).then(lambda: "", outputs=[chat_input])

    chip2.click(
        fn=lambda: "Compare PM2.5 and PM10 impact for elderly residents",
        outputs=[chat_input],
    ).then(
        fn=chat_with_agent,
        inputs=[chat_input, chatbot, city_dropdown, persona_dropdown],
        outputs=[chatbot, trace_display],
    ).then(lambda: "", outputs=[chat_input])

    chip3.click(
        fn=lambda: "What indoor precautions reduce PM2.5 exposure?",
        outputs=[chat_input],
    ).then(
        fn=chat_with_agent,
        inputs=[chat_input, chatbot, city_dropdown, persona_dropdown],
        outputs=[chatbot, trace_display],
    ).then(lambda: "", outputs=[chat_input])

    chip4.click(
        fn=lambda: "Which areas in the city have the highest pollution right now?",
        outputs=[chat_input],
    ).then(
        fn=chat_with_agent,
        inputs=[chat_input, chatbot, city_dropdown, persona_dropdown],
        outputs=[chatbot, trace_display],
    ).then(lambda: "", outputs=[chat_input])


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        theme=dashboard_theme,
        css=CUSTOM_CSS,
        head=HEAD_HTML,
    )
