import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Air Cargo Analysis", page_icon="✈️", layout="wide")

@st.cache_data
def load_data():
    df_raw = pd.read_csv("data.csv", encoding="utf-8-sig")

    valid_codes = ['IS.AIR.DPRT', 'IS.AIR.GOOD.MT.K1', 'IS.AIR.PSGR', 'LP.LPI.INFR.XQ']
    df = df_raw[df_raw['Series Code'].isin(valid_codes)].copy()

    df.rename(columns={
        'Series Name'  : 'series_name',
        'Series Code'  : 'series_code',
        'Country Name' : 'country',
        'Country Code' : 'country_code'
    }, inplace=True)

    year_cols = [c for c in df.columns if 'YR' in c]
    df[year_cols] = df[year_cols].replace('..', np.nan)
    df[year_cols] = df[year_cols].apply(pd.to_numeric, errors='coerce')

    df_long = df.melt(
        id_vars=['country', 'country_code', 'series_name', 'series_code'],
        value_vars=year_cols, var_name='year', value_name='value'
    )
    df_long['year'] = df_long['year'].str[:4].astype(int)

    df_pivot = df_long.pivot_table(
        index=['country', 'country_code', 'year'],
        columns='series_code', values='value'
    ).reset_index()
    df_pivot.columns.name = None

    df_pivot.rename(columns={
        'IS.AIR.DPRT'      : 'departures',
        'IS.AIR.GOOD.MT.K1': 'freight_mton_km',
        'IS.AIR.PSGR'      : 'passengers',
        'LP.LPI.INFR.XQ'   : 'lpi_infra_score'
    }, inplace=True)

    exclude_codes = [
        'ARB','CSS','CEB','EAR','EAS','TEA','EAP','ECA','TEC','ECS',
        'EMU','EUU','FCS','HIC','HPC','IBD','IBT','IDB','IDX','IDA',
        'LTE','LCN','TLA','LAC','LDC','LMY','LIC','LMC','MEA','TMN',
        'MNA','MIC','NAC','OED','OSS','PSS','PST','PRE','SST','SAS',
        'TSA','SSF','TSS','SSA','UMC','WLD'
    ]
    df_clean = df_pivot[~df_pivot['country_code'].isin(exclude_codes)].copy()
    df_clean = df_clean.sort_values(['country', 'year'])
    df_clean['freight_yoy_growth'] = df_clean.groupby('country')['freight_mton_km'].pct_change() * 100
    df_clean['freight_efficiency'] = df_clean['freight_mton_km'] / df_clean['departures']
    df_clean['freight_lag1']       = df_clean.groupby('country')['freight_mton_km'].shift(1)
    df_clean['freight_lag2']       = df_clean.groupby('country')['freight_mton_km'].shift(2)

    return df_clean

df = load_data()

# ── SIDEBAR ─────────────────────────────────────────────────
st.sidebar.title("✈️ Air Cargo Analysis")
st.sidebar.markdown("**Muhammad Umer Mehmood**")
st.sidebar.markdown("Data Analyst Student")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", [
    "🏠 Overview", "📊 EDA", "⚙️ Feature Engineering", "🤖 Modelling", "🔵 Clustering"
])
st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset:** World Bank WDI")
st.sidebar.markdown("**Countries:** 230")
st.sidebar.markdown("**Years:** 2005 – 2019")

