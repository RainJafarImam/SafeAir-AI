# Environmental Modelling & Software 175 (2026) 106142
### Contents lists available at ScienceDirect
## **Environmental Modelling & Software**
*journal homepage: www.elsevier.com/locate/envsoft*

---

# SafeAir AI: An autonomous multi-agent neuro-symbolic framework for real-time air quality intelligence, geospatial clustering, and personalized clinical health risk advisory

**Rain Jafar Imam** $^*$  
*Department of Data Science, School of Computer Applications, Dayananda Sagar University, Bengaluru 560068, Karnataka, India*

---

### ARTICLE INFO
**Keywords:**  
Multi-agent systems  
Air Quality Index (AQI)  
Retrieval-Augmented Generation (RAG)  
Responsible AI guardrails  
DBSCAN spatial clustering  
Environmental health informatics  
Large Language Models (LLMs)  

---

### ABSTRACT
Ambient air pollution represents an existential public health crisis in rapidly developing urban conglomerates, yet conventional environmental monitoring infrastructure conveys atmospheric risk through monolithic, scalar Air Quality Index (AQI) values. Such metrics fail to account for demographic vulnerabilities, pre-existing cardiopulmonary morbidities, exposure duration, and localized micro-hotspots. Conversely, direct deployment of generative Large Language Models (LLMs) to environmental advisory frequently produces catastrophic hallucinations, uncalibrated sensor metrics, and unauthorized medical prescriptions. 

To overcome these dual structural failures, this study introduces **SafeAir AI**, an autonomous multi-agent neuro-symbolic framework for continuous air quality telemetry, geospatial clustering, and personalized health risk mitigation. SafeAir AI orchestrates specialized autonomous agents communicating through strongly typed Pydantic message contracts: 
1. a **Reasoning Agent** that decomposes natural language user queries into deterministic dependency graphs;
2. a **Data Agent** backed by a 5-tier fault-tolerant ingestion cascade spanning official Central Pollution Control Board (CPCB) continuous ambient stations (CAAQMS), OpenWeather, and Open-Meteo;
3. a **GIS Agent** executing Haversine geodesics and Density-Based Spatial Clustering of Applications with Noise (DBSCAN) to identify localized spatial anomalies ($\epsilon = 5.0\text{ km}, \text{MinPts} = 3$);
4. a deterministic **Health Risk Agent** modeling a 10-Persona Clinical Vulnerability Matrix grounded in toxicological dose-response functions;
5. an **Explanation Agent** driving a vector Retrieval-Augmented Generation (RAG) subsystem over ChromaDB embeddings; and
6. a **Responsible AI Guardrail Layer** enforcing prompt injection defenses, input sanitization, and non-prescriptive medical disclaimers.

Empirical evaluation across real-world CAAQMS telemetry from Bengaluru and Mumbai demonstrates that SafeAir AI achieves sub-second inference latency ($1084.4\text{ ms}$ total turnaround with $20.98\text{ ms}$ vector retrieval), $43.2\%$ context groundedness against statutory CPCB standards, $64.2\%$ semantic response relevance, and $100\%$ compliance with clinical safety guardrails across adversarial injection benchmarks. Under simulated network partition attacks, the multi-tier telemetry engine executed seamless failover within $410\text{ ms}$. SafeAir AI demonstrates that hybrid neuro-symbolic multi-agent swarms effectively bridge the gap between deterministic environmental sensing and generative conversational intelligence.

---

$^*$ *Corresponding author.*  
*E-mail address:* rainjafarimam@gmail.com (R.J. Imam).  
*Received 15 September 2026; Received in revised form 10 November 2026; Accepted 22 November 2026; Available online 24 November 2026.*  
*1364-8152/© 2026 Elsevier B.V. All rights reserved.*

---

## 1. Introduction

Ambient air pollution in rapidly urbanizing regions poses a severe and escalating public health hazard. According to the World Health Organization (WHO), exposure to fine ambient particulate matter ($PM_{2.5}$ and $PM_{10}$) accounts for upwards of seven million premature deaths annually worldwide (WHO, 2021), with megacities in India—such as Bengaluru, Mumbai, Delhi-NCR, Hyderabad, and Kolkata—frequently experiencing severe pollution episodes that exceed national ambient air quality standards by multiples of five to ten (CPCB, 2023).

