# 👁️ Eye of Ra
### Ghana's AI-Powered Procurement Integrity System

Built for the Ghana AI Summit & Awards 2026 — Financial Inclusion / Public Services domain.

---

## What is Eye of Ra?

Eye of Ra is an AI system that monitors Ghana's public procurement 
transactions in real time, detects fraud fingerprints before contracts 
are awarded, and gives citizens, oversight bodies, and the PPA a live 
integrity dashboard.

Built on Ghana's Public Procurement Act (Act 663 & Act 914) and trained 
on publicly available Ghanaian procurement data.

---

## The Problem

Ghana lost **GH₵18.4 billion** to financial irregularities in 2024 alone 
— a 109% increase from 2023. Less than 0.5% was ever recovered.

The system is reactive. Auditors find fraud after the money is gone.

Eye of Ra makes it **predictive**.

---

## Solution Architecture

- **5 AI Detection Engines** — bid manipulation, supplier integrity, 
  price benchmarking, method abuse, plan deviation
- **XGBoost + Isolation Forest ensemble** trained on Auditor-General data
- **SHAP explainability** — plain English explanation for every flag
- **3-tier action system** — Monitor / Review / Escalate
- **Public dashboard** — any Ghanaian can see any procurement entity's 
  integrity score

---

## Legal Foundation

Grounded in Ghana's Public Procurement Act 663 (2003) as amended by 
Act 914 (2016). Every detection rule cites the specific legal provision 
it enforces.

---

## Data Sources

- PPA Monthly Procurement Bulletins (2020–2024)
- Auditor-General Annual Reports (2020–2024)
- Ghana Open Data Initiative
- GHANEPS procurement records

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python + pandas | Data cleaning & processing |
| XGBoost + sklearn | Fraud detection model |
| Isolation Forest | Anomaly detection |
| SHAP | Model explainability |
| Streamlit | Public dashboard |
| Google Cloud Run | Dashboard hosting |

---

## Project Status

🟡 Week 1 — Data collection & project setup

---

## Team

Built with purpose for Ghana 🇬🇭

*"The greatest threat to corruption is visibility."*
