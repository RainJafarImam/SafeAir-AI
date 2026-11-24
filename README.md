<div align="center">

# 🌫️ SafeAir AI
### Autonomous Multi-Agent Air Quality Intelligence & Personalized Health Advisory System

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Groq Cloud](https://img.shields.io/badge/LLM-Groq%20Cloud%20(GPT--OSS--120B)-f55036.svg?logo=fastapi&logoColor=white)](https://console.groq.com/)
[![Gradio 6](https://img.shields.io/badge/UI-Gradio%206%20Ocean-orange.svg?logo=gradio&logoColor=white)](https://gradio.app/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit%20Interactive-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![ChromaDB RAG](https://img.shields.io/badge/Vector%20Store-ChromaDB-green.svg)](https://www.trychroma.com/)
[![CPCB Standards](https://img.shields.io/badge/Standards-CPCB%20%2F%20WHO-purple.svg)](https://cpcb.nic.in/)
[![Responsible AI](https://img.shields.io/badge/Guardrails-Active-success.svg)](#-responsible-ai--clinical-guardrails)

**Author / Candidate:** Rain Jafar Imam (`SCA25MSD059`)  
**Degree Program:** Master of Science in Data Science (M.Sc. Data Science) — Semester III  
**Institution:** School of Computer Applications, Dayananda Sagar University (DSU), Bengaluru – 560068  
**Course Code & Title:** 25MSD5302 — Generative AI with LLM (Academic Year 2026–2027)

---

</div>

## 📌 Executive Summary & Problem Formulation

Urban air pollution represents one of the most critical public health crises in South Asia, with major metropolitan regions (Bengaluru, Mumbai, Delhi-NCR, Hyderabad, Chennai, Kolkata, Pune) experiencing recurrent severe pollution episodes driven by fine particulate matter ($PM_{2.5}$, $PM_{10}$), nitrogen oxides ($NO_x$), and ozone ($O_3$). While government agencies such as the Central Pollution Control Board (CPCB) operate continuous ambient air quality monitoring stations (CAAQMS), standard public air quality dashboards suffer from two critical limitations:

1. **Monolithic Generalization:** Standard reporting provides a single numeric index (e.g., "AQI 182 — Moderate/Poor") that treats all citizens identically, failing to account for clinical vulnerability differences (e.g., pediatric respiratory vulnerabilities, elderly cardiovascular fragilities, COPD, pregnancy, or high minute-ventilation in outdoor athletes).
2. **Conversational Hallucination in Generic LLMs:** When users query public LLMs regarding pollution and health safety, ungrounded models routinely hallucinate non-existent sensor readings, misquote statutory pollutant thresholds, or offer dangerous, unverified medical advice without safety disclaimers.

**SafeAir AI** solves this critical gap through a **hierarchical multi-agent cognitive architecture**. By decoupling data ingestion, spatial analysis, clinical risk calculation, vector retrieval-augmented generation (RAG), and user interaction into specialized deterministic agents governed by strict **Responsible AI Guardrails**, SafeAir AI delivers mathematically sound, station-grounded, and personalized environmental health advisories.

---

## 🏛️ System Architecture

SafeAir AI is architected around a multi-agent orchestration pattern where no single agent holds monolithic responsibility. Communication between agents occurs via strongly typed Pydantic models (`AgentMessage`) ensuring end-to-end schema validation.

```
                           +----------------------------------------+
                           |          USER / CITIZEN                |
                           |   (Web UI: Gradio 6 / Streamlit)       |
                           +-------------------+--------------------+
                                               |
                                     [User Query / City Selection]
                                               v
                           +----------------------------------------+
                           |     RESPONSIBLE AI GUARDRAIL LAYER     |
                           |  - Input Sanitization & 500-char clamp |
                           |  - Prompt Injection & Jailbreak Filter |
                           +-------------------+--------------------+
                                               | (Sanitized Input)
                                               v
                           +----------------------------------------+
                           |       REASONING AGENT / PLANNER        |
                           |   (LLM Task Decomposition & Intent)    |
                           +-------------------+--------------------+
                                               |
                     +-------------------------+-------------------------+
                     |                         |                         |
                     v                         v                         v
+--------------------------+ +--------------------------+ +--------------------------+
|        DATA AGENT        | |        GIS AGENT         | |       HEALTH AGENT       |
| 5-Layer Resilient Chain: | | - Haversine Geodesics    | | - 10-Persona Matrix      |
| 1. WAQI CAAQMS Stations  | | - DBSCAN Spatial Cluster | | - Sub-Index Calculator   |
| 2. OpenWeather Pollution | | - Leaflet / Folium Map   | | - Non-linear Exposure    |
| 3. Open-Meteo Air API    | | - Micro-hotspot Bounds   | |   Concentration Formula  |
| 4. SQLite Telemetry DB   | +--------------------------+ +--------------------------+
| 5. Synthetic CPCB Fallback |                         |                         |
+--------------------------+                           |                         |
                     |                                 |                         |
                     +-------------------------+-------+-------------------------+
                                               |
                                               v
                           +----------------------------------------+
                           |       EXPLANATION AGENT (RAG)          |
                           |  - ChromaDB Vector Store Retrieval     |
                           |  - sentence-transformers MiniLM-L6-v2  |
                           |  - CPCB & WHO Knowledge Base Ingestion |
                           |  - Groq Cloud (GPT-OSS-120B / Llama 3) |
                           +-------------------+--------------------+
                                               |
                                               v
                           +----------------------------------------+
                           |      VISUALIZATION & OUTPUT AGENT      |
                           |  - Plotly CPCB Radial Gauge (0-500)    |
                           |  - 6-Pollutant Threshold Stacked Bar   |
                           |  - Clinical Non-Prescriptive Disclaimer|
                           +-------------------+--------------------+
                                               |
                                               v
                           +----------------------------------------+
                           |      RENDERED PRODUCTION DASHBOARD     |
                           +----------------------------------------+
```

---

## 🤖 Multi-Agent Swarm Responsibilities

| Agent Node | Source File | Core Capabilities & Technical Implementation |
| :--- | :--- | :--- |
| **Reasoning Agent** | `agents/reasoning_agent.py` | Decomposes natural language queries into deterministic dependency graphs; applies safety guardrails; determines whether queries require telemetry, spatial analysis, or clinical profiling. |
| **Data Agent** | `agents/data_agent.py` | Executes real-time data ingestion across a 5-tier resilient fallback hierarchy: **WAQI API** $\to$ **OpenWeather** $\to$ **Open-Meteo** $\to$ **SQLite Archive** $\to$ **CPCB Fallback**. |
| **GIS Agent** | `agents/gis_agent.py` | Performs geodesic distance computations (Haversine), spatial bounding-box queries, and **DBSCAN machine learning spatial clustering** to isolate localized pollution hotspots. |
| **Health Agent** | `agents/health_agent.py` | Evaluates personalized vulnerability across a **10-Persona Clinical Matrix**; applies sub-index linear interpolation algorithms following official Indian CPCB guidelines. |
| **Visualization Agent** | `agents/visualization_agent.py` | Generates interactive high-contrast **Plotly** radial gauges, 6-pollutant concentration limit charts, and **Leaflet OpenStreetMap** spatial station tiles. |
| **Explanation Agent** | `agents/explanation_agent.py` | Drives the vector RAG pipeline; queries local ChromaDB collections embedding official CPCB/WHO documentation; synthesizes context-grounded executive health advisories. |

---

## 👥 The 10-Persona Clinical Vulnerability Matrix

Unlike standard tools that calculate risk generically, SafeAir AI models biological sensitivity, respiration volume, and pre-existing physiological vulnerabilities across 10 distinct cohorts:

| # | Persona Identifier | Target Biomarkers / Vulnerability Mechanism | Critical Pollutant Triggers |
| :---: | :--- | :--- | :--- |
| 1 | **Asthma Patient** | Airway hyper-reactivity, immediate bronchospasm | $PM_{2.5}$, $O_3$, $SO_2$ |
| 2 | **COPD Patient** | Irreversible airflow limitation, alveolar destruction | $PM_{2.5}$, $PM_{10}$, $NO_2$ |
| 3 | **Cardiovascular** | Systemic inflammation, endothelial dysfunction, arrhythmia | $PM_{2.5}$, $CO$, $NO_2$ |
| 4 | **Pregnant Woman** | Transplacental particle translocation, fetal hypoxia | $PM_{2.5}$, $CO$ |
| 5 | **Child (<12 yrs)** | Incomplete alveolar development, high minute ventilation | $PM_{2.5}$, $O_3$, $NO_2$ |
| 6 | **Elderly (>65 yrs)** | Diminished physiological reserve, cardiopulmonary aging | $PM_{2.5}$, $PM_{10}$, $O_3$ |
| 7 | **Outdoor Worker** | Prolonged cumulative exposure (8–12 hrs continuous) | $PM_{10}$, $PM_{2.5}$, $NO_2$ |
| 8 | **Athlete / Runner** | Deep oral respiration bypassing nasal cilia filtration | $O_3$, $PM_{2.5}$ |
| 9 | **Pet Owner** | Mammalian respiratory distress and low-ground settling | $PM_{10}$, $O_3$ |
| 10| **General Public** | Baseline standard CPCB epidemiological thresholds | Overall Dominant AQI |

---

## 🛡️ Responsible AI & Clinical Guardrails

SafeAir AI incorporates safety-by-design principles implemented in `utils/guardrails.py`:

1. **Input Sanitization & Length Clamping:** Inputs are clamped to 500 characters, stripped of non-printable ASCII control characters, and evaluated against 12+ prompt injection and jailbreak regex patterns (e.g., system prompt override attempts).
2. **Clinical Non-Prescriptive Enforcement:** To prevent the model from assuming the role of a licensed physician, all advisory outputs automatically append a deterministic, non-dismissible medical disclaimer:
   > *"⚠️ Medical Disclaimer: SafeAir AI provides environmental risk intelligence based on atmospheric models. It does not provide medical diagnoses or prescriptions. Individuals experiencing acute symptoms must consult a registered medical professional."*
3. **Uncertainty & Fallback Transparency:** When real-time CAAQMS sensors are offline or operating in fallback mode, the system surfaces clear data provenance badges so citizens know whether data is live or estimated.

---

## 📊 Empirical Quantitative RAG Benchmarks

The Retrieval-Augmented Generation subsystem was evaluated using an automated benchmark harness (`evaluate_rag.py`) across canonical CPCB queries. Evaluation metrics were collected across latency, semantic retrieval groundedness, contextual relevance, and guardrail compliance:

| Metric | Target Standard | Achieved Score | Evaluation Status |
| :--- | :---: | :---: | :---: |
| **Vector Retrieval Latency** | $< 100 \text{ ms}$ | **$20.98 \text{ ms}$** | 🟢 Exceeds Target (Fast) |
| **LLM Generation Latency (Groq)** | $< 2500 \text{ ms}$ | **$1063.46 \text{ ms}$** | 🟢 Sub-second Inference |
| **Total Query Turnaround** | $< 3000 \text{ ms}$ | **$1084.44 \text{ ms}$** | 🟢 Real-Time Interactive |
| **Contextual Groundedness** | $> 40.0\%$ | **$43.2\%$** | 🟢 Grounded in CPCB Docs |
| **Answer Relevance** | $> 60.0\%$ | **$64.2\%$** | 🟢 Highly Domain Specific |
| **Safety Guardrail Compliance** | $100.0\%$ | **$100.0\%$** | 🟢 Zero Jailbreak Vulnerability |

*Full quantitative tables and JSON log traces are archived in [evaluation/rag_evaluation_report.md](evaluation/rag_evaluation_report.md).*

---

## 📁 Repository Structure

```
GenAI-2/
├── .env.example                  # Environment configuration template (safe to commit)
├── .gitignore                    # Production gitignore protecting keys, DBs, and virtualenvs
├── config.py                     # Centralized settings, persona definitions, and CPCB breakpoints
├── gradio_app.py                 # Primary Production Dashboard (Gradio 6 Dark-Ocean Glassmorphic)
├── app.py                        # Alternative Multi-Tab Dashboard (Streamlit)
├── evaluate_rag.py               # Standalone automated RAG benchmark evaluation suite
├── requirements.txt              # Production dependency specifications
│
├── agents/                       # Multi-Agent Cognitive Swarm
│   ├── base_agent.py             # Abstract base agent with telemetry and lifecycle hooks
│   ├── orchestrator.py           # Master DAG orchestrator managing inter-agent message buses
│   ├── reasoning_agent.py        # Intent classification, planning, and guardrails
│   ├── data_agent.py             # Multi-source ingestion & 5-tier fallback engine
│   ├── gis_agent.py              # Geodesic calculation and DBSCAN spatial clustering
│   ├── health_agent.py           # 10-Persona clinical risk and CPCB sub-index calculator
│   ├── visualization_agent.py    # Plotly radial gauges, bar charts, and Leaflet map generator
│   └── explanation_agent.py      # Vector RAG synthesis engine
│
├── tools/                        # Deterministic Analytical Tools
│   ├── aqi_tools.py              # CPCB mathematical sub-index calculation routines
│   ├── geo_tools.py              # Haversine distance, bounding box, and geolocation utils
│   └── health_tools.py           # Physiological dose-response functions and symptom maps
│
├── schemas/                      # Strongly Typed Pydantic Contracts
│   └── agent_messages.py         # AgentMessage, SensorReading, and PersonaRisk schemas
│
├── utils/                        # System Utilities & Safety Framework
│   ├── guardrails.py             # Input sanitization, jailbreak defense, and medical disclaimer
│   ├── logger.py                 # Loguru structured JSON logger
│   └── retry.py                  # Tenacity exponential backoff decorators
│
├── data/                         # Data Architecture
│   ├── database.py               # SQLAlchemy SQLite persistence layer
│   ├── vector_store.py           # ChromaDB client wrapping sentence-transformers
│   └── sample_data.py            # Calibrated CPCB CAAQMS benchmark stations
│
├── evaluation/                   # Academic Benchmark Deliverables
│   ├── rag_evaluation_report.md  # Detailed empirical evaluation report
│   └── rag_benchmark_results.json# Raw benchmark metric logs
│
├── docs/                         # Formal Academic & Thesis Documentation
│   ├── SafeAir_AI_Project_Report.docx   # Complete 10-chapter formal Word project report
│   ├── SafeAir_AI_Project_Report.md     # Markdown companion report
│   ├── SafeAir_AI_Project_Synopsis.docx # Formal Word submission synopsis
│   ├── SafeAir_AI_Project_Synopsis.md   # Markdown companion synopsis
│   ├── safeair_ai_project_review.md     # Architecture review and roadmap specification
│   └── Research.md                      # Epidemiological and toxicological foundation paper
│
└── scripts/                      # Build & Report Generator Utilities
    ├── generate_report.py        # Word report (.docx) compilation utility
    └── generate_doc.py           # Word synopsis (.docx) compilation utility
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- Python **3.10+** or **3.11** installed.
- Git installed.
- Free API Keys:
  - **Groq Cloud API Key:** [console.groq.com](https://console.groq.com) (Free high-speed inference)
  - **WAQI API Token (Optional but recommended):** [aqicn.org/data-platform/token/](https://aqicn.org/data-platform/token/)
  - **OpenWeatherMap API Key (Optional):** [openweathermap.org/api](https://openweathermap.org/api)

### 2. Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/your-username/SafeAir-AI.git
cd SafeAir-AI

# Create and activate Python virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the template configuration file and add your credentials:

```bash
# On Windows Powershell:
Copy-Item .env.example .env
# On Linux / macOS:
cp .env.example .env
```

Open `.env` in any text editor and populate your keys:
```env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_groq_key_here
LLM_MODEL=openai/gpt-oss-120b
WAQI_API_KEY=your_waqi_token_here
OPENWEATHER_API_KEY=your_openweather_key_here
DEFAULT_CITY=Bengaluru
DEFAULT_PERSONA=asthma_patient
```

### 4. Launch the Applications

#### Option A: Production Gradio Dashboard (Recommended)
```bash
python gradio_app.py
```
*Access in browser at:* **`http://127.0.0.1:7860`**  
Features: Glassmorphic dark ocean theme, live KPI telemetry, Plotly radial gauge, 6-pollutant threshold bars, multi-agent pipeline trace, and 10-persona vulnerability matrix.

#### Option B: Streamlit Multi-Tab Dashboard
```bash
streamlit run app.py
```
*Access in browser at:* **`http://127.0.0.1:8501`**

#### Option C: Run RAG Benchmark Suite
```bash
python evaluate_rag.py
```
*Executes automated latency and accuracy benchmarks against CPCB standards and saves reports to `evaluation/`.*

---

## 📚 Academic Documentation & Research Papers

For academic evaluators, university committees, and researchers, complete thesis materials are located in the `docs/` folder:

| Document | Format | Description |
| :--- | :---: | :--- |
| **Academic Research Paper (Elsevier Format)** | [.docx](docs/SafeAir_AI_Research_Paper.docx) \| [.md](docs/SafeAir_AI_Research_Paper.md) | Final peer-reviewed journal format (Elsevier ScienceDirect standard, Article Info box, 3-line tables, CReDiT statement, Harvard/APA references). |
| **Comprehensive Project Report** | [.docx](docs/SafeAir_AI_Project_Report.docx) \| [.md](docs/SafeAir_AI_Project_Report.md) | 10-Chapter formal project report including Title Page, Certificate, Abstract, Architecture, Implementation, and References. |
| **Project Synopsis** | [.docx](docs/SafeAir_AI_Project_Synopsis.docx) \| [.md](docs/SafeAir_AI_Project_Synopsis.md) | Formal 4-page academic submission synopsis for project review committee. |
| **Medical & Epidemiological Research** | [.md](docs/Research.md) | Clinical analysis of $PM_{2.5}$, $PM_{10}$, $NO_2$, and $O_3$ health mechanics across vulnerable cohorts. |

---

## 📜 Ethical Considerations & Disclaimer

SafeAir AI is an academic research platform designed for educational and informational purposes. While calculation formulas adhere strictly to official Central Pollution Control Board (CPCB) and World Health Organization (WHO) publication standards, ambient atmospheric modeling involves inherent spatial variances. The platform should not be substituted for clinical advice from certified medical practitioners.

---

## 👨‍💻 Candidate Credit & Acknowledgments

- **Lead Developer & Researcher:** **Rain Jafar Imam** (`SCA25MSD059`)
- **Institution:** School of Computer Applications, **Dayananda Sagar University (DSU)**, Bengaluru, Karnataka, India.
- **Academic Advisor / Department:** M.Sc. Data Science Faculty, Department of Computer Applications.
- **Coursework:** 25MSD5302 — Generative AI with LLM.

<div align="center">
  <sub>© 2026–2027 SafeAir AI — Developed by Rain Jafar Imam. All rights reserved.</sub>
</div>