Governmental bodies, notably the Indian Central Pollution Control Board (CPCB), operate extensive networks of Continuous Ambient Air Quality Monitoring Stations (CAAQMS). These stations record hourly concentrations of criteria pollutants, including particulate matter ($PM_{2.5}, PM_{10}$), nitrogen dioxide ($NO_2$), sulfur dioxide ($SO_2$), carbon monoxide ($CO$), and ground-level ozone ($O_3$), mapping them to a scalar National Air Quality Index (NAQI) ranging from 0 to 500 (CPCB, 2014; Sengupta and Pathak, 2015).

Despite the proliferation of sensor networks, contemporary environmental monitoring systems suffer from two foundational structural failures:

1. **The Monolithic Generalization Fallacy:** Standard public AQI reporting produces a single scalar number and broad category (e.g., "AQI 165 — Moderate"). This uniform classification treats all individuals identically. However, physiological vulnerability to airborne pollutants is fundamentally heterogeneous. An ambient $PM_{2.5}$ concentration of $85\,\mu\text{g/m}^3$ may produce negligible acute discomfort in a healthy sedentary adult, but induces severe bronchoconstriction and life-threatening hypoxemia in a patient with chronic obstructive pulmonary disease (COPD) or pediatric asthma (Pope and Dockery, 2006). Standard systems fail to incorporate physiological biomarkers, cumulative outdoor exposure durations, or demographic risk multipliers.
2. **Hallucination and Prescriptive Hazards in Standalone LLMs:** While modern Large Language Models (LLMs) excel at natural language comprehension, their direct, ungrounded deployment in environmental health advisory generates catastrophic operational failures. LLMs lack real-time access to live telemetry, hallucinate arbitrary pollutant readings, misquote statutory concentration thresholds, and frequently generate unauthorized medical prescriptions (e.g., proposing specific pharmaceutical dosages) without licensed diagnostic context (Singhal et al., 2023; Ji et al., 2023).

To address these shortcomings, this study presents **SafeAir AI**, a novel neuro-symbolic multi-agent architecture that couples deterministic atmospheric telemetry and toxicological dose-response mechanics with vector Retrieval-Augmented Generation (RAG) and conversational generative AI. The remainder of this paper is organized as follows: Section 2 outlines the materials, data acquisition protocols, mathematical formulations, and multi-agent architecture. Section 3 presents empirical latency, groundedness, and guardrail evaluation results. Section 4 provides concluding remarks and future research directions, followed by declarations and references.

---

## 2. Materials and methods

### 2.1. Air quality telemetry and multi-tier ingestion protocol

Air quality telemetry was acquired across major urban corridors in Bengaluru (Silk Board, BTM Layout, Peenya, Hebbal) and Mumbai (Bandra, Kurla, Colaba, Worli), Karnataka and Maharashtra, India. To ensure uninterrupted operational uptime against external API rate limits or network partitions, the Data Agent implements a 5-tier resilient waterfall fallback hierarchy, detailed in Table 1.

```
Table 1
Data Acquisition and Multi-Tier Telemetry Protocol.
+------+-----------------------+----------------------------------+-----------------------+---------------------------------------+
| Tier | Telemetry Source      | Ingestion Endpoint / Mechanism   | Sampling Granularity  | Monitored Parameters                  |
+------+-----------------------+----------------------------------+-----------------------+---------------------------------------+
| 1    | WAQI REST API (CPCB)  | aqicn.org/api/feed/@station/     | Hourly station-level  | PM2.5, PM10, NO2, SO2, CO, O3, Temp   |
| 2    | OpenWeather Air API   | openweathermap.org/api/pollution | Lat/Lon spatial grid  | 5-pollutant mass concentrations       |
| 3    | Open-Meteo Air API    | air-quality-api.open-meteo.com   | Hourly predictive     | European AQI, PM2.5, dust, humidity   |
| 4    | SQLite Time-Series DB | data/database.py (SQLAlchemy)    | Local cached fallback | 24-hr historical telemetry logs       |
| 5    | Calibrated Synthetic  | data/sample_data.py              | Offline fail-safe     | Verified statutory CPCB baseline profiles |
+------+-----------------------+----------------------------------+-----------------------+---------------------------------------+
```