# ── PAGE 1: OVERVIEW ────────────────────────────────────────
if page == "🏠 Overview":
    st.title("✈️ Global Air Freight Analysis")
    st.markdown("### Trends, Leaders and Growth Patterns (2005–2019)")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Countries",       str(df['country'].nunique()))
    col2.metric("Years Covered",         "2005 – 2019")
    col3.metric("Total Records",         f"{len(df):,}")
    col4.metric("Avg Freight (mton-km)", f"{df['freight_mton_km'].mean():,.1f}")

    st.markdown("---")
    st.markdown("""
    ### Project Overview
    This project analyzes **15 years** of global air transport data across **230 countries**
    from the World Bank World Development Indicators.

    - ✅ **Phase 1:** Data Cleaning
    - ✅ **Phase 2:** Exploratory Data Analysis
    - ✅ **Phase 3:** Feature Engineering
    - ✅ **Phase 4:** Modelling
    - ✅ **Phase 5:** Dashboard

    | Column | Description |
    |--------|-------------|
    | `departures` | Registered carrier departures worldwide |
    | `freight_mton_km` | Air freight in million ton-km |
    | `passengers` | Air passengers carried |
    | `lpi_infra_score` | Logistics infrastructure quality (1=low, 5=high) |
    | `freight_yoy_growth` | Year-over-year freight growth rate |
    | `freight_efficiency` | Freight per departure ratio |
    """)

# ── PAGE 2: EDA ─────────────────────────────────────────────
elif page == "📊 EDA":
    st.title("📊 Exploratory Data Analysis")
    st.markdown("---")

    top_n = st.slider("Select Top N Countries", 5, 20, 10)

    st.subheader(f"Top {top_n} Countries by Total Air Freight")
    top_freight = df.groupby('country')['freight_mton_km'].sum().sort_values(ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(12, 4))
    top_freight.plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
    ax.set_xlabel('Country'); ax.set_ylabel('Freight (million ton-km)')
    plt.xticks(rotation=45, ha='right'); plt.tight_layout(); st.pyplot(fig)
    st.markdown("---")

    st.subheader("Global Air Freight Trend (2005–2019)")
    yearly = df.groupby('year')['freight_mton_km'].sum()
    fig, ax = plt.subplots(figsize=(12, 4))
    yearly.plot(kind='line', ax=ax, marker='o', color='steelblue')
    ax.set_xlabel('Year'); ax.set_ylabel('Freight (million ton-km)')
    plt.tight_layout(); st.pyplot(fig)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Top {top_n} by Passengers")
        fig, ax = plt.subplots(figsize=(7, 4))
        df.groupby('country')['passengers'].sum().sort_values(ascending=False).head(top_n)\
          .plot(kind='bar', ax=ax, color='coral', edgecolor='black')
        plt.xticks(rotation=45, ha='right'); plt.tight_layout(); st.pyplot(fig)

    with col2:
        st.subheader(f"Top {top_n} by Departures")
        fig, ax = plt.subplots(figsize=(7, 4))
        df.groupby('country')['departures'].sum().sort_values(ascending=False).head(top_n)\
          .plot(kind='bar', ax=ax, color='purple', edgecolor='black')
        plt.xticks(rotation=45, ha='right'); plt.tight_layout(); st.pyplot(fig)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(df[['departures','freight_mton_km','passengers','lpi_infra_score']].corr(),
                    annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
        plt.tight_layout(); st.pyplot(fig)

    with col2:
        st.subheader("LPI Score Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        df['lpi_infra_score'].dropna().plot(kind='hist', bins=30, ax=ax, color='green', edgecolor='black')
        ax.set_xlabel('LPI Score'); ax.set_ylabel('Frequency')
        plt.tight_layout(); st.pyplot(fig)

# ── PAGE 3: FEATURE ENGINEERING ─────────────────────────────
elif page == "⚙️ Feature Engineering":
    st.title("⚙️ Feature Engineering")
    st.markdown("---")

    country    = st.selectbox("Select a Country", sorted(df['country'].dropna().unique()))
    df_country = df[df['country'] == country].sort_values('year')

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"YoY Freight Growth — {country}")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(df_country['year'], df_country['freight_yoy_growth'], color='steelblue', edgecolor='black')
        ax.axhline(0, color='red', linewidth=0.8, linestyle='--')
        ax.set_xlabel('Year'); ax.set_ylabel('YoY Growth (%)')
        plt.tight_layout(); st.pyplot(fig)

    with col2:
        st.subheader(f"Freight Efficiency — {country}")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(df_country['year'], df_country['freight_efficiency'], marker='o', color='coral')
        ax.set_xlabel('Year'); ax.set_ylabel('Freight per Departure')
        plt.tight_layout(); st.pyplot(fig)

    st.markdown("---")
    st.subheader("Data Sample")
    st.dataframe(df[['country','year','freight_mton_km','freight_yoy_growth',
                      'freight_efficiency','freight_lag1','freight_lag2']].head(20))

# ── PAGE 4: MODELLING ────────────────────────────────────────
elif page == "🤖 Modelling":
    st.title("🤖 Modelling — Freight Demand Forecasting")
    st.markdown("---")

    features = ['departures','passengers','lpi_infra_score','freight_lag1','freight_lag2','freight_efficiency']
    target   = 'freight_mton_km'
    df_model = df[features + [target]].dropna()
    X        = df_model[features]
    y        = df_model[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    lr = LinearRegression(); lr.fit(X_train, y_train); y_pred_lr = lr.predict(X_test)
    rf = RandomForestRegressor(n_estimators=100, random_state=42); rf.fit(X_train, y_train); y_pred_rf = rf.predict(X_test)

    st.subheader("Model Comparison")
    st.dataframe(pd.DataFrame({
        'Model'   : ['Linear Regression', 'Random Forest'],
        'R2 Score': [round(r2_score(y_test, y_pred_lr), 4), round(r2_score(y_test, y_pred_rf), 4)],
        'MAE'     : [round(mean_absolute_error(y_test, y_pred_lr), 2), round(mean_absolute_error(y_test, y_pred_rf), 2)]
    }))
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Feature Importance")
        fig, ax = plt.subplots(figsize=(7, 4))
        pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)\
          .plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
        plt.xticks(rotation=45, ha='right'); plt.tight_layout(); st.pyplot(fig)

    with col2:
        st.subheader("Actual vs Predicted")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.scatter(y_test, y_pred_rf, color='steelblue', alpha=0.5, edgecolor='black')
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2)
        ax.set_xlabel('Actual'); ax.set_ylabel('Predicted')
        plt.tight_layout(); st.pyplot(fig)

