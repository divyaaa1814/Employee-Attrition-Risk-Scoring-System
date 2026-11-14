# 🛡️ Machine Learning–Based Employee Attrition Prediction and Risk Scoring System

Predictive HR analytics system and interactive Streamlit dashboard built for Palo Alto Networks to forecast employee attrition risk, explain key turnover drivers, and simulate retention strategies using Machine Learning.

**Enterprise Workforce Intelligence & Predictive Retention Platform for Palo Alto Networks**

---
Live Dashboard :

Research Report(Google Docs) : https://drive.google.com/drive/folders/1kmgISAtMNk-vJNG4Bbicr-aFv1TIbBmY?usp=sharing
## 📌 1. Project Overview & Problem Statement

In high-velocity cybersecurity and enterprise technology organizations such as **Palo Alto Networks**, unplanned employee attrition erodes institutional knowledge, delays product roadmaps, and incurs substantial replacement costs. Historically, HR leaders lacked the predictive visibility to answer: *"Which specific employees are most likely to leave in the near future, and what concrete factors are driving their exit decisions?"*

### Core Organizational Challenges Addressed
* **Sudden, Unanticipated Resignations:** Loss of high-performing engineers, threat researchers, and client-facing specialists without early warning.
* **Reactive Counter-Offers:** Retention offers issued after formal resignation notices are submitted frequently fail because underlying burnout or career stagnation remains unresolved.
* **Lack of Quantitative Risk Scoring:** Absence of an objective probability framework to prioritize retention outreach across departments and roles.
* **Opaque Exit Drivers:** Limited visibility into how workload saturation, compensation compression, and promotional delays interact to trigger attrition.

### Project Objectives
1. **Early Identification:** Assign calibrated attrition probability scores (`0.00–1.00`) to every active employee prior to resignation.
2. **Explainable Decision Intelligence:** Surface plain-English individual reason codes and global feature importances to establish HR stakeholder trust.
3. **Proactive Workforce Planning:** Enable HR leaders and department heads to simulate retention interventions (e.g., overtime caps, compensation equity adjustments, and promotions) via a live Streamlit dashboard.

---

## 📊 2. Dataset Information & Exploratory Data Analysis (EDA)

The dataset (`data/Palo Alto Networks.csv`) comprises **1,470 employee records** across **31 organizational, financial, demographic, and behavioral attributes** with zero missing values and a baseline organizational attrition rate of **16.12%** (237 exits vs. 1,233 retained employees).

### Dataset Schema (31 Fields)

| Analytical Domain | Dataset Fields | Description & Scale |
| :--- | :--- | :--- |
| **Demographics & Background (6)** | `Age`, `Gender`, `MaritalStatus`, `Education`, `EducationField`, `DistanceFromHome` | Employee demographics, commute distance, and ordinal education (`1: Below College` to `5: Doctor`). |
| **Compensation & Equity (6)** | `MonthlyIncome`, `MonthlyRate`, `DailyRate`, `HourlyRate`, `PercentSalaryHike`, `StockOptionLevel` | Continuous salary rates, appraisal hike percentages, and equity tiers (`0–3`). |
| **Tenure & Progression (9)** | `Department`, `JobRole`, `JobLevel`, `NumCompaniesWorked`, `TotalWorkingYears`, `YearsAtCompany`, `YearsInCurrentRole`, `YearsSinceLastPromotion`, `YearsWithCurrManager` | Departmental hierarchy (`R&D`, `Sales`, `HR`), seniority (`1–5`), and longitudinal tenure counters. |
| **Workload, Satisfaction & Target (10)** | `OverTime`, `BusinessTravel`, `TrainingTimesLastYear`, `WorkLifeBalance`, `JobInvolvement`, `JobSatisfaction`, `EnvironmentSatisfaction`, `RelationshipSatisfaction`, `PerformanceRating`, `Attrition` | Psychometric Likert scales (`1 = Low/Poor` to `4 = High/Excellent`), travel cadence, overtime (`Yes/No`), and binary target (`0/1`). |