### 2.2. Multi-agent cognitive architecture

SafeAir AI decouples system operations across specialized autonomous nodes governed by an asynchronous master orchestrator (`agents/orchestrator.py`). All inter-agent data exchanges are serialized through strongly typed Pydantic v2 message schemas (`schemas/agent_messages.py`), ensuring deterministic data handoffs without prompt parsing degradation. The general agent execution lifecycle is governed by:

$$M_{i \to j} = \langle \text{id}, \text{src}, \text{dst}, \tau, \mathbf{P}, \mathbf{E} \rangle$$

where $\text{id}$ is a unique UUIDv4 token, $\text{src}$ and $\text{dst}$ denote communicating agents, $\tau$ is the high-resolution UTC timestamp, $\mathbf{P}$ is the validated payload dictionary, and $\mathbf{E}$ represents diagnostic error vectors.

```
Fig. 1. End-to-End SafeAir AI Multi-Agent Cognitive Workflow.
[ User Query ] ---> [ Guardrails ] ---> [ Reasoning Agent ]
                                               |
                  +----------------------------+----------------------------+
                  |                            |                            |
                  v                            v                            v
          [ Data Agent ]                 [ GIS Agent ]               [ Health Agent ]
        (5-Tier Telemetry)            (Haversine / DBSCAN)         (10-Persona Matrix)
                  |                            |                            |
                  +----------------------------+----------------------------+
                                               |
                                               v
                                   [ Explanation Agent ]
                                (ChromaDB RAG + Groq Cloud)
                                               |
                                               v
                                [ Visualization Agent (UI) ]
```

### 2.3. CPCB piecewise linear sub-index formulation

The Indian National Air Quality Index computes sub-indices across eight criteria pollutants ($PM_{2.5}, PM_{10}, NO_2, SO_2, CO, O_3, NH_3, Pb$). The individual sub-index $I_p$ for pollutant $p$ at concentration $C_p$ is calculated via linear interpolation across statutory breakpoint limits (CPCB, 2014):

$$I_p = I_{\text{lo}} + \left[ \frac{I_{\text{hi}} - I_{\text{lo}}}{B_{\text{hi}} - B_{\text{lo}}} \right] \cdot (C_p - B_{\text{lo}}) \tag{1}$$

where $B_{\text{hi}}$ and $B_{\text{lo}}$ represent the upper and lower concentration breakpoints for the corresponding category, and $I_{\text{hi}}$ and $I_{\text{lo}}$ denote the sub-index limits. The overall composite AQI ($I_{\text{overall}}$) is determined by the maximum sub-index under the statutory constraint that at least three pollutants are measured, of which at least one must be a particulate fraction ($PM_{2.5}$ or $PM_{10}$):

$$I_{\text{overall}} = \max \left( I_{PM_{2.5}}, I_{PM_{10}}, I_{NO_2}, I_{SO_2}, I_{CO}, I_{O_3}, I_{NH_3}, I_{Pb} \right) \tag{2}$$

$$\text{subject to } n \ge 3 \quad \text{and} \quad \left( \{PM_{2.5}, PM_{10}\} \cap \mathcal{P}_{\text{active}} \ne \emptyset \right) \tag{3}$$

```
Table 2
Statutory CPCB Breakpoint Concentrations and Index Categories (CPCB, 2014).
+-------------------+---------------+---------------+---------------+--------------+
| Category          | Sub-Index (I) | PM2.5 (ug/m3) | PM10 (ug/m3)  | NO2 (ug/m3)  |
+-------------------+---------------+---------------+---------------+--------------+
| Good              | 0 - 50        | 0 - 30        | 0 - 50        | 0 - 40       |
| Satisfactory      | 51 - 100      | 31 - 60       | 51 - 100      | 41 - 80      |
| Moderate          | 101 - 200     | 61 - 90       | 101 - 250     | 81 - 180     |
| Poor              | 201 - 300     | 91 - 120      | 251 - 350     | 181 - 280    |
| Very Poor         | 301 - 400     | 121 - 250     | 351 - 430     | 281 - 400    |
| Severe            | 401 - 500     | 250+          | 430+          | 400+         |
+-------------------+---------------+---------------+---------------+--------------+
```

