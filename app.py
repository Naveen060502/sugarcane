import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_summary():
    return pd.read_excel("summary1.xlsx", sheet_name="summary")

@st.cache_data
def load_farmer():
    return pd.read_excel("summary1.xlsx", sheet_name="raw")

summary_df = load_summary()
farmer_df = load_farmer()

# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="Jubilant Sugarcane Project Dashboard", layout="wide")

st.title("🌾 Jubilant Sugarcane Project Dashboard")

# Tabs
tab1, tab2 = st.tabs(["📊 Overall Summary", "👩‍🌾 Farmer Summary"])

# -----------------------------
# Tab 1 - Overall Summary
# -----------------------------
with tab1:
    st.subheader("📊 Overall Summary - Kharif 2024")

    # Village filter
        # Sidebar filters (default = nothing selected)
    villages = summary_df["Village Name"].dropna().unique().tolist()
    selected_villages = st.sidebar.multiselect(
        "Select Village(s)", 
        options=villages, 
        default=[]  # <-- nothing selected by default
    )
    
    # If no selection, show all villages
    if selected_villages:
        filtered_summary = summary_df[summary_df["Village Name"].isin(selected_villages)]
    else:
        filtered_summary = summary_df.copy()

    # KPIs
    total_devices = filtered_summary["Device ID"].nunique()
    total_farmers = filtered_summary["Farmer Name"].nunique()
    avg_irrigation = filtered_summary["No of Irrigation"].mean()
    avg_yield = filtered_summary["Yield (quintal/acre)"].mean()

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Total Devices", total_devices)
    kpi2.metric("Total Farmers", total_farmers)
    kpi3.metric("Avg No. of Irrigation", f"{avg_irrigation:.2f}")
    kpi4.metric("Avg Yield (qtl/acre)", f"{avg_yield:.2f}")
    kpi5.metric("Season", "Kharif 2024")

    # Charts
    st.markdown("### 🌍 Village-wise Charts")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        sns.barplot(data=filtered_summary, x="Village Name", y="No of Irrigation", estimator=np.mean, ci=None, ax=ax)
        ax.set_title("Village-wise Avg No of Irrigation")
        ax.bar_label(ax.containers[0])
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        sns.barplot(data=filtered_summary, x="Village Name", y="Yield (quintal/acre)", estimator=np.mean, ci=None, ax=ax)
        ax.set_title("Village-wise Avg Yield")
        ax.bar_label(ax.containers[0])
        st.pyplot(fig)

    # Bell shape curves
    st.markdown("### 🔔 Distribution Curves")
    fig, ax = plt.subplots()
    sns.kdeplot(filtered_summary["Irrigated Water (lakh L/acre)"], fill=True, label="Irrigated Water", ax=ax)
    sns.kdeplot(filtered_summary["Total Water (lakh L/acre)"], fill=True, label="Total Water Used", ax=ax)
    ax.set_title("Distribution of Irrigation & Total Water")
    ax.legend()
    st.pyplot(fig)

    # Village-wise avg table
    st.markdown("### 📋 Village-wise Averages")
    village_table = filtered_summary.groupby("Village Name").agg({
        "No of Irrigation": "mean",
        "Total Water (lakh L/acre)": "mean",
        "Irrigated Water (lakh L/acre)": "mean",
        "Rain Water (lakh L/acre)": "mean",
        "Yield (quintal/acre)": "mean"
    }).reset_index()

    # Round numeric columns only (safe formatting)
    numeric_cols = village_table.select_dtypes(include=[np.number]).columns
    village_table[numeric_cols] = village_table[numeric_cols].round(2)

    st.dataframe(village_table)

# -----------------------------
# Tab 2 - Farmer Summary
# -----------------------------
# -----------------------------
# Tab 2 - Farmer Summary
# -----------------------------
with tab2:
    st.subheader("👩‍🌾 Farmer Summary")

    # Farmer filter
    farmers = farmer_df["Farmer Name"].unique().tolist()
    selected_farmers = st.multiselect(
        "Select Farmer(s)", 
        farmers, 
        default=[],   # default = empty
        placeholder="Select farmers"
    )

    # If no farmer is selected → show all
    if selected_farmers:
        filtered_farmer = farmer_df[farmer_df["Farmer Name"].isin(selected_farmers)]
    else:
        filtered_farmer = farmer_df.copy()

    # Loop farmer-wise
    for farmer in filtered_farmer["Farmer Name"].unique():
        st.markdown(f"## 👨‍🌾 {farmer}")

        # Farmer details (only that farmer)
        farmer_details = filtered_farmer[filtered_farmer["Farmer Name"] == farmer][
            ["Farmer Name", "Father Name", "Mobile Number", "Village Name", "Device ID"]
        ].drop_duplicates()

        st.markdown("### 📋 Farmer Details")
        st.dataframe(farmer_details)

        # Moisture line chart (only that farmer)
        st.markdown("### 📈 Moisture Variation Over Time")
        subset = filtered_farmer[filtered_farmer["Farmer Name"] == farmer]

        fig, ax = plt.subplots()
        ax.plot(subset["CreateDate"], subset["CalculatedValue"], marker="o", linestyle="-")
        ax.set_xlabel("Date")
        ax.set_ylabel("Moisture (%)")
        ax.set_title(f"Moisture % over Time - {farmer}")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

        st.markdown("---")  # separator line






