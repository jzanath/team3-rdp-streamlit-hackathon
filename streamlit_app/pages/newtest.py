import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Sustainability Dashboard", layout="wide")

# Title
st.title("🌿 Sustainability Dashboard")
st.markdown("Use the dropdowns below to explore plant performance metrics.")

# Dropdown options
sites = ["Orlando", "Houston", "Cleveland"]
energy_metrics = ["Total Energy Consumed", "Average Power Usage"]
batches = [f"Batch {i}" for i in range(1, 11)]
assets = ["Pump", "Compressor", "Mixer", "Meter"]
alerts = ["High Power", "Voltage Spike", "Overrun"]

# Dropdowns for Graph 1
site = st.selectbox("Select Site", sites)
energy_metric = st.selectbox("Select Energy Usage Metric", energy_metrics)

# Generate mock time series data
time_range = pd.date_range(start="2023-01-01", periods=12, freq="M")

# Mock data for energy usage
energy_data = pd.DataFrame({
    "Time": time_range,
    "Site": site,
    "Metric": energy_metric,
    "Usage": np.random.randint(1000, 5000, len(time_range))
})

# Graph 1: Energy usage vs time
st.markdown("### ⚡ Graph 1: Energy Usage Over Time")
fig1 = px.line(energy_data, x="Time", y="Usage", markers=True, title=f"{energy_metric} at {site}")
st.plotly_chart(fig1, use_container_width=True)

# Dropdown for Graph 2
batch = st.selectbox("Select Batch", batches)

# Mock data for batch performance
batch_data = pd.DataFrame({
    "Time": time_range,
    "Site": site,
    "Batch": batch,
    "Performance": np.random.uniform(70, 100, len(time_range))
})

# Graph 2: Batch performance vs time
st.markdown("### 🧪 Graph 2: Batch Performance Over Time")
fig2 = px.line(batch_data, x="Time", y="Performance", markers=True, title=f"{batch} Performance at {site}")
st.plotly_chart(fig2, use_container_width=True)

# Dropdowns for Graph 3
asset_id = st.selectbox("Select Asset ID", assets)
alert_type = st.selectbox("Select Alert Type", alerts)

# Mock data for alerts per asset
alert_data = pd.DataFrame({
    "Time": time_range,
    "Site": site,
    "Asset ID": asset_id,
    "Alert Type": alert_type,
    "Alert Count": np.random.randint(0, 20, len(time_range))
})

# Graph 3: Alerts per asset over time
st.markdown("### 🚨 Graph 3: Alerts Over Time")
fig3 = px.bar(alert_data, x="Time", y="Alert Count", title=f"{alert_type} for {asset_id} at {site}")
st.plotly_chart(fig3, use_container_width=True)

