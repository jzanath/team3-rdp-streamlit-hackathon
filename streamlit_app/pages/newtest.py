import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Sustainability Dashboard", layout="wide")

# Title
st.title("🏭 Sustainability Dashboard")
st.markdown("Use the dropdowns below to explore plant performance metrics.")

# Dropdown options
sites = ["Orlando", "Houston", "Cleveland"]
energy_metrics = ["Total Energy Consumed", "Average Power Usage"]
assets = ["Pump", "Compressor", "Mixer", "Meter"]
products = ["Produce One", "Produce Two", "Produce Three", "Produce Four", "Produce Five"]
chart_types = ["Pie Chart", "Bar Chart", "Line Chart", "Heat Map", "Scatter Plot"]

# Sidebar dropdowns
site = st.selectbox("Select Site", sites)
energy_metric = st.selectbox("Select Energy Usage Metric", energy_metrics)
asset = st.selectbox("Select Asset Type", assets)
product = st.selectbox("Select Product", products)
chart_type = st.selectbox("Select Chart Type", chart_types)

# Generate mock data
np.random.seed(42)
mock_data = pd.DataFrame({
    "Site": [site]*10,
    "Energy Metric": [energy_metric]*10,
    "Asset": [asset]*10,
    "Product": [product]*10,
    "Value 1": np.random.randint(100, 1000, 10),
    "Value 2": np.random.randint(50, 500, 10),
    "Category": [f"Category {i+1}" for i in range(10)]
})

# Display selected options
st.markdown(f"### 📍 Selected Configuration")
st.write(f"**Site:** {site}")
st.write(f"**Energy Metric:** {energy_metric}")
st.write(f"**Asset:** {asset}")
st.write(f"**Product:** {product}")
st.write(f"**Chart Type:** {chart_type}")

# Generate chart based on selection
st.markdown("### 📊 Visualization")

if chart_type == "Bar Chart":
    fig = px.bar(mock_data, x="Category", y="Value 1", title=f"{chart_type} - {energy_metric} for {asset} at {site}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Line Chart":
    fig = px.line(mock_data, x="Category", y="Value 1", markers=True, title=f"{chart_type} - {energy_metric} for {asset} at {site}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Pie Chart":
    fig = px.pie(mock_data, names="Category", values="Value 1", title=f"{chart_type} - {energy_metric} for {asset} at {site}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Scatter Plot":
    fig = px.scatter(mock_data, x="Value 1", y="Value 2", color="Category", size="Value 1", title=f"{chart_type} - {energy_metric} vs Value 2")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Heat Map":
    heat_data = mock_data[["Value 1", "Value 2"]].corr()
    fig = px.imshow(heat_data, text_auto=True, title=f"{chart_type} - Correlation between Value 1 and Value 2")
    st.plotly_chart(fig, use_container_width=True)