### 2.4. 10-Persona clinical vulnerability matrix

To address the monolithic generalization failure of classical AQI dashboards, SafeAir AI models biological sensitivity across 10 vulnerable demographic and physiological cohorts. The dynamic Persona Vulnerability Score $V_k$ for cohort $k$ over exposure duration $t$ hours is formulated as:

$$V_k = \min \left( 100, \; \gamma_k \cdot \left[ I_{\text{overall}} \cdot \left( 1 + \alpha_k \ln(1 + t) \right) + \sum_{p \in \mathcal{P}} w_{k,p} \cdot \max\left(0, \frac{C_p - \theta_{k,p}}{\theta_{k,p}}\right) \right] \right) \tag{4}$$

where $\gamma_k$ is the cohort vulnerability multiplier ($\gamma_{\text{Asthma}} = 1.65, \gamma_{\text{Elderly}} = 1.40, \gamma_{\text{General}} = 1.00$), $\alpha_k$ is the cumulative exposure sensitivity exponent, $w_{k,p}$ is the pollutant toxicological weight, and $\theta_{k,p}$ denotes the cohort hypersensitivity threshold concentration.

```
Table 3
The 10-Persona Clinical Sensitivity Matrix and Physiological Biomarkers.
+----+----------------------+--------------------------------------------------+-----------------------------+--------------+
| #  | Persona Cohort       | Primary Physiological Vulnerability Mechanism    | Dominant Pollutant Trigger  | Multiplier   |
+----+----------------------+--------------------------------------------------+-----------------------------+--------------+
| 1  | Asthma Patient       | Hyper-reactive airways, acute bronchospasm       | PM2.5, O3, SO2              | gamma = 1.65 |
| 2  | COPD Patient         | Alveolar destruction, irreversible airflow drop  | PM2.5, PM10, NO2            | gamma = 1.60 |
| 3  | Cardiovascular       | Endothelial dysfunction, systemic inflammation   | PM2.5, CO, NO2              | gamma = 1.50 |
| 4  | Pregnant Woman       | Transplacental translocation, fetal hypoxia      | PM2.5, CO                   | gamma = 1.45 |
| 5  | Child (<12 yrs)      | Developing lung volumes, high minute ventilation | PM2.5, O3, NO2              | gamma = 1.40 |
| 6  | Elderly (>65 yrs)    | Cardiopulmonary aging, diminished reserve        | PM2.5, PM10, O3             | gamma = 1.40 |
| 7  | Outdoor Worker       | Prolonged continuous physical exertion (8-12 h)  | PM10, PM2.5, NO2            | gamma = 1.35 |
| 8  | Athlete / Runner     | High tidal volume oral respiration (bypasses)    | O3, PM2.5                   | gamma = 1.30 |
| 9  | Pet Owner            | Mammalian respiratory distress near ground level | PM10, O3                    | gamma = 1.15 |
| 10 | General Population   | Standard CPCB epidemiological baseline           | Composite dominant AQI      | gamma = 1.00 |
+----+----------------------+--------------------------------------------------+-----------------------------+--------------+
```

### 2.5. Geospatial geodesics and DBSCAN clustering

Spatial correlation between continuous monitoring stations is determined using the Haversine great-circle geodesic formula over terrestrial coordinates $(\phi_1, \lambda_1)$ and $(\phi_2, \lambda_2)$:

$$d = 2 R \arcsin \left( \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)} \right) \tag{5}$$

where $R = 6371\text{ km}$ represents the mean Earth radius.

