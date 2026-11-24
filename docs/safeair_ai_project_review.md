# SafeAir AI — Gen AI Project Review, Architecture & Technical Guide

**Student:** Rain Jafar Imam (`SCA25MSD059`)  
**Program:** M.Sc. Data Science (Semester III), School of Computer Applications, Dayananda Sagar University (DSU), Bengaluru  
**Course:** 25MSD5302 — Generative AI with LLM ([Course Syllabus — GENAI_LLM.pdf](https://drive.google.com/file/d/1tGEvdSceKCfWDAYRay4Ud0MbYqy71kCe/view?usp=drivesdk))  
**System:** SafeAir AI Multi-Agent AQI Health Risk Intelligence System  
**Local Project Directory:** `D:\GenAI-2`  
**Review Date:** November 24, 2026

---

## 1. Executive Summary & Problem Statement

Urban air quality monitoring dashboards typically suffer from two limitations: either they display raw pollutant numbers (PM2.5, PM10, NO2, O3) without actionable personal guidance, or they wrap a general-purpose LLM that risks hallucinating live readings and medical thresholds.

**SafeAir AI** bridges this gap using a **hybrid Multi-Agent + RAG + Deterministic Health Scoring architecture** tailored to Indian cities and Central Pollution Control Board (CPCB) AQI standards:
- **Deterministic engines** compute exact CPCB AQI sub-indices and persona-specific health risk scores so numerical outputs remain auditable and hallucination-free.
- **Generative AI (LLM + RAG)** handles natural-language planning, context retrieval over station/guideline embeddings, and personalized preventive advisories.
- **Classical Machine Learning (DBSCAN)** identifies spatial pollution hotspots across monitoring stations.

---

## 2. Course Alignment (25MSD5302 — Generative AI with LLM)

| Syllabus Unit / Outcome | Course Topic ([GENAI_LLM.pdf](https://drive.google.com/file/d/1tGEvdSceKCfWDAYRay4Ud0MbYqy71kCe/view?usp=drivesdk)) | Implementation in SafeAir AI |
| --- | --- | --- |
| **Unit I / CO1** | Generative AI & Transformer / LLM fundamentals | Decoder-only LLM inference via Groq (`llama-3.3-70b-versatile`) for structured planning and natural-language synthesis |
| **Unit II / CO2** | Embeddings & task-specific LLM application | Dense text embeddings (`sentence-transformers` / `all-MiniLM-L6-v2`) stored in ChromaDB for semantic retrieval |
| **Unit III / CO3** | Prompt engineering, RAG, RAG evaluation, tool calling & Agents | 6-agent orchestrator with Pydantic JSON handoffs, ChromaDB RAG pipeline, tool-based AQI/GIS queries, and planned RAG evaluation harness |
| **Unit IV / CO4** | Responsible LLMs, hallucination mitigation & guardrails | Deterministic CPCB & persona risk engine prevents numeric hallucination; non-prescriptive medical disclaimer & input length/sanitization guardrails |
| **Unit V / CO5** | Reasoning with LLMs & real-world AI systems | Reasoning/Planner agent decomposes multi-part user queries into sequential tool and sub-agent calls |

---

## 3. Where Gen AI Is Used (vs. ML & Deterministic Logic)

A common project-review question is *"Which exact parts use Generative AI, and why isn't everything an LLM?"* Use this breakdown during your presentation and viva:

| Module / File | AI Category | Technology | Role in Pipeline |
| --- | --- | --- | --- |
| **Reasoning / Planner Agent** (`agents/reasoning_agent.py`) | **Generative AI (LLM)** | Groq API (or OpenAI) | Interprets free-form user questions and outputs a structured execution plan specifying which sub-agents to invoke |
| **Explanation Agent** (`agents/explanation_agent.py`) | **Generative AI (RAG + LLM)** | ChromaDB + `all-MiniLM-L6-v2` + Groq LLM | Retrieves grounded AQI readings and health guidelines from the vector store and synthesizes clear, persona-aware advice |
| **Gen AI Daily Briefing** (`gradio_app.py`) | **Generative AI (LLM)** | Groq API | Generates an instant, plain-English executive summary and 3 actionable precautions right on the main dashboard |
| **GIS Spatial Agent** (`agents/gis_agent.py`) | **Classical ML** | `scikit-learn` (DBSCAN), Folium | Clusters monitoring stations spatially to flag localized pollution hotspots |
| **Health Risk Engine** (`agents/health_agent.py`) | **Deterministic Rules** | Python / CPCB thresholds | Computes exact 0–10 risk scores across 10 vulnerable personas (Asthma, Elderly, Child, Athlete, etc.) without hallucination |
| **Data Ingestion Agent** (`agents/data_agent.py`) | **Data Engineering** | WAQI, OpenWeather, Open-Meteo, SQLite | Fetches live pollutant telemetry with multi-layer fallback so demos never fail offline |

---

## 4. Current Features Present in the System

The SafeAir AI architecture includes:
- **Hierarchical Multi-Agent Orchestrator:** Coordinates specialized agents (`reasoning_agent`, `data_agent`, `gis_agent`, `health_agent`, `visualization_agent`, `explanation_agent`).
- **Typed Inter-Agent Communication:** Pydantic v2 `AgentMessage` JSON schemas (`schemas/agent_messages.py`) for structured handoffs instead of brittle regex parsing.
- **ChromaDB RAG Store:** Local vector persistence (`data/vector_store.py`) using `sentence-transformers` (`all-MiniLM-L6-v2`).
- **5-Layer Data Resiliency Fallback:** WAQI API -> OpenWeather Air Pollution -> Web scraping -> User CSV upload -> Realistic mock data.
- **CPCB AQI & 10-Persona Risk Scoring:** Supports General Adult, Child, Elderly, Asthma, COPD/Respiratory, Heart Patient, Pregnant Individual, Outdoor Worker, Athlete, and Sensitive Groups.
- **Observability:** SQLite telemetry logging (`data/database.py`), Loguru rotating logs (`utils/logger.py`), and Tenacity retry decorators (`utils/retry.py`).

---

## 5. Gap Analysis — What Is Missing or Broken ("What Is Not There")

### A. Critical UI & Usability Defects (Observed in Local Run)
1. **Unreadable Dark-on-Dark Text (Missing Theme Config):** The original Streamlit app injects dark CSS without a `.streamlit/config.toml` dark theme, causing Streamlit to render dark gray text on a dark navy background alongside bright white headers, buttons, and upload boxes.
2. **Broken Map Basemap (`API KEY REQUIRED`):** Folium uses CartoDB map tiles that now require a registered Carto API key, displaying watermarked gray squares instead of a city map.
3. **Gen AI Not Visible on Landing Screen:** The landing view only displays deterministic risk scores and a broken map, hiding the actual Gen AI capabilities inside a secondary tab.
4. **No Visible Agent/RAG Execution Trace:** Reviewers cannot see which agents fired or what retrieved context grounded the LLM response.

### B. Gen AI & Academic Depth Gaps
5. **Unconfigured LLM API Key:** In the local run, `Groq`, `OpenAI`, and `WAQI` indicators were all red—meaning the LLM Reasoning and RAG Explanation agents were inactive.
6. **Mumbai-Only Default Focus:** The base repository defaults to Mumbai; adding **Bengaluru** (and major Indian metros such as Delhi, Chennai, Hyderabad, Kolkata, and Pune) makes the project far more relevant for a DSU Bengaluru review.
7. **No Quantitative RAG Evaluation Script:** Unit III of [GENAI_LLM.pdf](https://drive.google.com/file/d/1tGEvdSceKCfWDAYRay4Ud0MbYqy71kCe/view?usp=drivesdk) emphasizes *Evaluation of RAGs*. There is currently no benchmark script scoring groundedness/faithfulness or latency across test prompts.
8. **No Explicit Responsible AI / Safety Guardrail Layer:** Unit IV emphasizes *Responsible LLMs*. The system needs explicit input sanitization (prompt-injection protection), uncertainty disclosure when falling back to simulated data, and a consistent non-prescriptive medical disclaimer.
9. **No Multi-Turn Chat Memory:** Follow-up questions (e.g., *"What about for my 7-year-old?"*) are not consistently carried across turns in the default interface.

---

## 6. What You Have to Provide (Student Action Checklist)

Complete these items before your project review so the live demo and documentation are 100% ready:

### 1. API Keys & Environment (`.env` in `D:\GenAI-2`)
| Variable | Required? | Where to Get It | Purpose |
| --- | --- | --- | --- |
| `LLM_PROVIDER=groq` | **Yes** | Set directly in `.env` | Selects Groq instead of OpenAI |
| `GROQ_API_KEY` | **Yes** | Free tier at [Groq Console](https://console.groq.com/) | Powers the Gen AI Reasoning, Daily Briefing, and RAG Explanation agents |
| `WAQI_API_KEY` | Optional | Free token at [WAQI API](https://aqicn.org/data-platform/token/) | Primary Indian CAAQMS station feed (note: `gradio_app.py` also pulls live free data from Open-Meteo with zero API key needed) |
| `OPENWEATHER_API_KEY` | Optional | Free tier at [OpenWeather](https://openweathermap.org/api) | Secondary air-pollution fallback |

### 2. Python Packages for the New Gradio UI
From `(.venv) D:\GenAI-2>`, install the Gradio UI dependencies:
```bat
pip install gradio plotly requests python-dotenv groq
```

### 3. Project Review Deliverables You Should Prepare
- **Working Live Demo:** Run `python gradio_app.py` and keep `http://127.0.0.1:7860` open for the review panel.
- **5–10 Evaluation Queries:** Prepare a short list of real questions (e.g., *"Is it safe for an asthmatic person to jog in Bengaluru at 7 AM?"*, *"Compare PM2.5 and PM10 impact for elderly residents"*, *"What indoor precautions reduce PM2.5?"*) to demonstrate multi-agent planning, grounded RAG answers, and guardrails.
- **Screenshots & Metrics:** Capture screenshots of the Live AQI Dashboard + Gen AI Briefing, Conversational AI Chat + Agent Trace, and 10-Persona Risk Matrix for your final report and slides.
- **Architecture Diagram & Viva Talking Points:** Be ready to explain why CPCB AQI calculation and risk scoring are deterministic while planning and explanation use Gen AI (hallucination control).

---

## 7. Upgraded Gradio UI (`gradio_app.py`) — What Was Built for You

To replace the broken Streamlit interface with a clean, user-friendly UI, **`gradio_app.py`** has been created for `D:\GenAI-2`:

- **Modern Dark Dashboard UI:** High-contrast readable typography, glassmorphic KPI cards, color-coded CPCB AQI status badges, and live API/system status pills.
- **Live Indian City Telemetry (Zero-Key Ready):** Supports **Bengaluru, Mumbai, Delhi, Chennai, Hyderabad, Kolkata, and Pune** via the free Open-Meteo Air Quality API (with automatic deterministic fallback if offline) and official CPCB AQI sub-index math.
- **Working Interactive Map:** Uses free **OpenStreetMap** tiles via Leaflet—no CartoDB `API KEY REQUIRED` watermark.
- **Gen AI Front-and-Center:**
  - **Tab 1 — Live AQI & Gen AI Briefing:** Radial Plotly AQI gauge, 6-pollutant bar chart, interactive city map, and a one-click **Gen AI Executive Health Briefing** powered by Groq.
  - **Tab 2 — Conversational Gen AI + Agent Trace:** Multi-turn chat with quick-ask starter chips, automatic hook into your local `agents/orchestrator.py` (with seamless Groq + grounded-context fallback), and a **live Agent Pipeline Trace** showing *Reasoning -> Data -> Health -> RAG Explanation*.
  - **Tab 3 — 10-Persona Health Risk Matrix:** Interactive comparison chart across all 10 vulnerable groups with tailored preventive actions and a Responsible AI medical disclaimer.

### How to Run the New UI in `D:\GenAI-2`
1. Save `gradio_app.py` inside `D:\GenAI-2\`.
2. Ensure `D:\GenAI-2\.env` contains:
   ```env
   LLM_PROVIDER=groq
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. Run from `(.venv) D:\GenAI-2>`:
   ```bat
   pip install gradio plotly requests python-dotenv groq
   python gradio_app.py
   ```
4. Open the local URL printed in the terminal (`http://127.0.0.1:7860`).

---

## 8. Suggested 5-Minute Project Review Demo Script

1. **Problem & Architecture (1 min):** Explain why pure LLMs hallucinate AQI numbers and how SafeAir AI separates deterministic CPCB math from Gen AI reasoning and RAG synthesis.
2. **Live Dashboard & Gen AI Briefing (1.5 min):** Select **Bengaluru** and a persona (e.g., *Asthma Patient* or *Elderly*), show the live AQI gauge, pollutant chart, OpenStreetMap view, and click **Generate AI Briefing**.
3. **Multi-Agent + RAG Chat Demo (1.5 min):** Switch to the **Gen AI Assistant** tab, ask a multi-part question, and point out the **Agent Pipeline Trace** showing each stage executing in sequence.
4. **Persona Matrix & Responsible AI (1 min):** Open the **Persona Risk Matrix** tab, highlight how identical AQI produces different risk scores across demographics, and note the medical-disclaimer guardrail and fallback resiliency.
