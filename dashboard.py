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

# ══════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title="Air Cargo Analysis",
    page_icon="✈️",
    layout="wide"
)

# ══════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("air_cargo_features.csv")
    return df

df = load_data()

# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Kaggle_logo.png/320px-Kaggle_logo.png", width=120)
st.sidebar.title("✈️ Air Cargo Analysis")
st.sidebar.markdown("**Muhammad Umer Mehmood**")
st.sidebar.markdown("Data Analyst Student")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "🏠 Overview",
    "📊 EDA",
    "⚙️ Feature Engineering",
    "🤖 Modelling",
    "🔵 Clustering"
])

st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset:** World Bank WDI")
st.sidebar.markdown("**Countries:** 230")
st.sidebar.markdown("**Years:** 2005 – 2019")

# ══════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════
if page == "🏠 Overview":

    st.title("✈️ Global Air Freight Analysis")
    st.markdown("### Trends, Leaders and Growth Patterns (2005–2019)")
    st.markdown("---")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Countries", f"{df['country'].nunique()}")
    col2.metric("Years Covered", "2005 – 2019")
    col3.metric("Total Records", f"{len(df):,}")
    col4.metric("Avg Freight (mton-km)", f"{df['freight_mton_km'].mean():,.1f}")

    st.markdown("---")

    st.markdown("""
    ### Project Overview
    This project analyzes **15 years** of global air transport data across **230 countries**
    from the World Bank World Development Indicators. It covers:

    - ✅ **Phase 1:** Data Cleaning
    - ✅ **Phase 2:** Exploratory Data Analysis
    - ✅ **Phase 3:** Feature Engineering
    - ✅ **Phase 4:** Modelling (Linear Regression & Random Forest)
    - ✅ **Phase 5:** Dashboard (this!)

    ### Dataset Metrics
    | Column | Description |
    |--------|-------------|
    | `departures` | Registered carrier departures worldwide |
    | `freight_mton_km` | Air freight in million ton-km |
    | `passengers` | Air passengers carried |
    | `lpi_infra_score` | Logistics infrastructure quality (1=low, 5=high) |
    | `freight_yoy_growth` | Year-over-year freight growth rate |
    | `freight_efficiency` | Freight per departure ratio |
    | `continent` | Continent grouping |
    """)