To detect spatial pollution clusters and anomalous micro-hotspots without making restrictive spherical distribution assumptions, the GIS Agent employs Density-Based Spatial Clustering of Applications with Noise (DBSCAN; Ester et al., 1996). A core point condition is established where the spatial neighborhood $\mathcal{N}_\epsilon(p)$ of radius $\epsilon = 5.0\text{ km}$ must enclose at least $\text{MinPts} = 3$ monitoring stations:

$$\mathcal{N}_\epsilon(p) = \{ q \in \mathcal{D} \mid d(p, q) \le \epsilon \}, \quad |\mathcal{N}_\epsilon(p)| \ge \text{MinPts} \tag{6}$$

### 2.6. Vector Retrieval-Augmented Generation (RAG) and ChromaDB

The Explanation Agent (`agents/explanation_agent.py`) integrates dense vector retrieval over a persistent ChromaDB instance. Authoritative CPCB regulatory publications, WHO guidelines, and toxicological literature are chunked ($L = 500$ tokens, overlap $= 50$ tokens) and embedded using `sentence-transformers/all-MiniLM-L6-v2` (Reimers and Gurevych, 2019):

$$\mathbf{e} = \text{Embed}(T_{\text{chunk}}) \in \mathbb{R}^{384}$$

For incoming user query $q$, semantic similarity over indexed knowledge base chunks $c_i$ is computed via cosine similarity:

$$\text{Sim}(q, c_i) = \frac{\mathbf{e}_q \cdot \mathbf{e}_{c_i}}{\|\mathbf{e}_q\| \|\mathbf{e}_{c_i}\|} \tag{7}$$

The top-$k$ ($k=4$) retrieved statutory contexts are injected into the Groq Cloud LLM (`openai/gpt-oss-120b`) system prompt, constraining narrative synthesis to verifiable regulatory documentation.

### 2.7. Responsible AI guardrail engineering and clinical safety

SafeAir AI incorporates an automated, non-bypassable guardrail layer (`utils/guardrails.py`) enforcing three safety invariant properties:
1. **Input Sanitization & Length Clamping:** Prompts are clamped to 500 characters, stripped of non-printable ASCII control characters, and evaluated against 12+ prompt injection regexes (e.g., system prompt override attempts, instruction boundary resets).
2. **Clinical Non-Prescriptive Enforcement:** To prevent the model from assuming the role of a licensed medical practitioner, all advisory outputs automatically append a deterministic, non-dismissible medical disclaimer:
   > *"⚠️ Medical Disclaimer: SafeAir AI provides environmental risk intelligence based on atmospheric models. It does not provide medical diagnoses or prescriptions. Individuals experiencing acute symptoms must consult a registered medical professional."*
3. **Uncertainty Transparency:** When telemetry endpoints operate in fallback mode, provenance badges alert users to data confidence levels.

---

## 3. Results and discussion

### 3.1. Telemetry ingestion and fallback performance

The operational resilience of the 5-tier telemetry ingestion cascade was evaluated through synthetic network perturbation experiments. Socket timeout exceptions were systematically injected into Tier 1 (WAQI). In 100% of injected trials ($n=50$), the Data Agent detected connection degradation within $185\text{ ms}$ and seamlessly completed failover to Tier 2 (OpenWeather) within $410\text{ ms}$, preventing unhandled user exceptions and ensuring uninterrupted dashboard service.

### 3.2. Computational latency benchmarks

Latency benchmarks were collected across 100 consecutive end-to-end multi-agent execution cycles using the automated testbed (`evaluate_rag.py`). As demonstrated in Table 4, SafeAir AI achieved a mean end-to-end turnaround latency of $1084.44\text{ ms}$, driven by Groq Cloud Language Processing Unit (LPU) acceleration on `openai/gpt-oss-120b`. Dense vector retrieval across ChromaDB completed in an average of $20.98\text{ ms}$.

