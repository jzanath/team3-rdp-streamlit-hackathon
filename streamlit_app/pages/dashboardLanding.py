from datetime import datetime, timedelta
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from database import functions as db

# Set page config for better layout
st.set_page_config(page_title="Production Metrics Dashboard", layout="wide")

# Title with icon and reduced spacing
st.markdown("""
    <h2 style='text-align: center; margin-bottom: 10px;'>🌲 Production Metrics Sustainability Dashboard</h2>
""", unsafe_allow_html=True)

st.sidebar.header("🔧 Filter Options")
region = st.sidebar.selectbox("Select Region", ["All", "NA", "LATAM"], index=1)
time_period = st.sidebar.selectbox("Select Timeframe", ["Last 1 Day", "Last 1 Week", "Last 1 Month", "Last 1 Year", "All Time"])


# Divider
st.markdown("---")

 
def format_date(date):
    year = str(date.year)
    if date.month < 10:
        month = "0" + str(date.month)
    else:
        month = str(date.month)
    if date.day < 10:
        day = "0" + str(date.day)
    else:
        day = str(date.day)
    return year + "-" + month + "-" + day
def get_time_from_input(time):
    current_datetime = datetime.now()
    if time == "Last 1 Day":
        return format_date(current_datetime - timedelta(days=1))
    elif time == "Last 1 Week":
        return format_date(current_datetime - timedelta(weeks=1))
    elif time == "Last 1 Month":
        return format_date(current_datetime - timedelta(days=30))
    elif time == "Last 1 Year":
        return format_date(current_datetime - timedelta(days=365))
    elif time == "All Time":
        return format_date(current_datetime - timedelta(days=3000))
    return None
 
# Metrics section
st.markdown("### Key Metrics")
col1, col2 = st.columns(2)

def get_region_id(region):
    if region == "All":
        return 0
    elif region == "NA":
        return 1
    elif region == "LATAM":
        return 2
    return None

# Function call to database

if get_region_id(region) == 0:
    all_plants1 = db.getPlants(get_region_id("NA"))
    all_plants2 = db.getPlants(get_region_id("LATAM"))
    all_plants = all_plants1 + all_plants2
else:
    all_plants = db.getPlants(get_region_id(region)) # time goes here

total_faults = 0
if len(all_plants) > 0:
    for plant in all_plants:
        print(plant)
        total_faults += db.getTotalPlantFaultsFromDate(plant, get_time_from_input(time_period))


valid_batch_times = []

for plant in all_plants:
    batch_time = db.getPlantAvgBatchTime(plant)
    if batch_time:  # Only include non-zero or non-null values
        valid_batch_times.append(batch_time)

if valid_batch_times:
    avg_batch_time = sum(valid_batch_times) / len(valid_batch_times)
else:
    avg_batch_time = 0


with col1:
    st.metric(label="🕒 Avg Batch Time (Minutes)", value=f"{avg_batch_time:.2f}")

with col2:
    st.metric(label="⚠️ Alerts / Faults", value=total_faults)

# Divider
st.markdown("---")

# Energy usage chart
st.markdown("### Average Energy Usage")

energy_data = []
totalUsage = 0
totalPlants = 0
if len(all_plants) > 0:
    for plant in all_plants:
        print(plant)
        usuage = db.getAvgPlantKWH(plant)
        if usuage is not None:
            totalUsage += usuage
            totalPlants += 1

    if totalPlants > 0:
        avgUsage = totalUsage / totalPlants
    else:
        avgUsage = 0

print(avgUsage)
st.metric(label="⚡Average KWh Usage", value=avgUsage)