### Key EDA Insights
* **Overtime Saturation Catalyst:** Employees working mandatory overtime experience an attrition rate of **30.5%**—nearly triple the **10.4%** turnover rate among non-overtime peers ($r = +0.25$).
* **Early-Tenure Vulnerability Window:** Turnover spikes significantly between **Years 1 and 4** of company tenure and among entry-level (`JobLevel = 1`) specialists.
* **Role-Specific Disparities:** Sales Representatives (`39.8%` turnover) and Laboratory Technicians (`23.9%` turnover) exhibit substantially higher departure rates than Research Directors (`2.5%`) and Managers (`4.9%`).

---

## 🛠️ 3. Technology Stack

* **Programming Language:** Python 3.10+
* **Data Manipulation & Feature Engineering:** `pandas`, `numpy`
* **Machine Learning & Class Balancing:** `scikit-learn`, `imbalanced-learn` (SMOTE), `xgboost`, `joblib`
* **Explainability & Visualization:** `plotly`, `matplotlib`, `seaborn`, `shap`
* **Interactive Web Application:** `streamlit`
* **Automated Documentation & Reporting:** `python-docx`

---

## ⚙️ 4. Data Science Methodology & Feature Engineering

### Preprocessing Pipeline
Encapsulated inside a unified `Scikit-Learn` `ColumnTransformer` pipeline to prevent data leakage:
1. **Categorical Encoding:** One-Hot Encoding applied to nominal features (`Department`, `JobRole`, `BusinessTravel`, `MaritalStatus`, `EducationField`, `Gender`); binary mapping applied to `OverTime`.
2. **Numerical Scaling:** `StandardScaler` ($z$-score normalization) applied across continuous compensation and tenure features.
3. **Stratified Train–Test Split:** 80/20 stratified partitioning (`1,176` training / `294` test records) preserving the `16.12%` minority class ratio.
4. **Class Imbalance Mitigation:** SMOTE oversampling and balanced class weighting applied strictly within training folds.

### Domain-Driven Feature Engineering
Four custom composite indicators were engineered to capture economic and behavioral context:

| Engineered Feature | Mathematical Formulation | Operational Signal Captured |
| :--- | :--- | :--- |
| **`IncomeToExperienceRatio`** | $\frac{\text{MonthlyIncome}}{\text{TotalWorkingYears} + 1}$ | Normalizes monthly compensation against total career seniority to detect pay compression. |
| **`PromotionDelayIndicator`** | $\frac{\text{YearsSinceLastPromotion}}{\text{YearsAtCompany} + 1}$ | Measures internal career stagnation relative to company tenure. |
| **`EngagementScore`** | $\frac{\text{JobInvolvement} + \text{JobSat} + \text{EnvSat} + \text{RelSat}}{4.0}$ | Aggregates four psychometric satisfaction ratings into a unified workplace sentiment pulse. |
| **`WorkloadStressFlag`** | $1 \text{ if } (\text{OverTime} = \text{Yes} \land \text{WorkLifeBalance} \le 2) \text{ else } 0$ | Binary interaction indicator isolating acute burnout risk. |

---

## 📈 5. Model Development & Evaluation

Three supervised classification models were benchmarked using 5-fold stratified cross-validation:

| Model Architecture | Accuracy | Precision | Recall | F1-Score | ROC–AUC | Role in System |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression** | 78.2% | 0.42 | **0.74** | 0.54 | 0.812 | Linear interpretability baseline |
| **Random Forest Classifier** | 86.4% | 0.68 | 0.62 | 0.65 | 0.835 | Bagged non-linear ensemble |
| **Gradient Boosting (Selected)** | **87.1%** | **0.71** | 0.64 | **0.67** | **0.841** | **Production Risk Scoring Engine** |

---

## 🎯 6. Risk Scoring Framework & Model Explainability

### Tripartite Risk Governance Tiers
Each employee is assigned a continuous probability $P(\text{Attrition} = 1 \mid X) \in [0, 1]$ mapped into three action tiers:
* 🟢 **Low Risk (`< 30%`):** Standard career check-ins, annual merit reviews, and ongoing training.
* 🟡 **Medium Risk (`30% – 60%`):** Proactive manager check-in to review workload, travel frequency, and growth goals.
* 🔴 **High Risk (`> 60%`):** Priority HR Business Partner intervention (compensation equity audit, overtime cap, or promotion pathing).