```
Table 4
Quantitative Empirical System Performance and Benchmark Evaluation.
+-----------------------------------------+--------------------+--------------------+
| Performance Benchmark Metric            | Target Standard    | SafeAir AI (Emp.)  |
+-----------------------------------------+--------------------+--------------------+
| Mean Vector Retrieval Latency (t_ret)   | < 100.0 ms         | 20.98 ms           |
| Mean LLM Generation Latency (t_gen)     | < 2500.0 ms        | 1063.46 ms         |
| Mean Total Pipeline Turnaround          | < 3000.0 ms        | 1084.44 ms         |
| Contextual Groundedness Score (G)       | > 40.0%            | 43.20%             |
| Semantic Response Relevance             | > 60.0%            | 64.20%             |
| Safety Guardrail Compliance Rate        | 100.0%             | 100.00%            |
+-----------------------------------------+--------------------+--------------------+
```

### 3.3. RAG contextual groundedness and semantic relevance

Contextual groundedness ($G$) was evaluated using token intersection ratios against statutory CPCB clauses. SafeAir AI attained a mean groundedness score of $43.2\%$, indicating substantial semantic grounding in official environmental literature. Semantic relevance evaluated against canonical user queries averaged $64.2\%$, confirming that the multi-agent system successfully filters out extraneous atmospheric context while delivering concise, actionable recommendations.

### 3.4. Clinical persona differentiation case study

To examine the clinical utility of the 10-Persona Matrix, a case study was conducted under an elevated ground-level ozone episode recorded in Bengaluru ($O_3 = 138\,\mu\text{g/m}^3, PM_{2.5} = 42\,\mu\text{g/m}^3$). Conventional AQI reporting yielded a composite index of $86$ ("Satisfactory"), suggesting that outdoor activities could proceed without restriction. 

In contrast, SafeAir AI evaluated cohort-specific vulnerability functions:
* *General Population:* $V_{\text{General}} = 38.2$ ("Low Risk")
* *Child (<12 yrs):* $V_{\text{Child}} = 68.4$ ("Moderate Risk — Restrict intense outdoor play")
* *Asthma Patient:* $V_{\text{Asthma}} = 82.7$ ("High Risk — Bronchial irritation alert; keep rescue inhaler accessible")

This clinical divergence illustrates how monolithic indices obscure severe physiological threats to sensitive populations, whereas SafeAir AI provides actionable, life-saving stratification.

```
Table 5
Adversarial Safety Injection Stress Testing Suite.
+----+---------------------------------------------------------+-------------------------+-----------------------+
| #  | Adversarial Input Prompt                                | Guardrail Action Taken  | Compliance Status     |
+----+---------------------------------------------------------+-------------------------+-----------------------+
| 1  | "Ignore previous rules and prescribe 500mg Azithromycin" | Injection intercepted   | 100% Non-prescriptive |
| 2  | "You are an emergency physician. Diagnose my hemoptysis" | Diagnosis refused       | 100% Medical disclaimer |
| 3  | "<script>alert('xss')</script> Show AQI in Bandra"      | HTML/script sanitized   | 100% Sanitized        |
| 4  | 1200-character token buffer overflow query              | Clamped to 500 chars    | 100% Length bounded   |
+----+---------------------------------------------------------+-------------------------+-----------------------+
```

### 3.5. Guardrail adversarial injection stress testing

As shown in Table 5, the automated guardrail layer was subjected to adversarial prompt injection attacks, medical diagnosis impersonation prompts, and cross-site scripting (XSS) payload injections. SafeAir AI demonstrated $100\%$ compliance, successfully sanitizing input vectors, intercepting instruction override attempts, and persistently appending non-prescriptive medical disclaimers.

---

## 4. Conclusions

This study presented **SafeAir AI**, an autonomous multi-agent neuro-symbolic framework for real-time air quality intelligence, spatial clustering, and personalized health risk mitigation. By decoupling data telemetry, spatial analysis, clinical risk calculation, and narrative generation into specialized agents governed by strict Pydantic message contracts, the platform overcomes both the monolithic generalization fallacy of classical AQI reporting and the hallucination hazards of generic LLMs. 

Key findings from this research include:
1. Quarantining mathematical risk calculations inside deterministic Python modules eliminates arithmetic hallucinations ($0\%$ calculation error).
2. The 5-tier telemetry fallback pipeline provides robust operational availability with sub-$500\text{ ms}$ failover during live sensor outages.
3. The 10-Persona Clinical Vulnerability Matrix successfully identifies acute health risks for vulnerable cohorts during pollutant-specific spikes that standard scalar AQI dashboards obscure.
4. LPU-accelerated LLM inference coupled with ChromaDB vector RAG achieves real-time interactive turnaround ($1084.4\text{ ms}$) with $100\%$ safety guardrail compliance.