# ══════════════════════════════════════════
# PAGE 2 — EDA
# ══════════════════════════════════════════
elif page == "📊 EDA":

    st.title("📊 Exploratory Data Analysis")
    st.markdown("---")

    # Top N selector
    top_n = st.slider("Select Top N Countries", min_value=5, max_value=20, value=10)

    # Chart 1 — Top N by freight
    st.subheader(f"Top {top_n} Countries by Total Air Freight")
    top_freight = df.groupby('country')['freight_mton_km'].sum().sort_values(ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(12, 4))
    top_freight.plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
    ax.set_xlabel('Country')
    ax.set_ylabel('Freight (million ton-km)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    # Chart 2 — Global trend
    st.subheader("Global Air Freight Trend (2005–2019)")
    yearly = df.groupby('year')['freight_mton_km'].sum()
    fig, ax = plt.subplots(figsize=(12, 4))
    yearly.plot(kind='line', ax=ax, marker='o', color='steelblue')
    ax.set_xlabel('Year')
    ax.set_ylabel('Freight (million ton-km)')
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    col1, col2 = st.columns(2)

    # Chart 3 — Top N passengers
    with col1:
        st.subheader(f"Top {top_n} by Passengers")
        top_pax = df.groupby('country')['passengers'].sum().sort_values(ascending=False).head(top_n)
        fig, ax = plt.subplots(figsize=(7, 4))
        top_pax.plot(kind='bar', ax=ax, color='coral', edgecolor='black')
        ax.set_xlabel('Country')
        ax.set_ylabel('Passengers')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

    # Chart 4 — Top N departures
    with col2:
        st.subheader(f"Top {top_n} by Departures")
        top_dep = df.groupby('country')['departures'].sum().sort_values(ascending=False).head(top_n)
        fig, ax = plt.subplots(figsize=(7, 4))
        top_dep.plot(kind='bar', ax=ax, color='purple', edgecolor='black')
        ax.set_xlabel('Country')
        ax.set_ylabel('Departures')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")

    col1, col2 = st.columns(2)

    # Chart 5 — Heatmap
    with col1:
        st.subheader("Correlation Heatmap")
        corr = df[['departures','freight_mton_km','passengers','lpi_infra_score']].corr()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
        plt.tight_layout()
        st.pyplot(fig)

    # Chart 6 — LPI distribution
    with col2:
        st.subheader("LPI Infrastructure Score Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        df['lpi_infra_score'].dropna().plot(kind='hist', bins=30, ax=ax, color='green', edgecolor='black')
        ax.set_xlabel('LPI Score (1=low, 5=high)')
        ax.set_ylabel('Frequency')
        plt.tight_layout()
        st.pyplot(fig)

# ══════════════════════════════════════════
# PAGE 3 — FEATURE ENGINEERING
# ══════════════════════════════════════════
elif page == "⚙️ Feature Engineering":

    st.title("⚙️ Feature Engineering")
    st.markdown("---")

    # Country selector
    country = st.selectbox("Select a Country", sorted(df['country'].dropna().unique()))
    df_country = df[df['country'] == country].sort_values('year')

    col1, col2 = st.columns(2)

    # YoY Growth
    with col1:
        st.subheader(f"YoY Freight Growth — {country}")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(df_country['year'], df_country['freight_yoy_growth'], color='steelblue', edgecolor='black')
        ax.axhline(0, color='red', linewidth=0.8, linestyle='--')
        ax.set_xlabel('Year')
        ax.set_ylabel('YoY Growth (%)')
        plt.tight_layout()
        st.pyplot(fig)

    # Freight Efficiency
    with col2:
        st.subheader(f"Freight Efficiency — {country}")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(df_country['year'], df_country['freight_efficiency'], marker='o', color='coral')
        ax.set_xlabel('Year')
        ax.set_ylabel('Freight per Departure')
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")

    # Continent breakdown
    if 'continent' in df.columns:
        st.subheader("Average Freight by Continent")
        continent_avg = df.groupby('continent')['freight_mton_km'].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 4))
        continent_avg.plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
        ax.set_xlabel('Continent')
        ax.set_ylabel('Avg Freight (million ton-km)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")
    st.subheader("Feature Engineered Data Sample")
    st.dataframe(df[['country','year','freight_mton_km','freight_yoy_growth',
                      'freight_efficiency','freight_lag1','freight_lag2']].head(20))

# ══════════════════════════════════════════
# PAGE 4 — MODELLING
# ══════════════════════════════════════════
elif page == "🤖 Modelling":

    st.title("🤖 Modelling — Freight Demand Forecasting")
    st.markdown("---")

    features = ['departures','passengers','lpi_infra_score','freight_lag1','freight_lag2','freight_efficiency']
    target   = 'freight_mton_km'

    df_model = df[features + [target]].dropna()
    X = df_model[features]
    y = df_model[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train models
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)

    # Model comparison
    st.subheader("Model Comparison")
    results = pd.DataFrame({
        'Model'   : ['Linear Regression', 'Random Forest'],
        'R2 Score': [round(r2_score(y_test, y_pred_lr), 4), round(r2_score(y_test, y_pred_rf), 4)],
        'MAE'     : [round(mean_absolute_error(y_test, y_pred_lr), 2), round(mean_absolute_error(y_test, y_pred_rf), 2)]
    })
    st.dataframe(results)

    st.markdown("---")

    col1, col2 = st.columns(2)

    # Feature importance
    with col1:
        st.subheader("Feature Importance — Random Forest")
        feat_imp = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(7, 4))
        feat_imp.plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
        ax.set_xlabel('Features')
        ax.set_ylabel('Importance Score')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

    # Actual vs Predicted
    with col2:
        st.subheader("Actual vs Predicted — Random Forest")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.scatter(y_test, y_pred_rf, color='steelblue', alpha=0.5, edgecolor='black')
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2)
        ax.set_xlabel('Actual Freight')
        ax.set_ylabel('Predicted Freight')
        plt.tight_layout()
        st.pyplot(fig)

# ══════════════════════════════════════════
# PAGE 5 — CLUSTERING
# ══════════════════════════════════════════
elif page == "🔵 Clustering":

    st.title("🔵 Country Clustering by Air Transport Profile")
    st.markdown("---")

    cluster_features = ['departures','freight_mton_km','passengers','lpi_infra_score']
    df_cluster = df[cluster_features + ['country']].dropna()

    scaler  = StandardScaler()
    X_scaled = scaler.fit_transform(df_cluster[cluster_features])

    n_clusters = st.slider("Select Number of Clusters", min_value=2, max_value=6, value=4)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df_cluster['cluster'] = kmeans.fit_predict(X_scaled)

    # Cluster scatter
    st.subheader("Cluster Visualization")
    colors_list = ['steelblue','coral','green','purple','orange','red']
    fig, ax = plt.subplots(figsize=(12, 5))
    for cluster in sorted(df_cluster['cluster'].unique()):
        subset = df_cluster[df_cluster['cluster'] == cluster]
        ax.scatter(subset['departures'], subset['freight_mton_km'],
                   label=f'Cluster {cluster}',
                   color=colors_list[cluster], alpha=0.6, edgecolor='black')
    ax.set_xlabel('Departures')
    ax.set_ylabel('Freight (million ton-km)')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    # Cluster summary
    st.subheader("Cluster Summary")
    st.dataframe(df_cluster.groupby('cluster')[cluster_features].mean().round(2))

    st.markdown("---")

    # Countries per cluster
    selected_cluster = st.selectbox("View Countries in Cluster", sorted(df_cluster['cluster'].unique()))
    st.dataframe(df_cluster[df_cluster['cluster'] == selected_cluster][['country']].drop_duplicates().reset_index(drop=True))
