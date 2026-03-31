# ✈️ Global Air Freight Analysis: Trends, Leaders and Growth Patterns (2005–2019)

## Overview
This project analyzes global air transport data from the World Bank's World Development 
Indicators (WDI) database. It covers 230 countries over 15 years (2005–2019) and explores 
freight volume, passenger traffic, carrier departures, and logistics infrastructure quality.

## Background
Air cargo is the backbone of global trade — pharmaceuticals, electronics, perishables, 
and high-value goods all move by air. This project uncovers which countries dominate 
air freight, how the industry grew over 15 years, and whether better infrastructure 
leads to better freight performance.

## Objectives
- Identify the top countries by air freight volume
- Analyze global air freight trends over 15 years
- Explore the relationship between infrastructure quality and freight performance
- Compare passenger traffic vs freight across countries

## Dataset
| Property      | Detail                              |
|---------------|-------------------------------------|
| Source        | World Bank World Development Indicators |
| Countries     | 230                                 |
| Years         | 2005 – 2019                         |
| Metrics       | 4 (freight, departures, passengers, LPI) |
| Format        | CSV                                 |

### Metrics
| Column | Description |
|--------|-------------|
| `departures` | Registered carrier departures worldwide |
| `freight_mton_km` | Air freight in million ton-km |
| `passengers` | Air passengers carried |
| `lpi_infra_score` | Logistics infrastructure quality (1=low, 5=high) |

## Project Structure
```
air-cargo-analysis/
│
├── data/
│   ├── data.csv                  # Raw dataset
│   └── air_cargo_clean.csv       # Cleaned dataset
│
├── notebooks/
│   ├── phase1_data_cleaning.ipynb
│   └── phase2_eda.ipynb
│
├── outputs/
│   └── charts/                   # All generated plots
│
├── README.md
└── requirements.txt
```

## Project Phases

### Phase 1 — Data Cleaning
### Phase 2 — Exploratory Data Analysis

---

## Key Findings
- The **USA, China and Germany** dominate global air freight
- Global air freight showed **consistent growth** from 2005 to 2019
- **Strong positive correlation** exists between departures and freight volume
- Countries with **higher LPI scores** tend to handle more freight
- **LPI infrastructure scores** are mostly clustered between 2.0 and 3.5 globally

---

## Tools 
| Tool | Purpose |
|------|---------|
| Python | Core programming language |

---
## Author
**Muhammad Umer Mehmood**

- LinkedIn: [Umer](https://www.linkedin.com/in/umer-cheena-sp20bcs012/)
  
```