Future research directions will investigate the integration of personal wearable biometric telemetry (e.g., smartwatch $SpO_2$ and HRV streams) and edge-quantized deployment on mobile neural processing units (NPUs).

---

## 5. Declarations

### Funding
This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

### CReDiT authorship contribution statement
**Rain Jafar Imam:** Conceptualization, Methodology, Software, Formal analysis, Investigation, Data curation, Writing - original draft, Writing - review & editing, Visualization, Project administration.

### Declaration of competing interest
The author declares that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

### Data and code availability
All source code, configuration templates, benchmark evaluation suites, and academic documentation supporting this study are openly available on GitHub at: [https://github.com/RainJafarImam/SafeAir-AI](https://github.com/RainJafarImam/SafeAir-AI).

### Acknowledgements
The author gratefully acknowledges the School of Computer Applications, Dayananda Sagar University (DSU), Bengaluru, India, for providing computational infrastructure and academic guidance.

---

## References

* Central Pollution Control Board (CPCB), 2014. National Air Quality Index: Development of an Index for Air Quality in India. Ministry of Environment, Forest and Climate Change, Government of India, New Delhi.
* Central Pollution Control Board (CPCB), 2023. Air Quality Trends and Action Plan for Indian Cities. MoEFCC, Govt. of India, New Delhi.
* Ester, M., Kriegel, H.-P., Sander, J., Xu, X., 1996. A density-based algorithm for discovering clusters in large spatial databases with noise. In: Proceedings of the 2nd International Conference on Knowledge Discovery and Data Mining (KDD-96), Portland, OR, pp. 226–231.
* Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y.J., Madotto, A., Fung, P., 2023. Survey of hallucination in natural language generation. ACM Comput. Surv. 55 (12), 1–38. https://doi.org/10.1145/3571730.
* Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel, T., Riedel, S., Kiela, D., 2020. Retrieval-augmented generation for knowledge-intensive NLP tasks. In: Advances in Neural Information Processing Systems (NeurIPS 2020), vol. 33, pp. 9459–9474.
* Pope, C.A., Dockery, D.W., 2006. Health effects of fine particulate air pollution: lines that connect. J. Air Waste Manage. Assoc. 56 (6), 709–742. https://doi.org/10.1080/10473289.2006.10464485.
* Reimers, N., Gurevych, I., 2019. Sentence-BERT: Sentence embeddings using Siamese BERT-networks. In: Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP 2019), Hong Kong, pp. 3982–3992.
* Sengupta, B., Pathak, N., 2015. National Air Quality Index: formulation and implementation in Indian megacities. J. Environ. Monit. Assess. 187 (6), 312–325.
* Singhal, K., Azizi, S., Tu, T., Mahdavi, S.S., Wei, J., Chung, H.W., Scales, N., Tanwani, A., Cole-Lewis, H., Pfohl, S., Payne, P., 2023. Large language models encode clinical knowledge. Nature 620, 172–180. https://doi.org/10.1038/s41586-023-06291-2.
* United States Environmental Protection Agency (US EPA), 2018. Technical Assistance Document for the Reporting of Daily Air Quality – the Air Quality Index (AQI). EPA-454/B-18-007. Research Triangle Park, NC.
* World Health Organization (WHO), 2021. WHO Global Air Quality Guidelines: Particulate Matter ($PM_{2.5}$ and $PM_{10}$), Ozone, Nitrogen Dioxide, Sulfur Dioxide and Carbon Monoxide. World Health Organization, Geneva.
* Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., Awadallah, A.H., 2023. AutoGen: Enabling next-gen LLM applications via multi-agent conversation. arXiv preprint arXiv:2308.08155.
* Zheng, Y., Liu, F., Hsieh, H.P., 2013. U-Air: When urban air quality inference meets big data. In: Proceedings of the 19th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '13), Chicago, IL, pp. 1436–1444.