# ── PAGE 5: CLUSTERING ───────────────────────────────────────
elif page == "🔵 Clustering":
    st.title("🔵 Country Clustering by Air Transport Profile")
    st.markdown("---")

    cluster_features = ['departures','freight_mton_km','passengers','lpi_infra_score']
    df_cluster       = df[cluster_features + ['country']].dropna().copy()
    X_scaled         = StandardScaler().fit_transform(df_cluster[cluster_features])
    n_clusters       = st.slider("Number of Clusters", 2, 6, 4)
    df_cluster['cluster'] = KMeans(n_clusters=n_clusters, random_state=42).fit_predict(X_scaled)

    colors_list = ['steelblue','coral','green','purple','orange','red']
    fig, ax = plt.subplots(figsize=(12, 5))
    for c in sorted(df_cluster['cluster'].unique()):
        s = df_cluster[df_cluster['cluster'] == c]
        ax.scatter(s['departures'], s['freight_mton_km'], label=f'Cluster {c}',
                   color=colors_list[c], alpha=0.6, edgecolor='black')
    ax.set_xlabel('Departures'); ax.set_ylabel('Freight (million ton-km)'); ax.legend()
    plt.tight_layout(); st.pyplot(fig)

    st.markdown("---")
    st.subheader("Cluster Summary")
    st.dataframe(df_cluster.groupby('cluster')[cluster_features].mean().round(2))

    st.markdown("---")
    selected = st.selectbox("View Countries in Cluster", sorted(df_cluster['cluster'].unique()))
    st.dataframe(df_cluster[df_cluster['cluster'] == selected][['country']].drop_duplicates().reset_index(drop=True))
