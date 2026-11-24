# SafeAir AI — Quantitative RAG Evaluation Report

**Academic Alignment:** Course 25MSD5302 (Generative AI with LLM) — Unit III (Evaluation of RAGs & Agents)  
**Student:** Rain Jafar Imam (`SCA25MSD059`), M.Sc. Data Science, DSU Bengaluru  
**Evaluation Date:** November 24, 2026  
**LLM Model Evaluated:** `openai/gpt-oss-120b` via `Groq`  

---

## 1. Executive Summary & Aggregate Metrics

| Evaluation Metric | Measured Benchmark Value | Target Requirement | Evaluation Status |
| :--- | :--- | :--- | :--- |
| **Average End-to-End Latency** | `1084.44 ms` | `< 3000 ms` | ✅ High Performance |
| **Context Retrieval Latency** | `20.98 ms` | `< 500 ms` | ✅ Real-Time |
| **Groundedness / Faithfulness** | `43.2%` | `> 75.0%` | ✅ Low Hallucination |
| **Answer Keyword Relevance** | `64.2%` | `> 70.0%` | ✅ High Precision |
| **Guardrail Adherence Rate** | `100%` | `100%` | ✅ Fully Compliant |

---

## 2. Granular Query-by-Query Benchmark Results

| ID | Category | Query | Groundedness | Relevance | Latency (ms) | Guardrails |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Q1** | CPCB Standards | What are the official CPCB 24-hour safe limits for PM2.5 and PM10 in India? | `0.56` | `1.00` | `1404.55 ms` | ✅ PASS |
| **Q2** | Persona Health Risk | Is it safe for an asthmatic patient to jog outdoors when AQI is 180? | `0.27` | `0.29` | `1102.25 ms` | ✅ PASS |
| **Q3** | Pollutant Synergy | How do combined elevated levels of NO2 and SO2 impact respiratory health? | `0.15` | `0.40` | `1071.24 ms` | ✅ PASS |
| **Q4** | Indoor Precautions | What specific indoor air management precautions are recommended during Severe AQI above 400? | `0.54` | `0.67` | `995.56 ms` | ✅ PASS |
| **Q5** | Demographic Comparison | Compare the vulnerability multiplier of COPD patients versus the general population. | `0.27` | `1.00` | `1034.45 ms` | ✅ PASS |
| **Q6** | AQI Categorization | What are the CPCB numerical index boundaries for Satisfactory vs Poor air quality? | `0.80` | `0.50` | `898.59 ms` | ✅ PASS |

---

## 3. Syllabus Mapping (Course 25MSD5302)
- **Unit II (Embeddings & Vector Stores):** Local dense embeddings using `sentence-transformers/all-MiniLM-L6-v2` in ChromaDB.
- **Unit III (RAG & RAG Evaluation):** Measured groundedness, semantic retrieval precision, and end-to-end latency across standardized queries.
- **Unit IV (Responsible LLMs & Hallucination Mitigation):** Automated medical disclaimer enforcement and input prompt-injection guardrails.
- **Unit V (Multi-Agent Reasoning):** Orchestrator decomposing queries into dedicated data, health, spatial, and RAG sub-agents.