import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from database import functions as db

# Set page configuration
st.set_page_config(page_title="Sustainability Dashboard", layout="wide")

# Title
st.title("🌿 Sustainability Dashboard")
st.markdown("Use the dropdowns below to explore plant performance metrics.")

# Dropdown options
plants = ["Orlando", "Houston", "Cleveland"]
energy_metrics = ["Total Energy Consumed", "Average Power Usage"]
alerts = ["High Power", "Voltage Spike", "Overrun"]

# Dropdowns for Graph 1
plant = st.selectbox("Select Site", plants)

assets = db.getPlantAssets(plant)

asset_ids = []
asset_dropdown_options = []
for asset in assets:
    asset_ids.append(asset.get("Asset ID"))
    asset_dropdown_options.append(asset.get("Name"))

def getIdByName(assets, asset_name):
    res = ""
    for asset in assets:
        if asset.get("Name") == asset_name:
            res = asset.get("Asset ID")
    return res

# Dropdown for Graph 2
assetName = st.selectbox("Select Asset", asset_dropdown_options)

error_data = db.getAssetAlertTypes(getIdByName(assets, assetName))

asset_data = []
count = 0
currentError = ""
alreadyProcessed = []

for error in error_data:
    if error not in alreadyProcessed:
        count = error_data.count(error)
        alreadyProcessed.append((error, count))

dataframe = pd.DataFrame(alreadyProcessed, columns=["Error Name", "Count"])

# Asset Alerts
st.markdown("### Asset Errors")
fig2 = px.bar(dataframe, x="Error Name", y="Count", title=f"{assetName} at {plant}")
st.plotly_chart(fig2, use_container_width=True)

energy_metric = st.selectbox("Select Energy Usage Metric", energy_metrics)

# Generate mock time series data
time_range = pd.date_range(start="2023-01-01", periods=12, freq="M")

# Mock data for energy usage
energy_data = pd.DataFrame({
    "Time": time_range,
    "Site": plant,
    "Metric": energy_metric,
    "Usage": np.random.randint(1000, 5000, len(time_range))
})

# Graph 1: Energy usage vs time
st.markdown("### Energy Usage Over Time")
fig1 = px.line(energy_data, x="Time", y="Usage", markers=True, title=f"{energy_metric} at {plant}")
st.plotly_chart(fig1, use_container_width=True)