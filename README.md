# ✈️ Global Air Freight Analysis: Trends, Leaders and Growth Patterns (2005–2019)

## 🔗 Quick Links
| Resource | Link |
|----------|------|
| 🚀 Live Dashboard | [your-streamlit-link-here](https://air-cargo-analysis-adnamj8erkghrv4bhkksof.streamlit.app/) |
| 📓 Kaggle Notebook | [your-kaggle-link-here](https://www.kaggle.com/code/umercheena/air-cargo-project/edit) |
| 📊 Dataset |[ World Bank WDI](https://data.worldbank.org/indicator/IS.AIR.GOOD.MT.K1) |

---

## 📌 Overview
This project analyzes **15 years** of global air transport data across **230 countries**
from the World Bank World Development Indicators. It covers freight volume, passenger
traffic, carrier departures, and logistics infrastructure quality scores.

---

## 🎯 Objectives
- Identify top countries by air freight volume
- Analyze global air freight trends over 15 years
- Explore relationship between infrastructure quality and freight performance
- Compare passenger traffic vs freight across countries
- Forecast freight demand using Machine Learning
- Cluster countries by air transport profile

---

## 📁 Project Structure
air-cargo-analysis/
│
├── data.csv                        # Raw dataset (World Bank WDI)
├── dashboard.py                    # Streamlit dashboard
├── air-cargo-project.ipynb         # Kaggle notebook
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation

---

## 📊 Dataset
| Property | Detail |
|----------|--------|
| Source | World Bank World Development Indicators |
| Countries | 230 |
| Years | 2005 – 2019 |
| Metrics | 4 |
| Format | CSV |

### Metrics
| Column | Description |
|--------|-------------|
| `departures` | Registered carrier departures worldwide |
| `freight_mton_km` | Air freight in million ton-km |
| `passengers` | Air passengers carried |
| `lpi_infra_score` | Logistics infrastructure quality (1=low, 5=high) |
| `freight_yoy_growth` | Year-over-year freight growth rate |
| `freight_efficiency` | Freight per departure ratio |
| `freight_lag1` | Freight volume previous year |
| `freight_lag2` | Freight volume 2 years ago |

---

## 🚀 Project Phases

✅ Phase 1 — Data Cleaning

✅ Phase 2 — Exploratory Data Analysis

✅ Phase 3 — Feature Engineering

✅ Phase 4 — Modelling

✅ Phase 5 — Dashboard
---

## 🔑 Key Findings
- **USA, China and Germany** dominate global air freight
- Global air freight showed **consistent growth** from 2005 to 2019
- **Strong positive correlation** exists between departures and freight volume
- Countries with **higher LPI scores** tend to handle more freight
- **Random Forest** outperforms Linear Regression for freight prediction
- K-Means clustering reveals **4 distinct country profiles** by air transport activity

---

## 🛠️ Tools & Libraries
| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Scikit-learn | Machine learning & clustering |
| Streamlit | Interactive dashboard |

---

## ▶️ How to Run

### Run Dashboard Locally
1. Clone the repository
```bash
git clone https://github.com/muhammadumermehmood/air-cargo-analysis.git
cd air-cargo-analysis
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the dashboard
```bash
streamlit run dashboard.py
```

---

## 👤 Author
**Muhammad Umer Mehmood**
- 💼 LinkedIn: [Muhammad Umer Mehmood](https://linkedin.com/in/muhammad-umer-mehmood)
- 🎯 Role: Aspiring Data Analyst

---