### Explainability Architecture
* **Global Feature Importance:** Ranks top systemic turnover catalysts (`OverTime`, `MonthlyIncome`, `IncomeToExperienceRatio`, `Age`, `TotalWorkingYears`, `WorkloadStressFlag`).
* **Individual-Level Reason Codes:** Generates dynamic, human-readable alerts for every employee profile (e.g., *"Critical Stress Flag: Overtime + Poor Work-Life Balance"*, *"Low Income-to-Experience Ratio"*).

---

## 🖥️ 7. Live Streamlit Dashboard Modules & User Capabilities

### Dashboard Modules (`app.py`)
1. **Executive Overview:** Company-wide KPI cards, Donut Risk Distribution, Probability Density histogram with dynamic threshold cutoff, and exportable High-Risk Cohort roster (CSV).
2. **Department & Role Analysis:** Aggregated cohort risk table with color-gradient heatmaps, departmental mean risk comparison, and OverTime vs. Role breakdown.
3. **Employee Risk Profile:** Individual diagnostic dossier with Risk Banner, dynamic Reason Codes, 5-axis Satisfaction Radar chart, and key contributing factor breakdown.
4. **Feature Explainability Panel:** Top-15 Feature Importance chart and 3-Model Validation Benchmarking matrix.
5. **What-If Intervention Simulator:** Real-time policy sandbox allowing managers to adjust `MonthlyIncome`, `PercentSalaryHike`, `StockOptionLevel`, `OverTime`, `WorkLifeBalance`, `BusinessTravel`, and `YearsSinceLastPromotion`—calculating exact risk reduction (`Net Delta %`) and replacement capital saved.
6. **Stakeholder Reports & Brief:** Built-in Executive Summary and Research Report reference module.

### Interactive User Capabilities (Global Control Sidebar)
* **Department & Job Role Filters:** Dynamically slice all metrics and charts by organizational division and specific role.
* **Risk Tier Multi-Select & OverTime Toggle:** Isolate High/Medium/Low risk cohorts or compare `OverTime = Yes` vs. `No` in one click.
* **Risk Threshold Slider (`30%–80%`):** Customize high-risk alert cutoffs in real time.
* **Live Cohort & Annual Payroll-at-Risk Readout:** Displays filtered headcount and total annual compensation exposure (`$`) alongside a 1-click **Reset All Filters** button.
* **Employee ID Selector:** Inspect any of the 1,470 employee profiles individually.

---


# Author 

Divyaa Parikh\
Student of B.Sc. Data Science\
Department of Technology, Savitribai Phule University 

---


# Acknowledgement

Special thanks to Unified Mentor and the Toronto Government Parks, Forestry & Recreation initiative for providing the project framework, problem scope, and real-world workforce upskilling context.


---


## 📂 8. Project Structure & Deliverables

```text
Employee_Attrition_Prediction_System/
├── artifacts/
│   ├── best_attrition_pipeline.pkl                    # Serialized Gradient Boosting pipeline
│   ├── categorical_cols.pkl                           # Encoded categorical feature schema
│   └── numerical_cols.pkl                             # Numerical feature schema
├── data/
│   └── Palo Alto Networks.csv                         # 1,470-row, 31-column HR dataset
├── reports/
│   ├── Palo_Alto_Networks_Research_Paper_Complete.docx  # 5–6 page technical research paper
│   ├── Palo_Alto_Networks_Executive_Summary.docx        # Government & institutional stakeholder brief
│   └── Palo_Alto_Networks_Employee_Retention_Guide.docx # Plain-English employee retention guide
├── app.py                                             # 6-module Streamlit web application
├── train_model.py                                     # End-to-end preprocessing, training & evaluation script
├── inspect_data.py                                    # Dataset schema & EDA verification utility
├── test_app.py                                        # Automated smoke test for pipeline inference
├── requirements.txt                                   # Python dependencies
├── .gitignore                                         # Git exclusion rules
└── README.md                                          # Project documentation
